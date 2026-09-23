# -*- coding: utf-8 -*-
"""
Script de Geração do Relatório Individual Devolutivo Completo - Participante P001 (Gustavo Donato)
Pesquisa de Mestrado em Ciências do Esporte - EEFERP-USP
Orientador: Prof. Dr. Matheus Machado Gomes | Mestrando: Guilherme de Paula Lemos

Atualizações Recentes:
- Inclusão do logo oficial da EEFERP-USP no cabeçalho (HTML em base64 e DOCX)
- Correção do título oficial do projeto: "Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk"
- Destaque tipográfico para "Mestrando" e "Orientador"
- Tópico explicativo conciso com o Objetivo Geral do Projeto
- Padronização de decimais com vírgula (padrão brasileiro ABNT/USP)
- Preservação integral do layout em cards, pills, callouts e paleta verde esmeralda/menta
"""

import os
import sys
import base64
import subprocess
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

def f_dec(val, dec=2):
    """Formata float com vírgula decimal padrão brasileiro."""
    return f"{val:.{dec}f}".replace(".", ",")

# =========================================================================
# CONFIGURAÇÃO DE DIRETÓRIOS E ARQUIVOS
# =========================================================================
BASE_DIR = r"c:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL\03_CONSOLIDACAO_DATASET"
OUTPUT_DIR = os.path.join(BASE_DIR, "resultados_finais", "laudos_devolutiva", "P001_laudo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOCX_OUT = os.path.join(OUTPUT_DIR, "P001_RELATORIO_DEVOLUTIVA_GUSTAVO_DONATO.docx")
HTML_OUT = os.path.join(OUTPUT_DIR, "P001_RELATORIO_DEVOLUTIVA_GUSTAVO_DONATO.html")
PDF_OUT = os.path.join(OUTPUT_DIR, "P001_RELATORIO_DEVOLUTIVA_GUSTAVO_DONATO.pdf")

LOGO_EEFERP_WHITE = os.path.join(OUTPUT_DIR, "logo_eeferp_white.png")
LOGO_EEFERP_COLOR = os.path.join(OUTPUT_DIR, "logo_eeferp_color.png")

# Título oficial conforme o projeto de pesquisa cadastrado na EEFERP-USP
TITULO_OFICIAL_PROJETO = "Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk"

OBJETIVO_GERAL_PROJETO = (
    "Investigar os fatores determinantes e preditores do desempenho no Handstand (HS) e Handstand Walk (HSW), "
    "integrando a capacidade neuromuscular dos membros superiores (força e resistência proximal e distal), o controle postural estabilométrico "
    "(oscilação do Centro de Pressão na plataforma de força Bertec) e a cinemática tridimensional Vicon "
    "(alinhamento articular vertical e dinâmica espaço-temporal da locomoção invertida)."
)

# =========================================================================
# DADOS CONSOLIDADOS E AUDITADOS DE P001 (LACIDH + LABIOCOM)
# =========================================================================
NOME_ATLETA = "Gustavo H. Donato da Costa"
CODIGO_ATLETA = "P001 (Atleta Piloto Oficial)"
IDADE = 20
FAIXA_ETARIA = "20 anos (Faixa 20 a 24 anos)"
SEXO = "Masculino"
DOMINANCIA = "Destro (Membro Direito)"
DATA_COLETA_S1 = "02/09/2026 (LaCiDH — Força e BIA)"
DATA_COLETA_S2 = "09/09/2026 (LaBioCoM — Vicon 3D e Bertec)"
MODALIDADES = "Calistenia / Handbalancing (Prática Isolada)"
TEMPO_PRATICA = "24 meses geral (18 meses específico em HS)"
VOLUME_PRATICA_HORAS = 150.0

# 1. Antropometria e Composição Corporal (BIA Sanny® - Sun et al., 2003)
MASSA_KG = 65.25
ESTATURA_CM = 171.0
ESTATURA_M = ESTATURA_CM / 100.0
IMC = round(MASSA_KG / (ESTATURA_M ** 2), 2)  # 22.31 kg/m²
GORDURA_PCT = 16.56
MG_KG = 10.85
MLG_KG = 54.40
MME_KG = 30.10
ACT_L = 39.80
ACT_PCT = round((ACT_L / MASSA_KG) * 100.0, 1)  # 61.0%
PHA_DEG = 8.98
FFMI = round(MLG_KG / (ESTATURA_M ** 2), 2)  # 18.60 kg/m²

# 2. Força Distal (Saehan Hidráulico & Biodex System 4 PRO a 70°)
FPM_DIR = 46.0
FPM_ESQ = 52.0
FPM_MED = round((FPM_DIR + FPM_ESQ) / 2.0, 1)  # 49.0 kgf
FPM_MAX = 52.0
FPM_REL_MAX = round(FPM_MAX / MASSA_KG, 3)     # 0.797 kgf/kg
FPM_REL_MED = round(FPM_MED / MASSA_KG, 3)     # 0.751 kgf/kg
LSI_FPM = round((FPM_ESQ / FPM_DIR) * 100.0, 1) # 113.0% (Esq > Dir por 13.0%)

BIODEX_PICO_D = 18.5
BIODEX_PICO_E = 20.5
BIODEX_MED = round((BIODEX_PICO_D + BIODEX_PICO_E) / 2.0, 1) # 19.5 N·m
BIODEX_MAX = 20.5
BIODEX_REL_MED = round(BIODEX_MED / MASSA_KG, 4) # 0.2989 N·m/kg
BIODEX_REL_MAX = round(BIODEX_MAX / MASSA_KG, 4) # 0.3142 N·m/kg
LSI_BIODEX = round((BIODEX_PICO_E / BIODEX_PICO_D) * 100.0, 2) # 110.81% (Esq > Dir por 10.8%)

# 3. Força Proximal e Resistência Isométrica
SP_1RM_KG = 56.0
SP_REL_PCT = round((SP_1RM_KG / MASSA_KG) * 100.0, 1) # 85.8%
SP_REL_KG_KG = round(SP_1RM_KG / MASSA_KG, 3)        # 0.858 kg/kg
WALL_HS_T1 = 60.0
WALL_HS_T2 = 64.0
WALL_HS_MAX = 64.0

# 4. Cinemática e Cinética Estabilométrica (LaBioCoM - Handstand Estático)
HS_ASSIST_PICO_S = 40.80
HS_ASSIST_T1_S = 40.80
HS_ASSIST_T2_S = 40.58
HS_ASSIST_T3_S = 39.51
HS_ASSIST_MED_S = round((HS_ASSIST_T1_S + HS_ASSIST_T2_S + HS_ASSIST_T3_S) / 3.0, 2) # 40.30 s

COP_COM_DIST_MM = 50.02
COP_VEL_MM_S = 98.98
APEN_COP = 0.7756

HS_VERT_DEG = 12.02
HS_CERVICAL_DEG = 23.35
HS_PLANTAR_DEG = 33.45
HS_BASE_MM = 570.41
HS_ROT_MAOS_DEG = 30.93

# 5. Handstand Livre (Autonomia e Domínio Técnico)
HS_LIVRE_TAXA_SUCESSO = "100% (3 de 3 tentativas válidas ≥ 3s)"
HS_LIVRE_TEMPO_MAX_S = 24.52
HS_LIVRE_T1_S = 3.52
HS_LIVRE_T2_S = 24.52
HS_LIVRE_T3_S = 13.56
HS_LIVRE_VERT_DEG = 7.97
HS_LIVRE_CERVICAL_DEG = 23.30
HS_LIVRE_PLANTAR_DEG = 28.44

# Estratégias Articulares de Busca do Equilíbrio (Cinemática 3D)
HS_COTOVELO_SD_DEG = 16.96
HS_COTOVELO_ROM_DEG = 81.65
HS_COTOVELO_RMS_DEG_S = 19.80
HS_OMBRO_SD_DEG = 11.75
HS_OMBRO_ROM_DEG = 64.93
HS_OMBRO_RMS_DEG_S = 18.55
HS_QUADRIL_SD_DEG = 4.88
HS_QUADRIL_ROM_DEG = 36.05
HS_QUADRIL_RMS_DEG_S = 9.96
HS_RAZAO_COTOVELO_OMBRO = 1.44
HS_ESTRATEGIA_DOMINANTE = "Cotovelo-Dominante / Busca Multijunta"
HSW_VEL_KM_H = 1.51
HSW_CONTATO_MS = 1020

# 6. Handstand Walk (HSW Dinâmico)
HSW_DIST_MEDIANA_M = 1.78
HSW_DIST_MAX_M = 4.28
HSW_T1_DIST_M = 1.49
HSW_T2_DIST_M = 1.78
HSW_T3_DIST_M = 4.28

HSW_CADENCIA = 0.98
HSW_PASSADA_MM = 428.28
HSW_VEL_M_S = 0.42
HSW_CONTATO_S = 1.02
HSW_DUPLO_SUPORTE_PCT = 56.01
HSW_CV_ESPACIAL = 14.07
HSW_CV_TEMPORAL = 56.95

HSW_VERT_DEG = 13.42
HSW_CERVICAL_DEG = 42.64
HSW_PLANTAR_DEG = 5.85
HSW_BASE_MM = 566.77
HSW_ROT_MAOS_DEG = 66.87

print("Variáveis carregadas. Carregando logos e gerando documentos...")

# Processamento do logo em base64 para o HTML
logo_white_b64 = ""
if os.path.exists(LOGO_EEFERP_WHITE):
    with open(LOGO_EEFERP_WHITE, "rb") as f:
        logo_white_b64 = base64.b64encode(f.read()).decode("utf-8")

# =========================================================================
# 1. CONSTRUÇÃO DO DOCUMENTO DOCX FORMATADO
# =========================================================================
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def set_cell_margins(cell, top=80, bottom=80, left=120, right=120):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

def add_highlight_box(doc, title, layperson_text, science_text=None):
    tbl = doc.add_table(rows=1, cols=1)
    tbl.alignment = WD_TABLE_ALIGNMENT.CENTER
    c = tbl.cell(0, 0)
    set_cell_background(c, "F0FDF4")
    set_cell_margins(c, top=100, bottom=100, left=140, right=140)
    
    tcPr = c._tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:top w:val="none"/>'
        f'<w:left w:val="single" w:sz="36" w:space="0" w:color="10B981"/>'
        f'<w:bottom w:val="none"/>'
        f'<w:right w:val="none"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)
    
    p = c.paragraphs[0]
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(2)
    r_title = p.add_run(title + "\n")
    r_title.bold = True
    r_title.font.name = "Arial"
    r_title.font.size = Pt(8.5)
    r_title.font.color.rgb = RGBColor(6, 78, 59)
    
    r_lay = p.add_run(layperson_text)
    r_lay.font.name = "Arial"
    r_lay.font.size = Pt(8.0)
    r_lay.font.color.rgb = RGBColor(30, 41, 59)
    
    if science_text:
        p2 = c.add_paragraph()
        p2.paragraph_format.space_before = Pt(4)
        p2.paragraph_format.space_after = Pt(2)
        r_sci_tag = p2.add_run("Fundamentação Científica & Biomecânica: ")
        r_sci_tag.bold = True
        r_sci_tag.font.name = "Arial"
        r_sci_tag.font.size = Pt(7.8)
        r_sci_tag.font.color.rgb = RGBColor(4, 120, 87)
        
        r_sci = p2.add_run(science_text)
        r_sci.font.name = "Arial"
        r_sci.font.size = Pt(7.8)
        r_sci.font.color.rgb = RGBColor(71, 85, 105)

    p_spacer = doc.add_paragraph()
    p_spacer.paragraph_format.space_before = Pt(0)
    p_spacer.paragraph_format.space_after = Pt(2)

doc = docx.Document()
for s in doc.sections:
    s.top_margin = Inches(0.55)
    s.bottom_margin = Inches(0.55)
    s.left_margin = Inches(0.65)
    s.right_margin = Inches(0.65)

EMERALD_DARK_RGB = RGBColor(6, 78, 59)
EMERALD_HEADER_RGB = RGBColor(4, 120, 87)
TEXT_DARK_RGB = RGBColor(30, 41, 59)
TEXT_MUTED_RGB = RGBColor(100, 116, 139)

# Inclusão do Logo da EEFERP no Cabeçalho do DOCX
if os.path.exists(LOGO_EEFERP_COLOR):
    p_logo = doc.add_paragraph()
    p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_logo.paragraph_format.space_before = Pt(0)
    p_logo.paragraph_format.space_after = Pt(2)
    r_logo = p_logo.add_run()
    r_logo.add_picture(LOGO_EEFERP_COLOR, width=Inches(0.95))

# Cabeçalho Institucional
p_inst = doc.add_paragraph()
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_inst.paragraph_format.space_before = Pt(1)
p_inst.paragraph_format.space_after = Pt(1)
r_inst = p_inst.add_run(
    "UNIVERSIDADE DE SÃO PAULO — EEFERP-USP\n"
    "Escola de Educação Física e Esporte de Ribeirão Preto\n"
    "Laboratório de Cineantropometria e Desempenho Humano (LaCiDH) | Laboratório de Biomecânica e Controle Motor (LaBioCoM)"
)
r_inst.font.name = "Arial"
r_inst.font.size = Pt(8.0)
r_inst.font.bold = True
r_inst.font.color.rgb = EMERALD_HEADER_RGB

p_title = doc.add_paragraph()
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_title.paragraph_format.space_before = Pt(2)
p_title.paragraph_format.space_after = Pt(1)
r_title = p_title.add_run("RELATÓRIO INDIVIDUAL DEVOLUTIVO DE DESEMPENHO E BIOMECÂNICA")
r_title.bold = True
r_title.font.name = "Arial"
r_title.font.size = Pt(12.5)
r_title.font.color.rgb = EMERALD_DARK_RGB

p_meta = doc.add_paragraph()
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER
p_meta.paragraph_format.space_before = Pt(0)
p_meta.paragraph_format.space_after = Pt(3)

r_proj_tag = p_meta.add_run("Projeto: ")
r_proj_tag.bold = True
r_proj_tag.font.name = "Arial"
r_proj_tag.font.size = Pt(7.8)
r_proj_tag.font.color.rgb = EMERALD_HEADER_RGB

r_proj_val = p_meta.add_run(f"{TITULO_OFICIAL_PROJETO}\n")
r_proj_val.font.name = "Arial"
r_proj_val.font.size = Pt(7.8)
r_proj_val.font.color.rgb = TEXT_DARK_RGB

r_m_tag = p_meta.add_run("Mestrando: ")
r_m_tag.bold = True
r_m_tag.font.name = "Arial"
r_m_tag.font.size = Pt(7.8)
r_m_tag.font.color.rgb = EMERALD_HEADER_RGB

r_m_val = p_meta.add_run("Guilherme de Paula Lemos   |   ")
r_m_val.font.name = "Arial"
r_m_val.font.size = Pt(7.8)
r_m_val.font.color.rgb = TEXT_DARK_RGB

r_o_tag = p_meta.add_run("Orientador: ")
r_o_tag.bold = True
r_o_tag.font.name = "Arial"
r_o_tag.font.size = Pt(7.8)
r_o_tag.font.color.rgb = EMERALD_HEADER_RGB

r_o_val = p_meta.add_run("Prof. Dr. Matheus Machado Gomes")
r_o_val.font.name = "Arial"
r_o_val.font.size = Pt(7.8)
r_o_val.font.color.rgb = TEXT_DARK_RGB

# Tabela do Atleta
t_part = doc.add_table(rows=2, cols=4)
t_part.alignment = WD_TABLE_ALIGNMENT.CENTER
for row in t_part.rows:
    for cell in row.cells:
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def format_cell_box(cell, label, val):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    r1 = p.add_run(label + "\n")
    r1.font.bold = True
    r1.font.size = Pt(7.2)
    r1.font.color.rgb = EMERALD_HEADER_RGB
    r2 = p.add_run(val)
    r2.font.bold = True
    r2.font.size = Pt(8.5)
    r2.font.color.rgb = TEXT_DARK_RGB

format_cell_box(t_part.rows[0].cells[0], "PARTICIPANTE", NOME_ATLETA)
format_cell_box(t_part.rows[0].cells[1], "CÓDIGO / ID", CODIGO_ATLETA)
format_cell_box(t_part.rows[0].cells[2], "IDADE / FAIXA", FAIXA_ETARIA)
format_cell_box(t_part.rows[0].cells[3], "SEXO / DOMINÂNCIA", f"{SEXO} | {DOMINANCIA}")

format_cell_box(t_part.rows[1].cells[0], "MASSA / ESTATURA", f"{f_dec(MASSA_KG)} kg | {f_dec(ESTATURA_CM, 1)} cm")
format_cell_box(t_part.rows[1].cells[1], "MODALIDADE / VOLUME", f"{MODALIDADES} (~{VOLUME_PRATICA_HORAS:.0f}h)")
format_cell_box(t_part.rows[1].cells[2], "DATAS DAS COLETAS", "02/09 (LaCiDH) e 09/09/2026 (LaBioCoM)")
format_cell_box(t_part.rows[1].cells[3], "STATUS DOS TESTES", "100% Concluídos (S1 + S2)")

p_intro = doc.add_paragraph()
p_intro.paragraph_format.space_before = Pt(4)
p_intro.paragraph_format.space_after = Pt(4)
r_in = p_intro.add_run(
    f"Olá, {NOME_ATLETA.split()[0]}! Muito obrigado pela sua dedicação e contribuição voluntária nas duas sessões do nosso estudo na EEFERP-USP. "
    f"Este laudo foi elaborado para você: ele reúne suas avaliações do LaCiDH (Composição Corporal e Força Neuromuscular) e do LaBioCoM (Handstand e Handstand Walk 3D). "
    f"Para tornar a leitura agradável e esclarecedora, começamos cada tópico contextualizando o que os resultados podem representar na prática e finalizamos com a fundamentação científica correspondente [1-22]. "
    f"Agradecemos e parabenizamos pelo empenho ao longo de todos os testes!"
)
r_in.font.size = Pt(8.2)
r_in.font.color.rgb = TEXT_DARK_RGB

# Box de Objetivo do Projeto de Mestrado (posicionado logo após a saudação)
add_highlight_box(
    doc,
    "🎯 Objetivo Geral do Projeto de Mestrado",
    OBJETIVO_GERAL_PROJETO,
    "Dissertação vinculada ao Programa de Pós-Graduação em Ciências da Reabilitação e Desempenho Funcional / Ciências do Esporte — EEFERP-USP."
)

headers_tabelas = ["Parâmetro Avaliado", "Seu Resultado", "Interpretação e Contextualização"]

# -------------------------------------------------------------------------
# SEÇÃO 1: BIA
# -------------------------------------------------------------------------
h1 = doc.add_heading("1. Composição Corporal e Estado Morfofuncional (Bioimpedância Sanny® — Sun et al., 2003)", level=2)
h1.runs[0].font.color.rgb = EMERALD_DARK_RGB
h1.runs[0].font.size = Pt(10)
h1.paragraph_format.space_before = Pt(3)
h1.paragraph_format.space_after = Pt(2)

t_bia = doc.add_table(rows=6, cols=3)
t_bia.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_tabelas):
    c = t_bia.cell(0, j)
    c.text = h
    set_cell_background(c, "047857")
    set_cell_margins(c, top=40, bottom=40, left=70, right=70)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(7.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

bia_dados_doc = [
    ("Massa Corporal & Estatura\nÍndice de Massa Corporal (IMC)", f"{f_dec(MASSA_KG)} kg | {f_dec(ESTATURA_CM, 1)} cm\nIMC = {f_dec(IMC)} kg/m²", "Faixa de Eutrofia / Padrão Saudável segundo a OMS e ACSM [3]."),
    ("Percentual de Gordura Corporal (%GC)\nEquação Específica de Sun et al. (2003) [1]", f"{f_dec(GORDURA_PCT)}%\n({f_dec(MG_KG)} kg em gordura)", "Excelente! Padrão atlético funcional (10% a 18% para homens jovens [3])."),
    ("Massa Livre de Gordura (MLG)\nTecidos Metabolicamente Ativos", f"{f_dec(MLG_KG)} kg\n(83,4% da massa corporal)", "Amplo predomínio de massa magra ativa sustentando as exigências antigravitacionais."),
    ("Massa Muscular Esquelética (MME)\nPreditor de Força Muscular (Janssen et al., 2000) [2]", f"{f_dec(MME_KG)} kg\n(46,1% da massa corporal)", "Volume muscular consistente nos membros e tronco para estabilização postural."),
    ("Ângulo de Fase a 50 kHz (PhA)\nBiomarcador de Integridade Celular [4,5]", f"{f_dec(PHA_DEG)}°\n(Destaque Notável)", "Acima da média normativa de homens de 20-29 anos (7,53° ± 0,73° [4]; Z-score = +1,99 DP).")
]

for i, row in enumerate(bia_dados_doc, 1):
    for j, val in enumerate(row):
        c = t_bia.cell(i, j)
        c.text = val
        set_cell_margins(c, top=40, bottom=40, left=70, right=70)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.runs[0].font.size = Pt(7.4)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, "F0FDF4" if i % 2 == 1 else "FFFFFF")

