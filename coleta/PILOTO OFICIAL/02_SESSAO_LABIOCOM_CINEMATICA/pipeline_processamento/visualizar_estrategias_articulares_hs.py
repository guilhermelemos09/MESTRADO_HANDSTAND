"""
VISUALIZADOR DE ESTRATÉGIAS ARTICULARES DE BUSCA DO EQUILÍBRIO NO HANDSTAND
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes

Gera:
1. comparacao_temporal_p001_vs_p002.png: Curvas temporais contínuas (Cotovelo, Ombro, Quadril, CoP)
2. mapa_dispersao_estrategias_posturais.png: Diagrama de dispersão SD Cotovelo vs SD Ombro
3. perfil_rom_sd_comparativo.png: Gráficos de barras de ROM e SD entre tentativas e atletas
"""

import os
import glob
import numpy as np
import ezc3d
import matplotlib.pyplot as plt

# Configuração visual elegante para artigos e dissertação
plt.style.use('seaborn-v0_8-whitegrid' if 'seaborn-v0_8-whitegrid' in plt.style.available else 'default')
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.sans-serif'] = ['DejaVu Sans', 'Arial', 'Helvetica']
plt.rcParams['axes.edgecolor'] = '#333333'
plt.rcParams['axes.linewidth'] = 0.8

DIR_BASE = os.path.dirname(os.path.abspath(__file__))
DIR_LIMPOS = os.path.normpath(os.path.join(DIR_BASE, "..", "dados_limpos_c3d"))
DIR_OUT = os.path.normpath(os.path.join(DIR_BASE, "..", "resultados", "figuras_estrategias"))
os.makedirs(DIR_OUT, exist_ok=True)

def calcular_vetor(p1, p2):
    return p2 - p1

def calcular_angulo_entre_vetores(v1, v2):
    dot_product = np.sum(v1 * v2, axis=0)
    norm_v1 = np.linalg.norm(v1, axis=0)
    norm_v2 = np.linalg.norm(v2, axis=0)
    cosine_angle = np.clip(dot_product / (norm_v1 * norm_v2 + 1e-9), -1.0, 1.0)
    return np.degrees(np.arccos(cosine_angle))

