"""
PIPELINE DE LIMPEZA E RECONSTRUÇÃO AUTOMÁTICA DE ARQUIVOS C3D (LaBioCoM)
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes

Recursos:
1. Reconstrução de Ombros (LSHO/RSHO) via Transformação Rígida SVD (Algoritmo de Kabsch) 
   usando cluster dorsal de 4 âncoras (C7, T10, referencia1, referencia2).
2. Remoção de spikes (>60 mm) e interpolação de gaps (Spline/PCHIP).
3. Filtragem passa-baixa Butterworth 4ª ordem zero-lag (6 Hz para cinemática, 20 Hz para força).
"""

import numpy as np
import ezc3d
import pandas as pd
import os
import glob
from scipy.signal import butter, filtfilt

def calcular_transformacao_rigida(pontos_ref, pontos_mov):
    """Calcula a matriz de rotação R e vetor de translação t ótimos via SVD."""
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

def apply_lowpass_c3d(data, cutoff, fs, order=4):
    """Aplica filtro Butterworth passa-baixa zero-lag sem atraso de fase."""
    if fs <= 0 or np.all(np.isnan(data)): return data
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    if normal_cutoff >= 1: return data
    
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    valid_idx = np.where(~np.isnan(data))[0]
    if len(valid_idx) < 18: return data
    
    data_interp = np.copy(data)
    nan_idx = np.where(np.isnan(data))[0]
    if len(nan_idx) > 0:
        data_interp[nan_idx] = np.interp(nan_idx, valid_idx, data[valid_idx])
        
    data_filtered = filtfilt(b, a, data_interp)
    data_filtered[nan_idx] = np.nan
    return data_filtered

def find_marker_idx(labels, candidate_names):
    """Localiza o índice do marcador ignorando maiúsculas, espaços e prefixos de sujeito (ex: 'P001:LREF')."""
    if isinstance(candidate_names, str):
        candidate_names = [candidate_names]
    cands_clean = [c.strip().upper() for c in candidate_names]
    for idx, raw in enumerate(labels):
        lbl = raw.strip()
        if ':' in lbl:
            lbl = lbl.split(':')[-1]
        if lbl.upper() in cands_clean:
            return idx
    return None

