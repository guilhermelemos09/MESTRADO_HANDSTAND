import numpy as np
import ezc3d
import os
import csv
from scipy.signal import butter, filtfilt

# =============================================================================
# FUNÇÕES MATEMÁTICAS
# =============================================================================

def apply_lowpass(data, cutoff, fs, order=4):
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

def detectar_fases_marcha(posicao_3d, fs, vel_threshold=150.0):
    x = apply_lowpass(posicao_3d[0], 6.0, fs)
    y = apply_lowpass(posicao_3d[1], 6.0, fs)
    z = apply_lowpass(posicao_3d[2], 6.0, fs)
    dt = 1.0 / fs
    vx = np.gradient(x) / dt
    vy = np.gradient(y) / dt
    vz = np.gradient(z) / dt
    vel_resultante = np.sqrt(vx**2 + vy**2 + vz**2)
    stance_bool = vel_resultante < vel_threshold
    z_min = np.nanmin(z)
    stance_bool = stance_bool & (z < z_min + 100)
    transicoes = np.diff(stance_bool.astype(int))
    td_idx = np.where(transicoes == 1)[0] + 1
    lo_idx = np.where(transicoes == -1)[0] + 1
    return td_idx, lo_idx, stance_bool

def calcular_vetor(p1, p2):
    return p2 - p1

def calcular_angulo_entre_vetores(v1, v2):
    dot_product = np.sum(v1 * v2, axis=0)
    norm_v1 = np.linalg.norm(v1, axis=0)
    norm_v2 = np.linalg.norm(v2, axis=0)
    cosine_angle = np.clip(dot_product / (norm_v1 * norm_v2), -1.0, 1.0)
    return np.degrees(np.arccos(cosine_angle))

# =============================================================================
# PIPELINE PILOTO: HANDSTAND WALK DINÂMICO
# =============================================================================

