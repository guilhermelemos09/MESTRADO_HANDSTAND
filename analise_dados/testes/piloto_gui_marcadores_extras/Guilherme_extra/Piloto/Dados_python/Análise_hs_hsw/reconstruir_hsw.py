"""
Reconstrução Robusta de Marcadores - Handstand Walk (HSW)
==========================================================
Utiliza Algoritmo de Kabsch (SVD) para o tronco.
Para marcadores distais (LFIN, RFIN, LASI), faz busca por proximidade,
e preenche gaps longos com interpolação PCHIP/Linear suave.
"""
import numpy as np
import ezc3d
import pandas as pd


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


def reconstruir_teste(c3d_static_path, c3d_dynamic_path, output_path):
    print(f"\n--- Iniciando reconstrução (SVD + Interpolacao) para: {c3d_dynamic_path} ---")

    try:
        static = ezc3d.c3d(c3d_static_path)
        labels_static = [l.strip() for l in static['parameters']['POINT']['LABELS']['value']]
        data_static = static['data']['points']

        ancora_nomes_4 = ['C7', 'T10', 'referencia1', 'referencia2']
        ancora_nomes_3 = ['C7', 'T10', 'referencia2']

        def get_static_idx(nome):
            if nome in labels_static:
                return labels_static.index(nome)
            raise ValueError(f"Âncora '{nome}' não encontrada no estático!")

        ancora_idx_static_4 = [get_static_idx(n) for n in ancora_nomes_4]
        ancora_idx_static_3 = [get_static_idx(n) for n in ancora_nomes_3]

        ancora_est_4 = np.array([data_static[:3, i, 0] for i in ancora_idx_static_4])
        ancora_est_3 = np.array([data_static[:3, i, 0] for i in ancora_idx_static_3])

        marcadores_rigidos = ['LSHO', 'RSHO']
        marcadores_flexiveis = ['LASI', 'LFIN', 'RFIN']
        marcadores_alvo = marcadores_rigidos + marcadores_flexiveis
        
        offsets_local = {}
        for m in marcadores_alvo:
            if m in labels_static:
                idx_m = labels_static.index(m)
                offsets_local[m] = data_static[:3, idx_m, 0].copy()
                print(f"-> Vetor mapeado para '{m}'.")

        dynamic = ezc3d.c3d(c3d_dynamic_path)
        labels_dyn = [l.strip() for l in dynamic['parameters']['POINT']['LABELS']['value']]
        data_dyn = dynamic['data']['points']
        num_frames = data_dyn.shape[2]

        analogs_backup = dynamic['data']['analogs'].copy() if 'analogs' in dynamic['data'] else None

        def get_dyn_idx(nome):
            if nome in labels_dyn:
                return labels_dyn.index(nome)
            raise ValueError(f"Âncora '{nome}' ausente no dinâmico!")

        ancora_idx_dyn_4 = [get_dyn_idx(n) for n in ancora_nomes_4]
        ancora_idx_dyn_3 = [get_dyn_idx(n) for n in ancora_nomes_3]

        unlabeled_indices = [i for i, label in enumerate(labels_dyn)
                             if '*' in label or label.lower().startswith('unlabeled')]

        correcoes = {m: 0 for m in marcadores_alvo}
        stats = {'4pts': 0, '3pts': 0, 'skip': 0}

        for frame in range(num_frames):
            ancora_frame_4 = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn_4])
            usa_4 = all(ponto_valido(p) for p in ancora_frame_4)

            if usa_4:
                R, t = calcular_transformacao_rigida(ancora_est_4, ancora_frame_4)
                stats['4pts'] += 1
            else:
                ancora_frame_3 = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn_3])
                usa_3 = all(ponto_valido(p) for p in ancora_frame_3)
                if usa_3:
                    R, t = calcular_transformacao_rigida(ancora_est_3, ancora_frame_3)
                    stats['3pts'] += 1
                else:
                    stats['skip'] += 1
                    continue

            for m in marcadores_alvo:
                if m not in labels_dyn or m not in offsets_local:
                    continue

                idx_m_dyn = labels_dyn.index(m)
                pos_atual = data_dyn[:3, idx_m_dyn, frame]

                if not ponto_valido(pos_atual):
                    pos_prevista = R @ offsets_local[m] + t

                    melhor_idx = None
                    menor_dist = 60.0 # Aumentei um pouco a tolerancia para os dedos
                    for idx_un in unlabeled_indices:
                        pos_cand = data_dyn[:3, idx_un, frame]
                        if not ponto_valido(pos_cand):
                            continue
                        dist = np.linalg.norm(pos_cand - pos_prevista)
                        if dist < menor_dist:
                            menor_dist = dist
                            melhor_idx = idx_un

                    if melhor_idx is not None:
                        data_dyn[:3, idx_m_dyn, frame] = data_dyn[:3, melhor_idx, frame]
                        data_dyn[3, idx_m_dyn, frame] = 1.0
                        correcoes[m] += 1
                    else:
                        if m in marcadores_rigidos:
                            data_dyn[:3, idx_m_dyn, frame] = pos_prevista
                            data_dyn[3, idx_m_dyn, frame] = 1.0
                            correcoes[m] += 1
                        else:
                            # Flexiveis não encontrados na nuvem ficam como NaN para interpolar depois
                            data_dyn[:3, idx_m_dyn, frame] = np.nan
                            data_dyn[3, idx_m_dyn, frame] = -1.0

        print(f"   Frames com 4 âncoras:  {stats['4pts']} | 3 âncoras: {stats['3pts']}")
        
        # INTERPOLAÇÃO PARA MARCADORES FLEXÍVEIS (para evitar saltos abruptos)
        for m in marcadores_flexiveis:
            if m in labels_dyn:
                idx_m = labels_dyn.index(m)
                for coord in range(3):
                    serie = data_dyn[coord, idx_m, :].copy()
                    
                    # Garantir que [0,0,0] que passou batido vire NaN
                    for f in range(num_frames):
                        p = data_dyn[:3, idx_m, f]
                        if np.any(np.isnan(p)) or np.all(p == 0):
                            serie[f] = np.nan
                            
                    s = pd.Series(serie)
                    # Interpolação linear é a mais segura para não dar overshoot nas bordas
                    s_interp = s.interpolate(method='linear', limit_direction='both')
                    data_dyn[coord, idx_m, :] = s_interp.values
                
                # Após interpolar, tudo é válido
                data_dyn[3, idx_m, :] = 1.0

        dynamic['data']['points'] = data_dyn
        if analogs_backup is not None:
            dynamic['data']['analogs'] = analogs_backup
        
        if 'meta_points' in dynamic['data']:
            del dynamic['data']['meta_points']
            
        dynamic.write(output_path)
        print(f"-> Arquivo salvo em: {output_path}")

    except Exception as e:
        print(f"Erro inesperado: {e}")
        import traceback; traceback.print_exc()


if __name__ == "__main__":
    reconstruir_teste("Guilherme_extra Cal 01.c3d", "hsw01.c3d", "hsw01_limpo.c3d")
    reconstruir_teste("Guilherme_extra Cal 01.c3d", "hsw02.c3d", "hsw02_limpo.c3d")
