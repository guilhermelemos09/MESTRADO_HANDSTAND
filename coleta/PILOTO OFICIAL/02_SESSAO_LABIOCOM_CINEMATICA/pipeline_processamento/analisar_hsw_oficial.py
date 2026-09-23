"""
ANÁLISE BIOMECÂNICA OFICIAL - HANDSTAND WALK (HSW)
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes
"""

import numpy as np
import ezc3d
import os
from scipy.signal import find_peaks

def calcular_vetor(p1, p2):
    return p2 - p1

def calcular_angulo_entre_vetores(v1, v2):
    dot_product = np.sum(v1 * v2, axis=0)
    norm_v1 = np.linalg.norm(v1, axis=0)
    norm_v2 = np.linalg.norm(v2, axis=0)
    cosine_angle = np.clip(dot_product / (norm_v1 * norm_v2 + 1e-9), -1.0, 1.0)
    return np.degrees(np.arccos(cosine_angle))

def analisar_hsw_arquivo(c3d_path):
    """
    Processa um arquivo C3D limpo de Handstand Walk.
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

    rwra = get_marker(['RWRA', 'RWRB', 'RWRIST', 'RWR'])
    lwra = get_marker(['LWRA', 'LWRB', 'LWRIST', 'LWR'])
    rfin = get_marker(['RFIN', 'RFIN1', 'RFING'])
    lfin = get_marker(['LFIN', 'LFIN1', 'LFING'])
    rsho = get_marker(['RSHO', 'RSHO_clean'])
    lsho = get_marker(['LSHO', 'LSHO_clean'])
    rpsi = get_marker(['RPSI'])
    lpsi = get_marker(['LPSI'])
    c7 = get_marker(['C7'])
    rfhd = get_marker(['RFHD', 'RBHD', 'HEAD'])
    lfhd = get_marker(['LFHD', 'LBHD'])

    # Failsafe punho/dedo
    m_r = rwra if not np.all(np.isnan(rwra)) else rfin
    m_l = lwra if not np.all(np.isnan(lwra)) else lfin

    # Trajetória anteroposterior (Y) e vertical (Z)
    y_r = m_r[1, :]
    y_l = m_l[1, :]
    z_r = m_r[2, :]
    z_l = m_l[2, :]

    # Detecção de apoio e toques (Touchdowns via vales de Z e velocidade Y)
    # Evento de contato = Z baixo (< 120 mm)
    limiar_contato_z = 120.0
    apoio_r = (z_r < limiar_contato_z)
    apoio_l = (z_l < limiar_contato_z)

    # Identificação do início (primeiro lift-off) e fim (último touchdown)
    frames_marcha = np.where(apoio_r | apoio_l)[0]
    if len(frames_marcha) < 10:
        idx_ini = 0
        idx_fim = num_frames - 1
    else:
        idx_ini = frames_marcha[0]
        idx_fim = frames_marcha[-1]

    tempo_total = (idx_fim - idx_ini + 1) / fs_points

    def recortar(p): return p[:, idx_ini:idx_fim+1]

    # Distância percorrida (deslocamento da pelve no eixo Y/progressão)
    pelvis_y = (recortar(rpsi)[1, :] + recortar(lpsi)[1, :]) / 2.0
    distancia_percorrida_mm = float(np.nanmax(pelvis_y) - np.nanmin(pelvis_y))
    distancia_percorrida_m = distancia_percorrida_mm / 1000.0

    # Velocidade Média de Marcha
    velocidade_media_mm_s = distancia_percorrida_mm / tempo_total if tempo_total > 0 else 0

    # Identificação de Passos (Picos de elevação e toques alternados)
    picos_r, _ = find_peaks(m_r[2, idx_ini:idx_fim+1], distance=int(fs_points*0.3), prominence=40)
    picos_l, _ = find_peaks(m_l[2, idx_ini:idx_fim+1], distance=int(fs_points*0.3), prominence=40)
    num_passos = len(picos_r) + len(picos_l)

    # Critério Metodológico: Somente valida a distância se atingir no mínimo 3 passos
    # Se der 1 ou 2 passos e cair, a tentativa é nula e a distância computada é zero
    if num_passos < 3:
        distancia_percorrida_mm = 0.0
        distancia_percorrida_m = 0.0
        velocidade_media_mm_s = 0.0
        status_marcha = "Invalida (< 3 passos)"
    else:
        status_marcha = "Valida (>= 3 passos)"

    cadencia_passos_s = num_passos / tempo_total if tempo_total > 0 and num_passos >= 3 else 0
    comprimento_passada_medio_mm = distancia_percorrida_mm / num_passos if num_passos >= 3 else 0

    # Variabilidade Espacial e Temporal
    # Tempos entre passos consecutivos
    eventos = sorted(list(picos_r) + list(picos_l))
    if len(eventos) > 2:
        diff_tempos = np.diff(eventos) / fs_points
        cv_temporal = float(np.std(diff_tempos) / np.mean(diff_tempos) * 100.0) if np.mean(diff_tempos) > 0 else 0
    else:
        cv_temporal = 0.0

    # Estimativa de CV espacial a partir do deslocamento por passo
    if len(eventos) > 2:
        desloc_passos = np.diff([pelvis_y[e] for e in eventos])
        cv_espacial = float(np.std(desloc_passos) / np.mean(desloc_passos) * 100.0) if np.mean(desloc_passos) > 0 else 0
    else:
        cv_espacial = 0.0

    # Duplo Suporte vs Suporte Simples
    apoio_duplo = apoio_r[idx_ini:idx_fim+1] & apoio_l[idx_ini:idx_fim+1]
    pct_duplo_suporte = float(np.sum(apoio_duplo) / len(apoio_duplo) * 100.0) if len(apoio_duplo) > 0 else 0

    # Oscilação Médio-Lateral da Pelve (CoM sway)
    pelvis_x = (recortar(rpsi)[0, :] + recortar(lpsi)[0, :]) / 2.0
    oscilacao_ml_com_mm = float(np.nanmax(pelvis_x) - np.nanmin(pelvis_x))

    # Base de Apoio e Rotação das mãos na marcha
    base_apoio = np.linalg.norm(recortar(rwra) - recortar(lwra), axis=0)
    base_apoio_media = float(np.nanmean(base_apoio))

    vetor_mao_r = recortar(rfin) - recortar(rwra)
    ang_mao_r = np.degrees(np.arctan2(vetor_mao_r[0, :], vetor_mao_r[1, :]))
    vetor_mao_l = recortar(lfin) - recortar(lwra)
    ang_mao_l = np.degrees(np.arctan2(vetor_mao_l[0, :], vetor_mao_l[1, :]))
    rotacao_maos_media = float(np.nanmean((np.abs(ang_mao_r) + np.abs(ang_mao_l)) / 2.0))

    # Verticalidade do Tronco na Marcha
    centro_ombros = (recortar(rsho) + recortar(lsho)) / 2.0
    centro_pelvis = (recortar(rpsi) + recortar(lpsi)) / 2.0
    vetor_tronco = centro_pelvis - centro_ombros
    vert_ang = calcular_angulo_entre_vetores(vetor_tronco, np.array([[0], [0], [1]]))
    indice_verticalidade = float(np.nanmean(vert_ang))

    # Extensão Cervical na Marcha
    cabeca = (recortar(rfhd) + recortar(lfhd)) / 2.0
    c7_rec = recortar(c7)
    vetor_cabeca = cabeca - c7_rec
    vetor_c7_t10 = c7_rec - recortar(get_marker('T10'))
    ang_cervical = calcular_angulo_entre_vetores(vetor_cabeca, vetor_c7_t10)
    extensao_cervical = float(np.nanmean(ang_cervical))

    # Flexão Plantar do Tornozelo na Marcha
    rkne_rec = recortar(get_marker('RKNE'))
    lkne_rec = recortar(get_marker('LKNE'))
    rtoe_rec = recortar(get_marker('RTOE'))
    ltoe_rec = recortar(get_marker('LTOE'))
    rank_rec = recortar(get_marker('RANK'))
    lank_rec = recortar(get_marker('LANK'))
    r_ang_tornozelo = calcular_angulo_entre_vetores(rank_rec - rkne_rec, rtoe_rec - rank_rec)
    l_ang_tornozelo = calcular_angulo_entre_vetores(lank_rec - lkne_rec, ltoe_rec - lank_rec)
    flexao_plantar_media = float(np.nanmean(90.0 - (r_ang_tornozelo + l_ang_tornozelo) / 2.0))

    return {
        "Distancia_Percorrida_m": round(distancia_percorrida_m, 3),
        "Num_Passos": num_passos,
        "Status_Marcha": status_marcha,
        "Tempo_Execucao_s": round(tempo_total, 2),
        "Velocidade_Media_mm_s": round(velocidade_media_mm_s, 2),
        "Cadencia_passos_s": round(cadencia_passos_s, 2),
        "Comprimento_Passada_Medio_mm": round(comprimento_passada_medio_mm, 2),
        "Variabilidade_Espacial_CV_pct": round(cv_espacial, 2),
        "Variabilidade_Temporal_CV_pct": round(cv_temporal, 2),
        "Duplo_Suporte_pct": round(pct_duplo_suporte, 2),
        "Oscilacao_ML_CoM_mm": round(oscilacao_ml_com_mm, 2),
        "Indice_Verticalidade_deg": round(indice_verticalidade, 2),
        "Extensao_Cervical_deg": round(extensao_cervical, 2),
        "Flexao_Plantar_deg": round(flexao_plantar_media, 2),
        "Base_Apoio_mm": round(base_apoio_media, 2),
        "Rotacao_Maos_deg": round(rotacao_maos_media, 2)
    }