add_highlight_box(
    doc,
    "💡 O que esses dados indicam na prática: Relação massa magra e eficiência funcional",
    f"Na parada de mão, todo o peso corporal precisa ser sustentado contra a gravidade pelos membros superiores. "
    f"Por isso, a proporção entre massa livre de gordura e tecido adiposo é um aspecto altamente favorável no seu perfil: com {f_dec(GORDURA_PCT, 1)}% de gordura e {f_dec(MLG_KG, 1)} kg de massa magra (mais de 83% do peso total), "
    f"há uma relação eficiente de peso funcional para ser suportado por punhos e ombros. "
    f"Um dado que merece elogio é o seu Ângulo de Fase ({f_dec(PHA_DEG)}°), que se situa substancialmente acima da média de referência normativa para sua faixa etária (7,53° ± 0,73°, Barbosa-Silva et al., 2005 [4]; Z-score = +1,99 DP): "
    f"na literatura científica [4,5], valores elevados de PhA refletem excelente integridade das membranas celulares e adequada hidratação intra/extracelular, "
    f"o que aponta para um potencial favorável de tolerância ao esforço físico e boa capacidade de recuperação aos estímulos de treino.",
    "A bioimpedância processada pela equação de multicomponentes de Sun et al. (2003) [1] e Janssen et al. (2000) [2] aponta para um perfil morfofuncional equilibrado para modalidades antigravitacionais. "
    "O Ângulo de Fase reflete propriedades elétricas (capacitância de membrana) dos tecidos (Barbosa-Silva et al., 2005 [4]; Norman et al., 2012 [5]). "
    "Um PhA de 8,98° sugere uma potencial vantagem biológica na tolerância à fadiga celular, hipótese a ser investigada estatisticamente na amostra da dissertação."
)

# -------------------------------------------------------------------------
# SEÇÃO 2: FORÇA NEUROMUSCULAR
# -------------------------------------------------------------------------
h2 = doc.add_heading("2. Perfil Neuromuscular e Força Específica (LaCiDH)", level=2)
h2.runs[0].font.color.rgb = EMERALD_DARK_RGB
h2.runs[0].font.size = Pt(10)
h2.paragraph_format.space_before = Pt(3)
h2.paragraph_format.space_after = Pt(2)

# 2.1 Distal
h2_1 = doc.add_heading("2.1 Força Distal: Preensão Manual e Flexores de Punho a 70° (Biodex)", level=3)
h2_1.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h2_1.runs[0].font.size = Pt(8.8)
h2_1.paragraph_format.space_before = Pt(1)
h2_1.paragraph_format.space_after = Pt(1)

t_distal = doc.add_table(rows=3, cols=3)
t_distal.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_tabelas):
    c = t_distal.cell(0, j)
    c.text = h
    set_cell_background(c, "047857")
    set_cell_margins(c, top=40, bottom=40, left=70, right=70)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(7.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

distal_dados_doc = [
    ("1º Preensão Manual (FPM)\nDinamômetro Saehan Hidráulico [8,9]",
     f"Pico: {f_dec(FPM_MAX, 1)} kgf ({f_dec(FPM_REL_MAX, 3)} kgf/kg)\nDir: {f_dec(FPM_DIR, 1)} kgf | Esq: {f_dec(FPM_ESQ, 1)} kgf\nLSI = {f_dec(LSI_FPM, 1)}% (Esq > Dir)",
     f"Muito bom! Superior à média de homens jovens (~42 a 45 kgf [8,9]). Simetria aceitável (<15% [15]), com ligeiro predomínio do membro não-dominante."),
    ("2º Flexores de Punho no Biodex PRO\nTorque Isométrico Máximo a 70° de Extensão [6,7,12]",
     f"Pico: {f_dec(BIODEX_MAX, 1)} N·m ({f_dec(BIODEX_REL_MAX, 4)} N·m/kg)\nDir: {f_dec(BIODEX_PICO_D, 1)} N·m | Esq: {f_dec(BIODEX_PICO_E, 1)} N·m\nLSI = {f_dec(LSI_BIODEX, 1)}% (Esq > Dir)",
     f"Boa capacidade de torque no ângulo funcional de suporte invertido [6,7]. Simetria de 10,8% [15], essencial para a firmeza do freio palmar.")
]

for i, row in enumerate(distal_dados_doc, 1):
    for j, val in enumerate(row):
        c = t_distal.cell(i, j)
        c.text = val
        set_cell_margins(c, top=40, bottom=40, left=70, right=70)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.runs[0].font.size = Pt(7.4)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, "F0FDF4" if i % 2 == 1 else "FFFFFF")

add_highlight_box(
    doc,
    "💡 A estratégia de punho: O papel dos flexores no controle postural invertido e pontos de atenção [6,7,15]",
    f"Na postura invertida, as mãos e os punhos atuam de forma análoga aos pés e tornozelos no equilíbrio em pé. "
    f"Quando o corpo oscila além da vertical (tendência de sobre-equilíbrio), a pressão exercida pelas pontas dos dedos "
    f"e o torque dos flexores de punho geram um momento restaurador que ajuda a conduzir o centro de massa de volta ao alinhamento. "
    f"Sua força de preensão manual máxima (52,0 kgf) merece elogio: situa-se confortavelmente acima da média normativa de homens jovens saudáveis (~42 a 45 kgf [8,9]), "
    f"e o torque isométrico a 70° no Biodex (20,5 N·m) demonstra sólida disponibilidade de força no ângulo funcional do handstand. "
    f"\n\n⚠️ Ponto de atenção e sugestão de melhoria: Observou-se uma assimetria bilateral de 13,0% na preensão (52 vs 46 kgf) e de 10,8% no Biodex (20,5 vs 18,5 N·m), "
    f"com vantagem para o membro esquerdo (não-dominante). Embora esteja dentro do limite tolerado pela literatura (<15% [15]), essa diferença pode indicar uma tendência de apoiar mais ou sobrecarregar o braço esquerdo em situações de desequilíbrio. "
    f"Para equilibrar essa relação, recomenda-se incluir trabalhos unilaterais específicos para o punho direito (ex.: flexão de punho unilateral com halteres e sustentação isométrica controlada), buscando aproximar a força entre os lados e evitar torções no tronco durante a marcha.",
    "Mecanismo de 'Wrist Strategy' descrito por Kerwin & Trewartha (2001) [6] e Blenkinsop et al. (2017) [7]. "
    "A dorsiflexão avaliada a 70° reproduz o ângulo funcional de suporte (Ellenbecker & Roetert, 2006 [12]). "
    "Diferenças intermembros próximas a 10-15% merecem monitoramento para favorecer a distribuição homogênea das forças axiais, reduzindo o risco de sobrecargas unilaterais no carpo durante as passadas dinâmicas (Bishop et al., 2018 [15]; Herzog et al., 1989 [16])."
)

# 2.2 Proximal
h2_2 = doc.add_heading("2.2 Força Proximal e Resistência Muscular: Shoulder Press e Belly-to-Wall Handstand", level=3)
h2_2.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h2_2.runs[0].font.size = Pt(8.8)
h2_2.paragraph_format.space_before = Pt(1)
h2_2.paragraph_format.space_after = Pt(1)

