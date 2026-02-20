import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import os

# --- FUNÇÃO PARA CALCULAR ÂNGULOS ---
def calcular_angulo(p1, p2, p3):
    v1 = np.array(p1) - np.array(p2)
    v2 = np.array(p3) - np.array(p2)
    if np.linalg.norm(v1) == 0 or np.linalg.norm(v2) == 0:
        return 0
    cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
    cos_theta = np.clip(cos_theta, -1.0, 1.0)
    return np.degrees(np.arccos(cos_theta))

# --- COORDENADAS (Pixels) ---
# CALISTENIA (Esquerda)
c_pontos = [[500, 900], [580, 650], [450, 400], [650, 100]] # Punho, Ombro, Quadril, Tornozelo
# GINÁSTICA (Direita)
g_pontos = [[500, 900], [505, 600], [502, 350], [500, 50]]

labels = ["Punho", "Ombro", "Quadril", "Tornozelo"]

# --- FUNÇÃO DE PLOTAGEM ---
def plotar_analise(ax, img_path, pontos, titulo, inverter=False):
    p, o, q, t = pontos
    
    # Tenta carregar a imagem
    if os.path.exists(img_path):
        img = mpimg.imread(img_path)
        ax.imshow(img)
    else:
        ax.set_facecolor('#333333')
        ax.text(500, 500, f"FOTO AUSENTE:\n{img_path}", color='white', ha='center')
        ax.set_xlim(0, 1000); ax.set_ylim(1000, 0)

    # 1. Desenhar o esqueleto (Verde limão)
    xs, ys = zip(*pontos)
    ax.plot(xs, ys, 'o-', color='#00FF00', lw=4, markersize=10)

    # 2. Adicionar os nomes das articulações
    for i, label in enumerate(labels):
        ax.text(pontos[i][0]+20, pontos[i][1], label, color='white', 
                fontsize=10, fontweight='bold', bbox=dict(facecolor='black', alpha=0.6))

    # 3. Índice de Alinhamento (IAA) e Ângulo
    idx = abs(t[0] - p[0])
    ang = calcular_angulo(o, q, t)
    
    # Texto de resultado (Corrigindo o erro de f-string)
    info_texto = f"IAA: {idx}px\nAng. Quadril: {ang:.1f}°"
    ax.text(50, 50, info_texto, color='black', fontweight='bold', 
            fontsize=12, backgroundcolor='white', bbox=dict(pad=5, color='white'))

    if inverter:
        ax.invert_xaxis()
    
    ax.set_title(titulo, fontsize=15, fontweight='bold')
    ax.axis('off')

# --- EXECUÇÃO ---
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 9))

# Calistenia na ESQUERDA
plotar_analise(ax1, 'foto_calistenia.jpg', c_pontos, "CALISTENIA (Arqueado)", inverter=True)

# Ginástica na DIREITA
plotar_analise(ax2, 'foto_ginastica.jpg', g_pontos, "GINÁSTICA (Alinhado)", inverter=False)

plt.tight_layout()
plt.savefig('analise_biomecanica_V3.png')
print("✅ Código corrigido e imagem gerada: 'analise_biomecanica_V3.png'")