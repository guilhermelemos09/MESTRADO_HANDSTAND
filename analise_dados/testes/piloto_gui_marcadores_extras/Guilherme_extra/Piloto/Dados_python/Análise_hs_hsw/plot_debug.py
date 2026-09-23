import ezc3d
import numpy as np
import matplotlib.pyplot as plt

def plot_every_marker(c3d_file, output_img, title):
    try:
        c = ezc3d.c3d(c3d_file)
    except Exception as e:
        print(f"Erro ao abrir o arquivo {c3d_file}: {e}")
        return

    labels = [l.strip() for l in c['parameters']['POINT']['LABELS']['value']]

    plt.figure(figsize=(16, 8))

    for idx, marker_name in enumerate(labels):
        z = c['data']['points'][2, idx, :]
        z_plot = np.where(z == 0, np.nan, z)
        # Plotando com linha fina e transparente para não poluir tanto
        plt.plot(z_plot, linewidth=1.5, alpha=0.7, label=marker_name)

    plt.title(title)
    plt.xlabel('Frames')
    plt.ylabel('Posição Z (mm)')
    
    # Adicionando uma legenda externa em colunas pequenas para caber todos
    plt.legend(bbox_to_anchor=(1.01, 1), loc='upper left', ncol=2, fontsize='x-small')
    
    plt.grid(True)
    plt.tight_layout()
    plt.savefig(output_img, bbox_inches='tight')
    plt.close()
    print(f"Gráfico de debug salvo: {output_img}")

if __name__ == "__main__":
    plot_every_marker("hs01_limpo.c3d", "plot_debug_hs01.png", "Z de TODOS os marcadores - HS01")
    plot_every_marker("hs02_limpo.c3d", "plot_debug_hs02.png", "Z de TODOS os marcadores - HS02")
    plot_every_marker("hsw01_limpo.c3d", "plot_debug_hsw01.png", "Z de TODOS os marcadores - HSW01")
    plot_every_marker("hsw02_limpo.c3d", "plot_debug_hsw02.png", "Z de TODOS os marcadores - HSW02")