def extrair_series_temporais_hs(c3d_path):
    c3d = ezc3d.c3d(c3d_path)
    labels = [l.strip().upper().split(':')[-1] for l in c3d['parameters']['POINT']['LABELS']['value']]
    pts = c3d['data']['points']
    fs = c3d['parameters']['POINT']['RATE']['value'][0]
    num_frames = pts.shape[2]

    def get_pt(nomes):
        if isinstance(nomes, str): nomes = [nomes]
        for name in nomes:
            if name.upper() in labels:
                idx = labels.index(name.upper())
                p = pts[:3, idx, :].copy()
                p[p == 0] = np.nan
                if not np.all(np.isnan(p)):
                    return p
        return np.full((3, num_frames), np.nan)

    # Marcadores
    rsho, lsho = get_pt(['RSHO', 'RSHO_CLEAN']), get_pt(['LSHO', 'LSHO_CLEAN'])
    relb, lelb = get_pt(['RELB', 'RELB_CLEAN']), get_pt(['LELB', 'LELB_CLEAN'])
    rwra, lwra = get_pt(['RWRA', 'RWRB', 'RWRIST']), get_pt(['LWRA', 'LWRB', 'LWRIST'])
    rasi, lasi = get_pt(['RASI']), get_pt(['LASI'])
    rpsi, lpsi = get_pt(['RPSI']), get_pt(['LPSI'])
    rkne, lkne = get_pt(['RKNE', 'RKNE_CLEAN']), get_pt(['LKNE', 'LKNE_CLEAN'])
    rank, lank = get_pt(['RANK']), get_pt(['LANK'])
    rhee, lhee = get_pt(['RHEE']), get_pt(['LHEE'])
    rtoe, ltoe = get_pt(['RTOE']), get_pt(['LTOE'])

    pelvis = (rasi + lasi + rpsi + lpsi) / 4.0
    z_perna = np.nanmax([rank[2, :], lank[2, :], rhee[2, :], lhee[2, :], rtoe[2, :], ltoe[2, :]], axis=0)
    z_pelvis = pelvis[2, :]

    # Inversão
    is_livre = (z_perna > z_pelvis + 300).astype(int)
    diff_inv = np.diff(is_livre, prepend=0)
    entries = np.where(diff_inv == 1)[0]
    blocks = []
    for e in entries:
        exits = np.where(diff_inv[e:] == -1)[0]
        end_e = e + exits[0] if len(exits) else len(is_livre) - 1
        blocks.append((e, end_e, end_e - e + 1))

    if not blocks:
        return None

    best = max(blocks, key=lambda b: b[2])
    ini, fim = best[0], best[1]

    # Buffer de estabilidade (0.5s)
    buf = int(0.5 * fs)
    if (fim - ini) > 2 * buf + int(1.0 * fs):
        w_i, w_f = ini + buf, fim - buf
    else:
        w_i, w_f = ini, fim

    n_janela = w_f - w_i + 1
    tempo = np.arange(n_janela) / fs

    # 1. Cotovelo
    v_ante_r = rwra[:, w_i:w_f+1] - relb[:, w_i:w_f+1]
    v_braco_r = rsho[:, w_i:w_f+1] - relb[:, w_i:w_f+1]
    cot_r = calcular_angulo_entre_vetores(v_ante_r, v_braco_r)

    v_ante_l = lwra[:, w_i:w_f+1] - lelb[:, w_i:w_f+1]
    v_braco_l = lsho[:, w_i:w_f+1] - lelb[:, w_i:w_f+1]
    cot_l = calcular_angulo_entre_vetores(v_ante_l, v_braco_l)
    ang_cot = np.nanmean([cot_r, cot_l], axis=0)

    # 2. Ombro
    v_braco_sho_r = relb[:, w_i:w_f+1] - rsho[:, w_i:w_f+1]
    v_tronco_sho_r = pelvis[:, w_i:w_f+1] - rsho[:, w_i:w_f+1]
    sho_r = calcular_angulo_entre_vetores(v_braco_sho_r, v_tronco_sho_r)

    v_braco_sho_l = lelb[:, w_i:w_f+1] - lsho[:, w_i:w_f+1]
    v_tronco_sho_l = pelvis[:, w_i:w_f+1] - lsho[:, w_i:w_f+1]
    sho_l = calcular_angulo_entre_vetores(v_braco_sho_l, v_tronco_sho_l)
    ang_sho = np.nanmean([sho_r, sho_l], axis=0)

    # 3. Quadril
    v_tronco_hip_r = rsho[:, w_i:w_f+1] - pelvis[:, w_i:w_f+1]
    v_coxa_r = rkne[:, w_i:w_f+1] - pelvis[:, w_i:w_f+1]
    hip_r = calcular_angulo_entre_vetores(v_tronco_hip_r, v_coxa_r)

    v_tronco_hip_l = lsho[:, w_i:w_f+1] - pelvis[:, w_i:w_f+1]
    v_coxa_l = lkne[:, w_i:w_f+1] - pelvis[:, w_i:w_f+1]
    hip_l = calcular_angulo_entre_vetores(v_tronco_hip_l, v_coxa_l)
    ang_hip = np.nanmean([hip_r, hip_l], axis=0)

    return {
        'tempo': tempo,
        'cotovelo': ang_cot,
        'ombro': ang_sho,
        'quadril': ang_hip,
        'fs': fs
    }