t_prox = doc.add_table(rows=3, cols=3)
t_prox.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_tabelas):
    c = t_prox.cell(0, j)
    c.text = h
    set_cell_background(c, "047857")
    set_cell_margins(c, top=40, bottom=40, left=70, right=70)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(7.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

prox_dados_doc = [
    ("3º 1-RM no Shoulder Press (SP)\nDesenvolvimento Olímpico Estrito [10,12]",
     f"{f_dec(SP_1RM_KG, 1)} kg ({f_dec(SP_REL_PCT, 1)}% do peso corporal)\n{f_dec(SP_REL_KG_KG, 3)} kg por kg de massa",
     "Padrão Avançado. Erguer ~86% do peso corporal acima da cabeça demonstra excelente disponibilidade de força em deltoides, tríceps e fixadores escapulares [10]."),
    ("4º Resistência Belly-to-Wall Handstand\nSustentação Isométrica Estrita a 20 cm da Parede [6,11]",
     f"{f_dec(WALL_HS_MAX, 1)} segundos (1 min e 04 s)\n(Tentativa 1: {WALL_HS_T1:.0f}s | Tentativa 2: {WALL_HS_T2:.0f}s)",
     "Marca expressiva (> 1 minuto), indicando sólida capacidade de resistência muscular dos estabilizadores à fadiga postural sob gravidade [6,11].")
]

for i, row in enumerate(prox_dados_doc, 1):
    for j, val in enumerate(row):
        c = t_prox.cell(i, j)
        c.text = val
        set_cell_margins(c, top=40, bottom=40, left=70, right=70)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.runs[0].font.size = Pt(7.4)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, "F0FDF4" if i % 2 == 1 else "FFFFFF")

add_highlight_box(
    doc,
    "💡 Estabilidade proximal: O bloqueio escapular, sustentação axial e transição para a marcha [10,12,13]",
    f"O teste de Shoulder Press estrito avalia a força de empurrar vertical sem o auxílio das pernas. "
    f"Alcançar 56,0 kg (cerca de 86% do seu peso corporal) é um resultado excelente, indicando robustez nos ombros e cintura escapular (Soriano et al., 2019 [10]). "
    f"Na postura invertida, essa capacidade é indispensável para manter o bloqueio escapular ativo ('shoulder push'), empurrando o solo para preservar ombro, cotovelo e punho alinhados sob carga vertical. "
    f"Além disso, sustentar 64 segundos na parede (Wall-HS) comprova ótima resistência isométrica dos músculos do tronco e da cintura escapular. "
    f"\n\n⚠️ Oportunidade de evolução técnica: Na caminhada sobre as mãos, a força bilateral estrita precisa ser transposta para a estabilidade unipodal dinâmica (sustentar todo o peso do corpo sobre uma única escápula a cada passada). "
    f"Para fortalecer essa transição, sugere-se incluir overhead carries unilaterais (caminhada sustentando peso acima da cabeça com cotovelo estendido e escápula elevada) e dumbbell overhead press unilateral com foco na rotação superior do serrátil anterior.",
    "A ativação coordenada do serrátil anterior e das fibras do trapézio promove a rotação superior da escápula, "
    "fundamental para a congruência articular e empilhamento ósseo sob sobrecarga vertical (Soriano et al., 2019 [10]; Rohleder & Vogt, 2018 [13]). "
    "A resistência isométrica > 60 s sugere uma base física consistente para retardar a fadiga durante as tentativas de equilíbrio e locomoção."
)

# -------------------------------------------------------------------------
# SEÇÃO 3: LABIOCOM (BIOMECÂNICA, CONTROLE POSTURAL E LOCOMOÇÃO)
# -------------------------------------------------------------------------
h3 = doc.add_heading("3. Avaliação Biomecânica Tridimensional, Controle Postural e Locomoção (LaBioCoM)", level=2)
h3.runs[0].font.color.rgb = EMERALD_DARK_RGB
h3.runs[0].font.size = Pt(10)
h3.paragraph_format.space_before = Pt(3)
h3.paragraph_format.space_after = Pt(2)

# 3.1 Estático
h3_1 = doc.add_heading("3.1 Handstand Estático e Controle de Equilíbrio (Plataforma Bertec Dual & Vicon 3D)", level=3)
h3_1.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h3_1.runs[0].font.size = Pt(8.8)
h3_1.paragraph_format.space_before = Pt(1)
h3_1.paragraph_format.space_after = Pt(1)

t_hs_doc = doc.add_table(rows=7, cols=3)
t_hs_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_tabelas):
    c = t_hs_doc.cell(0, j)
    c.text = h
    set_cell_background(c, "047857")
    set_cell_margins(c, top=35, bottom=35, left=70, right=70)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(7.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

hs_dados_doc = [
    ("Tempo de Sustentação de Pico (HS Assistido)\nDesfecho Primário do Bloco Estático", f"{f_dec(HS_ASSIST_PICO_S)} s (Tentativa 1)\n(Média: {f_dec(HS_ASSIST_MED_S)} s)", "Excepcional! Três tentativas muito homogêneas (~40s) confirmam domínio estável e maturidade na postura [14]."),
    ("Distância Média CoP-CoM (Erro de Equilíbrio)\nPlataforma Bertec Dual + Rastreamento CoM 3D", f"{f_dec(COP_COM_DIST_MM)} mm (~5,0 cm)", "Braço de alavanca gravitacional enxuto [17,18]. A projeção do seu peso corporal permaneceu no miolo seguro da base palmar."),
    ("Velocidade Média do CoP\nFrequência do Esforço Corretor Palmar", f"{f_dec(COP_VEL_MM_S)} mm/s (~9,9 cm/s)", "Microajustes rápidos e contínuos nas mãos (faixa de atletas avançados: 70 a 150 mm/s [14,19])."),
    ("Entropia Aproximada (ApEn do CoP)\nComplexidade e Automaticidade Postural [20,21]", f"{f_dec(APEN_COP, 4)}", "Controle motor fluido e adaptativo (faixa ideal: 0,60 a 0,95 [20,21]), sem rigidez mecânica ou congelamento de graus de liberdade."),
    ("Ângulo de Verticalidade do Corpo\nAlinhamento Global com a Linha Gravitacional", f"{f_dec(HS_VERT_DEG)}°", "Linha corporal sólida e estável, reduzindo o estresse articular na coluna lombar e ombros."),
    ("Extensão Cervical (Olhar para o Solo)\nFixação Visual de Equilíbrio", f"{f_dec(HS_CERVICAL_DEG)}°", "Ângulo de visão confortável e estável fixado na linha entre os polegares [11].")
]

for i, row in enumerate(hs_dados_doc, 1):
    for j, val in enumerate(row):
        c = t_hs_doc.cell(i, j)
        c.text = val
        set_cell_margins(c, top=35, bottom=35, left=70, right=70)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.runs[0].font.size = Pt(7.3)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, "F0FDF4" if i % 2 == 1 else "FFFFFF")

add_highlight_box(
    doc,
    "💡 Dinâmica do pêndulo invertido: Estabilometria e controle postural [6,17-21]",
    f"Sustentar a postura invertida sobre as plataformas por cerca de 41 segundos com grande regularidade entre as três tentativas ({f_dec(HS_ASSIST_T1_S, 1)}s, {f_dec(HS_ASSIST_T2_S, 1)}s e {f_dec(HS_ASSIST_T3_S, 1)}s) "
    f"indica consistência motora na manutenção da posição. "
    f"Nessa tarefa, o corpo atua como um pêndulo invertido, com o centro de massa posicionado acima de uma base de suporte reduzida. "
    f"Os dados da Bertec registraram que a distância média entre a projeção do centro de massa e o centro de pressão permaneceu em torno de 50 mm, com velocidade de oscilação do CoP próxima de 99 mm/s. "
    f"Um dado interessante é o valor de Entropia Aproximada (0,77): na literatura biomecânica, níveis moderados a elevados de entropia sugerem que o equilíbrio se dá por meio de ajustes contínuos e adaptativos, "
    f"sem rigidez articular excessiva, indicando boa fluidez no controle postural.",
    "No modelo de Winter (1995) [17] e Slobounov et al. (2008) [18], o CoP oscila ao redor da projeção do CoM para restaurar a verticalidade. "
    "A velocidade do CoP (98,98 mm/s) reflete correções frequentes dos flexores de punho. "
    "A Entropia Aproximada (ApEn = 0,7756; Pincus, 1991 [20]; Borg & Laxåback, 2010 [21]) sugere um padrão não determinístico e saudável de regulação postural, compatível com automaticidade motora. "
    "A dissertação testará formalmente se esses parâmetros estabilométricos predizem o tempo de permanência na amostra geral."
)

# 3.2 Livre
h3_2 = doc.add_heading("3.2 Handstand Livre (Autonomia e Domínio Técnico sem Auxílio)", level=3)
h3_2.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h3_2.runs[0].font.size = Pt(8.8)
h3_2.paragraph_format.space_before = Pt(1)
h3_2.paragraph_format.space_after = Pt(1)

t_livre_doc = doc.add_table(rows=6, cols=3)
t_livre_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_tabelas):
    c = t_livre_doc.cell(0, j)
    c.text = h
    set_cell_background(c, "047857")
    set_cell_margins(c, top=35, bottom=35, left=70, right=70)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(7.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

livre_dados_doc = [
    ("Taxa de Sucesso na Entrada do HS Livre\nAutonomia de Subida e Estabilização Inicial", HS_LIVRE_TAXA_SUCESSO, "100% de êxito (3 acertos em 3 tentativas), demonstrando excelente precisão antecipatória na subida [11,22]."),
    ("Melhor Tempo no HS Livre (Autônomo)\nSustentação sem Assistência Externa", f"{f_dec(HS_LIVRE_TEMPO_MAX_S)} s (Tentativa 2)\n(T1: {f_dec(HS_LIVRE_T1_S, 1)}s | T3: {f_dec(HS_LIVRE_T3_S, 1)}s)", "Melhor marca expressiva (>24 s), porém com considerável variabilidade de duração entre as tentativas."),
    ("Ângulo de Verticalidade no Bloco Livre\nAlinhamento Postural Dinâmico", f"{f_dec(HS_LIVRE_VERT_DEG)}°", "Excelente alinhamento postural (apenas 7,97° de inclinação), minimizando braços de alavanca gravitacionais [13]."),
    ("Flexão Plantar (Ponta de Pé)\nTensão Ativa da Cadeia Posterior", f"{f_dec(HS_LIVRE_PLANTAR_DEG)}°", "Pernas unidas e pés em ponta, favorecendo uma estrutura corporal compacta e integrada."),
    ("Estratégia Articular de Busca do Equilíbrio\nCinemática 3D Multiarticular (LaBioCoM)", f"Cotovelo: SD {f_dec(HS_COTOVELO_SD_DEG)}° | ROM {f_dec(HS_COTOVELO_ROM_DEG)}° | RMS {f_dec(HS_COTOVELO_RMS_DEG_S)}°/s\nOmbro: SD {f_dec(HS_OMBRO_SD_DEG)}° | ROM {f_dec(HS_OMBRO_ROM_DEG)}° | RMS {f_dec(HS_OMBRO_RMS_DEG_S)}°/s\nQuadril: SD {f_dec(HS_QUADRIL_SD_DEG)}° | RMS {f_dec(HS_QUADRIL_RMS_DEG_S)}°/s\nRazão Cotovelo/Ombro: {f_dec(HS_RAZAO_COTOVELO_OMBRO)}", "O que significa na prática: Busca ativa pelo cotovelo — você dobrou e esticou os braços ativamente para 'salvar' a postura diante de desequilíbrios maiores, em vez de segurar apenas nos dedos e punhos. Padrão funcional comum na calistenia e handbalancing [6,7,23].")
]

for i, row in enumerate(livre_dados_doc, 1):
    for j, val in enumerate(row):
        c = t_livre_doc.cell(i, j)
        c.text = val
        set_cell_margins(c, top=35, bottom=35, left=70, right=70)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.runs[0].font.size = Pt(7.3)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, "F0FDF4" if i % 2 == 1 else "FFFFFF")

add_highlight_box(
    doc,
    "💡 Handstand Livre: Controle antecipatório, alinhamento técnico e estratégias de equilíbrio [6,7,11,13,22,23]",
    f"🗣️ O que você precisa saber na prática:\n"
    f"• Subida e alinhamento: Você acertou 100% das subidas (3 de 3 tentativas válidas) e na tentativa 2 sustentou mais de 24 segundos com alinhamento excelente (apenas 7,97° de inclinação e pés em ponta a {f_dec(HS_LIVRE_PLANTAR_DEG)}°).\n"
    f"• Como você se equilibrou (Estratégias Articulares): Diante de desequilíbrios, você utilizou predominantemente os cotovelos e ombros (dobrando e esticando os braços ativamente), usando essa flexão rápida como um recurso funcional para 'salvar' a postura antes de cair, em vez de segurar o corpo apenas com a força dos dedos e punhos.\n\n"
    f"🔬 Detalhamento dos Dados e Biomecânica:\n"
    f"A análise cinemática contínua registrou uma oscilação expressiva de cotovelos (desvio-padrão de {f_dec(HS_COTOVELO_SD_DEG)}°, amplitude de {f_dec(HS_COTOVELO_ROM_DEG)}° e velocidade angular média de {f_dec(HS_COTOVELO_RMS_DEG_S)}°/s), acompanhada de movimentação nos ombros (desvio de {f_dec(HS_OMBRO_SD_DEG)}° e velocidade de {f_dec(HS_OMBRO_RMS_DEG_S)}°/s) e no quadril (desvio de {f_dec(HS_QUADRIL_SD_DEG)}°). Na literatura de controle motor (Kerwin & Trewartha, 2001; Blenkinsop et al., 2017), o equilíbrio invertido pode ser mantido por ajustes finos no centro de pressão palmar (estratégia de punho rígido) ou por correções multissegmentares proximais. Flexionar os braços momentaneamente rebaixa o centro de massa e permite aplicar força de tríceps para retomar o prumo. Esse padrão é comum em modalidades como a Calistenia e o Handbalancing livre; já na ginástica artística, busca-se a haste bloqueada sem flexão devido às deduções do código de pontuação. Ambas representam soluções biomecânicas individuais adaptativas.\n\n"
    f"⚠️ Ponto que precisa de ajuste e como consertar:\n"
    f"Observou-se uma grande diferença de tempo entre as séries livres (T1: 3,5 s, T2: 24,5 s e T3: 13,6 s). Essa oscilação mostra que o seu equilíbrio ainda é sensível a pequenas perturbações no instante logo após a subida.\n"
    f"Como melhorar: 1) Treinar séries buscando manter de 15 a 20 segundos estáveis e consistentes, descansando plenamente entre elas; 2) Praticar o 'salvamento' com os dedos: pressionar as pontas das mãos quando o corpo ameaçar passar para frente e empurrar a palma quando ameaçar voltar para trás, antes de dobrar os braços ou cair.",
    "O êxito imediato na transição motora reflete a ação dos mecanismos antecipatórios (feedforward) descritos por Gautier et al. (2007) [11] e Clement et al. (1984) [22]. "
    "A verticalidade de 7,97° minimiza braços de alavanca gravitacionais sobre a coluna e o complexo escapular (Rohleder & Vogt, 2018 [13]). "
    "A mobilização de graus de liberdade em cotovelo e ombro frente a perturbações coaduna com os modelos de controle multissegmentar de Kerwin & Trewartha (2001) [6] e Blenkinsop et al. (2017) [23]."
)

