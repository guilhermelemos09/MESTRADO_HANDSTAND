import os
import glob
import sys
from datetime import datetime

# Importar as funções de análise atualizadas da mesma pasta
from analisar_hs_piloto import analisar_hs_piloto
from analisar_hsw_piloto import analisar_hsw_piloto
from analisar_hsw_piloto import analisar_hsw_piloto

def gerar_relatorio():
    caminho_base = r"C:\Users\User\Documents\MESTRADO_HANDSTAND\analise_dados\testes_pilotos\Guilherme_extra"
    caminho_limpos = os.path.join(caminho_base, "Arquivos_Reconstruidos_Limpos")
    caminho_saida = os.path.join(caminho_base, "Analise_Variaveis_Finais")
    
    if not os.path.exists(caminho_saida):
        os.makedirs(caminho_saida)
        
    arquivos = glob.glob(os.path.join(caminho_limpos, "*_limpo.c3d"))
    
    resultados_hs = []
    resultados_hsw = []
    
    for arq in arquivos:
        nome_arquivo = os.path.basename(arq)
        print(f"Processando: {nome_arquivo}")
        
        # Identificar se é HS ou HSW
        if "hsw" in nome_arquivo.lower():
            try:
                res = analisar_hsw_piloto(arq)
                res["Arquivo"] = nome_arquivo
                resultados_hsw.append(res)
            except Exception as e:
                print(f"[Erro HSW] {nome_arquivo}: {e}")
        elif "hs" in nome_arquivo.lower():
            try:
                cond = "assistido" if "assistido" in nome_arquivo.lower() else "livre"
                res = analisar_hs_piloto(arq, cond)
                res["Arquivo"] = nome_arquivo
                resultados_hs.append(res)
            except Exception as e:
                print(f"[Erro HS] {nome_arquivo}: {e}")

    def gerar_analise_comparativa(metrica, nomes, valores):
        if len(nomes) < 2 or len(valores) < 2: return "Sem dados suficientes para comparação."
        try:
            v1, v2 = float(valores[0]), float(valores[1])
        except: return ""
        n1, n2 = nomes[0], nomes[1]
        
        diff = abs(v1 - v2)
        if diff < 0.001: return "Resultados praticamente idênticos."
        
        maior = n1 if v1 > v2 else n2
        menor = n1 if v1 < v2 else n2
        
        if metrica == "ApEn CoP":
            return f"<b>{maior}</b> obteve maior entropia, indicando correções posturais mais automáticas e eficientes (menos rigidez) em relação a {menor}."
        elif "Velocidade" in metrica and "CoP" in metrica:
            return f"<b>{maior}</b> apresentou contrações mais rápidas/nervosas. <b>{menor}</b> foi mais estável com menor custo energético."
        elif "Distancia CoP-CoM" in metrica:
            return f"<b>{menor}</b> teve um erro de controle postural menor, mantendo o balanço mais centrado que {maior}."
        elif "Tempo de Equilibrio" in metrica:
            return f"<b>{maior}</b> demonstrou superioridade clara na manutenção do equilíbrio."
        elif "Verticalidade" in metrica:
            dif1 = abs(180 - v1)
            dif2 = abs(180 - v2)
            melhor = n1 if dif1 < dif2 else n2
            return f"<b>{melhor}</b> apresentou melhor empilhamento ósseo (mais próximo de 180º), reduzindo o torque compensatório necessário."
        elif "Velocidade Media" in metrica:
            return f"<b>{maior}</b> foi mais rápido, otimizando o tempo sob tensão isométrica."
        elif "CV" in metrica:
            return f"<b>{menor}</b> teve variabilidade menor, denotando maior maturidade motora e consistência na marcha que {maior}."
        elif "Tempo Total" in metrica or "Percorrida" in metrica:
            return f"<b>{maior}</b> demonstrou maior resistência e capacidade de locomoção."
        elif "Extensao Cervical" in metrica:
            return f"<b>{maior}</b> compensou mais na cervical (olhando mais o chão), o que pode influenciar na lordose lombar em relação a {menor}."
        elif "Base Apoio" in metrica:
            return f"<b>{maior}</b> usou base mais larga, priorizando estabilidade lateral, enquanto {menor} focou em eficiência frontal."
        elif "Duplo Suporte" in metrica:
            return f"<b>{maior}</b> passou mais tempo em duplo apoio, revelando maior busca por segurança contra quedas na marcha."
        elif "Rotacao" in metrica:
            return f"<b>{maior}</b> utilizou maior rotação externa das mãos, possivelmente aliviando mais a articulação do punho."
        elif "Altura CoM" in metrica:
            return f"<b>{menor}</b> manteve o centro de massa mais baixo, facilitando o controle pendular."
        else:
            return f"<b>{maior}</b> apresentou valor maior ({max(v1, v2):.2f}) que <b>{menor}</b> ({min(v1, v2):.2f})."

    # Dicionário descritivo base para quando não houver comparação direta
    comentarios = {
        "Tempo de Equilibrio (s)": "Tempo contínuo de inversão. Indicador primário de proficiência no suporte de peso.",
        "Base Apoio (mm)": "Distância mediolateral. Bases mais largas aumentam estabilidade lateral, mas exigem mais torque do ombro.",
        "Rotacao das Maos (deg)": "Rotação externa (toe-out). Facilita ajustes anteroposteriores do punho e alivia compressão articular.",
        "Altura CoM (mm)": "Altura do pêndulo. Quanto maior, maior o desafio estabilométrico.",
        "Distancia CoP-CoM (mm)": "Erro do controle postural. Mede a disparidade entre a perturbação real e a resposta corretiva.",
        "Velocidade CoP (mm/s)": "Rapidez das contrações musculares. Valores altos indicam menor estabilidade e maior custo energético.",
        "ApEn CoP": "Entropia. Valores mais altos indicam ajustes automáticos, eficientes e de menor rigidez cognitiva.",
        "Comprimento Braco (mm)": "Alavanca superior. Influencia a amplitude mecânica necessária para a locomoção.",
        "Comprimento Perna (mm)": "Alavanca inferior. Pernas longas amplificam dramaticamente o momento de inércia da queda.",
        "Indice Verticalidade (deg)": "Alinhamento 3D Global (Pêndulo Invertido). Aproximar-se de 180º reduz torques musculares compensatórios.",
        "Extensao Cervical (deg)": "Posição da cabeça. Extensão serve para ancoragem visual no solo, mas pode induzir lordose lombar.",
        "Distancia Percorrida (mm)": "Deslocamento total em inversão. Métrica absoluta de proficiência dinâmica.",
        "Tempo Total (s)": "Duração da caminhada. Combinada com a distância, define a eficiência de propulsão.",
        "Velocidade Media (mm/s)": "Eficiência da locomoção. Velocidades constantes reduzem tempo sob tensão isométrica.",
        "Cadencia (passos/s)": "Frequência de apoio. Cadências muito altas revelam instabilidade e urgência na troca de mãos.",
        "Comprimento Passada (mm)": "Avanço do braço. Passadas curtas sugerem hesitação na fase de balanço e pouca confiança.",
        "CV Comprimento (%)": "Consistência espacial. Baixa variabilidade atesta controle motor maduro.",
        "CV Tempo (%)": "Consistência rítmica. Maior regularidade evita perturbações no pêndulo dinâmico.",
        "Tempo de Contato (s)": "Duração do apoio no solo. Tempos longos refletem dependência de estabilidade em detrimento da progressão.",
        "% Duplo Suporte": "Análogo à marcha senil, altos % revelam busca extrema por proteção contra quedas durante a caminhada.",
        "Largura Base Apoio (mm)": "Afastamento lateral na caminhada. Protege contra desequilíbrios frontais.",
        "Rotacao Maos (graus)": "Rotação das mãos durante a caminhada. Guia a transferência de peso no eixo do punho."
    }

    # Gerar Arquivo .doc (Formato HTML legível no Word)
    doc_path = os.path.join(caminho_saida, "Matriz_Variaveis_Finais_Vertical.doc")
    
    html = f"""
    <html>
    <head><meta charset="utf-8"></head>
    <body style="font-family: Arial, sans-serif;">
        <h1 style="text-align: center;">Matriz de Variáveis Finais - Projeto Handstand</h1>
        <p><b>Data da Extração:</b> {datetime.now().strftime('%d/%m/%Y %H:%M')}</p>
        <p><i>Formatação Vertical (Métricas nas linhas, Participantes nas colunas). Tabela inclui comentários biomecânicos explicativos das implicações dos dados.</i></p>
    """

    # --- TABELA HS (VERTICAL) ---
    if resultados_hs:
        metricas_hs = [k for k in resultados_hs[0].keys() if k != "Arquivo" and k != "Condição"]
        arquivos_hs = [res["Arquivo"].split("_")[0].upper() for res in resultados_hs]
        
        html += "<h2>1. Handstand Estático (HS)</h2>"
        html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse; width: 100%; text-align: left;'>"
        # Cabeçalho
        html += "<tr style='background-color: #f2f2f2;'><th style='width: 20%;'>Métrica (Variável)</th>"
        for arq in arquivos_hs:
            html += f"<th>{arq}</th>"
        html += "<th style='width: 40%;'>Implicação Biomecânica / Relevância</th></tr>"
        
        # Linhas
        for metrica in metricas_hs:
            html += "<tr>"
            html += f"<td><b>{metrica}</b></td>"
            valores_num = []
            for res in resultados_hs:
                val = res.get(metrica, "N/A")
                if isinstance(val, (int, float)): valores_num.append(val)
                val_str = f"{val:.4f}".replace(".", ",") if isinstance(val, float) else val
                html += f"<td style='text-align: center;'>{val_str}</td>"
            
            analise = gerar_analise_comparativa(metrica, arquivos_hs, valores_num)
            if analise == "": analise = comentarios.get(metrica, "")
            html += f"<td><i>{analise}</i></td>"
            html += "</tr>"
        html += "</table><br><br>"

    # --- TABELA HSW (VERTICAL) ---
    if resultados_hsw:
        metricas_hsw = [k for k in resultados_hsw[0].keys() if k != "Arquivo"]
        arquivos_hsw = [res["Arquivo"].split("_")[0].upper() for res in resultados_hsw]
        
        html += "<h2>2. Handstand Walk (HSW)</h2>"
        html += "<table border='1' cellpadding='5' cellspacing='0' style='border-collapse: collapse; width: 100%; text-align: left;'>"
        # Cabeçalho
        html += "<tr style='background-color: #f2f2f2;'><th style='width: 20%;'>Métrica (Variável)</th>"
        for arq in arquivos_hsw:
            html += f"<th>{arq}</th>"
        html += "<th style='width: 40%;'>Análise Biomecânica Comparativa</th></tr>"
        
        # Linhas
        for metrica in metricas_hsw:
            html += "<tr>"
            html += f"<td><b>{metrica}</b></td>"
            valores_num = []
            for res in resultados_hsw:
                val = res.get(metrica, "N/A")
                if isinstance(val, (int, float)): valores_num.append(val)
                val_str = f"{val:.4f}".replace(".", ",") if isinstance(val, float) else val
                html += f"<td style='text-align: center;'>{val_str}</td>"
            
            analise = gerar_analise_comparativa(metrica, arquivos_hsw, valores_num)
            if analise == "": analise = comentarios.get(metrica, "")
            html += f"<td><i>{analise}</i></td>"
            html += "</tr>"
        html += "</table><br><br>"

    # --- FUNDAMENTAÇÃO TEÓRICA ---
    html += "<h2>3. Fundamentação Físico-Matemática e Referências</h2>"
    
    html += "<h3>Detecção dos Passos e Parâmetros Espaço-Temporais (Cadência e Comprimento)</h3>"
    html += "<ul><li><b>O que é:</b> Avaliar a velocidade e a extensão de cada toque das mãos, formando a base da Eficiência de Locomoção.</li>"
    html += "<li><b>Conceito Físico-Matemático (Script):</b> Os eventos de marcha (Touchdown e Lift-off) não foram marcados manualmente. Foram identificados algoritmicamente via limiar de velocidade resultante do marcador do punho (< 150 mm/s) alinhado à altura mínima no eixo Z, delimitando matematicamente as fases de balanço e suporte sem viés humano.</li>"
    html += "<li><b>Referência:</b> ZENI, J. A.; RICHARDS, J. G.; HIGGINSON, J. S. Two simple methods for determining gait events during treadmill and overground walking using kinematic data. Gait & Posture, v. 27, n. 4, p. 710-714, 2008.</li></ul>"

    html += "<h3>Cálculo do CoP (Centro de Pressão) e Velocidade do CoP</h3>"
    html += "<ul><li><b>O que é:</b> Medir o ponto de aplicação da força de reação do solo para inferir o esforço neuromuscular de controle e correções do balanço.</li>"
    html += "<li><b>Conceito Físico-Matemático (Script):</b> O CoP bidimensional (x,y) foi derivado estritamente pelas leis de Newton, dividindo o momento de força transversal (Mx, My) pela força vertical (Fz) medida na plataforma (CoPx = -My/Fz; CoPy = Mx/Fz). A velocidade foi obtida pela primeira derivada temporal desse deslocamento.</li>"
    html += "<li><b>Referência:</b> WINTER, D. A. Biomechanics and motor control of human movement. 4. ed. Hoboken: John Wiley & Sons, 2009.</li></ul>"

    html += "<h3>Índice de Verticalidade (Alinhamento 3D)</h3>"
    html += "<ul><li><b>O que é:</b> Avaliar o alinhamento corporal global (empilhamento ósseo) durante a inversão, visando a eficiência mecânica do Pêndulo Invertido.</li>"
    html += "<li><b>Conceito Físico-Matemático (Script):</b> Extraído independentemente das matrizes de Euler clássicas (para mitigar falhas de <i>Gimbal Lock</i> na postura invertida). Calculou-se o ângulo 3D absoluto via Produto Escalar (<i>Dot Product</i>) entre o vetor da base (Punho -> Pelve) e o vetor superior (Pelve -> Tornozelo). Valor ideal = 180º.</li>"
    html += "<li><b>Referência:</b> CRAIG, J. J. Introduction to robotics: mechanics and control. 3. ed. Pearson Prentice Hall, 2005 (Para validação matemática de vetores 3D) e BAKER, R. Measuring walking: a handbook of clinical gait analysis. Mac Keith Press, 2013 (Limitações do modelo pélvico de Euler).</li></ul>"

    html += "<h3>Entropia Aproximada (ApEn CoP)</h3>"
    html += "<ul><li><b>O que é:</b> Quantificar a regularidade e previsibilidade das flutuações do CoP, indicando a automaticidade do controle postural (menor rigidez cognitiva).</li>"
    html += "<li><b>Conceito Físico-Matemático (Script):</b> Medida não linear que avalia a probabilidade de padrões semelhantes no sinal de balanço se repetirem. O script aplicou a rotina matemática de Pincus com janela (m=2) e tolerância (r=0.2 desvios padrões do sinal).</li>"
    html += "<li><b>Referência:</b> PINCUS, S. M. Approximate entropy as a measure of system complexity. Proceedings of the National Academy of Sciences, v. 88, n. 6, p. 2297-2301, 1991.</li></ul>"

    html += "<h3>Distância Contínua CoP-CoM</h3>"
    html += "<ul><li><b>O que é:</b> Quantificar o 'erro dinâmico' de estabilidade. Ou seja, o quão distante a correção neuromotora (CoP) precisa se deslocar para resgatar a perturbação gravitacional da massa (CoM).</li>"
    html += "<li><b>Conceito Físico-Matemático (Script):</b> Diferença Euclidiana plana calculada frame a frame (fórmula de Pitágoras em 2D) entre a projeção vertical do Centro de Massa (estimado pelo centro pélvico) e as coordenadas instantâneas do Centro de Pressão.</li>"
    html += "<li><b>Referência:</b> CORRIVEAU, H. et al. Evaluation of postural stability in the elderly with stroke. Archives of Physical Medicine and Rehabilitation, v. 85, n. 7, p. 1095-1101, 2004.</li></ul>"

    html += "</body></html>"
    
    with open(doc_path, 'w', encoding='utf-8') as f:
        f.write(html)
        
    print(f"\n[SUCESSO] Relatório gerado em: {doc_path}")

if __name__ == "__main__":
    gerar_relatorio()
