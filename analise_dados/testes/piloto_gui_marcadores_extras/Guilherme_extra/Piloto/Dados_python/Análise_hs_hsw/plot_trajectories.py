import ezc3d
import numpy as np
import matplotlib.pyplot as plt
import os

def plot_all_markers_single_graph(c3d_limpo, markers_list, output_img, title):
    try:
        c_limpo = ezc3d.c3d(c3d_limpo)
    except Exception as e:
        print(f"Erro ao abrir o arquivo {c3d_limpo}: {e}")
        return

    labels_limpo = [l.strip() for l in c_limpo['parameters']['POINT']['LABELS']['value']]

    plt.figure(figsize=(14, 8))

    for marker_name in markers_list:
        if marker_name not in labels_limpo:
            print(f"{marker_name} não encontrado no arquivo.")
            continue

        idx_limpo = labels_limpo.index(marker_name)
        
        # Pegar o eixo Z (índice 2)
        z_limpo = c_limpo['data']['points'][2, idx_limpo, :]
        z_limpo_plot = np.where(z_limpo == 0, np.nan, z_limpo)

        plt.plot(z_limpo_plot, label=marker_name, linewidth=1.5)

    plt.title(title)
    plt.xlabel('Frames')
    plt.ylabel('Posição Z (mm)')
    
    # Colocar a legenda fora do gráfico em 2 colunas para caber tudo
    plt.legend(bbox_to_anchor=(1.02, 1), loc='upper left', ncol=2, fontsize='small')
    plt.grid(True)
    plt.tight_layout()
    
    plt.savefig(output_img, bbox_inches='tight')
    plt.close()
    print(f"Gráfico consolidado salvo: {output_img}")

if __name__ == "__main__":
    marcadores_para_plotar = [
        # Estruturais (Tronco)
        'LSHO', 'RSHO', 'C7', 'T10', 'referencia1', 'referencia2', 
        # Cruciais para Cálculo das Variáveis (Desvio Articular, Comprimento, etc)
        'RELB', 'LASI', 'RASI', 'LKNE', 'RKNE',
        # Gatilhos da Marcha (Apoio e Fases HSW)
        'LWRB', 'RWRB', 'LFIN', 'RFIN',
        # Gatilhos de Inversão / Equilíbrio (Pernas no ar para HS)
        'LANK', 'RANK', 'LHEE', 'RHEE'
    ]
    
    # HS
    plot_all_markers_single_graph("hs01_limpo.c3d", marcadores_para_plotar, "plot_unico_hs01.png", "Trajetórias Z (Limpo + Cruciais) - HS01")
    plot_all_markers_single_graph("hs02_limpo.c3d", marcadores_para_plotar, "plot_unico_hs02.png", "Trajetórias Z (Limpo + Cruciais) - HS02")
    
    # HSW
    plot_all_markers_single_graph("hsw01_limpo.c3d", marcadores_para_plotar, "plot_unico_hsw01.png", "Trajetórias Z (Limpo + Cruciais) - HSW01")
    plot_all_markers_single_graph("hsw02_limpo.c3d", marcadores_para_plotar, "plot_unico_hsw02.png", "Trajetórias Z (Limpo + Cruciais) - HSW02")
