import numpy as np
import ezc3d
import pandas as pd
import os
import glob

def calcular_transformacao_rigida(pontos_ref, pontos_mov):
    centroid_ref = np.mean(pontos_ref, axis=0)
    centroid_mov = np.mean(pontos_mov, axis=0)
    A = pontos_ref - centroid_ref
    B = pontos_mov - centroid_mov
    H = A.T @ B
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = centroid_mov - R @ centroid_ref
    return R, t

def ponto_valido(p):
    return not (np.any(np.isnan(p)) or np.all(p == 0))

def limpar_arquivo(c3d_static_path, c3d_dynamic_path, output_path):
    print(f"\n--- Iniciando Pipeline de Limpeza Automática: {c3d_dynamic_path} ---")
    try:
        # PARTE 1: RECONSTRUÇÃO RÍGIDA (OMBROS) VIA SVD
        static = ezc3d.c3d(c3d_static_path)
        labels_static = [l.strip() for l in static['parameters']['POINT']['LABELS']['value']]
        data_static = static['data']['points']

        ancora_nomes_4 = ['C7', 'T10', 'referencia1', 'referencia2']
        ancora_nomes_3 = ['C7', 'T10', 'referencia2']

        def get_static_idx(nome):
            if nome in labels_static: return labels_static.index(nome)
            raise ValueError(f"Âncora '{nome}' não encontrada no estático!")

        ancora_idx_static_4 = [get_static_idx(n) for n in ancora_nomes_4]
        ancora_idx_static_3 = [get_static_idx(n) for n in ancora_nomes_3]

        ancora_est_4 = np.array([data_static[:3, i, 0] for i in ancora_idx_static_4])
        ancora_est_3 = np.array([data_static[:3, i, 0] for i in ancora_idx_static_3])

        marcadores_rigidos = ['LSHO', 'RSHO']
        
        offsets_local = {}
        for m in marcadores_rigidos:
            if m in labels_static:
                idx_m = labels_static.index(m)
                offsets_local[m] = data_static[:3, idx_m, 0].copy()

        dynamic = ezc3d.c3d(c3d_dynamic_path)
        labels_dyn = [l.strip() for l in dynamic['parameters']['POINT']['LABELS']['value']]
        data_dyn = dynamic['data']['points']
        num_frames = data_dyn.shape[2]
        
        analogs_backup = dynamic['data']['analogs'].copy() if 'analogs' in dynamic['data'] else None

        # Tenta achar ancoras no dinâmico, se faltar aborta SVD mas continua pra suavização
        try:
            ancora_idx_dyn_4 = [labels_dyn.index(n) for n in ancora_nomes_4]
            ancora_idx_dyn_3 = [labels_dyn.index(n) for n in ancora_nomes_3]
            unlabeled_indices = [i for i, label in enumerate(labels_dyn) if '*' in label or label.lower().startswith('unlabeled')]
            
            for frame in range(num_frames):
                ancora_frame_4 = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn_4])
                usa_4 = all(ponto_valido(p) for p in ancora_frame_4)

                if usa_4:
                    R, t = calcular_transformacao_rigida(ancora_est_4, ancora_frame_4)
                else:
                    ancora_frame_3 = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn_3])
                    usa_3 = all(ponto_valido(p) for p in ancora_frame_3)
                    if usa_3:
                        R, t = calcular_transformacao_rigida(ancora_est_3, ancora_frame_3)
                    else:
                        continue

                for m in marcadores_rigidos:
                    if m not in labels_dyn or m not in offsets_local:
                        continue

                    idx_m_dyn = labels_dyn.index(m)
                    pos_atual = data_dyn[:3, idx_m_dyn, frame]

                    if not ponto_valido(pos_atual):
                        pos_prevista = R @ offsets_local[m] + t
                        melhor_idx = None
                        menor_dist = 50.0
                        for idx_un in unlabeled_indices:
                            pos_cand = data_dyn[:3, idx_un, frame]
                            if not ponto_valido(pos_cand): continue
                            dist = np.linalg.norm(pos_cand - pos_prevista)
                            if dist < menor_dist:
                                menor_dist = dist
                                melhor_idx = idx_un

                        if melhor_idx is not None:
                            data_dyn[:3, idx_m_dyn, frame] = data_dyn[:3, melhor_idx, frame]
                            data_dyn[3, idx_m_dyn, frame] = 1.0
                        else:
                            data_dyn[:3, idx_m_dyn, frame] = pos_prevista
                            data_dyn[3, idx_m_dyn, frame] = 1.0
                            
        except Exception as e:
            print(f"Aviso: Não foi possível aplicar SVD para {c3d_dynamic_path} ({e}). Prosseguindo para suavização.")

        # PARTE 2: SUAVIZAÇÃO UNIVERSAL E REMOÇÃO DE PICOS PARA TODOS OS MARCADORES
        for idx, marker in enumerate(labels_dyn):
            if marker.startswith('*') or marker.lower().startswith('unlabeled'):
                continue
                
            is_gap = np.isnan(data_dyn[0, idx, :]) | (np.all(data_dyn[:3, idx, :] == 0, axis=0))
            
            z_serie = pd.Series(np.where(is_gap, np.nan, data_dyn[2, idx, :]))
            rolling_med = z_serie.rolling(window=7, center=True, min_periods=1).median()
            spike_mask = np.abs(z_serie - rolling_med) > 60.0
            
            is_gap = is_gap | spike_mask.values
            
            if np.all(is_gap):
                print(f"  [ALERTA] Marcador {marker} totalmente ausente.")
                continue
                
            if np.any(is_gap):
                for coord in range(3):
                    serie = data_dyn[coord, idx, :].copy()
                    serie[is_gap] = np.nan
                    s = pd.Series(serie)
                    s_interp = s.interpolate(method='linear', limit_direction='both')
                    data_dyn[coord, idx, :] = s_interp.values
                    
                data_dyn[3, idx, is_gap] = 1.0
                
        dynamic['data']['points'] = data_dyn
        if analogs_backup is not None:
            dynamic['data']['analogs'] = analogs_backup
        if 'meta_points' in dynamic['data']:
            del dynamic['data']['meta_points']
            
        dynamic.write(output_path)
        print(f"-> Concluído: {output_path}")

    except Exception as e:
        print(f"Erro em {c3d_dynamic_path}: {e}")

if __name__ == "__main__":
    estatico = "Guilherme_extra Cal 01.c3d"
    
    # Processa estáticos e dinâmicos (Assumindo os originais .c3d)
    arquivos = glob.glob("hsw01.c3d") + glob.glob("hsw02.c3d") + glob.glob("hs01.c3d") + glob.glob("hs02.c3d")
    for arq in arquivos:
        saida = arq.replace(".c3d", "_limpo.c3d")
        limpar_arquivo(estatico, arq, saida)
