"""
ANÁLISE BIOMECÂNICA OFICIAL - HANDSTAND ESTÁTICO (HS)
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes
"""

import numpy as np
import ezc3d
import os
from scipy.signal import butter, filtfilt

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

def calcular_vetor(p1, p2):
    return p2 - p1

def calcular_angulo_entre_vetores(v1, v2):
    dot_product = np.sum(v1 * v2, axis=0)
    norm_v1 = np.linalg.norm(v1, axis=0)
    norm_v2 = np.linalg.norm(v2, axis=0)
    cosine_angle = np.clip(dot_product / (norm_v1 * norm_v2 + 1e-9), -1.0, 1.0)
    return np.degrees(np.arccos(cosine_angle))

def calcular_apen(sinal, m=2, r=0.2):
    sinal = sinal[~np.isnan(sinal)]
    N = len(sinal)
    if N < 10: return np.nan
    r_val = r * np.std(sinal)
    if r_val == 0: return np.nan
    def _phi(m):
        x = np.array([sinal[i:i + m] for i in range(N - m + 1)])
        diff = np.abs(x[:, None, :] - x[None, :, :])
        dist = np.max(diff, axis=2)
        C = np.sum(dist <= r_val, axis=1) / (N - m + 1.0)
        return np.sum(np.log(C + 1e-9)) / (N - m + 1.0)
    try:
        return np.abs(_phi(m) - _phi(m + 1))
    except Exception:
        return np.nan

def safe_stats(signal, dt=0.01):
    valid = signal[~np.isnan(signal)]
    if len(valid) < 5:
        return np.nan, np.nan, np.nan, np.nan
    media = float(np.mean(valid))
    rom = float(np.max(valid) - np.min(valid))
    sd = float(np.std(valid))
    diff = np.diff(valid) / dt
    vel_rms = float(np.sqrt(np.mean(diff**2)))
    return media, rom, sd, vel_rms