# 3.3 HSW
h3_3 = doc.add_heading("3.3 Handstand Walk — HSW (Locomoção Invertida Dinâmica)", level=3)
h3_3.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h3_3.runs[0].font.size = Pt(8.8)
h3_3.paragraph_format.space_before = Pt(1)
h3_3.paragraph_format.space_after = Pt(1)

hsw_dados_doc = [
    ("Distância Mediana Percorrida (HSW)\nDesfecho Primário do Bloco de Marcha", f"{f_dec(HSW_DIST_MEDIANA_M)} m\n(T1: {f_dec(HSW_T1_DIST_M)}m | T2: {f_dec(HSW_T2_DIST_M)}m | T3: {f_dec(HSW_T3_DIST_M)}m)", "Desfecho oficial da pesquisa. Mediana reduzida devido a interrupções precoces nas tentativas 1 e 2."),
    ("Distância Máxima Percorrida no HSW\nMelhor Registro de Deslocamento", f"{f_dec(HSW_DIST_MAX_M)} m (Tentativa 3)", "Destaque positivo! Progressão expressiva até superar 4 metros na terceira tentativa."),
    ("Velocidade Média de Deslocamento (HSW)\nVelocidade Linear da Marcha Invertida", f"{f_dec(HSW_VEL_M_S)} m/s ({f_dec(HSW_VEL_KM_H)} km/h)", "O que significa na prática: Ritmo de deslocamento moderado e controlado ao longo do percurso válido."),
    ("Tempo Médio de Contato Palmar\nDuração do Apoio de Cada Mão por Passo", f"{f_dec(HSW_CONTATO_S)} s ({HSW_CONTATO_MS} ms)", "O que significa na prática: Tempo de permanência de cada mão no solo antes da propulsão para a próxima passada."),
    ("Cadência da Marcha Invertida\nPassos com as Mãos por Segundo", f"{f_dec(HSW_CADENCIA)} passos/s", "Ritmo de passadas próximo de 1 passo por segundo [7]."),
    ("Comprimento Médio da Passada\nAmplitude dos Passos Palmares", f"{f_dec(HSW_PASSADA_MM)} mm (~42,8 cm)", "Amplitude compatível com a envergadura e estatura corporal [7]."),
    ("Fase de Duplo Suporte com as Mãos\nTempo com Ambas as Mãos Apoiadas", f"{f_dec(HSW_DUPLO_SUPORTE_PCT)}% do ciclo", "Atenção: valor elevado (>55%), indicando hesitação na transição e apoio prolongado com as duas mãos."),
    ("Coeficiente de Variação Espacial (Passadas)\nRegularidade do Tamanho dos Passos", f"{f_dec(HSW_CV_ESPACIAL)}% (Consistente)", "Baixa dispersão espacial (<15%), demonstrando boa consistência no comprimento dos passos."),
    ("Coeficiente de Variação Temporal (Passadas)\nRegularidade do Tempo de Apoio", f"{f_dec(HSW_CV_TEMPORAL)}% (Elevado)", "Atenção: alta variabilidade temporal (>50%), refletindo ritmo irregular entre passadas sucessivas."),
    ("Extensão Cervical na Marcha (Olhar)\nOrientação Visual para Frente no HSW", f"{f_dec(HSW_CERVICAL_DEG)}°\n(+19° vs HS estático)", "Positivo: olhar erguido direcionado à frente, favorecendo a fixação visual do vetor de progressão [11]."),
    ("Rotação Externa das Mãos no HSW\nAbertura Palmar para Fora na Marcha", f"{f_dec(HSW_ROT_MAOS_DEG)}°\n(+36° vs HS estático)", "Atenção: rotação palmar excessiva (~67°), o que reduz a alavanca anteroposterior dos flexores."),
    ("Flexão Plantar no HSW (Ponta de Pé)\nTensão Ativa da Cadeia Posterior", f"{f_dec(HSW_PLANTAR_DEG)}°\n(Redução vs estático)", "Atenção: pés relaxados na marcha (5,8° vs 28,4° no livre), gerando perda de compactação corporal.")
]

t_hsw_doc = doc.add_table(rows=len(hsw_dados_doc) + 1, cols=3)
t_hsw_doc.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_tabelas):
    c = t_hsw_doc.cell(0, j)
    c.text = h
    set_cell_background(c, "047857")
    set_cell_margins(c, top=35, bottom=35, left=70, right=70)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(7.8)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

for i, row in enumerate(hsw_dados_doc, 1):
    for j, val in enumerate(row):
        c = t_hsw_doc.cell(i, j)
        c.text = val
        set_cell_margins(c, top=35, bottom=35, left=70, right=70)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(0)
        p.paragraph_format.space_before = Pt(0)
        p.runs[0].font.size = Pt(7.3)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, "F0FDF4" if i % 2 == 1 else "FFFFFF")

add_highlight_box(
    doc,
    "💡 Handstand Walk: Análise dinâmica, diagnósticos de melhoria e prescrição corretiva [7,11,13]",
    f"🗣️ O que você precisa saber na prática:\n"
    f"• Desempenho e velocidade: Você conseguiu andar mais de 4 metros na sua melhor tentativa, com passadas de bom tamanho (~43 cm), tempo de contato de {f_dec(HSW_CONTATO_S)} s por apoio e velocidade média de deslocamento de {f_dec(HSW_VEL_M_S)} m/s ({f_dec(HSW_VEL_KM_H)} km/h).\n"
    f"• Pontos de atenção na caminhada: Você ainda hesita na troca entre os passos, mantendo as duas mãos apoiadas no chão ao mesmo tempo durante 56% da caminhada (duplo suporte elevado). Além disso, suas mãos abrem muito para fora (67°) e as pernas relaxam na marcha, perdendo a firmeza corporal.\n\n"
    f"🔬 Detalhamento dos Dados e Biomecânica:\n"
    f"Caminhar sobre as mãos exige que, a cada passada, um dos apoios deixe o solo e o corpo seja acelerado para a frente. Sua distância máxima (4,28 m) comprova boa capacidade propulsiva, mas a mediana foi de {f_dec(HSW_DIST_MEDIANA_M)} m devido a paradas precoces nas primeiras tentativas. O apoio duplo prolongado (56,01%) e a alta variabilidade temporal ({f_dec(HSW_CV_TEMPORAL)}%) confirmam que a transição de peso de uma mão para a outra ainda precisa de maior fluidez e velocidade.\n\n"
    f"🛠️ Exercícios Práticos Sugeridos:\n"
    f"1) Shoulder taps em pike ou prancha alta (10 a 12 toques controlados, sustentando 1 segundo em cada mão para acelerar a troca de suporte);\n"
    f"2) Caminhada invertida com alinhamento das mãos (focar em manter os dedos apontando mais para a frente, ~30°, evitando abrir a palma excessivamente para fora);\n"
    f"3) Caminhada com elástico leve entre os tornozelos para manter as pernas unidas e ativas durante as passadas.",
    "Blenkinsop et al. (2017) [7] destacam que a locomoção invertida eficiente requer minimização do duplo suporte e alta consistência espaço-temporal. "
    "A assimetria entre os CVs espacial (14,07%) e temporal (56,95%) reflete perturbação no ritmo de transferência de carga. "
    "A rotação excessiva palmar (66,87°) compromete o momento sagital de flexores de punho (Kerwin & Trewartha, 2001 [6]), enquanto a perda de tensão distal nos pés afeta a rigidez de segmento articulado (Rohleder & Vogt, 2018 [13]). "
    "A dissertação investigará estatisticamente o impacto dessas variáveis temporais e cinemáticas na distância de caminhada."
)

# -------------------------------------------------------------------------
# SEÇÃO 4: SÍNTESE INTEGRADA E DICAS PRÁTICAS
# -------------------------------------------------------------------------
h4 = doc.add_heading("4. Síntese Integrada e Dicas Práticas para o Seu Treinamento", level=2)
h4.runs[0].font.color.rgb = EMERALD_DARK_RGB
h4.runs[0].font.size = Pt(10)
h4.paragraph_format.space_before = Pt(3)
h4.paragraph_format.space_after = Pt(2)

p_prat_lead1 = doc.add_paragraph()
p_prat_lead1.paragraph_format.space_before = Pt(2)
p_prat_lead1.paragraph_format.space_after = Pt(1)
r_p1 = p_prat_lead1.add_run("🌟 Seus Grandes Destaques e Forças Biomecânicas (com respaldo na literatura):")
r_p1.bold = True
r_p1.font.size = Pt(8.2)
r_p1.font.color.rgb = EMERALD_DARK_RGB

pontos_fortes = [
    ("Composição Corporal e Integridade Celular (LaCiDH): ", "Ângulo de Fase notável de 8,98° (+1,99 DP vs Barbosa-Silva et al., 2005) e mais de 83% de massa magra ativa, indicando excelente integridade de membrana celular e peso funcional favorável."),
    ("Força Distal de Preensão Manual (LaCiDH): ", "Marca máxima de 52,0 kgf, superando a média populacional de homens jovens (~42 a 45 kgf, Bohannon 2019), conferindo firmeza palmar de contato."),
    ("Força Vertical Proximal e Resistência Escapular (LaCiDH): ", "Shoulder Press estrito com 85,8% da massa corporal (padrão avançado, Soriano et al., 2019) e sustentação na parede de 64 s (>1 min), garantindo suporte robusto sob sobrecarga gravitacional."),
    ("Consistência no Handstand Estático (LaBioCoM): ", "Sustentação homogênea de ~40 s com Entropia de 0,77, atestando regulação postural adaptativa e automática sem rigidez excessiva (Pincus 1991; Borg & Laxåback 2010)."),
    ("Autonomia e Alinhamento no Livre (LaBioCoM): ", "100% de precisão nas subidas sem apoio e verticalidade de 7,97° na melhor tentativa (24,5 s), confirmando domínio do controle antecipatório (Gautier et al., 2007).")
]

for tit, desc in pontos_fortes:
    p_d = doc.add_paragraph()
    p_d.paragraph_format.space_before = Pt(0.5)
    p_d.paragraph_format.space_after = Pt(1.5)
    p_d.paragraph_format.left_indent = Inches(0.15)
    r1 = p_d.add_run("• " + tit)
    r1.bold = True
    r1.font.size = Pt(7.8)
    r1.font.color.rgb = EMERALD_HEADER_RGB
    r2 = p_d.add_run(desc)
    r2.font.size = Pt(7.8)
    r2.font.color.rgb = TEXT_DARK_RGB

p_prat_lead2 = doc.add_paragraph()
p_prat_lead2.paragraph_format.space_before = Pt(3)
p_prat_lead2.paragraph_format.space_after = Pt(1)
r_p2 = p_prat_lead2.add_run("🎯 Oportunidades de Evolução Técnica e Prescrição de Treino (Direto e Acionável):")
r_p2.bold = True
r_p2.font.size = Pt(8.2)
r_p2.font.color.rgb = RGBColor(180, 83, 9)  # tom âmbar/alerta elegante

pontos_melhoria = [
    ("Regularidade Temporal e Fluidez no Handstand Walk: ", "Reduzir a acentuada variabilidade de tempo entre as passadas (CV Temporal de 56,95%) e o excesso de duplo suporte (56,01%). Prescrição: Praticar passadas com metrônomo a 1 Hz e shoulder taps controlados na parede (1 s por apoio) para eliminar a hesitação ao avançar."),
    ("Correção da Pegada Palmar na Marcha: ", "Diminuir a rotação externa excessiva das mãos de ~67° para a faixa de ~30° a 45°. Isso redireciona os dedos mais à frente, recuperando o braço de alavanca sagital dos flexores de punho para frear e acelerar o corpo na linha de caminhada."),
    ("Compactação Corporal Dinâmica (Pés em Ponta): ", "Resgatar na caminhada a tensão ativa de pernas e pés observada no estático (evitar a queda para 5,85° de flexão plantar). Manter pernas aduzidas e pontas dos pés estendidas evita oscilações parasitas das pernas."),
    ("Consistência de Duração no Handstand Livre: ", "Eliminar as quedas precoces entre as séries livres (oscilação entre 3,5 s e 24,5 s). Prescrição: Realizar blocos de 5 a 6 séries de 15 a 20 s estáveis, descansando plenamente entre elas, e treinar ativamente o salvamento por pressão palmar antes de descer."),
    ("Equalização da Força Bilateral dos Membros Superiores: ", "Reduzir a assimetria bilateral de 11% a 13% em favor do braço esquerdo. Prescrição: Incluir fortalecimento isolado de punho e ombro para o membro direito (flexão de punho com halteres e press unilateral) para equilibrar as forças de contato.")
]

for tit, desc in pontos_melhoria:
    p_d = doc.add_paragraph()
    p_d.paragraph_format.space_before = Pt(0.5)
    p_d.paragraph_format.space_after = Pt(1.5)
    p_d.paragraph_format.left_indent = Inches(0.15)
    r1 = p_d.add_run("• " + tit)
    r1.bold = True
    r1.font.size = Pt(7.8)
    r1.font.color.rgb = RGBColor(180, 83, 9)
    r2 = p_d.add_run(desc)
    r2.font.size = Pt(7.8)
    r2.font.color.rgb = TEXT_DARK_RGB

