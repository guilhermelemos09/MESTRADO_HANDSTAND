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
    if len(valid_idx) < 18: return data
    
    data_interp = np.copy(data)
    nan_idx = np.where(np.isnan(data))[0]
    if len(nan_idx) > 0:
        data_interp[nan_idx] = np.interp(nan_idx, valid_idx, data[valid_idx])
        
    data_filtered = filtfilt(b, a, data_interp)
    data_filtered[nan_idx] = np.nan
    return data_filtered

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
    if N < 10: return np.nan
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
# PIPELINE PILOTO: HANDSTAND ESTÁTICO (CoP nativo e Blocos)
# =============================================================================

def analisar_hs_piloto(path_c3d, condicao="livre"):
    print(f"\n[Processando] Arquivo: {path_c3d} | Condição: {condicao.upper()}")
    
    c = ezc3d.c3d(path_c3d)
    
    # --- DADOS CINEMÁTICOS ---
    points = c['data']['points']
    marker_names = c['parameters']['POINT']['LABELS']['value']
    freq_point = c['header']['points']['frame_rate']
    
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

    def get_highest_z(names_list):
        num_frames = points.shape[2]
        max_z = np.full(num_frames, -np.inf)
        found = False
        for name in names_list:
            for idx, m_name in enumerate(marker_names):
                if m_name.strip().upper() == name.strip().upper():
                    z = points[2, idx, :]
                    valid = ~np.isnan(z) & (z != 0)
                    max_z[valid] = np.maximum(max_z[valid], z[valid])
                    found = True
        if not found:
            return np.full(num_frames, np.nan)
        max_z[np.isinf(max_z)] = np.nan
        return max_z

    # Filtragem Cinemática
    for coord in range(3):
        for marcador in range(points.shape[1]):
            points[coord, marcador, :] = apply_lowpass(points[coord, marcador, :], cutoff=6.0, fs=freq_point)

    pelve_z = get_highest_z(["LASI", "LPSI", "RASI", "RPSI"])
    tornozelo_z = get_highest_z(["LANK", "RANK", "LHEE", "RHEE", "LTOE", "RTOE"])
    
    # GATILHO DE TRIM (ASSISTIDO VS LIVRE)
    condicao_inversao = ~np.isnan(pelve_z) & ~np.isnan(tornozelo_z) & (tornozelo_z > pelve_z + 300)
    
    if condicao.lower() == "assistido":
        mao_pesquisador = get_point(["Apoio", "APOIO", "M_PESQ", "Pesquisador"])
        tornozelo_3d = get_point(["LANK", "RANK"])
        # Distancia 3D
        distancia = np.linalg.norm(mao_pesquisador - tornozelo_3d, axis=0)
        # Inicia quando está invertido E a distancia do pesquisador for > 200mm
        frames_validos = np.where(condicao_inversao & (distancia > 200))[0]
    else:
        frames_validos = np.where(condicao_inversao)[0]
    
    if len(frames_validos) > 10:
        start_idx = frames_validos[0]
        end_idx = frames_validos[-1]
    else:
        start_idx = 0
        end_idx = points.shape[2] - 1

    tempo_equilibrio = (end_idx - start_idx) / freq_point if freq_point > 0 else np.nan

    # PONTOS DO CORPO
    punho_l = get_point(["LWRB", "LWR", "LWRA", "LWRIST"])
    punho_r = get_point(["RWRB", "RWR", "RWRA", "RWRIST"])
    dedo_l = get_point(["LFIN", "LFIN1", "LFING"])
    dedo_r = get_point(["RFIN", "RFIN1", "RFING"])
    t10 = get_point(["T10"])
    c7 = get_point(["C7"])
    head = get_point(["LFHD", "HEAD"])
    rsho = get_point(["RSHO", "RSHO_clean"])
    relb = get_point(["RELB"])
    pelve_l = get_point(["LASI", "LPSI"])
    pelve_r = get_point(["RASI", "RPSI"])
    pelve_centro = (pelve_l + pelve_r) / 2.0
    joelho = get_point(["RKNE", "LKNE"])

    # Base de Apoio e Angulo da Mao
    base_apoio_media = np.nanmean(np.linalg.norm(punho_l[:, start_idx:end_idx] - punho_r[:, start_idx:end_idx], axis=0))
    vetor_base_2d = punho_r[:2, start_idx:end_idx] - punho_l[:2, start_idx:end_idx]
    vetor_frente_2d = np.zeros_like(vetor_base_2d)
    vetor_frente_2d[0, :] = -vetor_base_2d[1, :]
    vetor_frente_2d[1, :] = vetor_base_2d[0, :]
    vetor_mao_l_2d = dedo_l[:2, start_idx:end_idx] - punho_l[:2, start_idx:end_idx]
    vetor_mao_r_2d = dedo_r[:2, start_idx:end_idx] - punho_r[:2, start_idx:end_idx]
    ang_mao_l = calcular_angulo_entre_vetores(vetor_mao_l_2d, vetor_frente_2d)
    ang_mao_r = calcular_angulo_entre_vetores(vetor_mao_r_2d, vetor_frente_2d)
    rotacao_mao_media = np.nanmean((ang_mao_l + ang_mao_r) / 2.0)

    # Comprimento dos Membros
    tornozelo_l = get_point(["LANK", "LHEE"])
    tornozelo_r = get_point(["RANK", "RHEE"])
    tornozelo_centro = (tornozelo_l + tornozelo_r) / 2.0
    comprimento_braco = np.nanmean(np.linalg.norm(rsho[:, start_idx:end_idx] - punho_r[:, start_idx:end_idx], axis=0))
    comprimento_perna = np.nanmean(np.linalg.norm(tornozelo_centro[:, start_idx:end_idx] - pelve_centro[:, start_idx:end_idx], axis=0))

    # Índice de Verticalidade (Punho -> Pelve -> Tornozelo)
    punho_centro = (punho_l + punho_r) / 2.0
    vetor_inferior = pelve_centro[:, start_idx:end_idx] - punho_centro[:, start_idx:end_idx]
    vetor_superior = tornozelo_centro[:, start_idx:end_idx] - pelve_centro[:, start_idx:end_idx]
    indice_verticalidade = np.nanmean(calcular_angulo_entre_vetores(vetor_inferior, vetor_superior))

    # Extensão Cervical
    vetor_tronco = c7[:, start_idx:end_idx] - t10[:, start_idx:end_idx]
    vetor_cabeca = head[:, start_idx:end_idx] - c7[:, start_idx:end_idx]
    extensao_cervical = np.nanmean(calcular_angulo_entre_vetores(vetor_tronco, vetor_cabeca))

    # CoM
    com_aprox = pelve_centro[:, start_idx:end_idx]
    com_z_medio = np.nanmean(com_aprox[2, :])

    # --- DADOS CINÉTICOS E CÁLCULO DE CoP ---
    analog_labels = c['parameters']['ANALOG']['LABELS']['value']
    analogs = c['data']['analogs']
    freq_analogo = c['header']['analogs']['frame_rate']
    ratio = int(freq_analogo / freq_point) if freq_point > 0 else 1
    start_analog = start_idx * ratio
    end_analog = end_idx * ratio

    def get_analog(name):
        for i, s in enumerate(analog_labels):
            if name.strip().upper() in s.strip().upper():
                return analogs[0, i, start_analog:end_analog]
        return np.zeros(end_analog - start_analog)

    fx1 = apply_lowpass(get_analog("Force.Fx1"), cutoff=20.0, fs=freq_analogo)
    fy1 = apply_lowpass(get_analog("Force.Fy1"), cutoff=20.0, fs=freq_analogo)
    fz1 = apply_lowpass(get_analog("Force.Fz1"), cutoff=20.0, fs=freq_analogo)
    mx1 = apply_lowpass(get_analog("Moment.Mx1"), cutoff=20.0, fs=freq_analogo)
    my1 = apply_lowpass(get_analog("Moment.My1"), cutoff=20.0, fs=freq_analogo)

    fx2 = apply_lowpass(get_analog("Force.Fx2"), cutoff=20.0, fs=freq_analogo)
    fy2 = apply_lowpass(get_analog("Force.Fy2"), cutoff=20.0, fs=freq_analogo)
    fz2 = apply_lowpass(get_analog("Force.Fz2"), cutoff=20.0, fs=freq_analogo)
    mx2 = apply_lowpass(get_analog("Moment.Mx2"), cutoff=20.0, fs=freq_analogo)
    my2 = apply_lowpass(get_analog("Moment.My2"), cutoff=20.0, fs=freq_analogo)

    # Identificar qual plataforma (1 ou 2) está sendo usada pelo atleta (a com maior força Z)
    mean_fz1 = np.nanmean(fz1) if len(fz1) > 0 else 0
    mean_fz2 = np.nanmean(fz2) if len(fz2) > 0 else 0
    
    if np.abs(mean_fz1) > np.abs(mean_fz2):
        fx, fy, fz, mx, my = fx1, fy1, fz1, mx1, my1
    else:
        fx, fy, fz, mx, my = fx2, fy2, fz2, mx2, my2

    # Evitar divisao por zero onde nao tem pisada (limiar de 20N)
    valid_force = np.abs(fz) > 20.0 
    
    # CÁLCULO DO CoP (dz = 0, origem na superfície da plataforma)
    cop_x = np.full_like(fz, np.nan)
    cop_y = np.full_like(fz, np.nan)
    cop_x[valid_force] = (-my[valid_force]) / fz[valid_force]
    cop_y[valid_force] = (mx[valid_force]) / fz[valid_force]

    # Distância CoP-CoM
    # Precisamos interpolar o CoM (que está na freq de ponto) para a freq análoga
    com_x_analog = np.interp(np.linspace(0, 1, len(cop_x)), np.linspace(0, 1, com_aprox.shape[1]), com_aprox[0, :])
    com_y_analog = np.interp(np.linspace(0, 1, len(cop_y)), np.linspace(0, 1, com_aprox.shape[1]), com_aprox[1, :])
    
    dist_cop_com = np.sqrt((cop_x - com_x_analog)**2 + (cop_y - com_y_analog)**2)
    distancia_cop_com_media = np.nanmean(dist_cop_com)

    # Velocidade do CoP
    dt = 1.0 / freq_analogo if freq_analogo > 0 else 0.001
    vel_cop_x = np.diff(cop_x) / dt
    vel_cop_y = np.diff(cop_y) / dt
    vel_cop = np.sqrt(vel_cop_x**2 + vel_cop_y**2)
    velocidade_cop_media = np.nanmean(vel_cop)

    # Entropia do CoP (Exemplo: Raio da trajetória do CoP)
    cop_raio = np.sqrt(cop_x**2 + cop_y**2)
    max_pts = 500
    cop_ds = cop_raio[~np.isnan(cop_raio)]
    if len(cop_ds) > max_pts:
        step = len(cop_ds) // max_pts
        cop_ds = cop_ds[::step][:max_pts]
    
    apen_cop = calcular_apen(cop_ds)

    return {
        "Condição": condicao.upper(),
        "Tempo de Equilibrio (s)": tempo_equilibrio,
        "Base Apoio (mm)": base_apoio_media,
        "Rotacao das Maos (deg)": rotacao_mao_media,
        "Altura CoM (mm)": com_z_medio,
        "Distancia CoP-CoM (mm)": distancia_cop_com_media,
        "Velocidade CoP (mm/s)": velocidade_cop_media,
        "ApEn CoP": apen_cop,
        "Comprimento Braco (mm)": comprimento_braco,
        "Comprimento Perna (mm)": comprimento_perna,
        "Indice Verticalidade (deg)": indice_verticalidade,
        "Extensao Cervical (deg)": extensao_cervical
    }