def analisar_hsw_piloto(path_c3d):
    print(f"\n[Processando HSW] Arquivo: {path_c3d}")
    
    c = ezc3d.c3d(path_c3d)
    points = c['data']['points']
    marker_names = c['parameters']['POINT']['LABELS']['value']
    freq = c['header']['points']['frame_rate']
    
    def get_point(names_list, fallbacks=None):
        best_marker = None
        best_valid = -1
        num_frames = points.shape[2]
        
        for name in names_list:
            for idx, m_name in enumerate(marker_names):
                if m_name.strip().upper() == name.strip().upper():
                    z = points[2, idx, :]
                    valid_count = np.sum(~np.isnan(z) & (z != 0))
                    if valid_count > best_valid:
                        best_valid = valid_count
                        best_marker = points[:3, idx, :]
                        
        if best_valid < (num_frames * 0.1) and fallbacks is not None:
            for name in fallbacks:
                for idx, m_name in enumerate(marker_names):
                    if m_name.strip().upper() == name.strip().upper():
                        z = points[2, idx, :]
                        valid_count = np.sum(~np.isnan(z) & (z != 0))
                        if valid_count > best_valid:
                            best_valid = valid_count
                            best_marker = points[:3, idx, :]
                            
        if best_marker is not None:
            return best_marker
        return np.full((3, num_frames), np.nan)

    # Filtragem Cinemática Base
    for coord in range(3):
        for marcador in range(points.shape[1]):
            points[coord, marcador, :] = apply_lowpass(points[coord, marcador, :], cutoff=6.0, fs=freq)

    # PONTOS DO CORPO
    punho_l = get_point(["LWRB", "LWR", "LWRA", "LWRIST"], fallbacks=["LFIN"])
    punho_r = get_point(["RWRB", "RWR", "RWRA", "RWRIST"], fallbacks=["RFIN"])
    dedo_l = get_point(["LFIN", "LFIN1", "LFING"])
    dedo_r = get_point(["RFIN", "RFIN1", "RFING"])
    pelve_l = get_point(["LASI", "LPSI"])
    pelve_r = get_point(["RASI", "RPSI"])
    pelve_centro = (pelve_l + pelve_r) / 2.0
    t10 = get_point(["T10"])
    c7 = get_point(["C7"])
    rsho = get_point(["RSHO", "RSHO_clean"])
    relb = get_point(["RELB"])
    joelho = get_point(["RKNE", "LKNE"])
    head = get_point(["LFHD", "HEAD"])
    tornozelo_l = get_point(["LANK", "LHEE"])
    tornozelo_r = get_point(["RANK", "RHEE"])
    
    # 1. Distância Total e Velocidade Média de Deslocamento
    y_pelve = pelve_centro[1, :]
    y_valido = y_pelve[~np.isnan(y_pelve)]
    distancia_total = 0
    velocidade_media = 0
    tempo_total = 0
    if len(y_valido) > 10:
        distancia_total = np.abs(y_valido[-1] - y_valido[0])
        tempo_total = len(y_valido) / freq
        velocidade_media = distancia_total / tempo_total if tempo_total > 0 else 0

    # 2. Eventos de Marcha e Fases
    td_l, lo_l, stance_l = detectar_fases_marcha(punho_l, freq)
    td_r, lo_r, stance_r = detectar_fases_marcha(punho_r, freq)
    
    # Combinar todos os Touchdowns ordenados no tempo para achar comprimento de cada passada
    td_all = []
    for td in td_l: td_all.append((td, 'L'))
    for td in td_r: td_all.append((td, 'R'))
    td_all.sort(key=lambda x: x[0])
    
    comprimentos_passos = []
    tempos_passos = [] # Tempo entre TDs consecutivos
    
    for i in range(1, len(td_all)):
        idx_atual = td_all[i][0]
        idx_ant = td_all[i-1][0]
        # Distancia Y entre a pelve nesses dois momentos (passada real do corpo)
        dist_passo = np.abs(pelve_centro[1, idx_atual] - pelve_centro[1, idx_ant])
        tempo_passo = (idx_atual - idx_ant) / freq
        if dist_passo > 0 and not np.isnan(dist_passo):
            comprimentos_passos.append(dist_passo)
        if tempo_passo > 0:
            tempos_passos.append(tempo_passo)

    # 3. CV Espacial e Temporal
    cv_espacial = (np.std(comprimentos_passos) / np.mean(comprimentos_passos)) * 100 if len(comprimentos_passos) > 2 else 0
    cv_temporal = (np.std(tempos_passos) / np.mean(tempos_passos)) * 100 if len(tempos_passos) > 2 else 0
    comprimento_passada_medio = np.mean(comprimentos_passos) if len(comprimentos_passos) > 0 else 0

    # 4. Tempos de Contato
    tempos_contato = []
    for td in td_l:
        lo_futuros = lo_l[lo_l > td]
        if len(lo_futuros) > 0: tempos_contato.append((lo_futuros[0] - td) / freq)
    for td in td_r:
        lo_futuros = lo_r[lo_r > td]
        if len(lo_futuros) > 0: tempos_contato.append((lo_futuros[0] - td) / freq)
        
    tempo_contato_medio = np.mean(tempos_contato) if len(tempos_contato) > 0 else 0

    # 5. Tempo em Duplo Suporte
    duplo_suporte_bool = stance_l & stance_r
    frames_ds = np.sum(duplo_suporte_bool)
    tempo_ds_total = frames_ds / freq
    percentual_ds = (tempo_ds_total / tempo_total) * 100 if tempo_total > 0 else 0

    # 6. Cadência
    total_passos = len(td_l) + len(td_r)
    cadencia = total_passos / tempo_total if tempo_total > 0 else 0

    # ================== VARIÁVEIS POSTURAIS ADICIONADAS ==================
    # Base de Apoio
    base_apoio_media = np.nanmean(np.linalg.norm(punho_l - punho_r, axis=0))
    
    # Rotação das Mãos
    vetor_base_2d = punho_r[:2, :] - punho_l[:2, :]
    vetor_frente_2d = np.zeros_like(vetor_base_2d)
    vetor_frente_2d[0, :] = -vetor_base_2d[1, :]
    vetor_frente_2d[1, :] = vetor_base_2d[0, :]
    
    vetor_mao_l_2d = dedo_l[:2, :] - punho_l[:2, :]
    vetor_mao_r_2d = dedo_r[:2, :] - punho_r[:2, :]
    
    ang_mao_l = calcular_angulo_entre_vetores(vetor_mao_l_2d, vetor_frente_2d)
    ang_mao_r = calcular_angulo_entre_vetores(vetor_mao_r_2d, vetor_frente_2d)
    rotacao_mao_media = np.nanmean((ang_mao_l + ang_mao_r) / 2.0)
    
    # Comprimento dos Membros
    tornozelo_centro = (tornozelo_l + tornozelo_r) / 2.0
    comprimento_braco = np.nanmean(np.linalg.norm(rsho - punho_r, axis=0))
    comprimento_perna = np.nanmean(np.linalg.norm(tornozelo_centro - pelve_centro, axis=0))

    # Índice de Verticalidade (Punho -> Pelve -> Tornozelo)
    punho_centro = (punho_l + punho_r) / 2.0
    vetor_inferior = pelve_centro - punho_centro
    vetor_superior = tornozelo_centro - pelve_centro
    indice_verticalidade = np.nanmean(calcular_angulo_entre_vetores(vetor_inferior, vetor_superior))

    # Extensão Cervical
    vetor_tronco = c7 - t10
    vetor_cabeca = head - c7
    extensao_cervical = np.nanmean(calcular_angulo_entre_vetores(vetor_tronco, vetor_cabeca))
    
    # Altura do CoM (Pelve Z)
    com_z_medio = np.nanmean(pelve_centro[2, :])

    return {
        "Distancia Percorrida (mm)": distancia_total,
        "Tempo Total (s)": tempo_total,
        "Velocidade Media (mm/s)": velocidade_media,
        "Cadencia (passos/s)": cadencia,
        "Comprimento Passada (mm)": comprimento_passada_medio,
        "CV Comprimento (%)": cv_espacial,
        "CV Tempo (%)": cv_temporal,
        "Tempo de Contato (s)": tempo_contato_medio,
        "% Duplo Suporte": percentual_ds,
        "Largura Base Apoio (mm)": base_apoio_media,
        "Rotacao Maos (graus)": rotacao_mao_media,
        "Altura CoM (mm)": com_z_medio,
        "Comprimento Braco (mm)": comprimento_braco,
        "Comprimento Perna (mm)": comprimento_perna,
        "Indice Verticalidade (deg)": indice_verticalidade,
        "Extensao Cervical (deg)": extensao_cervical
    }

if __name__ == "__main__":
    import glob
    arquivos_hsw = glob.glob("hsw*.c3d")
    
    resultados = {}
    for arq in arquivos_hsw:
        try:
            resultados[arq] = analisar_hsw_piloto(arq)
        except Exception as e:
            print(f"[Erro] Falha no teste {arq}: {e}")

    if resultados:
        print("\n" + "="*80)
        print("          RESULTADOS PILOTO - HANDSTAND WALK (Com Variáveis Antigas)")
        print("="*80)
        metricas = list(resultados[list(resultados.keys())[0]].keys())
        print(f"{'Métrica':<30} | " + " | ".join([f"{cond[:15]:<15}" for cond in resultados.keys()]))
        print("-" * 80)
        for metrica in metricas:
            valores = []
            for cond in resultados.keys():
                val = resultados[cond][metrica]
                valores.append(f"{val:<15.4f}")
            print(f"{metrica:<30} | " + " | ".join(valores))
        print("="*80)