def plotar_comparacao_temporal():
    f1 = os.path.join(DIR_LIMPOS, "P001_hs_livre01_limpo.c3d")
    f2 = os.path.join(DIR_LIMPOS, "P002_hs_livre01_limpo.c3d")
    if not os.path.exists(f1) or not os.path.exists(f2):
        print(f"[AVISO] Arquivos de teste não encontrados para plotagem.")
        return

    d1 = extrair_series_temporais_hs(f1)
    d2 = extrair_series_temporais_hs(f2)

    # Limitar para comparar os primeiros 14 segundos de cada atleta
    t_max = 14.0
    m1 = d1['tempo'] <= t_max
    m2 = d2['tempo'] <= t_max

    fig, axes = plt.subplots(3, 1, figsize=(11, 8.5), sharex=True)

    # Cores
    cor_p1 = '#D9534F' # Vermelho Coral / Calistenia P001
    cor_p2 = '#2E6DA4' # Azul Royal / Controle Rígido P002

    # Subplot 1: Cotovelo
    axes[0].plot(d1['tempo'][m1], d1['cotovelo'][m1], label=f'P001 (Calistenia) - SD: {np.nanstd(d1["cotovelo"][m1]):.1f}° | ROM: {np.nanmax(d1["cotovelo"][m1])-np.nanmin(d1["cotovelo"][m1]):.1f}°', color=cor_p1, linewidth=2.0)
    axes[0].plot(d2['tempo'][m2], d2['cotovelo'][m2], label=f'P002 (Padrão Rígido) - SD: {np.nanstd(d2["cotovelo"][m2]):.1f}° | ROM: {np.nanmax(d2["cotovelo"][m2])-np.nanmin(d2["cotovelo"][m2]):.1f}°', color=cor_p2, linewidth=2.0, linestyle='--')
    axes[0].set_ylabel('Ângulo Cotovelo (°)\n[Extensão Total ~180°]', fontsize=11, fontweight='bold')
    axes[0].set_title('Dinâmica das Estratégias Articulares de Equilíbrio no Handstand: P001 vs P002', fontsize=13, fontweight='bold', pad=12)
    axes[0].legend(loc='upper right', frameon=True, facecolor='#fbfbfb')
    axes[0].set_ylim(110, 185)

    # Subplot 2: Ombro
    axes[1].plot(d1['tempo'][m1], d1['ombro'][m1], label=f'P001 (Calistenia) - SD: {np.nanstd(d1["ombro"][m1]):.1f}° | ROM: {np.nanmax(d1["ombro"][m1])-np.nanmin(d1["ombro"][m1]):.1f}°', color=cor_p1, linewidth=2.0)
    axes[1].plot(d2['tempo'][m2], d2['ombro'][m2], label=f'P002 (Padrão Rígido) - SD: {np.nanstd(d2["ombro"][m2]):.1f}° | ROM: {np.nanmax(d2["ombro"][m2])-np.nanmin(d2["ombro"][m2]):.1f}°', color=cor_p2, linewidth=2.0, linestyle='--')
    axes[1].set_ylabel('Ângulo Ombro (°)\n[Flexão/Abertura]', fontsize=11, fontweight='bold')
    axes[1].legend(loc='upper right', frameon=True, facecolor='#fbfbfb')
    axes[1].set_ylim(120, 180)

    # Subplot 3: Quadril
    axes[2].plot(d1['tempo'][m1], d1['quadril'][m1], label=f'P001 (Calistenia) - SD: {np.nanstd(d1["quadril"][m1]):.1f}° | ROM: {np.nanmax(d1["quadril"][m1])-np.nanmin(d1["quadril"][m1]):.1f}°', color=cor_p1, linewidth=2.0)
    axes[2].plot(d2['tempo'][m2], d2['quadril'][m2], label=f'P002 (Padrão Rígido) - SD: {np.nanstd(d2["quadril"][m2]):.1f}° | ROM: {np.nanmax(d2["quadril"][m2])-np.nanmin(d2["quadril"][m2]):.1f}°', color=cor_p2, linewidth=2.0, linestyle='--')
    axes[2].set_ylabel('Ângulo Quadril (°)\n[Tronco vs Pernas]', fontsize=11, fontweight='bold')
    axes[2].set_xlabel('Tempo de Equilíbrio Sustentado (segundos)', fontsize=12, fontweight='bold')
    axes[2].legend(loc='upper right', frameon=True, facecolor='#fbfbfb')
    axes[2].set_ylim(130, 175)

    for ax in axes:
        ax.grid(True, linestyle=':', alpha=0.6)

    plt.tight_layout()
    out_path = os.path.join(DIR_OUT, "comparacao_temporal_p001_vs_p002.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[SUCESSO] Gráfico temporal salvo em: {out_path}")