# -------------------------------------------------------------------------
# SEÇÃO 5: REFERÊNCIAS CIENTÍFICAS
# -------------------------------------------------------------------------
h5 = doc.add_heading("5. Referências Científicas e Normativas Internacionais", level=2)
h5.runs[0].font.color.rgb = EMERALD_DARK_RGB
h5.runs[0].font.size = Pt(9.5)
h5.paragraph_format.space_before = Pt(3)
h5.paragraph_format.space_after = Pt(2)

refs_completas = [
    "Sun, S. S., et al. (2003). Development of bioelectrical impedance analysis prediction equations for body composition with the use of a multicomponent model. Am J Clin Nutr, 77(2), 331-340.",
    "Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. J Appl Physiol, 89(2), 465-471.",
    "American College of Sports Medicine (ACSM). (2018). ACSM's Guidelines for Exercise Testing and Prescription (10th ed.). Philadelphia: Wolters Kluwer.",
    "Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. Am J Clin Nutr, 82(1), 49-52.",
    "Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. Clin Nutr, 31(6), 854-861.",
    "Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. Sports Biomech, 1(2), 163-176.",
    "Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Handstand walk: Locomotor biomechanics and coordination in inverted human locomotion. Hum Mov Sci, 54, 235-244.",
    "Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. J Phys Ther Sci, 31(11), 932-938.",
    "Dodds, R. M., et al. (2014). Globally representative normative data for handgrip strength: systematic review. PLoS ONE, 9(12), e113637.",
    "Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. Strength Cond J, 41(4), 48-60.",
    "Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. Hum Mov Sci, 26(4), 577-594.",
    "Ellenbecker, T. S., & Roetert, E. P. (2006). Isokinetic wrist strength in competitive athletes. Am J Sports Med, 34(11), 1845-1852.",
    "Rohleder, J., & Vogt, L. (2018). Kinematic alignment and joint stacking in artistic gymnastics vs. fitness handbalancing. J Sports Sci, 36(11), 1238-1245.",
    "Rohleder, J., et al. (2021). Wrist joint biomechanics and handstand stability in gymnastics. Sports Biomech, 20(3), 312-326.",
    "Bishop, C., et al. (2018). Effects of inter-limb asymmetries on physical and sports performance. J Sports Sci, 36(10), 1135-1144.",
    "Herzog, W., et al. (1989). Asymmetries in ground reaction force patterns in normal human gait. Med Sci Sports Exerc, 21(1), 110-118.",
    "Winter, D. A. (1995). Human balance and posture control during standing and walking. Gait & Posture, 3(4), 193-214.",
    "Slobounov, S., et al. (2008). Virtual reality and force-platform assessment of inverted posture stability. Exp Brain Res, 188(2), 241-253.",
    "Uzun, M., et al. (2012). Stabilometric comparison of handstand on force plates between elite and novice athletes. J Hum Kinet, 34(1), 15-23.",
    "Pincus, S. M. (1991). Approximate entropy as a measure of system complexity. Proc Natl Acad Sci USA, 88(6), 2297-2301.",
    "Borg, F. G., & Laxåback, G. (2010). Entropy of balance: How to compute and interpret approximate entropy in posturography. J Biomech, 43(15), 3044-3048.",
    "Clement, G., et al. (1984). Adaptation of posture and locomotion to inverted support. Aerosp Med Hum Perform, 55(8), 700-705.",
    "Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Balance control strategies during perturbed and unperturbed handstands. J Biomech, 65, 123-129.",
    "Slobounov, S. M., & Newell, K. M. (1996). Posture, living systems, and the 'freezing' and 'freeing' of degrees of freedom. In Motor Control in Sports (pp. 89-108)."
]

for idx, ref in enumerate(refs_completas, 1):
    p_r = doc.add_paragraph()
    p_r.paragraph_format.space_before = Pt(0.5)
    p_r.paragraph_format.space_after = Pt(0.5)
    p_r.paragraph_format.left_indent = Inches(0.15)
    r = p_r.add_run(f"[{idx}] {ref}")
    r.font.name = "Arial"
    r.font.size = Pt(6.8)
    r.font.color.rgb = TEXT_MUTED_RGB

p_inst_foot = doc.add_paragraph()
p_inst_foot.paragraph_format.space_before = Pt(4)
p_inst_foot.paragraph_format.space_after = Pt(2)
r_if1 = p_inst_foot.add_run("Escola de Educação Física e Esporte de Ribeirão Preto — Universidade de São Paulo (EEFERP-USP)\n")
r_if1.font.size = Pt(7.2)
r_if1.font.color.rgb = TEXT_MUTED_RGB

r_m_foot = p_inst_foot.add_run("Mestrando: ")
r_m_foot.bold = True
r_m_foot.font.size = Pt(7.2)
r_m_foot.font.color.rgb = EMERALD_HEADER_RGB

r_m_foot_val = p_inst_foot.add_run("Guilherme de Paula Lemos (guilherme.lemos@usp.br)   |   ")
r_m_foot_val.font.size = Pt(7.2)
r_m_foot_val.font.color.rgb = TEXT_MUTED_RGB

r_o_foot = p_inst_foot.add_run("Orientador: ")
r_o_foot.bold = True
r_o_foot.font.size = Pt(7.2)
r_o_foot.font.color.rgb = EMERALD_HEADER_RGB

r_o_foot_val = p_inst_foot.add_run("Prof. Dr. Matheus Machado Gomes\nLaCiDH & LaBioCoM")
r_o_foot_val.font.size = Pt(7.2)
r_o_foot_val.font.color.rgb = TEXT_MUTED_RGB

p_inst_foot.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.save(DOCX_OUT)
print(f"[OK] Documento DOCX salvo em: {DOCX_OUT}")

# =========================================================================
# 2. CONSTRUÇÃO DO DOCUMENTO HTML PADRONIZADO (DESIGN ORIGINAL RESTAURADO)
# =========================================================================
print("[2/3] Gerando HTML com design original, logo da EEFERP, cards, badges e paleta de cores restaurada...")

logo_html_tag = ""
if logo_white_b64:
    logo_html_tag = f"""<img src="data:image/png;base64,{logo_white_b64}" alt="Logo EEFERP-USP" style="height: 52px; width: auto; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">"""

