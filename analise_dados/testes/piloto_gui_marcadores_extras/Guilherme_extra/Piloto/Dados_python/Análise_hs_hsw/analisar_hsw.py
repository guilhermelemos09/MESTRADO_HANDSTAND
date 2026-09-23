import ezc3d
import numpy as np
import scipy.signal as signal
from scipy.signal import butter, filtfilt
import os

def apply_lowpass(data, cutoff, fs, order=4):
    """Aplica filtro Butterworth passa-baixa zero-lag, lidando com NaNs."""
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

def analisar_hsw(path_c3d):
    print(f"\n[Processando HSW] Arquivo: {os.path.basename(path_c3d)}")
    try:
        c3d = ezc3d.c3d(path_c3d)
    except Exception as e:
        print(f"[Erro] Falha ao ler {path_c3d}: {e}")
        return None

    points = c3d['data']['points']
    labels = c3d['parameters']['POINT']['LABELS']['value']
    freq = c3d['header']['points']['frame_rate']
    dt = 1.0 / freq if freq > 0 else 0.01

    # --- NOVO: Filtragem Cinemática (6 Hz) ---
    for coord in range(3): # X, Y, Z
        for marcador in range(points.shape[1]):
            points[coord, marcador, :] = apply_lowpass(points[coord, marcador, :], cutoff=6.0, fs=freq)

    def get_point(names_list):
        for name in names_list:
            for i, l in enumerate(labels):
                if l.strip().upper() == name.strip().upper():
                    return points[:3, i, :]
        return np.full((3, points.shape[2]), np.nan)

    # Pegar Punhos (Para detectar passos)
    lwr = get_point(["LWRB", "LWR", "LWRA", "LWRIST"])
    rwr = get_point(["RWRB", "RWR", "RWRA", "RWRIST"])

    # Eixo de progressão da caminhada é predominantemente Y
    # Precisamos achar os momentos em que a mão entra em contato com o chão.
    # Quando em contato: Velocidade Horizontal ~ 0 e Altura Z baixa.
    
    # Suavização da cinemática para derivada
    def smooth(data, window=11):
        if np.all(np.isnan(data)): return data
        mask = ~np.isnan(data)
        smoothed = np.copy(data)
        if np.sum(mask) > window:
            smoothed[mask] = signal.savgol_filter(data[mask], window, 3)
        return smoothed

    lwr_y = smooth(lwr[1, :])
    rwr_y = smooth(rwr[1, :])
    
    vel_lwr_y = np.gradient(lwr_y) / dt
    vel_rwr_y = np.gradient(rwr_y) / dt

    # Algoritmo de Swing/Stance:
    # A passada (Swing) acontece quando a velocidade em Y é alta.
    # Vamos achar os picos de velocidade (momento do passo).
    peaks_l, _ = signal.find_peaks(np.abs(vel_lwr_y), height=500, distance=freq/2) # velocidade > 0.5 m/s
    peaks_r, _ = signal.find_peaks(np.abs(vel_rwr_y), height=500, distance=freq/2)

    # Cada pico é o meio de uma passada no ar.
    # O passo é completado quando a velocidade cai para zero após o pico.
    passos_l_y = []
    passos_l_x = []
    tempos_l = []
    for p in peaks_l:
        search_range = vel_lwr_y[p:p+int(freq)]
        if len(search_range) > 0:
            contato_idx = p + np.argmin(np.abs(search_range))
            passos_l_y.append(lwr[1, contato_idx])
            passos_l_x.append(lwr[0, contato_idx])
            tempos_l.append(contato_idx * dt)

    passos_r_y = []
    passos_r_x = []
    tempos_r = []
    for p in peaks_r:
        search_range = vel_rwr_y[p:p+int(freq)]
        if len(search_range) > 0:
            contato_idx = p + np.argmin(np.abs(search_range))
            passos_r_y.append(rwr[1, contato_idx])
            passos_r_x.append(rwr[0, contato_idx])
            tempos_r.append(contato_idx * dt)

    # Largura da Base de Apoio (Distância Mediolateral - Eixo X)
    largura_base = np.nanmean(np.abs(np.array(passos_l_x[:min(len(passos_l_x), len(passos_r_x))]) - 
                                     np.array(passos_r_x[:min(len(passos_l_x), len(passos_r_x))])))

    # Calcular Comprimentos das Passadas (Distância espacial entre os apoios Y)
    # Stride (mesmo lado)
    strides_l = np.abs(np.diff(passos_l_y))
    strides_r = np.abs(np.diff(passos_r_y))
    todas_strides = np.concatenate((strides_l, strides_r))
    
    if len(todas_strides) == 0:
        return {"Cadencia": 0, "Stride Media": 0, "CV Stride": 0, "CV Tempo": 0}

    stride_media = np.nanmean(todas_strides)
    cv_stride = (np.nanstd(todas_strides) / stride_media * 100) if stride_media > 0 else 0

    # Calcular Tempos
    tempos_strides_l = np.diff(tempos_l)
    tempos_strides_r = np.diff(tempos_r)
    todos_tempos = np.concatenate((tempos_strides_l, tempos_strides_r))
    
    tempo_medio = np.nanmean(todos_tempos)
    cv_tempo = (np.nanstd(todos_tempos) / tempo_medio * 100) if tempo_medio > 0 else 0

    # Distância Percorrida Total em Y (Metros / Milímetros)
    if len(passos_l_y) > 0 and len(passos_r_y) > 0:
        dist_min = min(min(passos_l_y), min(passos_r_y))
        dist_max = max(max(passos_l_y), max(passos_r_y))
        distancia_total = abs(dist_max - dist_min)
    else:
        distancia_total = 0

    # Cadência (passos por segundo). 1 stride = 2 passos.
    total_passos = len(tempos_l) + len(tempos_r)
    duracao_total = (max(tempos_l[-1] if tempos_l else 0, tempos_r[-1] if tempos_r else 0) - 
                     min(tempos_l[0] if tempos_l else 0, tempos_r[0] if tempos_r else 0))
    cadencia = total_passos / duracao_total if duracao_total > 0 else 0

    # --- MÓDULO 3: TÉCNICA ---
    def calcular_vetor(p1, p2): return p2 - p1
    def calc_ang(v1, v2):
        norm1, norm2 = np.linalg.norm(v1, axis=0), np.linalg.norm(v2, axis=0)
        cos_theta = np.sum(v1 * v2, axis=0) / (norm1 * norm2 + 1e-8)
        return np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

    # Marcadores
    t10 = get_point(["T10"])
    c7 = get_point(["C7"])
    lsho = get_point(["LSHO"])
    rsho = get_point(["RSHO"])
    lasi = get_point(["LASI"])
    rasi = get_point(["RASI"])
    lank = get_point(["LANK", "LHEE"])
    rank = get_point(["RANK", "RHEE"])
    head = get_point(["HEAD", "RFHD", "LFHD"])
    lfin = get_point(["LFIN", "LFIN1", "LFING"])
    rfin = get_point(["RFIN", "RFIN1", "RFING"])

    # Centros segmentares
    pelve_centro = (lasi + rasi) / 2.0
    tornozelo_centro = (lank + rank) / 2.0
    ombro_centro = (lsho + rsho) / 2.0
    punho_centro = (lwr + rwr) / 2.0

    # Vetores articulares
    vetor_tronco = calcular_vetor(t10, c7)
    vetor_braco = calcular_vetor(ombro_centro, punho_centro)
    vetor_perna = calcular_vetor(pelve_centro, tornozelo_centro)
    vetor_cabeca = calcular_vetor(c7, head)

    ang_ombro = calc_ang(vetor_tronco, vetor_braco)
    ang_quadril = calc_ang(vetor_tronco, vetor_perna)
    ang_cerv = calc_ang(vetor_tronco, vetor_cabeca)

    desvio_global = np.nanmean(ang_ombro + (180.0 - ang_quadril))
    cerv_media = np.nanmean(ang_cerv)

    # Rotação da mão (Eixo Frente é o Y, Eixo Base é o X)
    vetor_frente = np.array([0, 1]) # Caminhada é predominantemente em Y
    vetor_mao_l = (lfin[:2, :] - lwr[:2, :])
    vetor_mao_r = (rfin[:2, :] - rwr[:2, :])

    # Angulo com o eixo Y
    def calc_ang_2d(v1, v2):
        norm1 = np.linalg.norm(v1, axis=0)
        norm2 = np.linalg.norm(v2)
        cos_theta = np.sum(v1 * v2[:, np.newaxis], axis=0) / (norm1 * norm2 + 1e-8)
        return np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))

    ang_mao_l = calc_ang_2d(vetor_mao_l, vetor_frente)
    ang_mao_r = calc_ang_2d(vetor_mao_r, vetor_frente)
    rotacao_mao = np.nanmean((ang_mao_l + ang_mao_r) / 2.0)

    print(f"  - Desvio Articular Global: {desvio_global:.1f} graus")

    return {
        "Cadencia (passos/s)": cadencia,
        "Distancia Percorrida (m)": distancia_total / 1000.0,
        "Comprimento Passada (mm)": stride_media,
        "Largura Base Apoio (mm)": largura_base,
        "CV Comprimento (%)": cv_stride,
        "CV Tempo (%)": cv_tempo,
        "Rotacao Maos (deg)": rotacao_mao,
        "Desvio Articular Global (deg)": desvio_global,
        "Extensao Cervical (deg)": cerv_media
    }

if __name__ == "__main__":
    res_hsw01 = analisar_hsw("hsw01_limpo.c3d")
    res_hsw02 = analisar_hsw("hsw02_limpo.c3d")
    
    import pandas as pd
    if res_hsw01 and res_hsw02:
        df = pd.DataFrame({"Alinhado (hsw01)": res_hsw01, "Banana (hsw02)": res_hsw02})
        df.to_csv("resultados_hsw.csv")
        print("\n[Sucesso] Tabela exportada para resultados_hsw.csv")