def plotar_mapa_dispersao_estrategias():
    from analisar_hs_oficial import analisar_hs_arquivo

    arquivos = sorted(glob.glob(os.path.join(DIR_LIMPOS, "*hs*livre*limpo.c3d")))
    if not arquivos: return

    dados = []
    for arq in arquivos:
        nome = os.path.basename(arq)
        pid = "P001" if "P001" in nome else ("P002" if "P002" in nome else "Outro")
        res = analisar_hs_arquivo(arq, 'livre')
        if res and res.get('Cotovelo_SD_deg') != "" and res.get('Ombro_SD_deg') != "":
            dados.append({
                'nome': nome,
                'pid': pid,
                'cot_sd': float(res['Cotovelo_SD_deg']),
                'cot_rom': float(res['Cotovelo_ROM_deg']),
                'sho_sd': float(res['Ombro_SD_deg']),
                'sho_rom': float(res['Ombro_ROM_deg']),
                'estrategia': res['Estrategia_Dominante']
            })

    fig, ax = plt.subplots(figsize=(9, 7))

    # Regiões conceituais
    ax.axhline(6.0, color='#888888', linestyle='--', alpha=0.5)
    ax.axvline(6.0, color='#888888', linestyle='--', alpha=0.5)

    ax.fill_between([0, 6], 0, 6, color='#5cb85c', alpha=0.10, label='Zona Punho-Rígido (Ginástica Olímpica)')
    ax.fill_between([6, 25], 0, 6, color='#f0ad4e', alpha=0.10, label='Zona Cotovelo-Dominante (Calistenia)')
    ax.fill_between([0, 6], 6, 25, color='#5bc0de', alpha=0.10, label='Zona Ombro-Dominante')
    ax.fill_between([6, 25], 6, 25, color='#d9534f', alpha=0.10, label='Zona Multijunta / Alta Busca')

    cores_pid = {'P001': '#D9534F', 'P002': '#2E6DA4', 'Outro': '#333333'}
    marcadores = {'P001': 'o', 'P002': 's', 'Outro': '^'}

    for d in dados:
        cor = cores_pid.get(d['pid'], '#333333')
        marc = marcadores.get(d['pid'], 'o')
        ax.scatter(d['cot_sd'], d['sho_sd'], color=cor, marker=marc, s=140, edgecolors='black', linewidth=1.2, zorder=5)
        lbl_t = d['nome'].split('_')[2].replace('limpo.c3d', '')
        ax.annotate(f"{d['pid']} ({lbl_t})", (d['cot_sd'] + 0.3, d['sho_sd'] + 0.2), fontsize=9, fontweight='bold', color='#222222')

    ax.set_xlabel('Variabilidade do Cotovelo - SD (°)', fontsize=12, fontweight='bold')
    ax.set_ylabel('Variabilidade do Ombro - SD (°)', fontsize=12, fontweight='bold')
    ax.set_title('Classificação das Estratégias Motoras no Handstand Livre\n(Variabilidade Articular na Janela Estável)', fontsize=13, fontweight='bold', pad=12)
    ax.set_xlim(0, 22)
    ax.set_ylim(0, 16)
    ax.grid(True, linestyle=':', alpha=0.6)
    ax.legend(loc='upper right', frameon=True, facecolor='#ffffff')

    plt.tight_layout()
    out_path = os.path.join(DIR_OUT, "mapa_dispersao_estrategias_posturais.png")
    plt.savefig(out_path, dpi=300)
    plt.close()
    print(f"[SUCESSO] Mapa de dispersão salvo em: {out_path}")

if __name__ == "__main__":
    print("Iniciando geração de gráficos das estratégias articulares...")
    plotar_comparacao_temporal()
    plotar_mapa_dispersao_estrategias()
    print("Processo finalizado com sucesso!")