def limpar_arquivo_c3d(c3d_static_path, c3d_dynamic_path, output_path):
    print(f"\n[PIPELINE] Limpando: {os.path.basename(c3d_dynamic_path)}")
    try:
        static = ezc3d.c3d(c3d_static_path)
        labels_static = [l.strip() for l in static['parameters']['POINT']['LABELS']['value']]
        data_static = static['data']['points']

        # Mapeamento com tolerância a variações de nomes/aliases
        aliases = {
            'LREF': ['LREF', 'referencia1', 'REF_L', 'L_REF'],
            'RREF': ['RREF', 'referencia2', 'REF_R', 'R_REF'],
            'LSHO': ['LSHO', 'LSHO_clean'],
            'RSHO': ['RSHO', 'RSHO_clean'],
            'RWRA': ['RWRA', 'RWRIST', 'RWR'],
            'LWRA': ['LWRA', 'LWRIST', 'LWR'],
            'RFIN': ['RFIN', 'RFIN1', 'RFING'],
            'LFIN': ['LFIN', 'LFIN1', 'LFING'],
        }
        def get_alias(name):
            return aliases.get(name, [name])

        clusters_def = [
            {
                "nome": "Tronco / Ombros",
                "ancoras": ['C7', 'T10', 'RBAK', 'LREF', 'RREF', 'STRN'],
                "alvos": ['LSHO', 'RSHO']
            },
            {
                "nome": "Pelve",
                "ancoras": ['LASI', 'RASI', 'LPSI', 'RPSI'],
                "alvos": ['LASI', 'RASI', 'LPSI', 'RPSI']
            },
            {
                "nome": "Pé/Perna E",
                "ancoras": ['LTHI', 'LKNE', 'LTIB', 'LHEE', 'LTOE'],
                "alvos": ['LANK', 'LHEE', 'LKNE']
            },
            {
                "nome": "Pé/Perna D",
                "ancoras": ['RTHI', 'RKNE', 'RTIB', 'RHEE', 'RTOE'],
                "alvos": ['RANK', 'RHEE', 'RKNE']
            },
            {
                "nome": "Antebraço/Mão E",
                "ancoras": ['LELB', 'LFRM', 'LWRA', 'LWRB', 'LFIN'],
                "alvos": ['LWRA', 'LWRB', 'LFIN']
            },
            {
                "nome": "Antebraço/Mão D",
                "ancoras": ['RELB', 'RFRM', 'RWRA', 'RWRB', 'RFIN'],
                "alvos": ['RWRA', 'RWRB', 'RFIN']
            }
        ]

        dynamic = ezc3d.c3d(c3d_dynamic_path)
        labels_dyn = [l.strip() for l in dynamic['parameters']['POINT']['LABELS']['value']]
        data_dyn = dynamic['data']['points']
        num_frames = data_dyn.shape[2]
        fs_points = dynamic['parameters']['POINT']['RATE']['value'][0]
        
        analogs_backup = dynamic['data']['analogs'].copy() if 'analogs' in dynamic['data'] else None
        stats_svd = {}

        # 1. Reconstrução SVD por Clusters Anatômicos Multi-Segmentares
        for cl in clusters_def:
            # Localizar âncoras disponíveis no estático
            anc_static_map = {}
            for a in cl['ancoras']:
                idx_s = find_marker_idx(labels_static, get_alias(a))
                if idx_s is not None and ponto_valido(data_static[:3, idx_s, 0]):
                    anc_static_map[a] = data_static[:3, idx_s, 0].copy()

            if len(anc_static_map) < 3:
                continue

            # Mapear posições de referência dos alvos no estático
            alvos_static_map = {}
            for m in cl['alvos']:
                idx_s = find_marker_idx(labels_static, get_alias(m))
                if idx_s is not None and ponto_valido(data_static[:3, idx_s, 0]):
                    alvos_static_map[m] = data_static[:3, idx_s, 0].copy()

            if not alvos_static_map:
                continue

            # Garantir existência dos marcadores no dinâmico
            labels_modificados = False
            for m in list(anc_static_map.keys()) + list(alvos_static_map.keys()):
                idx_d = find_marker_idx(labels_dyn, get_alias(m))
                if idx_d is None:
                    idx_d = data_dyn.shape[1]
                    new_slice = np.zeros((4, 1, num_frames), dtype=data_dyn.dtype)
                    data_dyn = np.concatenate([data_dyn, new_slice], axis=1)
                    labels_dyn.append(m)
                    labels_modificados = True

            if labels_modificados:
                dynamic['parameters']['POINT']['LABELS']['value'] = labels_dyn
                dynamic['parameters']['POINT']['USED']['value'] = [len(labels_dyn)]
                if 'meta_points' in dynamic['data']:
                    del dynamic['data']['meta_points']

            # Índices dinâmicos
            anc_dyn_indices = {a: find_marker_idx(labels_dyn, get_alias(a)) for a in anc_static_map}
            alvo_dyn_indices = {m: find_marker_idx(labels_dyn, get_alias(m)) for m in alvos_static_map}

            # Reconstrução frame a frame
            for m_tgt, p_ref_tgt in alvos_static_map.items():
                idx_tgt = alvo_dyn_indices[m_tgt]
                reconst_count = 0
                for f in range(num_frames):
                    p_curr = data_dyn[:3, idx_tgt, f]
                    if not ponto_valido(p_curr):
                        # Encontrar âncoras válidas neste frame (excluindo o próprio alvo)
                        valid_anc = []
                        for a, idx_a in anc_dyn_indices.items():
                            if a == m_tgt: continue
                            if ponto_valido(data_dyn[:3, idx_a, f]):
                                valid_anc.append(a)

                        if len(valid_anc) >= 3:
                            pts_ref_sub = np.array([anc_static_map[a] for a in valid_anc])
                            pts_mov_sub = np.array([data_dyn[:3, anc_dyn_indices[a], f] for a in valid_anc])
                            R, t = calcular_transformacao_rigida(pts_ref_sub, pts_mov_sub)
                            p_reconst = R @ p_ref_tgt + t
                            data_dyn[:3, idx_tgt, f] = p_reconst
                            data_dyn[3, idx_tgt, f] = 0.0
                            reconst_count += 1
                if reconst_count > 0:
                    stats_svd[f"{m_tgt}_reconst"] = reconst_count

        # 2. Remoção de Spikes e Interpolação de Gaps em todos os marcadores
        for m_idx in range(len(labels_dyn)):
            for axis in range(3):
                sinal = data_dyn[axis, m_idx, :].copy()
                sinal[sinal == 0] = np.nan
                
                # Se for todo NaN, não há o que interpolar
                if np.all(np.isnan(sinal)):
                    continue

                s = pd.Series(sinal)
                rolling_med = s.rolling(window=7, center=True, min_periods=1).median()
                spike_mask = np.abs(s - rolling_med) > 60.0
                s[spike_mask] = np.nan
                
                if s.count() >= 2:
                    s_interp = s.interpolate(method='pchip', limit_area='inside').bfill().ffill()
                else:
                    s_interp = s.bfill().ffill()
                
                # 3. Filtragem Butterworth (6 Hz)
                s_filt = apply_lowpass_c3d(s_interp.values, cutoff=6.0, fs=fs_points, order=4)
                data_dyn[axis, m_idx, :] = s_filt
            # Marca o marcador como rastreado e válido (residual 0.0)
            data_dyn[3, m_idx, :] = 0.0

        dynamic['data']['points'] = data_dyn
        # Remove meta_points para que o ezc3d não reaplique as máscaras de oclusão das câmeras do arquivo bruto
        if 'meta_points' in dynamic['data']:
            del dynamic['data']['meta_points']
        if analogs_backup is not None:
            dynamic['data']['analogs'] = analogs_backup

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        dynamic.write(output_path)
        print(f"[OK] Arquivo limpo salvo em: {output_path}")
        reconst_summary = " | ".join([f"{k.replace('_reconst','')}:{v}/{num_frames}" for k, v in stats_svd.items() if v > 0])
        print(f"     Reconstrução SVD ({len(stats_svd)} marcadores): {reconst_summary if reconst_summary else 'Nenhuma necessária'}")
        return True, stats_svd
    except Exception as e:
        print(f"[ERRO] Falha ao limpar {c3d_dynamic_path}: {e}")
        return False, {}

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="Pipeline de Limpeza Automática C3D (LaBioCoM)")
    parser.add_argument("--cal", type=str, help="Caminho do arquivo C3D estático de calibração")
    parser.add_argument("--dyn", type=str, nargs="+", help="Caminho(s) do(s) arquivo(s) C3D dinâmico(s)")
    parser.add_argument("--outdir", type=str, help="Diretório de saída para os arquivos limpos")
    args = parser.parse_args()

    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    pasta_brutos = os.path.join(diretorio_base, "..", "dados_brutos_c3d")
    pasta_limpos = args.outdir if args.outdir else os.path.join(diretorio_base, "..", "dados_limpos_c3d")

    if args.cal and args.dyn:
        for dyn in args.dyn:
            nome_limpo = os.path.basename(dyn).replace(".c3d", "_limpo.c3d")
            saida = os.path.join(pasta_limpos, nome_limpo)
            limpar_arquivo_c3d(args.cal, dyn, saida)
    else:
        # Modo padrão: limpa as tentativas encontradas
        print("Uso: python pipeline_limpeza_automatica.py --cal <c3d_cal> --dyn <c3d_dyn1> [<c3d_dyn2> ...] --outdir <pasta_saida>")