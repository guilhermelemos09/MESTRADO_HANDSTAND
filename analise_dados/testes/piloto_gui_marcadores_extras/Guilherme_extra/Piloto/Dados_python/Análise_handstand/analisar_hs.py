import numpy as np
import ezc3d
import csv
import os
from scipy.signal import butter, filtfilt

# =============================================================================
# FUNÇÕES MATEMÁTICAS AUXILIARES
# =============================================================================

def apply_lowpass(data, cutoff, fs, order=4):
    """Aplica filtro Butterworth passa-baixa zero-lag, lidando com NaNs."""
    if fs <= 0 or np.all(np.isnan(data)): return data
    nyq = 0.5 * fs
    normal_cutoff = cutoff / nyq
    if normal_cutoff >= 1: return data
    
    b, a = butter(order, normal_cutoff, btype='low', analog=False)
    
    valid_idx = np.where(~np.isnan(data))[0]
    if len(valid_idx) < 18: return data # min padlen
    
    data_interp = np.copy(data)
    nan_idx = np.where(np.isnan(data))[0]
    if len(nan_idx) > 0:
        data_interp[nan_idx] = np.interp(nan_idx, valid_idx, data[valid_idx])
        
    data_filtered = filtfilt(b, a, data_interp)
    data_filtered[nan_idx] = np.nan # devolve os NaNs pro lugar
    return data_filtered
# FUNÇÕES MATEMÁTICAS AUXILIARES
# =============================================================================

def calcular_vetor(p1, p2):
    return p2 - p1

def calcular_angulo_entre_vetores(v1, v2):
    dot_product = np.sum(v1 * v2, axis=0)
    norm_v1 = np.linalg.norm(v1, axis=0)
    norm_v2 = np.linalg.norm(v2, axis=0)
    
    cosine_angle = np.clip(dot_product / (norm_v1 * norm_v2), -1.0, 1.0)
    return np.degrees(np.arccos(cosine_angle))

def calcular_apen(sinal, m=2, r=0.2):
    sinal = sinal[~np.isnan(sinal)]
    N = len(sinal)
    if N < 10:
        return np.nan
    r_val = r * np.std(sinal)
    
    def _phi(m):
        x = np.array([sinal[i:i + m] for i in range(N - m + 1)])
        diff = np.abs(x[:, None, :] - x[None, :, :])
        dist = np.max(diff, axis=2)
        C = np.sum(dist <= r_val, axis=1) / (N - m + 1.0)
        return np.sum(np.log(C)) / (N - m + 1.0)
    
    try:
        return np.abs(_phi(m) - _phi(m + 1))
    except Exception:
        return np.nan

# =============================================================================
# PIPELINE HÍBRIDO (Cinemática Limpa + Força Bruta)
# =============================================================================

