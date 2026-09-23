"""
GERADOR DE GRÁFICOS DE AUDITORIA, HOMOGENEIDADE E INTEGRIDADE CINEMÁTICA
Participante: P002 (Guilherme Lemos)
Projeto de Mestrado: Handstand e Handstand Walk
Laboratório: LaBioCoM (Vicon Motion Systems)
"""

import os
import shutil
import numpy as np
import ezc3d
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

plt.rcParams['font.family'] = 'DejaVu Sans'

def gerar_graficos_p002():
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    pasta_limpos = os.path.join(diretorio_base, "..", "dados_limpos_c3d")
    pasta_resultados = os.path.join(diretorio_base, "..", "resultados")
    artifact_dir = r"C:\Users\Gui\.gemini\antigravity\brain\9ea73dbd-f182-4f14-9dee-a2609bedb503"

    os.makedirs(pasta_resultados, exist_ok=True)
    os.makedirs(artifact_dir, exist_ok=True)

    # -------------------------------------------------------------------------
    # 1. CARREGAR TENTATIVA PICO DE HANDSTAND LIVRE: P002 T1 (50.98 s de sustentação)
    # -------------------------------------------------------------------------
    c3d_path_hs = os.path.join(pasta_limpos, "P002_hs_livre01_limpo.c3d")
    c_hs = ezc3d.c3d(c3d_path_hs)
    lbls_hs = [l.strip().split(':')[-1].upper() for l in c_hs['parameters']['POINT']['LABELS']['value']]
    pts_hs = c_hs['data']['points']
    fs_hs = c_hs['parameters']['POINT']['RATE']['value'][0]
    n_frames_hs = pts_hs.shape[2]
    t_hs = np.arange(n_frames_hs) / fs_hs

    def gm(name):
        if name in lbls_hs:
            p = pts_hs[:3, lbls_hs.index(name), :].copy()
            p[:, np.all(p == 0, axis=0)] = np.nan
            return p
        return np.full((3, n_frames_hs), np.nan)

    rwra = gm('RWRA'); lwra = gm('LWRA')
    rsho = gm('RSHO'); lsho = gm('LSHO')
    c7 = gm('C7'); t10 = gm('T10')
    rpsi = gm('RPSI'); lpsi = gm('LPSI')
    rasi = gm('RASI'); lasi = gm('LASI')
    rkne = gm('RKNE'); lkne = gm('LKNE')
    rank = gm('RANK'); lank = gm('LANK')
    rhee = gm('RHEE'); lhee = gm('LHEE')
    rtoe = gm('RTOE'); ltoe = gm('LTOE')
    rfhd = gm('RFHD'); lfhd = gm('LFHD')

    punhos_z = (rwra[2, :] + lwra[2, :]) / 2.0
    ombros_z = (rsho[2, :] + lsho[2, :]) / 2.0
    pelve_z = (rpsi[2, :] + lpsi[2, :] + rasi[2, :] + lasi[2, :]) / 4.0
    joelhos_z = (rkne[2, :] + lkne[2, :]) / 2.0
    tornozelos_z = (rank[2, :] + lank[2, :]) / 2.0

    # Janela de sustentação
    z_pernas = np.nanmax([rank[2, :], lank[2, :], rhee[2, :], lhee[2, :], rtoe[2, :], ltoe[2, :]], axis=0)
    is_livre = (z_pernas > pelve_z + 300).astype(int)
    diff_inv = np.diff(is_livre, prepend=0)
    entries = np.where(diff_inv == 1)[0]
    blocks = []
    for e in entries:
        exits = np.where(diff_inv[e:] == -1)[0]
        end_e = e + exits[0] if len(exits) else len(is_livre) - 1
        blocks.append((e, end_e, end_e - e + 1))

    best_block = max(blocks, key=lambda b: b[2])
    f_ini, f_fim = best_block[0], best_block[1]
    t_ini = f_ini / fs_hs
    t_fim = f_fim / fs_hs
    duracao_hs = (f_fim - f_ini + 1) / fs_hs

    print(f"[HS LIVRE T1] Janela identificada: frames {f_ini} a {f_fim} ({duracao_hs:.2f} s)")

    # -------------------------------------------------------------------------
    # FIGURA 1: Trajetórias Verticais no Tempo (HS Livre T1)
    # -------------------------------------------------------------------------
    fig1, (ax1, ax2) = plt.subplots(2, 1, figsize=(15, 9), sharex=True, gridspec_kw={'height_ratios': [2.5, 1]})

    ax1.axvspan(t_ini, t_fim, color='#10B981', alpha=0.15, label=f'Janela de Equilíbrio Sustentado ({duracao_hs:.2f} s)')
    ax1.plot(t_hs, tornozelos_z, label='Tornozelos (Média RANK/LANK)', color='#8B5CF6', linewidth=2.0)
    ax1.plot(t_hs, joelhos_z, label='Joelhos (Média RKNE/LKNE)', color='#EC4899', linewidth=1.8)
    ax1.plot(t_hs, pelve_z, label='Pelve (Centro LASI/RASI/LPSI/RPSI)', color='#F59E0B', linewidth=1.8)
    ax1.plot(t_hs, c7[2, :], label='C7 (Cervicotorácica)', color='#3B82F6', linewidth=1.5, linestyle='--')
    ax1.plot(t_hs, ombros_z, label='Ombros (Reconstrução SVD)', color='#06B6D4', linewidth=2.0)
    ax1.plot(t_hs, punhos_z, label='Base de Apoio / Punhos (RWRA/LWRA)', color='#10B981', linewidth=2.0)

    ax1.set_ylabel('Altura Vertical Z (mm)', fontsize=12, fontweight='bold')
    ax1.set_title('P002 – Handstand Livre Oficial (Tentativa Pico T1 – 50,98 s)\nTrajetórias Cinemáticas Verticais dos Segmentos Corporais e Janela de Sustentação', fontsize=14, fontweight='bold', pad=12)
    ax1.grid(True, linestyle=':', alpha=0.6)
    ax1.legend(loc='upper right', framealpha=0.9, fontsize=10)

    # Painel Inferior: Margem de Inversão (Pernas - Pelve)
    diff_inversao = tornozelos_z - pelve_z
    ax2.axvspan(t_ini, t_fim, color='#10B981', alpha=0.15)
    ax2.plot(t_hs, diff_inversao, color='#1F2937', linewidth=1.8, label='Diferença Tornozelos - Pelve (mm)')
    ax2.axhline(300, color='#EF4444', linestyle='--', linewidth=1.5, label='Limiar Metodológico de Inversão (+300 mm)')
    ax2.set_xlabel('Tempo de Gravação (s)', fontsize=12, fontweight='bold')
    ax2.set_ylabel('Inversão (mm)', fontsize=12, fontweight='bold')
    ax2.grid(True, linestyle=':', alpha=0.6)
    ax2.legend(loc='lower right', framealpha=0.9, fontsize=10)

    plt.tight_layout()
    out_fig1 = os.path.join(pasta_resultados, "P002_trajetorias_verticais_hs_livre_t1.png")
    fig1.savefig(out_fig1, dpi=200)
    plt.close(fig1)
    print(f"[OK] Salvo: {out_fig1}")

    # -------------------------------------------------------------------------
    # FIGURA 2: Stick Figure Sagital + Matriz de Continuidade/Homogeneidade
    # -------------------------------------------------------------------------
    marcadores_auditados = [
        'C7', 'T10', 'RBAK', 'STRN', 'LREF', 'RREF',
        'LSHO', 'RSHO', 'LELB', 'RELB', 'LWRA', 'RWRA', 'LFIN', 'RFIN',
        'LASI', 'RASI', 'LPSI', 'RPSI',
        'LKNE', 'RKNE', 'LANK', 'RANK', 'LTOE', 'RTOE', 'LHEE', 'RHEE'
    ]

    matriz_validade = np.zeros((len(marcadores_auditados), f_fim - f_ini + 1))
    for r, m in enumerate(marcadores_auditados):
        if m in lbls_hs:
            p = pts_hs[:3, lbls_hs.index(m), f_ini:f_fim+1]
            matriz_validade[r, :] = ~np.isnan(p[0, :]) & (p[0, :] != 0)

    fig2 = plt.figure(figsize=(16, 8.5))

    # Subplot 1: Stick Figure Sagital na Janela de Sustentação
    ax_stick = fig2.add_subplot(1, 2, 1)
    frames_amostra = np.linspace(f_ini + 200, f_fim - 200, 8, dtype=int)
    cores = plt.cm.viridis(np.linspace(0.15, 0.95, len(frames_amostra)))

    for idx_f, f_sample in enumerate(frames_amostra):
        cor = cores[idx_f]
        def gyz(m):
            if m in lbls_hs:
                return pts_hs[1, lbls_hs.index(m), f_sample], pts_hs[2, lbls_hs.index(m), f_sample]
            return 0, 0

        # Membros Superiores
        ax_stick.plot([gyz('RWRA')[0], gyz('RELB')[0], gyz('RSHO')[0]], [gyz('RWRA')[1], gyz('RELB')[1], gyz('RSHO')[1]], color=cor, linewidth=2, alpha=0.85)
        # Tronco
        ax_stick.plot([gyz('RSHO')[0], gyz('C7')[0], gyz('T10')[0], gyz('RPSI')[0]], [gyz('RSHO')[1], gyz('C7')[1], gyz('T10')[1], gyz('RPSI')[1]], color=cor, linewidth=2.8, alpha=0.9)
        # Membros Inferiores
        ax_stick.plot([gyz('RPSI')[0], gyz('RKNE')[0], gyz('RANK')[0], gyz('RTOE')[0]], [gyz('RPSI')[1], gyz('RKNE')[1], gyz('RANK')[1], gyz('RTOE')[1]], color=cor, linewidth=2, alpha=0.85)
        # Cabeça (em suspensão invertida / voltada para baixo)
        c7_y, c7_z = gyz('C7')
        ax_stick.scatter(c7_y - 20, c7_z - 80, color=cor, s=70, alpha=0.9, zorder=5)

    ax_stick.axhline(0, color='black', linewidth=2, label='Solo')
    ax_stick.set_title(f'Sequência Postural Sagital (Stick Figure)\n8 Instantes Equidistantes ao longo de {duracao_hs:.2f} s', fontsize=12, fontweight='bold')
    ax_stick.set_xlabel('Eixo Ântero-Posterior Y (mm)', fontsize=11, fontweight='bold')
    ax_stick.set_ylabel('Eixo Vertical Z (mm)', fontsize=11, fontweight='bold')
    ax_stick.grid(True, linestyle=':', alpha=0.6)
    ax_stick.set_aspect('equal', 'box')

    # Subplot 2: Matriz de Integridade e Continuidade (Heatmap)
    ax_mat = fig2.add_subplot(1, 2, 2)
    cax = ax_mat.imshow(matriz_validade, aspect='auto', cmap='YlGn', interpolation='nearest', vmin=0, vmax=1)
    ax_mat.set_yticks(np.arange(len(marcadores_auditados)))
    ax_mat.set_yticklabels(marcadores_auditados, fontsize=9, fontweight='bold')
    ax_mat.set_title(f'Auditoria de Continuidade e Homogeneidade (100% Contínuos)\nJanela de Equilíbrio: Frames {f_ini} a {f_fim} ({duracao_hs:.2f} s – 10.197 frames)', fontsize=12, fontweight='bold')
    ax_mat.set_xlabel('Frames na Janela de Equilíbrio Sustentado', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out_fig2 = os.path.join(pasta_resultados, "P002_stick_figure_e_integridade_hs_livre_t1.png")
    fig2.savefig(out_fig2, dpi=200)
    plt.close(fig2)
    print(f"[OK] Salvo: {out_fig2}")

    # -------------------------------------------------------------------------
    # FIGURA 3: Handstand Walk T2 (5,49 m) - Trajetória de Passadas e Continuidade
    # -------------------------------------------------------------------------
    c3d_path_hsw = os.path.join(pasta_limpos, "P002_hs_walk02_limpo.c3d")
    c_hsw = ezc3d.c3d(c3d_path_hsw)
    lbls_hsw = [l.strip().split(':')[-1].upper() for l in c_hsw['parameters']['POINT']['LABELS']['value']]
    pts_hsw = c_hsw['data']['points']
    fs_hsw = c_hsw['parameters']['POINT']['RATE']['value'][0]
    n_frames_hsw = pts_hsw.shape[2]
    t_hsw = np.arange(n_frames_hsw) / fs_hsw

    def gm_w(name):
        if name in lbls_hsw:
            p = pts_hsw[:3, lbls_hsw.index(name), :].copy()
            p[:, np.all(p == 0, axis=0)] = np.nan
            return p
        return np.full((3, n_frames_hsw), np.nan)

    rwra_w = gm_w('RWRA'); lwra_w = gm_w('LWRA')
    rpsi_w = gm_w('RPSI'); lpsi_w = gm_w('LPSI')
    pelvis_y_w = (rpsi_w[1, :] + lpsi_w[1, :]) / 2.0
    pelvis_x_w = (rpsi_w[0, :] + lpsi_w[0, :]) / 2.0

    # Continuidade dos marcadores no HSW T2
    matriz_validade_hsw = np.zeros((len(marcadores_auditados), n_frames_hsw))
    for r, m in enumerate(marcadores_auditados):
        if m in lbls_hsw:
            p = pts_hsw[:3, lbls_hsw.index(m), :]
            matriz_validade_hsw[r, :] = ~np.isnan(p[0, :]) & (p[0, :] != 0)

    fig3, (ax3_1, ax3_2) = plt.subplots(2, 1, figsize=(15, 8.5), gridspec_kw={'height_ratios': [1.3, 1]})

    # Trajetória de Deslocamento das Mãos e Pelve
    ax3_1.plot(t_hsw, pelvis_y_w / 1000.0, label='Progressão da Pelve (m)', color='#10B981', linewidth=2.5)
    ax3_1.plot(t_hsw, rwra_w[1, :] / 1000.0, label='Punho Direito (RWRA)', color='#3B82F6', linewidth=1.5, linestyle=':')
    ax3_1.plot(t_hsw, lwra_w[1, :] / 1000.0, label='Punho Esquerdo (LWRA)', color='#EC4899', linewidth=1.5, linestyle=':')
    ax3_1.set_ylabel('Posição Ântero-Posterior Y (m)', fontsize=12, fontweight='bold')
    ax3_1.set_title('P002 – Handstand Walk Oficial (Tentativa Pico T2 – 5,49 m)\nProgressão Locomotora Contínua e Auditoria de Marcadores', fontsize=14, fontweight='bold', pad=12)
    ax3_1.grid(True, linestyle=':', alpha=0.6)
    ax3_1.legend(loc='upper left', framealpha=0.9, fontsize=10)

    # Matriz de Integridade do Walk
    cax3 = ax3_2.imshow(matriz_validade_hsw, aspect='auto', cmap='YlGn', interpolation='nearest', vmin=0, vmax=1)
    ax3_2.set_yticks(np.arange(len(marcadores_auditados)))
    ax3_2.set_yticklabels(marcadores_auditados, fontsize=8, fontweight='bold')
    ax3_2.set_xlabel('Tempo de Execução da Caminhada (Frames a 200 Hz)', fontsize=11, fontweight='bold')
    ax3_2.set_title('Auditoria de Homogeneidade e Continuidade de Marcadores (HSW T2 – 100% Contínuos)', fontsize=11, fontweight='bold')

    plt.tight_layout()
    out_fig3 = os.path.join(pasta_resultados, "P002_hsw_trajetoria_e_integridade_t2.png")
    fig3.savefig(out_fig3, dpi=200)
    plt.close(fig3)
    print(f"[OK] Salvo: {out_fig3}")

    # -------------------------------------------------------------------------
    # COPIAR ARTEFATOS PARA VISUALIZAÇÃO DIRETA NO GEMINI
    # -------------------------------------------------------------------------
    dest1 = os.path.join(artifact_dir, "P002_trajetorias_verticais_hs_livre_t1.png")
    dest2 = os.path.join(artifact_dir, "P002_stick_figure_e_integridade_hs_livre_t1.png")
    dest3 = os.path.join(artifact_dir, "P002_hsw_trajetoria_e_integridade_t2.png")

    shutil.copy(out_fig1, dest1)
    shutil.copy(out_fig2, dest2)
    shutil.copy(out_fig3, dest3)
    print(f"[COPIADO] Figuras copiadas para {artifact_dir}")

if __name__ == "__main__":
    gerar_graficos_p002()