def analisar_hs_arquivo(c3d_path, condicao="assistido"):
    """
    Processa um arquivo C3D limpo de Handstand.
    condicao: 'assistido' ou 'livre'
    """
    c3d = ezc3d.c3d(c3d_path)
    labels = [l.strip() for l in c3d['parameters']['POINT']['LABELS']['value']]
    points = c3d['data']['points']
    fs_points = c3d['parameters']['POINT']['RATE']['value'][0]
    num_frames = points.shape[2]
    
    def get_marker(nomes):
        if isinstance(nomes, str):
            nomes = [nomes]
        cands_clean = [c.strip().upper() for c in nomes]
        for idx, raw in enumerate(labels):
            lbl = raw.strip()
            if ':' in lbl:
                lbl = lbl.split(':')[-1]
            if lbl.upper() in cands_clean:
                p = points[:3, idx, :].copy()
                p[p == 0] = np.nan
                if not np.all(np.isnan(p)):
                    return p
        return np.full((3, num_frames), np.nan)

    # Marcadores
    rsho = get_marker(['RSHO', 'RSHO_clean'])
    lsho = get_marker(['LSHO', 'LSHO_clean'])
    relb = get_marker(['RELB', 'RELB_clean'])
    lelb = get_marker(['LELB', 'LELB_clean'])
    rkne = get_marker(['RKNE', 'RKNE_clean'])
    lkne = get_marker(['LKNE', 'LKNE_clean'])
    rpsi = get_marker(['RPSI'])
    lpsi = get_marker(['LPSI'])
    rasi = get_marker(['RASI'])
    lasi = get_marker(['LASI'])
    rank = get_marker(['RANK'])
    lank = get_marker(['LANK'])
    rhee = get_marker(['RHEE'])
    lhee = get_marker(['LHEE'])
    rtoe = get_marker(['RTOE'])
    ltoe = get_marker(['LTOE'])
    rwra = get_marker(['RWRA', 'RWRB', 'RWRIST', 'RWR'])
    lwra = get_marker(['LWRA', 'LWRB', 'LWRIST', 'LWR'])
    rwrb = get_marker(['RWRB', 'RWRA'])
    lwrb = get_marker(['LWRB', 'LWRA'])
    rfin = get_marker(['RFIN', 'RFIN1', 'RFING'])
    lfin = get_marker(['LFIN', 'LFIN1', 'LFING'])
    c7 = get_marker(['C7'])
    rfhd = get_marker(['RFHD', 'RBHD', 'HEAD'])
    lfhd = get_marker(['LFHD', 'LBHD'])
    m_pesq = get_marker(['Apoio', 'APOIO', 'M_PESQ', 'Pesquisador', 'PESQUISADOR', 'M_pesq', 'ASSIST'])

    # Centros Anatômicos
    centro_ombros = (rsho + lsho) / 2.0
    centro_pelvis = (rpsi + lpsi + rasi + lasi) / 4.0
    centro_punhos = (rwra + lwra + rwrb + lwrb) / 4.0
    centro_cabeca = (rfhd + lfhd) / 2.0

    # Determinação do início e fim do equilíbrio
    # Marcador distal mais alto (Z)
    z_pernas = np.nanmax([rank[2, :], lank[2, :], rhee[2, :], lhee[2, :], rtoe[2, :], ltoe[2, :]], axis=0)
    z_pelvis = centro_pelvis[2, :]

    if condicao.lower() == "assistido" and not np.all(np.isnan(m_pesq)):
        dist_pesq = np.linalg.norm(m_pesq - (rank + lank)/2.0, axis=0)
        is_livre = ((dist_pesq > 250) & (z_pernas > z_pelvis + 300)).astype(int)
    else:
        is_livre = (z_pernas > z_pelvis + 300).astype(int)

    diff_inv = np.diff(is_livre, prepend=0)
    entries = np.where(diff_inv == 1)[0]
    blocks = []
    for e in entries:
        exits = np.where(diff_inv[e:] == -1)[0]
        end_e = e + exits[0] if len(exits) else len(is_livre) - 1
        blocks.append((e, end_e, end_e - e + 1))

    if blocks:
        best_block = max(blocks, key=lambda b: b[2])
        idx_ini, idx_fim = best_block[0], best_block[1]
        tempo_equilibrio = (idx_fim - idx_ini + 1) / fs_points
    else:
        idx_ini = 0
        idx_fim = num_frames - 1
        tempo_equilibrio = (num_frames / fs_points)

    # Segmento de equilíbrio
    def recortar(p): return p[:, idx_ini:idx_fim+1]
    
    ombros_eq = recortar(centro_ombros)
    pelvis_eq = recortar(centro_pelvis)
    punhos_eq = recortar(centro_punhos)
    cabeca_eq = recortar(centro_cabeca)
    c7_eq = recortar(c7)

    # 1. Base de Apoio (Distância entre punhos)
    base_apoio = np.linalg.norm(recortar(rwra) - recortar(lwra), axis=0)
    base_apoio_media = float(np.nanmean(base_apoio))

    # 2. Rotação das mãos (Toe-out em graus)
    vetor_mao_r = recortar(rfin) - recortar(rwra)
    ang_mao_r = np.degrees(np.arctan2(vetor_mao_r[0, :], vetor_mao_r[1, :]))
    vetor_mao_l = recortar(lfin) - recortar(lwra)
    ang_mao_l = np.degrees(np.arctan2(vetor_mao_l[0, :], vetor_mao_l[1, :]))
    rotacao_maos_media = float(np.nanmean((np.abs(ang_mao_r) + np.abs(ang_mao_l)) / 2.0))

    # 3. Índice de Verticalidade (Empilhamento 3D: Ombros - Pelve - Tornozelos)
    vetor_tronco = pelvis_eq - ombros_eq
    vetor_pernas = (recortar(rank) + recortar(lank))/2.0 - pelvis_eq
    vert_ang = calcular_angulo_entre_vetores(vetor_tronco, vetor_pernas)
    indice_verticalidade = float(np.nanmean(vert_ang))

    # 4. Extensão Cervical
    vetor_cabeca = cabeca_eq - c7_eq
    vetor_c7_t10 = c7_eq - recortar(get_marker('T10'))
    ang_cervical = calcular_angulo_entre_vetores(vetor_cabeca, vetor_c7_t10)
    extensao_cervical = float(np.nanmean(ang_cervical))

    # 4b. Flexão Plantar do Tornozelo (Engajamento segmentar distal single-link)
    rkne_rec = recortar(rkne)
    lkne_rec = recortar(lkne)
    rtoe_rec = recortar(get_marker('RTOE'))
    ltoe_rec = recortar(get_marker('LTOE'))
    rank_rec = recortar(rank)
    lank_rec = recortar(lank)
    r_ang_tornozelo = calcular_angulo_entre_vetores(rank_rec - rkne_rec, rtoe_rec - rank_rec)
    l_ang_tornozelo = calcular_angulo_entre_vetores(lank_rec - lkne_rec, ltoe_rec - lank_rec)
    # Flexão plantar a partir dos 90° anatômicos neutros (positivo = ponta de pé estendida)
    flexao_plantar_media = float(np.nanmean(90.0 - (r_ang_tornozelo + l_ang_tornozelo) / 2.0))

    # 4c. Estratégias Articulares de Busca do Equilíbrio (Cotovelo, Ombro, Quadril)
    relb_eq = recortar(relb)
    lelb_eq = recortar(lelb)
    rkne_eq = rkne_rec
    lkne_eq = lkne_rec
    rsho_eq = recortar(rsho)
    lsho_eq = recortar(lsho)
    rwra_eq = recortar(rwra)
    lwra_eq = recortar(lwra)

    # Janela estável para análise articular (descarta 0.5s de subida/descida se durar > 2s)
    buf_frames = int(0.5 * fs_points)
    n_eq = ombros_eq.shape[1]
    if n_eq > 2 * buf_frames + int(1.0 * fs_points):
        w_i, w_f = buf_frames, n_eq - buf_frames
    else:
        w_i, w_f = 0, n_eq

    dt_p = 1.0 / fs_points if fs_points > 0 else 0.01

    # 1. Ângulo do Cotovelo (Antebraço vs Braço)
    v_ante_r = rwra_eq[:, w_i:w_f] - relb_eq[:, w_i:w_f]
    v_braco_r = rsho_eq[:, w_i:w_f] - relb_eq[:, w_i:w_f]
    ang_cot_r = calcular_angulo_entre_vetores(v_ante_r, v_braco_r)

    v_ante_l = lwra_eq[:, w_i:w_f] - lelb_eq[:, w_i:w_f]
    v_braco_l = lsho_eq[:, w_i:w_f] - lelb_eq[:, w_i:w_f]
    ang_cot_l = calcular_angulo_entre_vetores(v_ante_l, v_braco_l)

    ang_cot = np.nanmean([ang_cot_r, ang_cot_l], axis=0) if (not np.all(np.isnan(ang_cot_r)) or not np.all(np.isnan(ang_cot_l))) else ang_cot_r
    cotovelo_medio, cotovelo_rom, cotovelo_sd, cotovelo_vel_rms = safe_stats(ang_cot, dt=dt_p)

    # 2. Ângulo do Ombro (Braço vs Tronco)
    v_braco_sho_r = relb_eq[:, w_i:w_f] - rsho_eq[:, w_i:w_f]
    v_tronco_sho_r = pelvis_eq[:, w_i:w_f] - rsho_eq[:, w_i:w_f]
    ang_sho_r = calcular_angulo_entre_vetores(v_braco_sho_r, v_tronco_sho_r)

    v_braco_sho_l = lelb_eq[:, w_i:w_f] - lsho_eq[:, w_i:w_f]
    v_tronco_sho_l = pelvis_eq[:, w_i:w_f] - lsho_eq[:, w_i:w_f]
    ang_sho_l = calcular_angulo_entre_vetores(v_braco_sho_l, v_tronco_sho_l)

    ang_sho = np.nanmean([ang_sho_r, ang_sho_l], axis=0) if (not np.all(np.isnan(ang_sho_r)) or not np.all(np.isnan(ang_sho_l))) else ang_sho_r
    ombro_medio, ombro_rom, ombro_sd, ombro_vel_rms = safe_stats(ang_sho, dt=dt_p)

    # 3. Ângulo do Quadril (Tronco vs Coxa)
    v_tronco_hip_r = rsho_eq[:, w_i:w_f] - pelvis_eq[:, w_i:w_f]
    v_coxa_r = rkne_eq[:, w_i:w_f] - pelvis_eq[:, w_i:w_f]
    ang_hip_r = calcular_angulo_entre_vetores(v_tronco_hip_r, v_coxa_r)

    v_tronco_hip_l = lsho_eq[:, w_i:w_f] - pelvis_eq[:, w_i:w_f]
    v_coxa_l = lkne_eq[:, w_i:w_f] - pelvis_eq[:, w_i:w_f]
    ang_hip_l = calcular_angulo_entre_vetores(v_tronco_hip_l, v_coxa_l)

    ang_hip = np.nanmean([ang_hip_r, ang_hip_l], axis=0) if (not np.all(np.isnan(ang_hip_r)) or not np.all(np.isnan(ang_hip_l))) else ang_hip_r
    quadril_medio, quadril_rom, quadril_sd, quadril_vel_rms = safe_stats(ang_hip, dt=dt_p)

    # Classificação da Estratégia Predominante
    if np.isnan(cotovelo_sd) or np.isnan(ombro_sd):
        razao_cot_ombro = np.nan
        estrategia_dominante = "Indeterminado"
    else:
        razao_cot_ombro = float(cotovelo_sd / (ombro_sd + 1e-6))
        if cotovelo_sd > 6.0 and razao_cot_ombro >= 1.0:
            estrategia_dominante = "Cotovelo-Dominante"
        elif ombro_sd > 6.0 and razao_cot_ombro < 1.0:
            estrategia_dominante = "Ombro-Dominante"
        elif cotovelo_sd > 5.0 or ombro_sd > 5.0 or (not np.isnan(quadril_sd) and quadril_sd > 5.0):
            estrategia_dominante = "Mista/Multijunta"
        else:
            estrategia_dominante = "Punho-Rigido"

    # 5. Centro de Massa (CoM) aproximado
    com_aprox = (ombros_eq*0.3 + pelvis_eq*0.4 + ((recortar(rank)+recortar(lank))/2.0)*0.3)
    com_z_medio = float(np.nanmean(com_aprox[2, :]))

    # 6. Centro de Pressão (CoP) e Plataforma Bertec
    freq_analogo = fs_points
    cop_x = np.zeros(ombros_eq.shape[1])
    cop_y = np.zeros(ombros_eq.shape[1])
    
    tem_plataforma = ('analogs' in c3d['data']) and (c3d['data']['analogs'].shape[1] >= 6)
    if tem_plataforma:
        analogs = c3d['data']['analogs']
        freq_analogo = c3d['parameters']['ANALOG']['RATE']['value'][0]
        ratio = int(freq_analogo / fs_points) if fs_points > 0 else 1
        
        n_ch = analogs.shape[1]
        a_ini = idx_ini * ratio
        a_fim = (idx_fim + 1) * ratio
        
        if n_ch >= 12:
            # Duas plataformas Bertec combinadas (Mãos D e E)
            fz1 = analogs[0, 2, a_ini:a_fim]
            mx1 = analogs[0, 3, a_ini:a_fim]
            my1 = analogs[0, 4, a_ini:a_fim]
            
            fz2 = analogs[0, 8, a_ini:a_fim]
            mx2 = analogs[0, 9, a_ini:a_fim]
            my2 = analogs[0, 10, a_ini:a_fim]
            
            fz_tot = fz1 + fz2
            mx_tot = mx1 + mx2
            my_tot = my1 + my2
        else:
            fz_tot = analogs[0, 2, a_ini:a_fim]
            mx_tot = analogs[0, 3, a_ini:a_fim]
            my_tot = analogs[0, 4, a_ini:a_fim]
        
        # Filtro passa-baixa 20 Hz (padrão Bertec / posturografia)
        fz_filt = apply_lowpass(fz_tot, cutoff=20.0, fs=freq_analogo, order=4)
        mx_filt = apply_lowpass(mx_tot, cutoff=20.0, fs=freq_analogo, order=4)
        my_filt = apply_lowpass(my_tot, cutoff=20.0, fs=freq_analogo, order=4)
        mask = np.abs(fz_filt) > 50 # Limiar de contato na plataforma (N)
        
        cop_x_an = np.full_like(fz_filt, np.nan)
        cop_y_an = np.full_like(fz_filt, np.nan)
        # Unidades C3D: Momento em N.mm e Força em N -> Divisão já resulta em mm!
        cop_x_an[mask] = -my_filt[mask] / fz_filt[mask]
        cop_y_an[mask] = mx_filt[mask] / fz_filt[mask]
        
        # Downsample para sincronizar com cinemática (fs_points)
        cop_x = np.nanmean(cop_x_an.reshape(-1, ratio), axis=1) if len(cop_x_an) % ratio == 0 else np.interp(np.linspace(0, 1, ombros_eq.shape[1]), np.linspace(0, 1, len(cop_x_an)), cop_x_an)
        cop_y = np.nanmean(cop_y_an.reshape(-1, ratio), axis=1) if len(cop_y_an) % ratio == 0 else np.interp(np.linspace(0, 1, ombros_eq.shape[1]), np.linspace(0, 1, len(cop_y_an)), cop_y_an)
    else:
        # Failsafe se não houver plataforma (usar centro de punhos)
        cop_x = punhos_eq[0, :]
        cop_y = punhos_eq[1, :]

    # Distância CoP - CoM
    dist_cop_com = np.sqrt((cop_x - com_aprox[0, :])**2 + (cop_y - com_aprox[1, :])**2)
    distancia_cop_com_media = float(np.nanmean(dist_cop_com))

    # Velocidade do CoP
    dt = 1.0 / fs_points if fs_points > 0 else 0.01
    vel_cop = np.sqrt(np.diff(cop_x)**2 + np.diff(cop_y)**2) / dt
    velocidade_cop_media = float(np.nanmean(vel_cop))

    # ApEn do CoP (sinal decimado para 20 Hz, recomendação posturográfica)
    cop_raio = np.sqrt(cop_x**2 + cop_y**2)
    step_ds = max(1, int(fs_points / 20.0))
    cop_raio_20hz = cop_raio[::step_ds]
    apen_cop = float(calcular_apen(cop_raio_20hz))

    # Comprimento de membros
    comp_braco = float(np.nanmean(np.linalg.norm(recortar(rsho) - recortar(rwra), axis=0)))
    comp_perna = float(np.nanmean(np.linalg.norm(recortar(rpsi) - recortar(rank), axis=0)))

    return {
        "Condicao": condicao.upper(),
        "Tempo_Sustentacao_s": round(tempo_equilibrio, 2),
        "Distancia_CoP_CoM_mm": round(distancia_cop_com_media, 2),
        "Velocidade_CoP_mm_s": round(velocidade_cop_media, 2),
        "ApEn_CoP": round(apen_cop, 4) if not np.isnan(apen_cop) else "",
        "Indice_Verticalidade_deg": round(indice_verticalidade, 2),
        "Extensao_Cervical_deg": round(extensao_cervical, 2),
        "Flexao_Plantar_deg": round(flexao_plantar_media, 2),
        "Base_Apoio_mm": round(base_apoio_media, 2),
        "Rotacao_Maos_deg": round(rotacao_maos_media, 2),
        "Altura_CoM_mm": round(com_z_medio, 2),
        "Comprimento_Braco_mm": round(comp_braco, 2),
        "Comprimento_Perna_mm": round(comp_perna, 2),
        # --- ESTRATÉGIAS ARTICULARES DE BUSCA DO EQUILÍBRIO ---
        "Cotovelo_Angulo_Medio_deg": round(cotovelo_medio, 2) if not np.isnan(cotovelo_medio) else "",
        "Cotovelo_ROM_deg": round(cotovelo_rom, 2) if not np.isnan(cotovelo_rom) else "",
        "Cotovelo_SD_deg": round(cotovelo_sd, 2) if not np.isnan(cotovelo_sd) else "",
        "Cotovelo_Velocidade_RMS_deg_s": round(cotovelo_vel_rms, 2) if not np.isnan(cotovelo_vel_rms) else "",
        "Ombro_Angulo_Medio_deg": round(ombro_medio, 2) if not np.isnan(ombro_medio) else "",
        "Ombro_ROM_deg": round(ombro_rom, 2) if not np.isnan(ombro_rom) else "",
        "Ombro_SD_deg": round(ombro_sd, 2) if not np.isnan(ombro_sd) else "",
        "Ombro_Velocidade_RMS_deg_s": round(ombro_vel_rms, 2) if not np.isnan(ombro_vel_rms) else "",
        "Quadril_Angulo_Medio_deg": round(quadril_medio, 2) if not np.isnan(quadril_medio) else "",
        "Quadril_ROM_deg": round(quadril_rom, 2) if not np.isnan(quadril_rom) else "",
        "Quadril_SD_deg": round(quadril_sd, 2) if not np.isnan(quadril_sd) else "",
        "Quadril_Velocidade_RMS_deg_s": round(quadril_vel_rms, 2) if not np.isnan(quadril_vel_rms) else "",
        "Razao_Estrategia_Cotovelo_Ombro": round(razao_cot_ombro, 2) if not np.isnan(razao_cot_ombro) else "",
        "Estrategia_Dominante": estrategia_dominante
    }