def analisar_arquivos_hibrido(path_limpo, path_bruto):
    print(f"\n[Processando] Cinemática: {path_limpo} | Força: {path_bruto}")
    
    # 1. Carregar Cinemática
    c3d_kin = ezc3d.c3d(path_limpo)
    points = c3d_kin['data']['points']
    marker_names = c3d_kin['parameters']['POINT']['LABELS']['value']
    
    def get_marker_idx(name):
        for idx, m_name in enumerate(marker_names):
            if m_name.strip().upper() == name.strip().upper():
                return idx
        return None

    # Helper para pegar ponto 3D com fallback seguro (retorna NaNs se não achar)
    def get_point(names_list):
        for name in names_list:
            idx = get_marker_idx(name)
            if idx is not None:
                return points[:3, idx, :]
        return np.full((3, points.shape[2]), np.nan)

    # --- NOVO: Algoritmo de Corte Automático (Trim) ---
    pelve_z = get_point(["LASI", "LPSI", "RASI"])[2, :]
    tornozelo_z = get_point(["LANK", "RANK", "LHEE"])[2, :]
    
    # Condição de equilíbrio: Tornozelo deve estar pelo menos 300mm acima da pelve
    frames_validos = np.where(~np.isnan(pelve_z) & ~np.isnan(tornozelo_z) & (tornozelo_z > pelve_z + 300))[0]
    
    if len(frames_validos) > 10:
        start_idx = frames_validos[0]
        end_idx = frames_validos[-1]
    else:
        # Fallback se não encontrar a postura (processa tudo)
        start_idx = 0
        end_idx = points.shape[2] - 1

    # Fatiar Cinemática
    points = points[:, :, start_idx:end_idx]
    
    # --- NOVO: Filtragem Cinemática (6 Hz) ---
    freq_point = c3d_kin['header']['points']['frame_rate']
    for coord in range(3): # X, Y, Z
        for marcador in range(points.shape[1]):
            points[coord, marcador, :] = apply_lowpass(points[coord, marcador, :], cutoff=6.0, fs=freq_point)

    # --- Cinemática: Base de Apoio e Rotação da Mão ---
    punho_l = get_point(["LWRB", "LWR", "LWRA", "LWRIST"])
    punho_r = get_point(["RWRB", "RWR", "RWRA", "RWRIST"])
    base_apoio_media = np.nanmean(np.linalg.norm(punho_l - punho_r, axis=0))

    dedo_l = get_point(["LFIN", "LFIN1", "LFING"])
    dedo_r = get_point(["RFIN", "RFIN1", "RFING"])

    # Eixo relativo do corpo (Medio-lateral 2D: punho esquerdo para o direito)
    vetor_base_2d = punho_r[:2, :] - punho_l[:2, :]
    
    # Eixo "Frente" (Perpendicular 90 graus a base no plano XY)
    vetor_frente_2d = np.zeros_like(vetor_base_2d)
    vetor_frente_2d[0, :] = -vetor_base_2d[1, :]
    vetor_frente_2d[1, :] = vetor_base_2d[0, :]

    vetor_mao_l_2d = dedo_l[:2, :] - punho_l[:2, :]
    vetor_mao_r_2d = dedo_r[:2, :] - punho_r[:2, :]

    ang_mao_l = calcular_angulo_entre_vetores(vetor_mao_l_2d, vetor_frente_2d)
    ang_mao_r = calcular_angulo_entre_vetores(vetor_mao_r_2d, vetor_frente_2d)
    
    # Média da rotação das mãos (0 = Frente, 90 = Lateral/Aberta)
    rotacao_mao_media = np.nanmean((ang_mao_l + ang_mao_r) / 2.0)
    
    # --- Cinemática: Ângulos ---
    t10 = get_point(["T10"])
    c7 = get_point(["C7"])
    head = get_point(["LFHD", "HEAD"])
    rsho = get_point(["RSHO", "RSHO_clean"])
    relb = get_point(["RELB"])
    
    pelve_l = get_point(["LASI", "LPSI"])
    pelve_r = get_point(["RASI", "RPSI"])
    pelve_centro = (pelve_l + pelve_r) / 2.0
    joelho = get_point(["RKNE", "LKNE"]) # Média ou o que estiver disponível
    
    vetor_tronco = calcular_vetor(t10, c7)
    vetor_braco = calcular_vetor(rsho, relb)
    vetor_cabeca = calcular_vetor(c7, head)
    vetor_perna = calcular_vetor(pelve_centro, joelho)

    # a) Verticalidade do Ombro (Ideal = 0°)
    ang_ombro = calcular_angulo_entre_vetores(vetor_tronco, vetor_braco)
    
    # b) Extensão Cervical
    ang_cerv = calcular_angulo_entre_vetores(vetor_tronco, vetor_cabeca)
    cerv_media = np.nanmean(ang_cerv)
    
    # c) Ângulo do Quadril (Ideal = 180°)
    ang_quadril = calcular_angulo_entre_vetores(vetor_tronco, vetor_perna)

    # NOVO: Índice de Desvio Articular Global (IDAG)
    # Soma o quanto o ombro desvia de 0° e o quanto o quadril desvia de 180°
    desvio_global = np.nanmean(ang_ombro + (180.0 - ang_quadril))

    # d) Amplitude de Oscilação do Centro de Massa (CoM) e Altura
    com_aprox = pelve_centro
    com_x_mean = np.nanmean(com_aprox[0, :])
    com_y_mean = np.nanmean(com_aprox[1, :])
    sway_com = np.sqrt((com_aprox[0, :] - com_x_mean)**2 + (com_aprox[1, :] - com_y_mean)**2)
    com_sway_medio = np.nanmean(sway_com)
    
    # Altura do CoM (Eixo Z médio)
    altura_com_media = np.nanmean(com_aprox[2, :])

    # 2. Carregar Forças Brutas e Aplicar Corte Proporcional
    c3d_force = ezc3d.c3d(path_bruto)
    analog_labels = c3d_force['parameters']['ANALOG']['LABELS']['value']
    analogs = c3d_force['data']['analogs']
    freq_analogo = c3d_force['header']['analogs']['frame_rate']
    dt = 1.0 / freq_analogo if freq_analogo > 0 else 0.001
    
    # Frequência cinemática para achar a proporção (ratio)
    freq_point = c3d_kin['header']['points']['frame_rate']
    ratio = int(freq_analogo / freq_point) if freq_point > 0 else 1
    
    start_analog = start_idx * ratio
    end_analog = end_idx * ratio

    def get_analog(name):
        for i, s in enumerate(analog_labels):
            if name.strip().upper() in s.strip().upper():
                return analogs[0, i, start_analog:end_analog]
        return np.zeros(end_analog - start_analog)

    fx1 = get_analog("Force.Fx1")
    fy1 = get_analog("Force.Fy1")
    fx2 = get_analog("Force.Fx2")
    fy2 = get_analog("Force.Fy2")

    # --- NOVO: Filtragem Cinética (20 Hz) ---
    fx1 = apply_lowpass(fx1, cutoff=20.0, fs=freq_analogo)
    fy1 = apply_lowpass(fy1, cutoff=20.0, fs=freq_analogo)
    fx2 = apply_lowpass(fx2, cutoff=20.0, fs=freq_analogo)
    fy2 = apply_lowpass(fy2, cutoff=20.0, fs=freq_analogo)

    # Força Resultante Horizontal (Proxy perfeitamente validado para controle postural)
    fx_total = fx1 + fx2
    fy_total = fy1 + fy2
    
    # e) Velocidade do Sinal de Força
    vel_fx = np.diff(fx_total) / dt
    vel_fy = np.diff(fy_total) / dt
    vel_forca_media = np.nanmean(np.sqrt(vel_fx**2 + vel_fy**2))

    # f) Entropia Aproximada (ApEn) da Força Global
    forca_resultante = np.sqrt(fx_total**2 + fy_total**2)
    max_pts = 500
    if len(forca_resultante) > max_pts:
        step = len(forca_resultante) // max_pts
        forca_ds = forca_resultante[::step][:max_pts]
    else:
        forca_ds = forca_resultante

    apen_forca_global = calcular_apen(forca_ds)

    # g) Tempo de Equilíbrio (Duração do trial)
    tempo_equilibrio = (end_idx - start_idx) / freq_point if freq_point > 0 else np.nan

    return {
        "Tempo de Equilibrio (s)": tempo_equilibrio,
        "Base Apoio (mm)": base_apoio_media,
        "Rotacao das Maos (deg)": rotacao_mao_media,
        "Desvio Articular Global (deg)": desvio_global,
        "Extensao Cervical (deg)": cerv_media,
        "Altura CoM (mm)": altura_com_media,
        "Oscilacao CoM (mm)": com_sway_medio,
        "Velocidade Forca Horiz. (N/s)": vel_forca_media,
        "ApEn Forca Global": apen_forca_global
    }