if __name__ == "__main__":
    # Teste de execução no piloto (Assumindo que os nomes são de "livre" pois nao tinhamos marcador de pesquisador no piloto anterior)
    testes = [
        ("Piloto HS01", "hs01_limpo.c3d", "livre"),
        ("Piloto HS02", "hs02_limpo.c3d", "livre")
    ]
    
    resultados = {}
    
    for nome, arq, cond in testes:
        if os.path.exists(arq):
            try:
                resultados[nome] = analisar_hs_piloto(arq, cond)
            except Exception as e:
                print(f"[Erro] Falha no teste {nome}: {e}")
        else:
            print(f"[Aviso] Arquivo {arq} não encontrado.")

    if resultados:
        print("\n" + "="*80)
        print("          RESULTADOS PILOTO - HANDSTAND ESTÁTICO (CoP)")
        print("="*80)
        metricas = list(resultados[list(resultados.keys())[0]].keys())
        print(f"{'Métrica':<30} | " + " | ".join([f"{cond:<15}" for cond in resultados.keys()]))
        print("-" * 80)
        for metrica in metricas:
            valores = []
            for cond in resultados.keys():
                val = resultados[cond][metrica]
                if isinstance(val, float):
                    valores.append(f"{val:<15.4f}")
                else:
                    valores.append(f"{str(val):<15}")
            print(f"{metrica:<30} | " + " | ".join(valores))
        print("="*80)