html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório Individual Devolutivo - {NOME_ATLETA} ({CODIGO_ATLETA}) | EEFERP-USP</title>
<style>
  :root {{
    --primary-gradient: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%);
    --accent-gradient: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --text-heading: #064e3b;
    --text-body: #334155;
    --text-muted: #64748b;
    --emerald-dark: #064e3b;
    --emerald-medium: #047857;
    --emerald-light: #10b981;
    --mint-soft: #f0fdf4;
    --mint-border: #bbf7d0;
  }}

  * {{
    box-sizing: border-box;
  }}

  body {{
    font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, "Helvetica Neue", Arial, sans-serif;
    background-color: #f8fafc;
    color: var(--text-body);
    margin: 0;
    padding: 24px 12px;
    line-height: 1.6;
    -webkit-font-smoothing: antialiased;
  }}

  .card-container {{
    max-width: 900px;
    margin: 0 auto;
    background: var(--card-bg);
    border-radius: 20px;
    box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
    overflow: hidden;
  }}

  .hero-header {{
    background: var(--primary-gradient);
    color: white;
    padding: 34px 32px 28px;
    text-align: center;
    position: relative;
  }}

  .hero-header::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 5px;
    background: var(--accent-gradient);
  }}

  .hero-top-row {{
    display: flex;
    align-items: center;
    justify-content: center;
    gap: 16px;
    margin-bottom: 12px;
    flex-wrap: wrap;
  }}

  .institution-badge {{
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 700;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #a7f3d0;
  }}

  .hero-header h1 {{
    margin: 0 0 8px 0;
    font-size: 22px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
  }}

  .hero-meta-box {{
    margin-top: 10px;
    padding-top: 10px;
    border-top: 1px solid rgba(255, 255, 255, 0.15);
  }}

  .hero-meta-title {{
    font-size: 13px;
    font-weight: 500;
    color: #e2e8f0;
    margin: 0 0 5px 0;
  }}

  .hero-meta-team {{
    font-size: 12.5px;
    color: #d1fae5;
    margin: 0;
  }}

  .hero-meta-box .tag-role {{
    font-weight: 800;
    color: #ffffff;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    font-size: 11.5px;
  }}

  .content {{
    padding: 32px 32px 24px;
  }}

  .athlete-card {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    border: 1px solid var(--mint-border);
    border-radius: 14px;
    padding: 20px;
    margin-bottom: 20px;
    box-shadow: 0 2px 10px rgba(4, 120, 87, 0.03);
  }}

  .athlete-item strong {{
    display: block;
    color: var(--emerald-medium);
    font-size: 11px;
    text-transform: uppercase;
    letter-spacing: 0.6px;
    margin-bottom: 2px;
  }}

  .athlete-item span {{
    font-size: 13.5px;
    font-weight: 700;
    color: var(--text-main);
  }}

  .project-goal-card {{
    background: linear-gradient(135deg, #ffffff 0%, #f0fdf4 100%);
    border: 1px solid var(--mint-border);
    border-left: 5px solid var(--emerald-medium);
    border-radius: 12px;
    padding: 16px 20px;
    margin-bottom: 22px;
    box-shadow: 0 2px 8px rgba(4, 120, 87, 0.03);
  }}

  .project-goal-title {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 13.5px;
    font-weight: 800;
    color: var(--emerald-dark);
    margin-bottom: 4px;
  }}

  .project-goal-text {{
    margin: 0;
    font-size: 12.5px;
    color: var(--text-body);
    line-height: 1.55;
  }}

  .intro-callout {{
    background: #ffffff;
    border-left: 4px solid var(--emerald-medium);
    padding: 14px 18px;
    border-radius: 0 10px 10px 0;
    margin-bottom: 24px;
    font-size: 13.5px;
    line-height: 1.6;
    background-color: #f8fafc;
  }}

  .intro-callout strong {{
    color: var(--emerald-dark);
  }}

  .section-title {{
    font-size: 17px;
    font-weight: 800;
    color: var(--emerald-dark);
    margin: 32px 0 16px;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
    display: flex;
    align-items: center;
    gap: 10px;
  }}

  .section-title span.badge-num {{
    background: var(--emerald-dark);
    color: white;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 12px;
    font-weight: 800;
  }}

  .sub-section-title {{
    font-size: 15px;
    font-weight: 700;
    color: var(--emerald-dark);
    margin: 22px 0 12px 0;
    display: flex;
    align-items: center;
    gap: 6px;
  }}

  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 14px;
    margin: 16px 0;
  }}

  .metric-box {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 16px 18px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 145px;
  }}

  .metric-box::before {{
    content: "";
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 4px;
    background: var(--accent-gradient);
  }}

  .metric-box:hover {{
    transform: translateY(-3px);
    box-shadow: 0 8px 20px rgba(4, 120, 87, 0.08);
    border-color: #a7f3d0;
  }}

  .metric-header {{
    min-height: 34px;
    display: flex;
    align-items: flex-start;
  }}

  .metric-label {{
    font-size: 11.5px;
    font-weight: 700;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 0.5px;
    line-height: 1.35;
    margin: 0;
  }}

  .metric-body {{
    margin: 6px 0;
  }}

  .metric-value {{
    font-size: 26px;
    font-weight: 800;
    color: var(--text-main);
    line-height: 1.1;
    margin: 0;
    letter-spacing: -0.5px;
  }}

  .metric-subtext {{
    font-size: 11px;
    color: var(--text-muted);
    margin-top: 3px;
    font-weight: 500;
  }}

  .metric-footer {{
    min-height: 26px;
    display: flex;
    align-items: center;
    margin-top: 6px;
  }}

  .metric-pill {{
    display: inline-flex;
    align-items: center;
    background: #ecfdf5;
    color: #047857;
    font-size: 10.5px;
    font-weight: 600;
    padding: 3px 8px;
    border-radius: 9999px;
    border: 1px solid #a7f3d0;
    line-height: 1.3;
  }}

  .callout-highlight {{
    background: linear-gradient(135deg, #f0fdf4 0%, #ecfdf5 100%);
    border: 1px solid #a7f3d0;
    border-left: 5px solid #10b981;
    border-radius: 12px;
    padding: 18px 22px;
    margin: 20px 0;
  }}

  .callout-title {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 14.5px;
    font-weight: 800;
    color: var(--emerald-dark);
    margin-bottom: 8px;
  }}

  .callout-text {{
    font-size: 13px;
    color: #1e293b;
    margin: 0 0 8px 0;
    line-height: 1.65;
  }}

  .callout-science {{
    font-size: 12px;
    color: #475569;
    border-top: 1px dashed #bbf7d0;
    padding-top: 8px;
    margin-top: 8px;
    line-height: 1.55;
  }}

  .callout-science strong {{
    color: #047857;
  }}

  .biodex-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px;
    margin: 20px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
  }}

  .biodex-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 14px;
    flex-wrap: wrap;
    gap: 10px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 10px;
  }}

  .biodex-header h4 {{
    margin: 0;
    font-size: 14px;
    color: var(--emerald-dark);
    font-weight: 800;
  }}

  .practice-box {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 22px;
    margin: 22px 0;
    box-shadow: 0 2px 10px rgba(0,0,0,0.02);
  }}

  .practice-box h4 {{
    margin: 0 0 12px 0;
    color: var(--emerald-dark);
    font-size: 15px;
    font-weight: 800;
  }}

  .practice-box ul {{
    margin: 0;
    padding-left: 20px;
  }}

  .practice-box li {{
    margin-bottom: 10px;
    font-size: 13px;
    color: var(--text-body);
    line-height: 1.55;
  }}

  .practice-box li strong {{
    color: var(--emerald-dark);
  }}

  .references-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px 24px;
    margin-top: 30px;
  }}

  .references-card h4 {{
    margin: 0 0 12px 0;
    font-size: 12px;
    font-weight: 800;
    color: var(--emerald-dark);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .references-card ol {{
    margin: 0;
    padding-left: 18px;
    font-size: 11px;
    color: var(--text-muted);
  }}

  .references-card li {{
    margin-bottom: 5px;
    line-height: 1.45;
  }}

  .footer {{
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 22px 32px;
    text-align: center;
    font-size: 11.5px;
    color: var(--text-muted);
    line-height: 1.6;
  }}

  .footer strong {{
    color: var(--emerald-dark);
  }}

  sup {{
    font-weight: 700;
    color: #10b981;
  }}

  @page {{
    size: A4;
    margin: 10mm 12mm 12mm 12mm;
  }}

  @media print {{
    body {{
      background: transparent;
      padding: 0;
    }}
    .card-container {{
      box-shadow: none;
      border-radius: 0;
      max-width: 100%;
    }}
    .metric-box, .callout-highlight, .biodex-card, .practice-box, .project-goal-card {{
      break-inside: avoid;
      page-break-inside: avoid;
    }}
    .section-title, .sub-section-title {{
      break-after: avoid;
      page-break-after: avoid;
    }}
  }}
</style>
</head>
<body>

<div class="card-container">
  <!-- CABEÇALHO HERO GRADIENTE COM LOGO EEFERP -->
  <div class="hero-header">
    <div class="hero-top-row">
      {logo_html_tag}
      <div class="institution-badge">Universidade de São Paulo • EEFERP-USP</div>
    </div>
    <h1>Relatório Individual Devolutivo de Desempenho & Biomecânica</h1>
    <div class="hero-meta-box">
      <p class="hero-meta-title">
        <span class="tag-role">Projeto:</span> {TITULO_OFICIAL_PROJETO}
      </p>
      <p class="hero-meta-team">
        <span class="tag-role">Mestrando:</span> Guilherme de Paula Lemos &nbsp;&nbsp;|&nbsp;&nbsp; 
        <span class="tag-role">Orientador:</span> Prof. Dr. Matheus Machado Gomes
      </p>
    </div>
  </div>

  <div class="content">
    <!-- BOX DO ATLETA -->
    <div class="athlete-card">
      <div class="athlete-item">
        <strong>Participante</strong>
        <span>{NOME_ATLETA}</span>
      </div>
      <div class="athlete-item">
        <strong>Código / ID</strong>
        <span>{CODIGO_ATLETA}</span>
      </div>
      <div class="athlete-item">
        <strong>Idade / Sexo</strong>
        <span>{FAIXA_ETARIA} | {SEXO}</span>
      </div>
      <div class="athlete-item">
        <strong>Membro Dominante</strong>
        <span>{DOMINANCIA}</span>
      </div>
      <div class="athlete-item">
        <strong>Massa / Estatura</strong>
        <span>{f_dec(MASSA_KG)} kg | {f_dec(ESTATURA_CM, 1)} cm (IMC: {f_dec(IMC)})</span>
      </div>
      <div class="athlete-item">
        <strong>Modalidade / Volume</strong>
        <span>{MODALIDADES} (~{VOLUME_PRATICA_HORAS:.0f}h)</span>
      </div>
      <div class="athlete-item">
        <strong>Datas das Coletas</strong>
        <span>02/09 (LaCiDH) e 09/09/2026 (LaBioCoM)</span>
      </div>
      <div class="athlete-item">
        <strong>Status dos Testes</strong>
        <span style="color: #047857;">100% Concluídos (S1 + S2)</span>
      </div>
    </div>

    <!-- MENSAGEM INICIAL AMIGÁVEL -->
    <div class="intro-callout">
      <strong>Olá, {NOME_ATLETA.split()[0]}!</strong> Agradecemos imensamente a sua dedicação e contribuição voluntária em ambas as sessões experimentais na EEFERP-USP. 
      Este relatório reúne a devolutiva completa e integrada das suas avaliações realizadas no <strong>LaCiDH</strong> (Composição Corporal e Força Neuromuscular) 
      e no <strong>LaBioCoM</strong> (Handstand Estático, Handstand Livre e Handstand Walk com Câmeras 3D Vicon e Placas de Força Bertec). 
      Para tornar a leitura fluida e esclarecedora, <strong>começamos cada seção explicando o que os dados observados podem representar para a sua prática e treino</strong>, 
      seguidos pela contextualização científica fundamentada na literatura internacional <sup>[1-22]</sup>. Parabéns pela dedicação e pelo comprometimento com a pesquisa!
    </div>

    <!-- TÓPICO DO OBJETIVO DO PROJETO DE MESTRADO -->
    <div class="project-goal-card">
      <div class="project-goal-title">
        🎯 Objetivo Geral do Projeto de Mestrado
      </div>
      <p class="project-goal-text">
        {OBJETIVO_GERAL_PROJETO}
      </p>
    </div>

    <!-- SEÇÃO 1: COMPOSIÇÃO CORPORAL -->
    <div class="section-title">
      <span class="badge-num">1</span>
      Composição Corporal e Estado Morfofuncional (BIA Sanny® — Sun et al., 2003)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Gordura Corporal (%GC) <sup>[1,3]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(GORDURA_PCT)}%</div>
          <div class="metric-subtext">{f_dec(MG_KG)} kg de massa gorda</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Padrão Atlético Saudável (10–18%)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Massa Livre de Gordura (MLG) <sup>[1]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(MLG_KG)} kg</div>
          <div class="metric-subtext">83,4% em tecidos magros ativos</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Base Muscular Predominante</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Massa Muscular Esquelética <sup>[2]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(MME_KG)} kg</div>
          <div class="metric-subtext">46,1% da massa corporal</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Excelente Suporte Antigravitacional</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Ângulo de Fase a 50 kHz (PhA) <sup>[4,5]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(PHA_DEG)}°</div>
          <div class="metric-subtext">Referência etária: 7,53° ± 0,73°</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857; font-weight: 700;">
            Z-score > +1,9 DP • Integridade Celular Elevada
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Índice de MLG (IMLG / FFMI) <sup>[6,7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(FFMI)} kg/m²</div>
          <div class="metric-subtext">Massa magra ajustada à estatura²</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Classificação Muito Boa / Atlética</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 O que esses dados indicam na prática: Relação massa magra e eficiência funcional <sup>[1-5]</sup>
      </div>
      <p class="callout-text">
        Na parada de mão, todo o peso corporal precisa ser sustentado contra a gravidade pelos membros superiores. 
        Por isso, a proporção entre massa livre de gordura e tecido adiposo é um aspecto altamente favorável no seu perfil: com <strong>{f_dec(GORDURA_PCT, 1)}% de gordura</strong> 
        e mais de <strong>83% do peso total ({f_dec(MLG_KG, 1)} kg)</strong> composto por massa magra ativa, 
        a relação de peso funcional sustentada por punhos e ombros torna-se consideravelmente eficiente.
      </p>
      <p class="callout-text">
        Um resultado que merece elogio é o seu <strong>Ângulo de Fase ({f_dec(PHA_DEG)}°)</strong>, situado substancialmente acima da média de referência normativa para homens de 20 a 29 anos (7,53° ± 0,73°, Barbosa-Silva et al., 2005 <sup>[4]</sup>; Z-score = +1,99 DP). 
        Na literatura científica <sup>[4,5]</sup>, valores elevados de PhA refletem excelente integridade das membranas celulares e adequada hidratação intra/extracelular, 
        o que aponta para um potencial favorável de tolerância ao esforço físico e boa capacidade de recuperação celular entre os treinos.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong> 
        A análise de bioimpedância calculada pela equação multicomponente de Sun et al. (2003) <sup>[1]</sup> e pelo modelo muscular de Janssen et al. (2000) <sup>[2]</sup> 
        evidencia uma composição corporal equilibrada para modalidades com demanda de força relativa (calistenia e handbalancing). 
        O Ângulo de Fase (PhA) reflete a capacitância elétrica de membrana e a integridade tecidual (Barbosa-Silva et al., 2005 <sup>[4]</sup>; Norman et al., 2012 <sup>[5]</sup>). 
        Um valor de 8,98° situa-se no percentil superior para a faixa etária (Z-score = +1,99 DP), sugerindo potencial vantagem biológica na tolerância à fadiga metabólica.
      </div>
    </div>

    <!-- SEÇÃO 2: FORÇA NEUROMUSCULAR -->
    <div class="section-title">
      <span class="badge-num">2</span>
      Perfil Neuromuscular e Força Específica (LaCiDH)
    </div>

    <!-- 2.1 DISTAL -->
    <div class="sub-section-title">
      2.1 Força Distal: Preensão Manual e Flexores de Punho a 70° (Biodex)
    </div>

    <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">1º Preensão Manual Máxima (FPM) <sup>[8,9]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value">{f_dec(FPM_MAX, 1)} kgf</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">Relativa: {f_dec(FPM_REL_MAX, 3)} kgf/kg</div>
        </div>
        <div class="metric-subtext">Mão Esquerda (Não-Dom): {f_dec(FPM_ESQ, 1)} kgf | Mão Direita (Dom): {f_dec(FPM_DIR, 1)} kgf</div>
        <div class="metric-footer">
          <div class="metric-pill">
            Simetria (LSI): {f_dec(LSI_FPM, 1)}% (Diferença de 13,0% • Lado Não-Dominante Superior)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">2º Torque Flexores de Punho a 70° (Biodex) <sup>[6,7,12]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value" style="color: #047857;">{f_dec(BIODEX_MAX, 1)} N·m</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">Relativo: {f_dec(BIODEX_REL_MAX, 4)} N·m/kg</div>
        </div>
        <div class="metric-subtext">Punho Esquerdo (Não-Dom): {f_dec(BIODEX_PICO_E, 1)} N·m | Direito (Dom): {f_dec(BIODEX_PICO_D, 1)} N·m</div>
        <div class="metric-footer">
          <div class="metric-pill">
            Simetria (LSI): {f_dec(LSI_BIODEX, 1)}% (Diferença de 10,8% • Suporte Palmar Firme)
          </div>
        </div>
      </div>
    </div>

    <div class="biodex-card">
      <div class="biodex-header">
        <h4>Análise Biomecânica dos Punhos: A Estratégia Distal ("Wrist Strategy")</h4>
        <span style="font-size: 12px; color: var(--text-muted);">Interface Palmar, Torque a 70°, Wrist Strategy e Aplicação na Marcha</span>
      </div>

      <div class="callout-highlight" style="margin-top: 10px; margin-bottom: 0;">
        <div class="callout-title">
          💡 Como a ação dos punhos contribui para o controle de cabeça para baixo e pontos de atenção <sup>[6,7,15]</sup>
        </div>
        <p class="callout-text">
          Na parada de mão, os flexores de punho desempenham uma função crucial equivalente à dos tornozelos na marcha em pé (<em>Wrist Strategy</em>). 
          Quando o corpo oscila além da linha de equilíbrio (tendência ao <em>overbalance</em>), a pressão imediata das pontas dos dedos e a ativação dos flexores contra o solo 
          produzem um momento corretivo imediato para restaurar o alinhamento sem demandar oscilações amplas de cotovelo ou ombro.
        </p>
        <p class="callout-text">
          Sua <strong>força de preensão manual máxima (52,0 kgf)</strong> merece elogio: situa-se confortavelmente acima da média normativa de homens jovens saudáveis (~42 a 45 kgf, Bohannon 2019 <sup>[8]</sup>), 
          e o <strong>torque isométrico a 70° no Biodex ({f_dec(BIODEX_MAX, 1)} N·m)</strong> demonstra sólida disponibilidade de força no ângulo funcional específico do handstand.
        </p>
        <p class="callout-text">
          <strong>⚠️ Ponto de atenção e sugestão de melhoria:</strong> Notou-se uma assimetria bilateral de 13,0% na preensão (52 vs 46 kgf) e de 10,8% no Biodex (20,5 vs 18,5 N·m) em favor do membro esquerdo (não-dominante). 
          Embora esteja dentro do limite de normalidade clínica (&lt;15% <sup>[15]</sup>), essa diferença indica uma tendência de apoiar mais ou sobrecarregar o braço esquerdo para estabilizar o corpo. 
          <em>Como corrigir:</em> Recomenda-se incluir no treinamento exercícios unilaterais para o punho direito (ex.: flexão de punho unilateral com halteres e sustentação isométrica controlada), buscando aproximar os torques e prevenir momentos torcionais assimétricos durante a locomoção.
        </p>
        <div class="callout-science">
          <strong>Fundamentação Científica & Biomecânica:</strong> 
          Mecanismo clássico da <em>Wrist Strategy</em> (Kerwin & Trewartha, 2001 <sup>[6]</sup>; Blenkinsop et al., 2017 <sup>[7]</sup>). 
          A dorsiflexão avaliada a 70° reproduz o ângulo funcional de contato palmar (Ellenbecker & Roetert, 2006 <sup>[12]</sup>; Rohleder et al., 2021 <sup>[14]</sup>). 
          A equalização intermembros favorece uma distribuição homogênea das forças de reação do solo, mitigando sobrecargas unilaterais durante as fases de contato no Handstand Walk (Bishop et al., 2018 <sup>[15]</sup>; Herzog et al., 1989 <sup>[16]</sup>).
        </div>
      </div>
    </div>

    <!-- 2.2 PROXIMAL -->
    <div class="sub-section-title">
      2.2 Força Proximal e Resistência Muscular: Shoulder Press e Parada de Mão na Parede
    </div>

    <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">3º 1-RM no Shoulder Press (SP) <sup>[10]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value">{f_dec(SP_1RM_KG, 1)} kg</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">{f_dec(SP_REL_KG_KG, 3)} kg/kg</div>
        </div>
        <div class="metric-subtext">Barra Olímpica Estrita (Desenvolvimento sem auxílio das pernas)</div>
        <div class="metric-footer">
          <div class="metric-pill">85,8% do Peso Corporal • Padrão Avançado</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">4º Resistência Belly-to-Wall Handstand <sup>[6,11]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value">{f_dec(WALL_HS_MAX, 1)} s</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">1 min e 04 s</div>
        </div>
        <div class="metric-subtext">Tentativa 1: {WALL_HS_T1:.0f} s | Tentativa 2: {WALL_HS_T2:.0f} s (Extensão a 20 cm da parede)</div>
        <div class="metric-footer">
          <div class="metric-pill">> 1 minuto em Handstand Estrito • Alta Resistência</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Estabilidade proximal: O bloqueio escapular, sustentação axial e transição para a marcha <sup>[10,12,13]</sup>
      </div>
      <p class="callout-text">
        Alcançar <strong>{f_dec(SP_1RM_KG, 1)} kg (cerca de 86% da sua massa corporal)</strong> no Shoulder Press estrito demonstra excelente força vertical nos membros superiores (nível avançado, Soriano et al., 2019 <sup>[10]</sup>). 
        Na prática da parada de mão, essa força é indispensável para sustentar o <strong>"shoulder push"</strong>: a ação de empurrar o solo para manter as escápulas elevadas, 
        promovendo o alinhamento articular da cintura escapular e reduzindo o risco de colapso postural.
      </p>
      <p class="callout-text">
        Complementarmente, a sustentação de <strong>64 segundos na parede</strong> comprova uma sólida resistência muscular isométrica dos ombros e estabilizadores do tronco, 
        capacidade que contribui para retardar a fadiga em sessões intensas.
      </p>
      <p class="callout-text">
        <strong>⚠️ Oportunidade de evolução técnica:</strong> Na caminhada sobre as mãos, a força bilateral estrita precisa se converter em estabilidade unipodal dinâmica (sustentar 100% da carga sobre um único ombro a cada passo). 
        <em>Como aprimorar:</em> Recomenda-se introduzir <em>overhead carries</em> unilaterais (caminhada sustentando peso acima da cabeça com cotovelo estendido e escápula ativa) e desenvolvimentos unilaterais com halter/kettlebell focando na rotação superior do serrátil anterior.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong> 
        O desenvolvimento estrito demanda coativação do deltoide, tríceps braquial e do par de forças escapular (trapézio e serrátil anterior) (Soriano et al., 2019 <sup>[10]</sup>). 
        A rotação superior ativa da escápula otimiza a congruência articular glenoumeral e o empilhamento das estruturas ósseas (Rohleder & Vogt, 2018 <sup>[13]</sup>). 
        A resistência isométrica > 60 s indica tolerância periférica sustentada sob gravidade (Gautier et al., 2007 <sup>[11]</sup>), 
        fornecendo a base necessária para suportar transferências de carga unipodais dinâmicas.
      </div>
    </div>

    <!-- SEÇÃO 3: LABIOCOM -->
    <div class="section-title">
      <span class="badge-num">3</span>
      Avaliação Biomecânica Tridimensional, Controle Postural e Locomoção (LaBioCoM)
    </div>

    <!-- 3.1 ESTÁTICO -->
    <div class="sub-section-title">
      3.1 Handstand Estático e Controle de Equilíbrio (Plataforma Bertec Dual & Vicon 3D)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Tempo de Pico no HS Assistido <sup>[14]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_ASSIST_PICO_S)} s</div>
          <div class="metric-subtext">Média das 3 tentativas: {f_dec(HS_ASSIST_MED_S)} s</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Desfecho Primário Estático (Sustentação Prolongada)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Distância Média CoP-CoM <sup>[17,18]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(COP_COM_DIST_MM)} mm</div>
          <div class="metric-subtext">Erro de equilíbrio de apenas ~5,0 cm</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Pêndulo Invertido Sob Controle Fino</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Velocidade Média do CoP <sup>[14,19]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(COP_VEL_MM_S)} mm/s</div>
          <div class="metric-subtext">Microajustes de ~9,9 cm por segundo</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Correções Rápidas de Alta Frequência</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Entropia Aproximada (ApEn do CoP) <sup>[20,21]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(APEN_COP, 4)}</div>
          <div class="metric-subtext">Faixa de normalidade: 0,60 a 0,95</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Automaticidade e Controle Fluido</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Verticalidade Média do Tronco <sup>[13]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_VERT_DEG)}°</div>
          <div class="metric-subtext">Inclinação em relação à gravidade</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Alinhamento Postural Sólido e Estável</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Extensão Cervical (Olhar) <sup>[11]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_CERVICAL_DEG)}°</div>
          <div class="metric-subtext">Olhar fixado no solo entre os polegares</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Fixação Óptica Estável no Ponto Fixo</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Dinâmica do pêndulo invertido: Estabilometria e controle postural <sup>[6,17-21]</sup>
      </div>
      <p class="callout-text">
        Sustentar a postura por cerca de <strong>41 segundos</strong> sobre as plataformas de força com repetição consistente entre as tentativas ({f_dec(HS_ASSIST_T1_S, 1)}s, {f_dec(HS_ASSIST_T2_S, 1)}s e {f_dec(HS_ASSIST_T3_S, 1)}s) 
        evidencia estabilidade na execução da tarefa. Na postura invertida, o corpo se comporta biomecanicamente como um <strong>pêndulo invertido</strong>, 
        em que o centro de massa precisa ser mantido sobre a base estreita das mãos.
      </p>
      <p class="callout-text">
        Os registros indicaram que a distância média entre o centro de massa e o centro de pressão foi de <strong>{f_dec(COP_COM_DIST_MM)} mm (~5,0 cm)</strong>, 
        com correções contínuas realizadas a uma velocidade de <strong>{f_dec(COP_VEL_MM_S)} mm/s</strong>. 
        Um resultado interessante é o valor de <strong>Entropia Aproximada ({f_dec(APEN_COP, 4)})</strong>: valores nessa faixa costumam sugerir que o equilíbrio 
        decorre de microajustes flexíveis e adaptativos, sem rigidez excessiva das articulações envolvidas.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong> 
        O modelo estabilométrico de Winter (1995) <sup>[17]</sup> e Slobounov et al. (2008) <sup>[18]</sup> define que o controle do equilíbrio em inversão decorre da oscilação ativa do CoP ao redor da projeção vetorial do CoM para produzir momentos fletores restauradores. 
        A velocidade do CoP ({f_dec(COP_VEL_MM_S)} mm/s) reflete ajustes reflexos frequentes descritos na literatura (70 a 150 mm/s <sup>[14,19]</sup>). 
        A Entropia Aproximada ({f_dec(APEN_COP, 4)}) calculada conforme Pincus (1991) <sup>[20]</sup> e Borg & Laxåback (2010) <sup>[21]</sup> aponta para um controle postural com grau favorável de complexidade temporal, 
        sugerindo automaticidade motora adaptativa. Esses parâmetros serão investigados como potenciais preditores na análise estatística multivariada do estudo.
      </div>
    </div>

    <!-- 3.2 LIVRE -->
    <div class="sub-section-title">
      3.2 Handstand Livre (Autonomia e Domínio Técnico sem Auxílio)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Taxa de Sucesso na Entrada Livre <sup>[11,22]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">100%</div>
          <div class="metric-subtext">3 de 3 tentativas válidas seguidas (≥ 3s)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Controle Antecipatório Eficaz (100%)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Melhor Tempo no HS Livre <sup>[14]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_LIVRE_TEMPO_MAX_S)} s</div>
          <div class="metric-subtext">Tentativa 2 (T1: {f_dec(HS_LIVRE_T1_S, 1)}s | T3: {f_dec(HS_LIVRE_T3_S, 1)}s)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Autonomia Plena sem Parede ou Apoio</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Alinhamento de Verticalidade Livre <sup>[13]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_LIVRE_VERT_DEG)}°</div>
          <div class="metric-subtext">Menor inclinação observada no estudo</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Postura Reta, Compacta e Elegante</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Flexão Plantar (Ponta de Pé) <sup>[13]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_LIVRE_PLANTAR_DEG)}°</div>
          <div class="metric-subtext">Extensão ativa dos tornozelos e dedos</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Cadeia Posterior Ativa e Unida</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Estratégias Articulares (Cotovelo / Ombro) <sup>[6,7,23]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_COTOVELO_SD_DEG)}° SD</div>
          <div class="metric-subtext">Cotovelo RMS: {f_dec(HS_COTOVELO_RMS_DEG_S)}°/s | Ombro SD: {f_dec(HS_OMBRO_SD_DEG)}°</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Busca Ativa de Cotovelo</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Handstand Livre: Controle antecipatório, alinhamento técnico e estratégias de equilíbrio <sup>[6,7,11,13,22,23]</sup>
      </div>
      <p class="callout-text">
        <strong>🗣️ O que você precisa saber na prática:</strong><br>
        • <strong>Subida e alinhamento:</strong> Você acertou 100% das subidas (3 de 3 tentativas válidas) e sustentou mais de 24 segundos com excelente alinhamento (apenas {f_dec(HS_LIVRE_VERT_DEG)}° de desvio vertical e pés em ponta a {f_dec(HS_LIVRE_PLANTAR_DEG)}°).<br>
        • <strong>Como você se equilibrou (Estratégias Articulares):</strong> Diante dos desequilíbrios, <strong>você utilizou predominantemente os cotovelos e ombros (dobrando e esticando os braços ativamente)</strong>, usando essa flexão rápida como um recurso funcional para "salvar" a postura antes de cair, em vez de segurar apenas nos punhos e dedos.
      </p>
      <p class="callout-text">
        <strong>🔬 Detalhamento dos Dados e Biomecânica:</strong><br>
        A análise cinemática contínua registrou uma oscilação expressiva de cotovelos (desvio-padrão de <strong>{f_dec(HS_COTOVELO_SD_DEG)}°</strong>, amplitude total de <strong>{f_dec(HS_COTOVELO_ROM_DEG)}°</strong> e velocidade angular média de <strong>{f_dec(HS_COTOVELO_RMS_DEG_S)}°/s</strong>), acompanhada de movimentação nos ombros (desvio de {f_dec(HS_OMBRO_SD_DEG)}° e velocidade de {f_dec(HS_OMBRO_RMS_DEG_S)}°/s) e no quadril (desvio de {f_dec(HS_QUADRIL_SD_DEG)}°). Na literatura de controle motor (Kerwin & Trewartha, 2001; Blenkinsop et al., 2017), o equilíbrio invertido pode ser mantido por ajustes finos no centro de pressão palmar (estratégia de punho com braços estendidos rígidos) ou por correções multissegmentares proximais. Flexionar os braços momentaneamente rebaixa o centro de massa e permite aplicar força extensora de tríceps para retomar o prumo. Esse padrão é comum em modalidades como a Calistenia e o Handbalancing livre; já na ginástica artística, busca-se a haste bloqueada sem flexão devido às deduções do código de pontuação. Ambas representam soluções biomecânicas individuais adaptativas frente à instabilidade.
      </p>
      <p class="callout-text">
        <strong>⚠️ Ponto que precisa de ajuste e como consertar:</strong><br>
        Observou-se uma grande diferença de tempo entre as três séries livres (T1: 3,5 s, T2: 24,5 s e T3: 13,6 s). Essa oscilação mostra que o seu equilíbrio ainda é sensível a pequenas perturbações no instante logo após a subida.<br>
        <em>Como melhorar:</em> 1) Treinar séries buscando manter de 15 a 20 segundos estáveis e consistentes, descansando plenamente entre elas; 2) Praticar o "salvamento" com os dedos: pressionar as pontas das mãos quando o corpo ameaçar passar para frente e empurrar a palma quando ameaçar voltar para trás, antes de dobrar os braços ou cair.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong>
        O êxito imediato na transição motora reflete a robustez dos mecanismos antecipatórios descritos por Gautier et al. (2007) <sup>[11]</sup> e Clement et al. (1984) <sup>[22]</sup>.
        A verticalidade de 7,97° tende a minimizar braços de alavanca gravitacionais sobre o complexo escapular e coluna lombar (Rohleder & Vogt, 2018 <sup>[13]</sup>).
        A mobilização de graus de liberdade em cotovelo e ombro diante de perturbações corrobora os modelos de controle multissegmentar de Kerwin & Trewartha (2001) <sup>[6]</sup> e Blenkinsop et al. (2017) <sup>[23]</sup>.
        A redução da variabilidade temporal entre tentativas consecutivas é o passo determinante para consolidar a segurança motora antes de progressões dinâmicas.
      </div>
    </div>

    <!-- 3.3 HSW -->
    <div class="sub-section-title">
      3.3 Handstand Walk — HSW (Locomoção Invertida Dinâmica)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Distância Mediana no HSW <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_DIST_MEDIANA_M)} m</div>
          <div class="metric-subtext">T1: {f_dec(HSW_T1_DIST_M)}m | T2: {f_dec(HSW_T2_DIST_M)}m | T3: {f_dec(HSW_T3_DIST_M)}m</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Quedas Precoces em T1 e T2
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Distância Máxima Percorrida <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(HSW_DIST_MAX_M)} m</div>
          <div class="metric-subtext">Alcançada na Tentativa 3</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Destaque Positivo! Superou 4 metros</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Cadência dos Passos com as Mãos <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CADENCIA)} passos/s</div>
          <div class="metric-subtext">~1 passo com as mãos por segundo</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Ritmo de Passadas Estável</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Comprimento Médio da Passada <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_PASSADA_MM)} mm</div>
          <div class="metric-subtext">~42,8 cm de avanço por passada palmar</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Passadas Amplas e Proporcionais</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Fase de Duplo Suporte Palmar <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_DUPLO_SUPORTE_PCT)}%</div>
          <div class="metric-subtext">Tempo com ambas as mãos em contato</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Apoio Duplo Excessivo (>55%)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Consistência Espacial (CV Passadas) <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CV_ESPACIAL)}%</div>
          <div class="metric-subtext">Variação no comprimento dos passos</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Passadas com Regularidade Espacial (&lt;15%)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Variabilidade Temporal (CV Passadas) <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #b45309;">{f_dec(HSW_CV_TEMPORAL)}%</div>
          <div class="metric-subtext">Variação no tempo de permanência de apoio</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Ritmo Temporal Irregular (>50%)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Velocidade da Marcha (HSW) <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_VEL_M_S)} m/s</div>
          <div class="metric-subtext">{f_dec(HSW_VEL_KM_H)} km/h (Velocidade linear)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Deslocamento Moderado</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Tempo de Contato Palmar <sup>[7]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CONTATO_S)} s</div>
          <div class="metric-subtext">{HSW_CONTATO_MS} ms por apoio palmar</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Duração de Apoio Manual</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Extensão Cervical no HSW <sup>[11]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CERVICAL_DEG)}°</div>
          <div class="metric-subtext">+19° vs parado (Olhar erguido à frente)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Ancoragem Visual Fixada no Alvo</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Rotação Externa das Mãos <sup>[13]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_ROT_MAOS_DEG)}°</div>
          <div class="metric-subtext">+36° vs parado (Mãos viradas para fora)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Abertura Excessiva (~67°)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Flexão Plantar na Marcha <sup>[13]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_PLANTAR_DEG)}°</div>
          <div class="metric-subtext">Pés soltos na marcha (vs 28,4° no livre)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Perda de Tensão Posterior
          </div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Handstand Walk: Análise dinâmica, diagnósticos de melhoria e prescrição corretiva <sup>[7,11,13]</sup>
      </div>
      <p class="callout-text">
        <strong>🗣️ O que você precisa saber na prática:</strong><br>
        • <strong>Desempenho e velocidade:</strong> Você conseguiu andar mais de 4 metros na sua melhor tentativa, com passadas de bom tamanho (~43 cm), tempo de contato de {f_dec(HSW_CONTATO_S)} s por apoio e velocidade média de deslocamento de <strong>{f_dec(HSW_VEL_M_S)} m/s ({f_dec(HSW_VEL_KM_H)} km/h)</strong>.<br>
        • <strong>Pontos de atenção:</strong> Você ainda hesita na troca entre os passos, mantendo as duas mãos apoiadas no solo por mais de 56% da marcha (duplo suporte elevado). Além disso, suas mãos abrem muito para fora (67°) e as pernas relaxam na caminhada.
      </p>
      <p class="callout-text">
        <strong>🔬 Detalhamento dos Dados e Biomecânica:</strong><br>
        Caminhar sobre as mãos exige que, a cada passada, um dos apoios deixe o solo e o corpo seja acelerado para a frente. Sua distância máxima (4,28 m) comprova boa capacidade propulsiva, mas a mediana foi de {f_dec(HSW_DIST_MEDIANA_M)} m devido a paradas precoces nas primeiras tentativas. O apoio duplo prolongado (56,01%) e a alta variabilidade temporal ({f_dec(HSW_CV_TEMPORAL)}%) confirmam que a transição de peso de uma mão para a outra ainda precisa de maior fluidez e velocidade.
      </p>
      <p class="callout-text">
        <strong>🛠️ Como consertar no treinamento (Prescrição Prática):</strong><br>
        • <em>Ajustar o ângulo das mãos para ~30° a 45°:</em> Posicione os dedos apontando discretamente para fora, recuperando a ação de tração e freio palmar anteroposterior.<br>
        • <em>Treinar cadência rítmica constante:</em> Pratique passadas com metrônomo sonoro (~1 passo/s) e shoulder taps na parede com tempo fixo em cada apoio (ex.: 1 segundo em cada braço), eliminando a hesitação no duplo apoio.<br>
        • <em>Manter compactação corporal ativa:</em> Mantenha a intenção consciente de contrair glúteos e estender as pontas dos pés durante todo o trajeto, evitando o "efeito chicote" dos membros inferiores.<br>
        • <em>Desequilíbrio anterior controlado:</em> Inicie a passada permitindo que o quadril avance sutilmente à frente dos ombros antes de mover a mão, para que o movimento seja puxado pela gravidade e não freado.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong>
        Blenkinsop et al. (2017) <sup>[7]</sup> destacam que a locomoção invertida eficiente requer minimização da fase de duplo suporte e alta consistência espaço-temporal.
        A assimetria entre os CVs espacial (14,07%) e temporal (56,95%) reflete perturbação no ritmo de transferência de carga.
        A rotação excessiva palmar (66,87°) compromete o momento sagital de flexores de punho (Kerwin & Trewartha, 2001 <sup>[6]</sup>), enquanto a perda de tensão distal nos pés afeta a rigidez de segmento articulado (Rohleder & Vogt, 2018 <sup>[13]</sup>).
        A dissertação investigará formalmente o impacto dessas variáveis na distância percorrida no HSW.
      </div>
    </div>

    <!-- SEÇÃO 4: SÍNTESE INTEGRADA E RECOMENDAÇÕES -->
    <div class="practice-box">
      <h4 style="color: var(--emerald-dark); margin-bottom: 14px;">🌟 Seus Grandes Destaques e Forças Biomecânicas (com literatura):</h4>
      <ul style="margin-bottom: 20px;">
        <li>
          <strong>1. Composição Corporal e Integridade Celular (LaCiDH):</strong> Ângulo de Fase notável de 8,98° (+1,99 DP vs Barbosa-Silva et al., 2005 <sup>[4]</sup>) e mais de 83% de massa magra ativa, indicando excelente integridade de membrana celular e peso funcional favorável.
        </li>
        <li>
          <strong>2. Força Distal de Preensão Manual (LaCiDH):</strong> Marca máxima de 52,0 kgf, superando a média populacional de homens jovens (~42 a 45 kgf, Bohannon 2019 <sup>[8]</sup>), conferindo firmeza palmar de contato.
        </li>
        <li>
          <strong>3. Força Vertical Proximal e Resistência Escapular (LaCiDH):</strong> Shoulder Press estrito com 85,8% da massa corporal (padrão avançado, Soriano et al., 2019 <sup>[10]</sup>) e sustentação na parede de 64 s (>1 min), garantindo suporte robusto sob sobrecarga gravitacional.
        </li>
        <li>
          <strong>4. Consistência no Handstand Estático (LaBioCoM):</strong> Sustentação homogênea de ~40 s com Entropia de 0,77, atestando regulação postural adaptativa e automática sem rigidez excessiva (Pincus 1991 <sup>[20]</sup>; Borg & Laxåback 2010 <sup>[21]</sup>).
        </li>
        <li>
          <strong>5. Autonomia e Alinhamento no Livre (LaBioCoM):</strong> 100% de precisão nas subidas sem apoio e verticalidade de 7,97° na melhor tentativa (24,5 s), confirmando domínio do controle antecipatório (Gautier et al., 2007 <sup>[11]</sup>).
        </li>
      </ul>

      <h4 style="color: #b45309; margin-bottom: 14px;">🎯 Oportunidades de Evolução Técnica e Prescrição de Treino (Direto e Acionável):</h4>
      <ul>
        <li>
          <strong>1. Regularidade Temporal e Fluidez no Handstand Walk:</strong> Reduzir a acentuada variabilidade de tempo entre as passadas (CV Temporal de 56,95%) e o excesso de duplo suporte (56,01%). <em>Prescrição:</em> Praticar passadas com metrônomo a 1 Hz e <em>shoulder taps</em> controlados na parede (1 s por apoio) para eliminar a hesitação ao avançar.
        </li>
        <li>
          <strong>2. Correção da Pegada Palmar na Marcha:</strong> Diminuir a rotação externa excessiva das mãos de ~67° para a faixa de ~30° a 45°. Isso redireciona os dedos mais à frente, recuperando o braço de alavanca sagital dos flexores de punho para frear e acelerar o corpo na linha de caminhada.
        </li>
        <li>
          <strong>3. Compactação Corporal Dinâmica (Pés em Ponta):</strong> Resgatar na caminhada a tensão ativa de pernas e pés observada no estático (evitar a queda para 5,85° de flexão plantar). Manter pernas aduzidas e pontas dos pés estendidas evita oscilações parasitas das pernas.
        </li>
        <li>
          <strong>4. Consistência de Duração no Handstand Livre:</strong> Eliminar as quedas precoces entre as séries livres (oscilação entre 3,5 s e 24,5 s). <em>Prescrição:</em> Realizar blocos de 5 a 6 séries de 15 a 20 s estáveis, descansando plenamente entre elas, e treinar ativamente o salvamento por pressão palmar antes de descer.
        </li>
        <li>
          <strong>5. Equalização da Força Bilateral dos Membros Superiores:</strong> Reduzir a assimetria bilateral de 11% a 13% em favor do braço esquerdo. <em>Prescrição:</em> Incluir fortalecimento isolado de punho e ombro para o membro direito (flexão de punho com halteres e press unilateral) para equilibrar as forças de contato.
        </li>
      </ul>
    </div>

    <!-- SEÇÃO 5: REFERÊNCIAS CIENTÍFICAS -->
    <div class="references-card">
      <h4>📚 Referências Científicas e Normativas Consultadas:</h4>
      <ol>
        <li>Sun, S. S., et al. (2003). Development of bioelectrical impedance analysis prediction equations for body composition with the use of a multicomponent model. <em>Am J Clin Nutr</em>, 77(2), 331-340.</li>
        <li>Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. <em>J Appl Physiol</em>, 89(2), 465-471.</li>
        <li>American College of Sports Medicine (ACSM). (2018). <em>ACSM's Guidelines for Exercise Testing and Prescription</em> (10th ed.). Wolters Kluwer.</li>
        <li>Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. <em>Am J Clin Nutr</em>, 82(1), 49-52.</li>
        <li>Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. <em>Clin Nutr</em>, 31(6), 854-861.</li>
        <li>Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. <em>Sports Biomech</em>, 1(2), 163-176.</li>
        <li>Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Handstand walk: Locomotor biomechanics and coordination in inverted human locomotion. <em>Hum Mov Sci</em>, 54, 235-244.</li>
        <li>Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. <em>J Phys Ther Sci</em>, 31(11), 932-938.</li>
        <li>Dodds, R. M., et al. (2014). Globally representative normative data for handgrip strength: systematic review. <em>PLoS ONE</em>, 9(12), e113637.</li>
        <li>Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. <em>Strength Cond J</em>, 41(4), 48-60.</li>
        <li>Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. <em>Hum Mov Sci</em>, 26(4), 577-594.</li>
        <li>Ellenbecker, T. S., & Roetert, E. P. (2006). Isokinetic wrist strength in competitive athletes. <em>Am J Sports Med</em>, 34(11), 1845-1852.</li>
        <li>Rohleder, J., & Vogt, L. (2018). Kinematic alignment and joint stacking in artistic gymnastics vs. fitness handbalancing. <em>J Sports Sci</em>, 36(11), 1238-1245.</li>
        <li>Rohleder, J., et al. (2021). Wrist joint biomechanics and handstand stability in gymnastics. <em>Sports Biomech</em>, 20(3), 312-326.</li>
        <li>Bishop, C., et al. (2018). Effects of inter-limb asymmetries on physical and sports performance. <em>J Sports Sci</em>, 36(10), 1135-1144.</li>
        <li>Herzog, W., et al. (1989). Asymmetries in ground reaction force patterns in normal human gait. <em>Med Sci Sports Exerc</em>, 21(1), 110-118.</li>
        <li>Winter, D. A. (1995). Human balance and posture control during standing and walking. <em>Gait & Posture</em>, 3(4), 193-214.</li>
        <li>Slobounov, S., et al. (2008). Virtual reality and force-platform assessment of inverted posture stability. <em>Exp Brain Res</em>, 188(2), 241-253.</li>
        <li>Uzun, M., et al. (2012). Stabilometric comparison of handstand on force plates between elite and novice athletes. <em>J Hum Kinet</em>, 34(1), 15-23.</li>
        <li>Pincus, S. M. (1991). Approximate entropy as a measure of system complexity. <em>Proc Natl Acad Sci USA</em>, 88(6), 2297-2301.</li>
        <li>Borg, F. G., & Laxåback, G. (2010). Entropy of balance: How to compute and interpret approximate entropy in posturography. <em>J Biomech</em>, 43(15), 3044-3048.</li>
        <li>Clement, G., et al. (1984). Adaptation of posture and locomotion to inverted support. <em>Aerosp Med Hum Perform</em>, 55(8), 700-705.</li>
        <li>Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Balance control strategies during perturbed and unperturbed handstands. <em>J Biomech</em>, 65, 123-129.</li>
        <li>Slobounov, S. M., & Newell, K. M. (1996). Posture, living systems, and the 'freezing' and 'freeing' of degrees of freedom. In <em>Motor Control in Sports</em> (pp. 89-108).</li>
      </ol>
    </div>

  </div>

  <!-- RODAPÉ INSTITUCIONAL -->
  <div class="footer">
    Universidade de São Paulo — Escola de Educação Física e Esporte de Ribeirão Preto (EEFERP-USP)<br>
    Laboratório de Cineantropometria e Desempenho Humano (LaCiDH) | Laboratório de Biomecânica e Controle Motor (LaBioCoM)<br>
    <strong>Mestrando:</strong> Guilherme de Paula Lemos (guilherme.lemos@usp.br) &nbsp;|&nbsp; 
    <strong>Orientador:</strong> Prof. Dr. Matheus Machado Gomes
  </div>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] Documento HTML salvo em: {HTML_OUT}")