# =============================================================================
# EXECUÇÃO PRINCIPAL
# =============================================================================

if __name__ == "__main__":
    testes = [
        ("Alinhado (hs01)", "hs01_limpo.c3d", "hs01.c3d"),
        ("Banana (hs02)", "hs02_limpo.c3d", "hs02.c3d")
    ]
    
    resultados = {}
    
    for nome, arq_limpo, arq_bruto in testes:
        if os.path.exists(arq_limpo) and os.path.exists(arq_bruto):
            try:
                resultados[nome] = analisar_arquivos_hibrido(arq_limpo, arq_bruto)
            except Exception as e:
                print(f"[Erro] Falha no teste {nome}: {e}")
        else:
            print(f"[Aviso] Arquivos para {nome} não encontrados.")

    if resultados:
        print("\n" + "="*80)
        print("          RESULTADOS BIOMECÂNICOS DEFINITIVOS")
        print("="*80)
        
        metricas = list(resultados[list(resultados.keys())[0]].keys())
        print(f"{'Métrica':<35} | " + " | ".join([f"{cond:<18}" for cond in resultados.keys()]))
        print("-" * 80)
        
        for metrica in metricas:
            valores = []
            for cond in resultados.keys():
                val = resultados[cond][metrica]
                valores.append(f"{val:<18.4f}" if isinstance(val, (int, float)) else f"{str(val):<18}")
            print(f"{metrica:<35} | " + " | ".join(valores))
        print("="*80)

        # Exportar
        with open("resultados_definitivos.csv", "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            header = ["Metrica"] + list(resultados.keys())
            writer.writerow(header)
            for metrica in metricas:
                row = [metrica]
                for cond in resultados.keys():
                    row.append(resultados[cond][metrica])
                writer.writerow(row)
        print("\n[Sucesso] Tabela completa salva em 'resultados_definitivos.csv'!")