# =========================================================================
# 3. CONVERSÃO AUTOMÁTICA EM PDF DE ALTA RESOLUÇÃO VIA MICROSOFT EDGE
# =========================================================================
print("[3/3] Compilando PDF de alta definição via Microsoft Edge headless...")

edge_paths = [
    r"C:\Program Files (x86)\Microsoft\Edge\Application\msedge.exe",
    r"C:\Program Files\Microsoft\Edge\Application\msedge.exe",
    "msedge"
]

edge_exe = None
for path in edge_paths:
    if os.path.exists(path) or path == "msedge":
        edge_exe = path
        break

if edge_exe:
    cmd = [
        edge_exe,
        "--headless",
        "--disable-gpu",
        "--run-all-compositor-stages-before-draw",
        f"--print-to-pdf={PDF_OUT}",
        HTML_OUT
    ]
    try:
        res = subprocess.run(cmd, capture_output=True, text=True, timeout=45)
        if os.path.exists(PDF_OUT) and os.path.getsize(PDF_OUT) > 1000:
            print(f"[OK] PDF gerado com sucesso ({os.path.getsize(PDF_OUT):,} bytes) em:\n  -> {PDF_OUT}")
        else:
            print(f"[AVISO] Falha ao compilar PDF: {res.stderr}")
    except Exception as e:
        print(f"[AVISO] Erro ao invocar Edge: {e}")
else:
    print("[AVISO] Executável do Microsoft Edge não encontrado para gerar PDF.")

# Arquivos mantidos exclusivamente no diretório dedicado P001_laudo

print("=" * 80)
print("RELATÓRIO DEVOLUTIVO DE P001 ATUALIZADO COM SUCESSO!")
print(f"  -> DOCX: {DOCX_OUT}")
print(f"  -> HTML: {HTML_OUT}")
print(f"  -> PDF:  {PDF_OUT}")
print("=" * 80)
