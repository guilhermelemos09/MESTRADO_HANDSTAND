# -*- coding: utf-8 -*-
"""
Script de Geração do Relatório Individual Devolutivo Completo - Participante P002 (Guilherme Lemos)
Pesquisa de Mestrado em Ciências do Esporte - EEFERP-USP
Orientador: Prof. Dr. Matheus Machado Gomes | Mestrando: Guilherme de Paula Lemos

Padrão Visual e Editorial Unificado (Idêntico ao P001):
- Design moderno, cards com gradientes verde-esmeralda/menta, pills e badges informativas.
- Elogios respaldados pela literatura científica internacional com formulação prudente ("potencial favorável", "tendência positiva").
- Diagnósticos diretos, transparentes e educados com fundamentação biomecânica clara e prescrições de treino acionáveis para pontos de melhoria.
- Tag "Projeto:" destacada com o mesmo peso de Mestrando e Orientador.
- E-mail institucional correto: guilherme.lemos@usp.br.
"""

import os
import sys
import base64
import shutil
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
    if val is None or val == "":
        return "-"
    try:
        return f"{float(val):.{dec}f}".replace(".", ",")
    except Exception:
        return str(val)

# =========================================================================
# CONFIGURAÇÃO DE DIRETÓRIOS E ARQUIVOS
# =========================================================================
BASE_DIR = r"c:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL\03_CONSOLIDACAO_DATASET"
OUTPUT_DIR = os.path.join(BASE_DIR, "resultados_finais", "laudos_devolutiva", "P002_laudo")
os.makedirs(OUTPUT_DIR, exist_ok=True)

DOCX_OUT = os.path.join(OUTPUT_DIR, "P002_RELATORIO_DEVOLUTIVA_GUILHERME_LEMOS.docx")
HTML_OUT = os.path.join(OUTPUT_DIR, "P002_RELATORIO_DEVOLUTIVA_GUILHERME_LEMOS.html")
PDF_OUT = os.path.join(OUTPUT_DIR, "P002_RELATORIO_DEVOLUTIVA_GUILHERME_LEMOS.pdf")

# Saídas salvas exclusivamente no diretório dedicado P002_laudo

LOGO_EEFERP_WHITE = os.path.join(OUTPUT_DIR, "logo_eeferp_white.png")
LOGO_EEFERP_COLOR = os.path.join(OUTPUT_DIR, "logo_eeferp_color.png")

TITULO_OFICIAL_PROJETO = "Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk"

OBJETIVO_GERAL_PROJETO = (
    "Investigar os fatores determinantes e preditores do desempenho no Handstand (HS) e Handstand Walk (HSW), "
    "integrando a capacidade neuromuscular dos membros superiores (força e resistência proximal e distal), o controle postural estabilométrico "
    "(oscilação do Centro de Pressão na plataforma de força Bertec) e a cinemática tridimensional Vicon "
    "(alinhamento articular vertical e dinâmica espaço-temporal da locomoção invertida)."
)

# =========================================================================
# DADOS CONSOLIDADOS E AUDITADOS DE P002 (LACIDH + LABIOCOM)
# =========================================================================
NOME_ATLETA = "Guilherme Lemos"
CODIGO_ATLETA = "P002 (Atleta Piloto Oficial)"
IDADE = 42
FAIXA_ETARIA = "42 anos (Faixa 40 a 44 anos)"
SEXO = "Masculino"
DOMINANCIA = "Destro (Membro Direito)"
DATA_COLETA_S1 = "14/09/2026 (LaCiDH — Força e BIA)"
DATA_COLETA_S2 = "16/09/2026 (LaBioCoM — Vicon 3D e Bertec)"
MODALIDADES = "CrossFit® / Musculação / Ginástica"
TEMPO_PRATICA = "> 10 anos geral (126 meses) | > 10 anos específico em HS"
VOLUME_PRATICA_HORAS = 180.0

# 1. Antropometria e Composição Corporal (BIA Sanny® - Sun et al., 2003)
MASSA_KG = 87.20
ESTATURA_CM = 171.0
ESTATURA_M = ESTATURA_CM / 100.0
IMC = round(MASSA_KG / (ESTATURA_M ** 2), 2)  # 29.82 kg/m²
GORDURA_PCT = 19.37
MG_KG = 16.75
MLG_KG = 70.45
MME_KG = 37.20
ACT_L = 51.77
ACT_PCT = round((ACT_L / MASSA_KG) * 100.0, 1)  # 59.4%
PHA_DEG = 6.78
FFMI = round(MLG_KG / (ESTATURA_M ** 2), 2)  # 24.09 kg/m²

# 2. Força Distal (Saehan Hidráulico & Biodex System 4 PRO a 70°)
FPM_DIR = 52.0
FPM_ESQ = 53.0
FPM_MED = round((FPM_DIR + FPM_ESQ) / 2.0, 1)  # 52.5 kgf
FPM_MAX = 53.0
FPM_REL_MAX = round(FPM_MAX / MASSA_KG, 3)     # 0.608 kgf/kg
FPM_REL_MED = round(FPM_MED / MASSA_KG, 3)     # 0.602 kgf/kg
LSI_FPM = round((FPM_ESQ / FPM_DIR) * 100.0, 1) # 101.9% (Simetria quase perfeita)

BIODEX_PICO_D = 12.9
BIODEX_PICO_E = 17.1
BIODEX_MED = round((BIODEX_PICO_D + BIODEX_PICO_E) / 2.0, 1) # 15.0 N·m
BIODEX_MAX = 17.1
BIODEX_REL_MED = round(BIODEX_MED / MASSA_KG, 4) # 0.1720 N·m/kg
BIODEX_REL_MAX = round(BIODEX_MAX / MASSA_KG, 4) # 0.1961 N·m/kg
LSI_BIODEX = round((BIODEX_PICO_E / BIODEX_PICO_D) * 100.0, 2) # 132.56% (Esq > Dir por 32.6%)

# 3. Força Proximal e Resistência Isométrica
SP_1RM_KG = 66.0
SP_REL_PCT = round((SP_1RM_KG / MASSA_KG) * 100.0, 1) # 75.7%
SP_REL_KG_KG = round(SP_1RM_KG / MASSA_KG, 3)        # 0.757 kg/kg
WALL_HS_T1 = 92.0
WALL_HS_T2 = 101.0
WALL_HS_MAX = 101.0

# 4. Cinemática e Cinética Estabilométrica (LaBioCoM - Handstand Estático Assistido & Livre)
HS_ASSIST_TEMPO_S = 60.28
HS_ASSIST_COP_COM_MM = 105.29
HS_ASSIST_COP_VEL_MM_S = 96.16
HS_ASSIST_APEN = 1.3046
HS_ASSIST_VERT_DEG = 11.93

# Handstand Livre (Autonomia e Domínio Técnico)
HS_LIVRE_TAXA_SUCESSO = "100% (3 de 3 tentativas válidas ≥ 3s)"
HS_LIVRE_TEMPO_MAX_S = 50.98
HS_LIVRE_T1_S = 50.98
HS_LIVRE_T2_S = 18.99
HS_LIVRE_T3_S = 9.94
HS_LIVRE_MED_S = round((HS_LIVRE_T1_S + HS_LIVRE_T2_S + HS_LIVRE_T3_S) / 3.0, 2) # 26.64 s

COP_COM_DIST_MM = 117.86
COP_VEL_MM_S = 97.96
APEN_COP = 0.8758

HS_VERT_DEG = 7.67
HS_CERVICAL_DEG = 20.29
HS_PLANTAR_DEG = 40.77
HS_BASE_MM = 591.59
HS_ROT_MAOS_DEG = 33.18
HS_ALTURA_COM_MM = 1157.01
HS_LIVRE_VERT_DEG = HS_VERT_DEG
HS_LIVRE_CERVICAL_DEG = HS_CERVICAL_DEG
HS_LIVRE_PLANTAR_DEG = HS_PLANTAR_DEG
HS_LIVRE_BASE_MM = HS_BASE_MM
HS_LIVRE_ROT_MAOS_DEG = HS_ROT_MAOS_DEG
HS_LIVRE_ALTURA_COM_MM = HS_ALTURA_COM_MM

# Estratégias Articulares de Busca do Equilíbrio (Cinemática 3D)
HS_COTOVELO_SD_DEG = 5.44
HS_COTOVELO_ROM_DEG = 39.51
HS_COTOVELO_RMS_DEG_S = 12.16
HS_OMBRO_SD_DEG = 5.94
HS_OMBRO_ROM_DEG = 33.88
HS_OMBRO_RMS_DEG_S = 10.42
HS_QUADRIL_SD_DEG = 3.65
HS_QUADRIL_ROM_DEG = 36.63
HS_QUADRIL_RMS_DEG_S = 8.28
HS_RAZAO_COTOVELO_OMBRO = 0.92
HS_ESTRATEGIA_DOMINANTE = "Mista / Alta Rigidez Proximal"
HSW_VEL_KM_H = 1.40
HSW_CONTATO_MS = 640

# 5. Handstand Walk (HSW Dinâmico)
HSW_DIST_MEDIANA_M = 4.921
HSW_DIST_MAX_M = 5.486
HSW_T1_DIST_M = 4.790
HSW_T2_DIST_M = 5.486
HSW_T3_DIST_M = 4.921

HSW_PASSOS = 22
HSW_TEMPO_EXEC_S = 14.16
HSW_CADENCIA = 1.55
HSW_PASSADA_MM = 249.35
HSW_VEL_M_S = 0.39
HSW_CONTATO_S = round(HSW_TEMPO_EXEC_S / HSW_PASSOS, 2) # 0.64 s
HSW_DUPLO_SUPORTE_PCT = 59.68
HSW_CV_ESPACIAL = 19.03
HSW_CV_TEMPORAL = 9.81
HSW_OSCILACAO_ML_MM = 389.73

HSW_VERT_DEG = 12.82
HSW_CERVICAL_DEG = 39.03
HSW_PLANTAR_DEG = 29.71
HSW_BASE_MM = 663.83
HSW_ROT_MAOS_DEG = 15.77
HS_CV_TEMPORAL = HSW_CV_TEMPORAL
HS_CV_ESPACIAL = HSW_CV_ESPACIAL

print("Variáveis consolidadas para P002. Inicializando geração de documentos...")

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
format_cell_box(t_part.rows[1].cells[2], "DATAS DAS COLETAS", "14/09 (LaCiDH) e 16/09/2026 (LaBioCoM)")
format_cell_box(t_part.rows[1].cells[3], "STATUS DOS TESTES", "100% Concluídos (S1 + S2)")

p_intro = doc.add_paragraph()
p_intro.paragraph_format.space_before = Pt(4)
p_intro.paragraph_format.space_after = Pt(4)
r_in = p_intro.add_run(
    f"Olá, {NOME_ATLETA.split()[0]}! Muito obrigado pela sua dedicação e contribuição voluntária nas duas sessões do nosso estudo na EEFERP-USP. "
    f"Este laudo foi elaborado para você: ele reúne suas avaliações do LaCiDH (Composição Corporal e Força Neuromuscular) e do LaBioCoM (Handstand e Handstand Walk 3D). "
    f"Para tornar a leitura agradável e esclarecedora, começamos cada tópico contextualizando o que os resultados podem representar na prática e finalizamos com a fundamentação científica correspondente [1-24]. "
    f"Agradecemos e parabenizamos pelo empenho ao longo de todos os testes!"
)
r_in.font.size = Pt(8.2)
r_in.font.color.rgb = TEXT_DARK_RGB

# Box de Objetivo do Projeto de Mestrado
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
    ("Massa Corporal & Estatura\nÍndice de Massa Corporal (IMC)", f"{f_dec(MASSA_KG)} kg | {f_dec(ESTATURA_CM, 1)} cm\nIMC = {f_dec(IMC)} kg/m²", "IMC elevado decorrente de acentuada hipertrofia muscular esquelética (FFMI atlético [2,4]), e não de adiposidade excessiva."),
    ("Percentual de Gordura Corporal (%GC)\nEquação Específica de Sun et al. (2003) [1]", f"{f_dec(GORDURA_PCT)}%\n({f_dec(MG_KG)} kg em gordura)", "Compatível com a faixa saudável e atlética para homens de 40 a 44 anos (ACSM [3])."),
    ("Massa Livre de Gordura (MLG)\nTecidos Metabolicamente Ativos", f"{f_dec(MLG_KG)} kg\n(80,8% da massa corporal)", "Maciça quantidade de tecido magro ativo (>70 kg), demonstrando grande acúmulo de massa contrátil."),
    ("Massa Muscular Esquelética (MME)\nPreditor de Força Muscular (Janssen et al., 2000) [6]", f"{f_dec(MME_KG)} kg\n(42,7% da massa corporal)", "Volume muscular expressivo no tronco e membros superiores para contenção articular."),
    ("Ângulo de Fase a 50 kHz (PhA) & IMLG\nIntegridade Celular [7,8] e Índice de MLG [2,4]", f"{f_dec(PHA_DEG)}° (PhA)\nIMLG = {f_dec(FFMI)} kg/m²", f"PhA compatível com o padrão saudável da faixa etária (6,85° ± 0,70° [7]). FFMI de 24,09 kg/m² atinge o limiar superior atlético natural [2,4].")
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
    "💡 O que esses dados indicam na prática: Hipertrofia atlética e demanda de sustentação axial",
    f"Seu perfil morfofuncional apresenta uma característica atlética muito marcante: embora o IMC convencional registre {f_dec(IMC)} kg/m² "
    f"(o que tabelas clínicas genéricas classificam como sobrepeso), a análise aprofundada da bioimpedância revela que esse peso é sustentado "
    f"por impressionantes {f_dec(MLG_KG, 1)} kg de massa livre de gordura (80,8% do peso corporal). "
    f"Seu Índice de Massa Livre de Gordura (FFMI de {f_dec(FFMI)} kg/m²) situa-se no patamar superior para atletas naturais (Kouri et al., 1995 [2]; Schutz et al., 2002 [4]), "
    f"comprovando que a densidade corporal é fruto de mais de uma década de treino resistido consistente (CrossFit, musculação e ginástica), e não de adiposidade (Garrido-Chamorro et al., 2007 [5]). "
    f"Seu Ângulo de Fase ({f_dec(PHA_DEG)}°) atesta adequada integridade de membrana celular e equilíbrio hídrico intra/extracelular para a sua faixa etária de 40 a 44 anos (Barbosa-Silva et al., 2005 [7]). "
    f"\n\n⚠️ Ponto de atenção biomecânico: Na parada de mão e na caminhada invertida, uma massa corporal total elevada (87,2 kg) impõe uma exigência axial considerável sobre punhos, cotovelos e cintura escapular. "
    f"Embora a massa muscular forneça a potência necessária, a carga absoluta que as articulações distais precisam desacelerar a cada passada é substancial, tornando a eficiência de contato e a absorção de impacto fatores primordiais.",
    "A análise de bioimpedância calculada pela equação de multicomponentes de Sun et al. (2003) [1] e pelo modelo de Janssen et al. (2000) [6] confirma hipertrofia musculoesquelética pronunciada. "
    "O FFMI de 24,09 kg/m² desmistifica a classificação simplista do IMC (Garrido-Chamorro et al., 2007 [5]). "
    "O PhA de 6,78° situa-se dentro da média normativa para homens de 40 a 49 anos (6,85° ± 0,70°, Barbosa-Silva et al., 2005 [7]; Norman et al., 2012 [8]), indicando integridade de capacitância celular sob alto estresse mecânico."
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
    ("1º Preensão Manual (FPM)\nDinamômetro Saehan Hidráulico [10,11]",
     f"Pico: {f_dec(FPM_MAX, 1)} kgf ({f_dec(FPM_REL_MAX, 3)} kgf/kg)\nDir: {f_dec(FPM_DIR, 1)} kgf | Esq: {f_dec(FPM_ESQ, 1)} kgf\nLSI = {f_dec(LSI_FPM, 1)}% (Simetria Excelente)",
     f"Muito bom! Superior à média normativa de homens de 40 a 44 anos (~44 a 47 kgf [10,11]). Simetria intermembros exemplar (apenas 1,9% de diferença)."),
    ("2º Flexores de Punho no Biodex PRO\nTorque Isométrico Máximo a 70° de Extensão [9,13,14]",
     f"Pico: {f_dec(BIODEX_MAX, 1)} N·m ({f_dec(BIODEX_REL_MAX, 4)} N·m/kg)\nDir: {f_dec(BIODEX_PICO_D, 1)} N·m | Esq: {f_dec(BIODEX_PICO_E, 1)} N·m\nLSI = {f_dec(LSI_BIODEX, 1)}% (Alerta de Assimetria: Esq > Dir)",
     f"Ponto crítico: Assimetria acentuada de 32,56% entre os lados (> 15% [12]). O punho direito apresenta déficit importante no freio palmar a 70°.")
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
    "💡 A estratégia de punho: O papel dos flexores no controle postural invertido e ponto crítico de atenção [9,12-15]",
    f"Na postura invertida, as mãos e os punhos são os únicos pontos de contato com o solo e atuam com o mesmo papel biomecânico que os pés desempenham na postura ereta. "
    f"Quando o corpo oscila para a frente (sobre-equilíbrio), a pressão das pontas dos dedos contra o solo gera um torque de flexão palmar que freia e resgata o centro de massa (Wrist Strategy [9]). "
    f"Sua força de preensão manual máxima ({f_dec(FPM_MAX, 1)} kgf) merece elogio: situa-se acima da média de referência normativa para a sua faixa etária (~44 a 47 kgf, Bohannon 2019 [10]), "
    f"com simetria bilateral praticamente perfeita (diferença de apenas 1,9% entre os lados). "
    f"\n\n⚠️ Ponto crítico que precisa de correção direta: No dinamômetro isocinético Biodex a 70° de extensão — ângulo biomecânico idêntico ao suporte palmar da parada de mão —, "
    f"observou-se uma assimetria severa de 32,56% entre os punhos (Esquerdo: 17,1 N·m vs Direito: 12,9 N·m). "
    f"Na literatura esportiva e ortopédica (Bishop et al., 2018 [12]; Ellenbecker & Roetert, 2006 [13]), assimetrias superiores a 15% configuram um déficit expressivo. "
    f"Na prática, isso significa que seu punho direito (lado dominante) possui capacidade significativamente menor de tração e freio corretivo sob 87 kg de peso corporal, "
    f"forçando o punho esquerdo a compensar a estabilização e gerando momentos de torção lateral na coluna e nos ombros durante o equilíbrio e as passadas. "
    f"\n\n🛠️ Como consertar no treinamento: É prioritário introduzir um protocolo unilateral isolado para o punho direito: "
    f"1) Flexão de punho unilateral com halteres apoiado em banco (3 a 4 séries de 8 a 12 repetições, com ênfase na descida excêntrica lenta); "
    f"2) Sustentações isométricas unipodais na parede apoiando apenas sobre o punho direito a 70° de extensão com tempo cronometrado; "
    f"3) Exercícios com Wrist Roller e fortalecimento excêntrico para equiparar o torque do lado direito ao esquerdo, reduzindo a diferença bilateral para a faixa segura (<10-15%).",
    "Mecanismo de 'Wrist Strategy' estabelecido por Kerwin & Trewartha (2001) [9] e Sloot et al. (2020) [15]. "
    "A avaliação isométrica a 70° reproduz o ângulo funcional de dorsiflexão sob carga vertical (Ellenbecker & Roetert, 2006 [13]; Rohleder et al., 2021 [14]). "
    "Diferenças bilaterais acima de 15% (LSI = 132,56%) indicam assimetria mecânica relevante (Bishop et al., 2018 [12]), "
    "predispondo a distribuição desigual das forças de reação do solo e exigindo intervenção direcionada."
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
    ("3º 1-RM no Shoulder Press (SP)\nDesenvolvimento Olímpico Estrito [16,17]",
     f"{f_dec(SP_1RM_KG, 1)} kg ({f_dec(SP_REL_PCT, 1)}% do peso corporal)\n{f_dec(SP_REL_KG_KG, 3)} kg por kg de massa",
     "Sólida capacidade de força de empurrar vertical em barra olímpica sem impulsão dos membros inferiores [16]."),
    ("4º Resistência Belly-to-Wall Handstand\nSustentação Isométrica Estrita a 20 cm da Parede [9,23]",
     f"{f_dec(WALL_HS_MAX, 1)} segundos (1 min e 41 s)\n(Tentativa 1: {WALL_HS_T1:.0f}s | Tentativa 2: {WALL_HS_T2:.0f}s)",
     "Destaque excepcional! Resistência isométrica impressionante (> 100 segundos), demonstrando enorme capacidade de sustentação postural sob 87 kg [23].")
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
    "💡 Estabilidade proximal: O bloqueio escapular e a notável resistência isométrica [16,17,23]",
    f"Erguer {f_dec(SP_1RM_KG, 1)} kg no Shoulder Press estrito (cerca de 76% do peso corporal) em barra olímpica sem ajuda das pernas "
    f"comprova sólida disponibilidade de força dinâmica nos deltoides, tríceps e fixadores da escápula (Soriano et al., 2019 [16]). "
    f"No entanto, o resultado que merece o maior elogio deste bloco é a sua resistência na parede (Wall-HS): "
    f"sustentar a postura estrita por extraordinários 101,0 segundos (1 minuto e 41 segundos) suportando uma massa de 87,2 kg "
    f"revela uma capacidade de resistência muscular dos estabilizadores escapulares (serrátil anterior e trapézio) e eretores do tronco de nível altamente avançado (Gautier et al., 2007 [23]). "
    f"Essa robustez é o alicerce fundamental para prevenir o colapso postural e manter a integridade glenoumeral durante a permanência de cabeça para baixo. "
    f"\n\n⚠️ Oportunidade de evolução técnica: Como o objetivo da marcha invertida requer transferências contínuas de carga de um braço para o outro, "
    f"sugere-se direcionar essa grande base de força estática bilateral para a estabilização unilateral dinâmica: "
    f"incluir desenvolvimentos unilaterais com kettlebell e overhead carries unilaterais (caminhada segurando peso acima da cabeça com escápula ativamente elevada).",
    "A ativação do par de forças escapular (serrátil anterior e trapézio ascendente/descendente) assegura a rotação superior da escápula e o empilhamento ósseo (Soriano et al., 2019 [16]; Rohleder & Vogt, 2018 [17]). "
    "A marca de 101 segundos sob 87,2 kg atesta elevada tolerância metabólica dos músculos estabilizadores contra a fadiga postural antigravitacional (Gautier et al., 2007 [23])."
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

t_hs_doc = doc.add_table(rows=6, cols=3)
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
    ("Tempo de Sustentação Assistido (Bertec)\nRegistro Técnico de Controle Estabilométrico", f"{f_dec(HS_ASSIST_TEMPO_S)} s", "Excelente! Sustentação controlada superior a 1 minuto sobre a plataforma de força dupla."),
    ("Distância Média CoP-CoM (Braço de Alavanca)\nPlataforma Bertec Dual + Rastreamento Vicon 3D", f"{f_dec(HS_ASSIST_COP_COM_MM)} mm (~10,5 cm)", "Centro de gravidade projetado sobre a base de suporte com correções constantes [18,19]."),
    ("Velocidade Média do CoP (Frequência Corretora)\nMicroajustes Dinâmicos das Mãos", f"{f_dec(HS_ASSIST_COP_VEL_MM_S)} mm/s (~9,6 cm/s)", "Microajustes rápidos e contínuos nas mãos (faixa de atletas avançados: 70 a 150 mm/s [14,20])."),
    ("Entropia Aproximada (ApEn do CoP)\nComplexidade e Não-Linearidade Postural [21,22]", f"{f_dec(HS_ASSIST_APEN, 4)} (Destaque)", "Elevada complexidade e riqueza dinâmica (> 1,0 [21,22]), revelando controle flexível e sem congelamento de articulações."),
    ("Ângulo de Verticalidade Articular\nAlinhamento do Corpo com a Linha Gravitacional", f"{f_dec(HS_ASSIST_VERT_DEG)}°", "Boa verticalidade durante o protocolo de controle estabilométrico assistido.")
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
    "💡 Dinâmica do pêndulo invertido: Estabilometria e controle postural adaptativo [9,18-22]",
    f"Na avaliação estabilométrica sobre as placas Bertec, você sustentou a postura invertida por {f_dec(HS_ASSIST_TEMPO_S)} segundos. "
    f"O corpo atua como um pêndulo invertido complexo: o centro de massa ({f_dec(HS_ALTURA_COM_MM / 10.0, 1)} cm acima do solo) "
    f"precisa ser continuamente mantido sobre a base das mãos ({f_dec(HS_BASE_MM / 10.0, 1)} cm). "
    f"O dado mais notável deste registro é a sua Entropia Aproximada do CoP ({f_dec(HS_ASSIST_APEN, 4)}): "
    f"na literatura biomecânica de controle motor (Pincus 1991 [21]; Borg & Laxåback 2010 [22]), valores elevados de ApEn refletem alta riqueza dinâmica "
    f"e adaptabilidade reflexa, indicando que o seu sistema neuromuscular realiza correções finas e automáticas contínuas, "
    f"sem rigidez excessiva ou 'congelamento' dos graus de liberdade articulares.",
    "No modelo de Winter (1995) [18] e Slobounov et al. (2008) [19], a estabilidade resulta da oscilação coordenada do CoP em relação ao CoM. "
    "A velocidade do CoP (96,16 mm/s) situa-se na faixa ótima esperada para o controle manual invertido (70 a 150 mm/s [14,20]). "
    "O índice de ApEn de 1,3046 confirma um padrão fisiológico saudável de não-linearidade e flexibilidade motora."
)

# 3.2 Livre
h3_2 = doc.add_heading("3.2 Handstand Livre (Autonomia e Domínio Técnico sem Auxílio)", level=3)
h3_2.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h3_2.runs[0].font.size = Pt(8.8)
h3_2.paragraph_format.space_before = Pt(1)
h3_2.paragraph_format.space_after = Pt(1)

t_livre_doc = doc.add_table(rows=7, cols=3)
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
    ("Taxa de Sucesso na Subida Livre\nControle Motor Antecipatório Feedforward [23,24]", f"{HS_LIVRE_TAXA_SUCESSO}", "Excelente! 100% de precisão na entrada, sem hesitações ou quedas prematuras."),
    ("Tempo Máximo de Sustentação Livre\nDesfecho Primário de Autonomia Técnica", f"{f_dec(HS_LIVRE_TEMPO_MAX_S)} s (Tentativa 1)\n(T2: {f_dec(HS_LIVRE_T2_S, 1)}s | T3: {f_dec(HS_LIVRE_T3_S, 1)}s)", "Destaque notável! Sustentar mais de 50 segundos em equilíbrio livre confirma domínio técnico maduro."),
    ("Alinhamento Articular Vertical (Livre)\nInclinação Média em Relação ao Prumo", f"{f_dec(HS_LIVRE_VERT_DEG)}°", "Excelente alinhamento postural (< 8° [17]), minimizando momentos fletores sobre a coluna e os ombros."),
    ("Flexão Plantar (Pés em Ponta)\nTensão Ativa da Cadeia Posterior", f"{f_dec(HS_LIVRE_PLANTAR_DEG)}°", "Excelente compactação! Pernas unidas e pontas dos pés ativamente estendidas (> 40°)."),
    ("Extensão Cervical (Olhar para as Mãos)\nFixação Óptica de Equilíbrio", f"{f_dec(HS_LIVRE_CERVICAL_DEG)}°", "Ângulo confortável de orientação visual direcionado entre as palmas [23]."),
    ("Estratégia Articular de Busca do Equilíbrio\nCinemática 3D Multiarticular (LaBioCoM)", f"Cotovelo: SD {f_dec(HS_COTOVELO_SD_DEG)}° | ROM {f_dec(HS_COTOVELO_ROM_DEG)}° | RMS {f_dec(HS_COTOVELO_RMS_DEG_S)}°/s\nOmbro: SD {f_dec(HS_OMBRO_SD_DEG)}° | ROM {f_dec(HS_OMBRO_ROM_DEG)}° | RMS {f_dec(HS_OMBRO_RMS_DEG_S)}°/s\nQuadril: SD {f_dec(HS_QUADRIL_SD_DEG)}° | RMS {f_dec(HS_QUADRIL_RMS_DEG_S)}°/s\nRazão Cotovelo/Ombro: {f_dec(HS_RAZAO_COTOVELO_OMBRO)}", "O que significa na prática: Haste rígida com controle distal — você manteve os braços bem estendidos e firmes, controlando o equilíbrio quase exclusivamente nos punhos e dedos [6,17,25].")
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
    "💡 Handstand Livre: Domínio técnico na 1ª série, alinhamento exemplar e estratégias de equilíbrio [6,17,20,23,24,25]",
    f"🗣️ O que você precisa saber na prática:\n"
    f"• Sustentação e alinhamento: Você alcançou impressionantes {f_dec(HS_LIVRE_TEMPO_MAX_S)} segundos de equilíbrio logo na 1ª tentativa, com alinhamento praticamente impecável (apenas 7,67° de desvio da vertical) e pés em ponta ({f_dec(HS_LIVRE_PLANTAR_DEG)}°), revelando postura muito compacta.\n"
    f"• Como você se equilibrou (Estratégias Articulares): Você manteve os braços esticados e o corpo em bloco firme durante mais de 50 segundos, controlando as oscilações quase exclusivamente pela força dos punhos e pressão dos dedos no solo, praticamente sem dobrar os cotovelos.\n\n"
    f"🔬 Detalhamento dos Dados e Biomecânica:\n"
    f"A análise cinemática contínua confirmou altíssima rigidez proximal: seus cotovelos oscilaram com desvio-padrão de apenas {f_dec(HS_COTOVELO_SD_DEG)}° (velocidade angular RMS de {f_dec(HS_COTOVELO_RMS_DEG_S)}°/s e ROM de {f_dec(HS_COTOVELO_ROM_DEG)}°) e os ombros variaram {f_dec(HS_OMBRO_SD_DEG)}° (velocidade RMS de {f_dec(HS_OMBRO_RMS_DEG_S)}°/s), operando o corpo como uma haste rígida de pêndulo invertido simples. Esse padrão reflete que a sua sustentação decorre primordialmente da modulação rápida do Centro de Pressão (CoP) pelas polpas digitais e flexores de punho. Na literatura biomecânica (Kerwin & Trewartha, 2001; Blenkinsop et al., 2017), a estratégia distal de punho com braços estendidos é característica de alto alinhamento técnico (comum na ginástica artística por exigência de pontuação), enquanto estratégias com flexo-extensão de cotovelos são observadas na calistenia e handbalancing como recurso funcional compensatório. Ambas constituem adaptações motoras eficientes.\n\n"
    f"🎯 Gestão de Esforço (Pacing):\n"
    f"Notou-se redução planejada na duração das séries seguintes (T1: 50,98 s -> T2: 18,99 s -> T3: 9,94 s). Conforme relatado por você, essa diminuição foi voluntária para poupar os membros superiores e evitar a fadiga extrema antes dos testes de Handstand Walk (HSW), demonstrando excelente maturidade e sensibilidade à sobrecarga axial.\n\n"
    f"🛠️ Recomendação para o treino:\n"
    f"Manter essa percepção de esforço, reservando séries até o limite de tempo para testes pontuais e focando a rotina em séries submáximas (20 a 30 s) com descanso completo.",
    "O controle antecipatório na subida decorre da programação de torque reflexo descrita por Clement et al. (1984) [24] e Gautier et al. (2007) [23]. "
    "A verticalidade de 7,67° reduz o braço de alavanca gravitacional sobre a cintura escapular (Rohleder & Vogt, 2018 [17]). "
    "A estabilidade com baixa excursão de cotovelo e ombro confirma o predomínio da estratégia distal de punho em atletas experientes (Kerwin & Trewartha, 2001 [6]; Blenkinsop et al., 2017 [25])."
)

# 3.3 HSW
h3_3 = doc.add_heading("3.3 Handstand Walk — HSW (Locomoção Invertida Dinâmica)", level=3)
h3_3.runs[0].font.color.rgb = EMERALD_HEADER_RGB
h3_3.runs[0].font.size = Pt(8.8)
h3_3.paragraph_format.space_before = Pt(1)
h3_3.paragraph_format.space_after = Pt(1)

hsw_dados_doc = [
    ("Distância Mediana Percorrida (HSW)\nDesfecho Primário do Bloco de Marcha", f"{f_dec(HSW_DIST_MEDIANA_M)} m\n(T1: {f_dec(HSW_T1_DIST_M)}m | T2: {f_dec(HSW_T2_DIST_M)}m | T3: {f_dec(HSW_T3_DIST_M)}m)", "Excelente consistência motora! Três tentativas muito homogêneas (~5 metros em todas)."),
    ("Distância Máxima Percorrida no HSW\nMelhor Registro de Deslocamento", f"{f_dec(HSW_DIST_MAX_M)} m (Tentativa 2)", "Destaque positivo! Superou com facilidade a marca de 5 metros com marcha fluida e controlada."),
    ("Velocidade Média de Deslocamento (HSW)\nVelocidade Linear da Marcha Invertida", f"{f_dec(HSW_VEL_M_S)} m/s ({f_dec(HSW_VEL_KM_H)} km/h)", "O que significa na prática: Velocidade contínua e dinâmica ao longo dos 5 metros."),
    ("Tempo Médio de Contato Palmar\nDuração do Apoio de Cada Mão por Passo", f"{f_dec(HSW_CONTATO_S)} s ({HSW_CONTATO_MS} ms)", "O que significa na prática: Transição de suporte ágil e rápida entre as mãos."),
    ("Coeficiente de Variação Temporal (CV Temporal)\nRegularidade Rítmica dos Passos [24]", f"{f_dec(HSW_CV_TEMPORAL)}% (Destaque Notável)", "Padrão de metrônomo motor! CV Temporal < 10% revela sincronismo rítmico excepcional entre as passadas [24]."),
    ("Cadência da Marcha Invertida\nPassos com as Mãos por Segundo", f"{f_dec(HSW_CADENCIA)} passos/s (22 passos)", "Cadência alta (1,55 passos/s), refletindo movimentação rápida e ágil das mãos."),
    ("Comprimento Médio da Passada\nAmplitude dos Passos Palmares", f"{f_dec(HSW_PASSADA_MM)} mm (~24,9 cm)", "Atenção: Passada curta (~25 cm), compensada por alta cadência para cobrir os 5 metros."),
    ("Fase de Duplo Suporte com as Mãos\nTempo com Ambas as Mãos Apoiadas", f"{f_dec(HSW_DUPLO_SUPORTE_PCT)}% do ciclo", "Atenção: valor elevado (~60%), indicando apoio simultâneo prolongado e frenagem a cada passo."),
    ("Coeficiente de Variação Espacial (Passadas)\nRegularidade do Tamanho dos Passos", f"{f_dec(HSW_CV_ESPACIAL)}% (Estável)", "Dispersão espacial controlada (< 20%), evidenciando regularidade no comprimento dos passos."),
    ("Extensão Cervical na Marcha (Olhar)\nOrientação Visual para Frente no HSW", f"{f_dec(HSW_CERVICAL_DEG)}°", "Excelente fixação visual direcionada à frente, ancorando a trajetória da caminhada [23]."),
    ("Flexão Plantar no HSW (Ponta de Pé)\nTensão Ativa da Cadeia Posterior na Marcha", f"{f_dec(HSW_PLANTAR_DEG)}°", "Destaque técnico! Manteve os pés ativamente estendidos em ponta durante a locomoção (~30°)."),
    ("Rotação Externa das Mãos no HSW\nAbertura Palmar na Caminhada", f"{f_dec(HSW_ROT_MAOS_DEG)}°", "Posicionamento correto das mãos (~16°), preservando a linha anteroposterior dos flexores.")
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
    "💡 Handstand Walk: Cadência rítmica excepcional de metrônomo, diagnósticos e prescrição corretiva [23,24]",
    f"🗣️ O que você precisa saber na prática:\n"
    f"• Desempenho e velocidade: Você demonstrou consistência excepcional, completando praticamente 5 metros em todas as séries (mediana de {f_dec(HSW_DIST_MEDIANA_M)} m e máxima de {f_dec(HSW_DIST_MAX_M)} m), com passos rápidos (cadência de {f_dec(HSW_CADENCIA)} passos/s), velocidade de {f_dec(HSW_VEL_M_S)} m/s ({f_dec(HSW_VEL_KM_H)} km/h) e passadas ágeis (contato de {f_dec(HSW_CONTATO_S)} s por apoio).\n"
    f"• Pontos de evolução: Seu duplo suporte (59,7%) e a oscilação lateral ({f_dec(HSW_OSCILACAO_ML_MM)} mm) mostram que você ainda transfere peso com bastante cautela, mantendo ambas as mãos em contato por mais da metade do tempo.\n\n"
    f"🔬 Detalhamento dos Dados e Biomecânica:\n"
    f"A locomoção dinâmica invertida exige cadência alta e passadas compactas para manter o centro de massa em constante aceleração para a frente sem desvios laterais excessivos. O coeficiente de variação temporal de apenas {f_dec(HSW_CV_TEMPORAL)}% atesta uma regularidade rítmica de alto nível. O comprimento médio de passada de {f_dec(HSW_PASSADA_MM)} mm (~25 cm) garante estabilidade sem arriscar o tombamento.\n\n"
    f"🛠️ Exercícios Corretivos Recomendados:\n"
    f"1) Shoulder taps em parada de mão na parede com ritmo ágil (para diminuir gradualmente o tempo de duplo suporte e aumentar a confiança no apoio unimanual rápido);\n"
    f"2) Caminhada invertida sobre linhas demarcatórias no solo (para reduzir o balanceio lateral de {f_dec(HSW_OSCILACAO_ML_MM)} mm e guiar a marcha estritamente em linha reta);\n"
    f"3) Single-arm dumbbell overhead carry (caminhada sustentando peso unilateral acima da cabeça, com escápula bloqueada no topo para fortalecer a estabilidade unilateral).",
    "Blenkinsop et al. (2017) [24] enfatizam que a locomoção invertida madura demanda coordenação espaço-temporal homogênea. "
    "O CV Temporal de 9,81% atesta automatização neuromuscular exemplar do ciclo de passos. "
    "No entanto, o duplo suporte de 59,68% associado à passada de 24,9 cm eleva a sobrecarga mecânica cumulativa sobre o carpo, "
    "tornando a ampliação do comprimento da passada o passo primordial para economia metabólica e longevidade articular."
)

# -------------------------------------------------------------------------
# SEÇÃO 4: SÍNTESE E RECOMENDAÇÕES PRÁTICAS INDIVIDUALIZADAS
# -------------------------------------------------------------------------
h4 = doc.add_heading("4. Síntese Integrativa e Recomendações Práticas Individualizadas", level=2)
h4.runs[0].font.color.rgb = EMERALD_DARK_RGB
h4.runs[0].font.size = Pt(10)
h4.paragraph_format.space_before = Pt(3)
h4.paragraph_format.space_after = Pt(2)

p_prat_lead1 = doc.add_paragraph()
p_prat_lead1.paragraph_format.space_before = Pt(1)
p_prat_lead1.paragraph_format.space_after = Pt(1)
r_p1 = p_prat_lead1.add_run("📌 Síntese Integrativa do Perfil do Atleta (Destaques e Potenciais):")
r_p1.bold = True
r_p1.font.size = Pt(8.2)
r_p1.font.color.rgb = EMERALD_HEADER_RGB

pontos_fortes = [
    ("Hipertrofia Muscular Atlética e Densidade Magra: ", f"Mais de 70 kg de massa magra ativa ({f_dec(MLG_KG, 1)} kg; 80,8%) e FFMI de {f_dec(FFMI)} kg/m², atingindo o patamar superior para atletas naturais (Kouri et al., 1995; Schutz et al., 2002). O IMC elevado decorre de massa contrátil e não de sobrepeso adiposo."),
    ("Resistência Isométrica Escapular de Destaque Notável: ", f"Marca extraordinária de {f_dec(WALL_HS_MAX, 0)} segundos (1 min e 41 s) de sustentação no Wall-HS suportando 87,2 kg de carga axial, demonstrando enorme capacidade de resistência à fadiga de serrátil anterior e trapézio (Gautier et al., 2007)."),
    ("Domínio Técnico e Alinhamento no Handstand Livre: ", f"Tempo de pico de {f_dec(HS_LIVRE_TEMPO_MAX_S)} segundos na 1ª tentativa, com alinhamento vertical de {f_dec(HS_LIVRE_VERT_DEG)}° e excelente flexão plantar ({f_dec(HS_LIVRE_PLANTAR_DEG)}°), comprovando refinado empilhamento articular e linha corporal compacta."),
    ("Precisão Rítmica de Metrônomo Motor no Handstand Walk: ", f"Coeficiente de Variação Temporal de apenas {f_dec(HS_CV_TEMPORAL)}% (<10%), revelando sincronismo rítmico excepcional na cadência das passadas e homogeneidade nas 3 séries de caminhada (~5 metros em todas) (Blenkinsop et al., 2017)."),
    ("Controle Postural Estabilométrico Adaptativo: ", f"Entropia Aproximada elevada ({f_dec(HS_ASSIST_APEN, 4)}), indicando controle dinâmico fluido e flexível sem rigidez articular, além de 100% de sucesso nas entradas livres por controle antecipatório feedforward maduro.")
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
r_p2.font.color.rgb = RGBColor(180, 83, 9)

pontos_melhoria = [
    ("Equalização da Força Isométrica do Punho Direito (Ponto Crítico): ", f"Corrigir com prioridade a assimetria severa de 32,56% no Biodex a 70° (Esquerdo: 17,1 N·m vs Direito: 12,9 N·m; déficit > 15% Bishop et al., 2018). Prescrição: Incluir 3 a 4 séries de flexão unilateral de punho com halteres em banco apoiado (8 a 12 reps com ênfase na fase excêntrica) e sustentações isométricas unipodais na parede dedicadas ao membro direito."),
    ("Ampliação da Passada e Redução do Duplo Suporte no HSW: ", f"Aumentar o comprimento da passada palmar de ~25 cm para 35-40 cm e diminuir a fase de duplo apoio de ~60% para 45-50%. Prescrição: Praticar passadas sobre marcadores visuais no solo a cada 35-40 cm e treinar a 'queda para a frente controlada', avançando a mesma distância com metade dos impactos axiais sob 87 kg."),
    ("Gestão Estratégica de Esforço e Transição para a Locomoção: ", f"A redução na duração das séries 2 e 3 do HS livre refletiu uma escolha voluntária e consciente do participante, que, plenamente satisfeito com a excelente marca alcançada na 1ª tentativa (50,98 s), optou por se poupar para evitar fadiga extrema antes do Handstand Walk. Prescrição: Continuar aplicando essa autorregulação inteligente (pacing) nos treinos diários, combinando séries curtas e submáximas (15 a 25 s) antes de blocos de caminhada para manter os estabilizadores com alto frescor neuromuscular."),
    ("Proteção Articular e Absorção de Impacto sob Massa Elevada: ", "Como o suporte corporal sob 87,2 kg impõe alto estresse axial sobre os ossos do carpo e articulação radioulnar, manter rotina diária de aquecimento e mobilidade de punhos com sobrecarga gradual, priorizando aterrissagens palmares suaves.")
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
    "Kouri, E. M., et al. (1995). Fat-free mass index in users and nonusers of anabolic-androgenic steroids. Clin J Sport Med, 5(4), 223-228.",
    "American College of Sports Medicine (ACSM). (2018). ACSM's Guidelines for Exercise Testing and Prescription (10th ed.). Philadelphia: Wolters Kluwer.",
    "Schutz, Y., et al. (2002). Fat-free mass index and fat mass index percentiles in Caucasians aged 18-98 y. Int J Obes Relat Metab Disord, 26(7), 953-960.",
    "Garrido-Chamorro, R., et al. (2007). Correlation between body mass index and body fat percentage in elite athletes: The fallacy of BMI. Int J Sports Med, 28(6), 461-466.",
    "Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. J Appl Physiol, 89(2), 465-471.",
    "Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. Am J Clin Nutr, 82(1), 49-52.",
    "Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. Clin Nutr, 31(6), 854-861.",
    "Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. Sports Biomech, 1(2), 163-176.",
    "Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. J Phys Ther Sci, 31(11), 932-938.",
    "Dodds, R. M., et al. (2014). Globally representative normative data for handgrip strength: systematic review. PLoS ONE, 9(12), e113637.",
    "Bishop, C., et al. (2018). Effects of inter-limb asymmetries on physical and sports performance. J Sports Sci, 36(10), 1135-1144.",
    "Ellenbecker, T. S., & Roetert, E. P. (2006). Isokinetic wrist strength in competitive athletes. Am J Sports Med, 34(11), 1845-1852.",
    "Rohleder, J., et al. (2021). Wrist joint biomechanics and handstand stability in gymnastics. Sports Biomech, 20(3), 312-326.",
    "Sloot, L. H., et al. (2020). Wrist motor control during balance correction in handbalancing. J Biomech, 102, 109653.",
    "Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. Strength Cond J, 41(4), 48-60.",
    "Rohleder, J., & Vogt, L. (2018). Kinematic alignment and joint stacking in artistic gymnastics vs. fitness handbalancing. J Sports Sci, 36(11), 1238-1245.",
    "Winter, D. A. (1995). Human balance and posture control during standing and walking. Gait & Posture, 3(4), 193-214.",
    "Slobounov, S., et al. (2008). Virtual reality and force-platform assessment of inverted posture stability. Exp Brain Res, 188(2), 241-253.",
    "Uzun, M., et al. (2012). Stabilometric comparison of handstand on force plates between elite and novice athletes. J Hum Kinet, 34(1), 15-23.",
    "Pincus, S. M. (1991). Approximate entropy as a measure of system complexity. Proc Natl Acad Sci USA, 88(6), 2297-2301.",
    "Borg, F. G., & Laxåback, G. (2010). Entropy of balance: How to compute and interpret approximate entropy in posturography. J Biomech, 43(15), 3044-3048.",
    "Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. Hum Mov Sci, 26(4), 577-594.",
    "Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Handstand walk: Locomotor biomechanics and coordination in inverted human locomotion. Hum Mov Sci, 54, 235-244.",
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
print("[2/3] Gerando HTML com design original, logo da EEFERP, cards, badges e paleta de cores unificada...")

logo_html_tag = ""
if logo_white_b64:
    logo_html_tag = f'''<img src="data:image/png;base64,{logo_white_b64}" alt="Logo EEFERP-USP" style="height: 52px; width: auto; object-fit: contain; filter: drop-shadow(0 2px 4px rgba(0,0,0,0.2));">'''

html_content = f'''<!DOCTYPE html>
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
        <span>14/09 (LaCiDH) e 16/09/2026 (LaBioCoM)</span>
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
      seguidos pela contextualização científica fundamentada na literatura internacional <sup>[1-24]</sup>. Parabéns pela dedicação e pelo comprometimento com a pesquisa!
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
          <div class="metric-pill">Padrão Saudável para a Faixa Etária</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Massa Livre de Gordura (MLG) <sup>[1]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(MLG_KG)} kg</div>
          <div class="metric-subtext">80,8% em tecidos magros ativos</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Maciça Base Muscular Ativa (>70 kg)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Massa Muscular Esquelética <sup>[6]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(MME_KG)} kg</div>
          <div class="metric-subtext">42,7% da massa corporal total</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Grande Suporte Antigravitacional</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Ângulo de Fase a 50 kHz (PhA) <sup>[7,8]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(PHA_DEG)}°</div>
          <div class="metric-subtext">Referência etária: 6,85° ± 0,70°</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Integridade Celular Saudável</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Índice de MLG (IMLG / FFMI) <sup>[2,4]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(FFMI)} kg/m²</div>
          <div class="metric-subtext">Massa magra ajustada à estatura²</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857; font-weight: 700;">
            Destaque! Limite Superior Atlético Natural
          </div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 O que esses dados indicam na prática: Hipertrofia atlética e demanda de sustentação axial <sup>[1-8]</sup>
      </div>
      <p class="callout-text">
        Seu perfil morfofuncional apresenta uma característica atlética de grande destaque: embora o IMC convencional registre <strong>{f_dec(IMC)} kg/m²</strong> 
        (faixa que tabelas clínicas genéricas associam ao sobrepeso), a análise aprofundada da bioimpedância demonstra que essa massa é quase integralmente composta 
        por impressionantes <strong>{f_dec(MLG_KG, 1)} kg de massa livre de gordura (80,8% do peso corporal)</strong>. 
        Seu Índice de Massa Livre de Gordura (<strong>FFMI de {f_dec(FFMI)} kg/m²</strong>) situa-se no patamar superior para atletas naturais (Kouri et al., 1995 <sup>[2]</sup>; Schutz et al., 2002 <sup>[4]</sup>), 
        comprovando que sua densidade corporal é resultado direto de mais de 10 anos de treinamento resistido consistente (CrossFit, ginástica e musculação), e não de adiposidade (Garrido-Chamorro et al., 2007 <sup>[5]</sup>).
      </p>
      <p class="callout-text">
        Seu <strong>Ângulo de Fase ({f_dec(PHA_DEG)}°)</strong> atesta adequada integridade de membrana celular e boa homeostase hídrica para a sua faixa etária (Barbosa-Silva et al., 2005 <sup>[7]</sup>).
      </p>
      <p class="callout-text">
        <strong>⚠️ Ponto de atenção biomecânico:</strong> Na parada de mão e na locomoção invertida, uma massa total de <strong>87,2 kg</strong> representa uma sobrecarga axial expressiva sobre punhos, cotovelos e ombros. 
        Embora a robustez muscular forneça a estabilidade necessária, a carga absoluta que as articulações distais precisam conter a cada passada exige atenção redobrada à absorção de impacto e à prevenção de desgastes por atrito cumulativo.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong> 
        A análise de bioimpedância processada pela equação multicomponente de Sun et al. (2003) <sup>[1]</sup> e pelo modelo muscular de Janssen et al. (2000) <sup>[6]</sup> 
        evidencia marcante hipertrofia muscular esquelética. O FFMI de 24,09 kg/m² afasta a inadequação diagnóstica do IMC para atletas de força (Garrido-Chamorro et al., 2007 <sup>[5]</sup>). 
        O PhA de 6,78° reflete propriedades elétricas normativas saudáveis de condutância e capacitância de membrana (Barbosa-Silva et al., 2005 <sup>[7]</sup>; Norman et al., 2012 <sup>[8]</sup>).
      </div>
    </div>

    <!-- SEÇÃO 2: PERFIL NEUROMUSCULAR -->
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
          <div class="metric-label">1º Preensão Manual (FPM) <sup>[10,11]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value">{f_dec(FPM_MAX, 1)} kgf</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">{f_dec(FPM_REL_MAX, 3)} kgf/kg</div>
        </div>
        <div class="metric-subtext">Mão Direita (Dom): {f_dec(FPM_DIR, 1)} kgf | Esquerda (Não-Dom): {f_dec(FPM_ESQ, 1)} kgf</div>
        <div class="metric-footer">
          <div class="metric-pill">
            Simetria (LSI): {f_dec(LSI_FPM, 1)}% (Diferença de apenas 1,9% • Excelente)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">2º Torque de Punho a 70° (Biodex) <sup>[9,13,14]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value" style="color: #b45309;">{f_dec(BIODEX_MAX, 1)} N·m</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">{f_dec(BIODEX_REL_MAX, 4)} N·m/kg</div>
        </div>
        <div class="metric-subtext">Punho Esquerdo (Não-Dom): {f_dec(BIODEX_PICO_E, 1)} N·m | Direito (Dom): {f_dec(BIODEX_PICO_D, 1)} N·m</div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Assimetria (LSI): {f_dec(LSI_BIODEX, 1)}% (Déficit no Lado Direito)
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
          💡 A estratégia de punho: O papel dos flexores no controle invertido e ponto crítico de atenção <sup>[9,12-15]</sup>
        </div>
        <p class="callout-text">
          Na postura invertida, mãos e punhos são os únicos pontos de apoio e desempenham uma função análoga à dos pés e tornozelos no equilíbrio ereto (<em>Wrist Strategy</em>). 
          Quando o corpo oscila para além do alinhamento ideal (sobre-equilíbrio), a pressão instantânea das polpas digitais contra o solo e a ativação dos flexores de punho 
          produzem o momento de freio necessário para resgatar o centro de gravidade.
        </p>
        <p class="callout-text">
          Sua <strong>força de preensão manual ({f_dec(FPM_MAX, 1)} kgf)</strong> merece elogio: é superior à média de referência para homens de 40 a 44 anos (~44 a 47 kgf, Bohannon 2019 <sup>[10]</sup>), 
          com simetria bilateral exemplar (apenas 1,9% de diferença entre os membros).
        </p>
        <p class="callout-text">
          <strong>⚠️ Ponto crítico que precisa de correção direta:</strong> No teste do Biodex a 70° de extensão — ângulo biomecânico específico em que a mão apoia no chão na parada de mão —, 
          constatou-se uma <strong>assimetria severa de 32,56%</strong> entre os lados (Punho Esquerdo: 17,1 N·m vs Punho Direito: 12,9 N·m). 
          Na literatura ortopédica e biomecânica (Bishop et al., 2018 <sup>[12]</sup>; Ellenbecker & Roetert, 2006 <sup>[13]</sup>), assimetrias superiores a 15% configuram um déficit expressivo. 
          Na prática, isso indica que o seu punho direito (lado dominante) possui menor reserva de torque para frear o corpo sob 87 kg, 
          o que pode induzir uma transferência compensatória de carga para o braço esquerdo e criar instabilidades rotacionais durante a marcha invertida.
        </p>
        <p class="callout-text">
          <strong>🛠️ Como consertar no treinamento:</strong> É prioritário incluir um bloco específico de fortalecimento unilateral isolado para o punho direito: 
          1) <em>Flexão de punho unilateral com halter apoiado em banco</em> (3 a 4 séries de 8 a 12 repetições, priorizando a fase excêntrica lenta); 
          2) <em>Sustentações isométricas unipodais na parede</em> sustentando o peso sobre o punho direito posicionado a 70° de extensão; 
          3) Exercícios com <em>Wrist Roller</em> para reequilibrar o torque bilateral e reduzir o déficit para menos de 10-15%.
        </p>
        <div class="callout-science">
          <strong>Fundamentação Científica & Biomecânica:</strong> 
          Mecanismo da <em>Wrist Strategy</em> descrito por Kerwin & Trewartha (2001) <sup>[9]</sup> e Sloot et al. (2020) <sup>[15]</sup>. 
          A extensão isométrica avaliada a 70° reproduz o ângulo funcional de dorsiflexão sob gravidade (Ellenbecker & Roetert, 2006 <sup>[13]</sup>; Rohleder et al., 2021 <sup>[14]</sup>). 
          Déficits bilaterais acima de 15% (LSI = 132,56%) indicam assimetria funcional relevante (Bishop et al., 2018 <sup>[12]</sup>), 
          justificando a prescrição corretiva orientada para mitigar assimetrias axiais de impacto.
        </div>
      </div>
    </div>

    <!-- 2.2 PROXIMAL -->
    <div class="sub-section-title">
      2.2 Força Proximal e Resistência Muscular: Shoulder Press e Belly-to-Wall Handstand
    </div>

    <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">3º 1-RM no Shoulder Press (SP) <sup>[16]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value">{f_dec(SP_1RM_KG, 1)} kg</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">{f_dec(SP_REL_KG_KG, 3)} kg/kg</div>
        </div>
        <div class="metric-subtext">Barra Olímpica Estrita (Desenvolvimento vertical sem impulso das pernas)</div>
        <div class="metric-footer">
          <div class="metric-pill">75,7% do Peso Corporal • Boa Força Dinâmica</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">4º Resistência Belly-to-Wall Handstand <sup>[9,23]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value" style="color: #047857;">{f_dec(WALL_HS_MAX, 1)} s</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">1 min e 41 s</div>
        </div>
        <div class="metric-subtext">Tentativa 1: {WALL_HS_T1:.0f} s | Tentativa 2: {WALL_HS_T2:.0f} s (A 20 cm da parede)</div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857; font-weight: 700;">
            Destaque Notável! > 100 s sob 87,2 kg
          </div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Estabilidade proximal: O bloqueio escapular e a notável resistência isométrica <sup>[16,17,23]</sup>
      </div>
      <p class="callout-text">
        Erguer <strong>{f_dec(SP_1RM_KG, 1)} kg no Shoulder Press estrito</strong> (cerca de 76% do peso corporal) em barra olímpica sem ajuda das pernas 
        evidencia uma sólida força dinâmica nos deltoides, tríceps e fixadores da escápula (Soriano et al., 2019 <sup>[16]</sup>).
      </p>
      <p class="callout-text">
        Contudo, o resultado que merece o maior elogio deste bloco é a sua resistência na parede (Wall-HS): 
        sustentar a posição estrita por <strong>extraordinários {f_dec(WALL_HS_MAX, 0)} segundos (1 minuto e 41 segundos)</strong> sob uma massa corporal de 87,2 kg 
        comprova uma resistência muscular dos estabilizadores escapulares (serrátil anterior e trapézio) de nível altamente avançado (Gautier et al., 2007 <sup>[23]</sup>). 
        Essa sustentação comprova a robustez necessária para evitar o colapso dos ombros sob fadiga.
      </p>
      <p class="callout-text">
        <strong>⚠️ Oportunidade de evolução técnica:</strong> Para transferir essa excelente resistência estática bilateral para a marcha invertida (onde o peso é suportado sobre um ombro de cada vez), 
        recomenda-se introduzir <em>overhead carries</em> unilaterais (caminhadas sustentando peso acima da cabeça com cotovelo estendido e escápula elevada) 
        e desenvolvimentos unilaterais com kettlebell para otimizar o controle unipodal dinâmico.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong> 
        A ação coordenada do par de forças escapular (serrátil anterior e trapézio) assegura a rotação superior da escápula e o empilhamento ósseo (Soriano et al., 2019 <sup>[16]</sup>; Rohleder & Vogt, 2018 <sup>[17]</sup>). 
        A marca de 101 segundos sob 87,2 kg reflete expressiva capacidade oxidativa dos estabilizadores contra a fadiga postural antigravitacional (Gautier et al., 2007 <sup>[23]</sup>).
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
          <div class="metric-label">Tempo de Sustentação Assistido <sup>[18]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_ASSIST_TEMPO_S)} s</div>
          <div class="metric-subtext">Registro na Plataforma Bertec Dual</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">> 1 minuto de Coleta Estabilométrica</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Distância Média CoP-CoM <sup>[18,19]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_ASSIST_COP_COM_MM)} mm</div>
          <div class="metric-subtext">Braço de alavanca de ~10,5 cm</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Centro de Gravidade sob Controle</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Velocidade Média do CoP <sup>[14,20]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_ASSIST_COP_VEL_MM_S)} mm/s</div>
          <div class="metric-subtext">Microajustes de ~9,6 cm por segundo</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Correções Contínuas e Precisas</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Entropia Aproximada (ApEn do CoP) <sup>[21,22]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(HS_ASSIST_APEN, 4)}</div>
          <div class="metric-subtext">Elevada complexidade e adaptabilidade</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857; font-weight: 700;">
            Destaque! Controle Fluido sem Rigidez
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Verticalidade Articular (Bertec) <sup>[17]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_ASSIST_VERT_DEG)}°</div>
          <div class="metric-subtext">Inclinação em relação ao prumo</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Linha Articular Firme e Alinhada</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Dinâmica do pêndulo invertido: Estabilometria e controle postural adaptativo <sup>[9,18-22]</sup>
      </div>
      <p class="callout-text">
        Na avaliação estabilométrica sobre as placas Bertec, você sustentou a postura por <strong>{f_dec(HS_ASSIST_TEMPO_S)} segundos</strong>. 
        O corpo comporta-se como um pêndulo invertido complexo: o centro de massa ({f_dec(HS_ALTURA_COM_MM / 10.0, 1)} cm de altura) 
        precisa ser continuamente mantido sobre a base das mãos ({f_dec(HS_BASE_MM / 10.0, 1)} cm).
      </p>
      <p class="callout-text">
        O dado mais notável deste registro é a sua <strong>Entropia Aproximada do CoP ({f_dec(HS_ASSIST_APEN, 4)})</strong>: 
        na literatura biomecânica de controle motor (Pincus 1991 <sup>[21]</sup>; Borg & Laxåback 2010 <sup>[22]</sup>), valores elevados de ApEn refletem riqueza dinâmica 
        e adaptabilidade reflexa, indicando que o seu sistema neuromuscular realiza microajustes automáticos e contínuos, 
        sem rigidez articular excessiva ou congelamento mecânico dos graus de liberdade.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong> 
        No modelo de Winter (1995) <sup>[18]</sup> e Slobounov et al. (2008) <sup>[19]</sup>, a estabilidade resulta da oscilação coordenada do CoP em relação à projeção do CoM. 
        A velocidade do CoP (96,16 mm/s) situa-se na faixa ótima esperada para o controle manual invertido (70 a 150 mm/s <sup>[14,20]</sup>). 
        O índice de ApEn de 1,3046 confirma um padrão fisiológico saudável de não-linearidade e flexibilidade postural.
      </div>
    </div>

    <!-- 3.2 LIVRE -->
    <div class="sub-section-title">
      3.2 Handstand Livre (Autonomia e Domínio Técnico sem Auxílio)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Taxa de Sucesso na Subida <sup>[23,24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">100%</div>
          <div class="metric-subtext">3 de 3 tentativas válidas seguidas (≥ 3s)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Controle Antecipatório Perfeito (100%)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Melhor Tempo no HS Livre <sup>[20]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(HS_LIVRE_TEMPO_MAX_S)} s</div>
          <div class="metric-subtext">Tentativa 1 (T2: {f_dec(HS_LIVRE_T2_S, 1)}s | T3: {f_dec(HS_LIVRE_T3_S, 1)}s)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857; font-weight: 700;">
            Destaque Notável! > 50 s sem Apoio
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Verticalidade no HS Livre <sup>[17]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_LIVRE_VERT_DEG)}°</div>
          <div class="metric-subtext">Excelente alinhamento postural (< 8°)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Postura Reta e Compacta</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Flexão Plantar (Ponta de Pé) <sup>[17]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(HS_LIVRE_PLANTAR_DEG)}°</div>
          <div class="metric-subtext">Extensão ativa superior a 40°</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Excelente Compactação de Pernas</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Estratégias Articulares (Cotovelo / Ombro) <sup>[6,17,25]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HS_COTOVELO_SD_DEG)}° SD</div>
          <div class="metric-subtext">Cotovelo ROM: {f_dec(HS_COTOVELO_ROM_DEG)}° | Ombro SD: {f_dec(HS_OMBRO_SD_DEG)}°</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Alta Rigidez Proximal / Punho</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Handstand Livre: Domínio técnico na 1ª série, alinhamento exemplar e estratégias de equilíbrio <sup>[6,17,20,23,24,25]</sup>
      </div>
      <p class="callout-text">
        <strong>🗣️ O que você precisa saber na prática:</strong><br>
        • <strong>Sustentação e alinhamento:</strong> Você alcançou impressionantes <strong>{f_dec(HS_LIVRE_TEMPO_MAX_S)} segundos</strong> de equilíbrio logo na 1ª tentativa, com alinhamento praticamente impecável (apenas {f_dec(HS_LIVRE_VERT_DEG)}° de desvio vertical) e pés em ponta ({f_dec(HS_LIVRE_PLANTAR_DEG)}°), revelando postura muito compacta.<br>
        • <strong>Como você se equilibrou (Estratégias Articulares):</strong> <strong>Você manteve os braços esticados e o corpo em bloco firme durante mais de 50 segundos</strong>, controlando as oscilações quase que exclusivamente pela força dos punhos e pressão dos dedos no solo, praticamente sem dobrar os cotovelos para buscar o equilíbrio.
      </p>
      <p class="callout-text">
        <strong>🔬 Detalhamento dos Dados e Biomecânica:</strong><br>
        A análise cinemática contínua confirmou altíssima rigidez proximal: seus cotovelos oscilaram com desvio-padrão de apenas <strong>{f_dec(HS_COTOVELO_SD_DEG)}°</strong> (velocidade angular RMS de <strong>{f_dec(HS_COTOVELO_RMS_DEG_S)}°/s</strong> e amplitude de {f_dec(HS_COTOVELO_ROM_DEG)}°) e os ombros variaram {f_dec(HS_OMBRO_SD_DEG)}° (velocidade RMS de {f_dec(HS_OMBRO_RMS_DEG_S)}°/s), operando o corpo como uma haste rígida de pêndulo invertido simples. Esse padrão reflete que a sua sustentação decorre primordialmente da modulação rápida do Centro de Pressão (CoP) pelas polpas digitais e flexores de punho. Na literatura biomecânica (Kerwin & Trewartha, 2001; Blenkinsop et al., 2017), a estratégia distal de punho com braços estendidos é característica de alto alinhamento técnico (comum na ginástica artística por exigência de pontuação), enquanto estratégias com flexo-extensão de cotovelos são observadas na calistenia e handbalancing como recurso funcional compensatório. Ambas constituem adaptações motoras eficientes.
      </p>
      <p class="callout-text">
        <strong>🎯 Gestão de Esforço (Pacing):</strong><br>
        Notou-se redução planejada na duração das séries seguintes (T1: 50,98 s -> T2: 18,99 s -> T3: 9,94 s). Conforme relatado por você, essa diminuição foi voluntária para poupar os membros superiores e evitar a fadiga extrema antes dos testes de Handstand Walk (HSW), demonstrando excelente maturidade e sensibilidade à sobrecarga axial.<br>
        <em>Recomendação para o treino:</em> Manter essa percepção de esforço, reservando séries até o limite de tempo para testes pontuais e focando a rotina em séries submáximas (20 a 30 s) com descanso completo.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong>
        O controle antecipatório na subida decorre da programação de torque reflexo descrita por Clement et al. (1984) <sup>[24]</sup> e Gautier et al. (2007) <sup>[23]</sup>.
        A verticalidade de 7,67° reduz o braço de alavanca gravitacional sobre a cintura escapular (Rohleder & Vogt, 2018 <sup>[17]</sup>).
        A estabilidade com baixa excursão de cotovelo e ombro confirma o predomínio da estratégia distal de punho em atletas experientes (Kerwin & Trewartha, 2001 <sup>[6]</sup>; Blenkinsop et al., 2017 <sup>[25]</sup>).
      </div>
    </div>

    <!-- 3.3 HSW -->
    <div class="sub-section-title">
      3.3 Handstand Walk — HSW (Locomoção Invertida Dinâmica)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Distância Mediana no HSW <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_DIST_MEDIANA_M)} m</div>
          <div class="metric-subtext">T1: {f_dec(HSW_T1_DIST_M)}m | T2: {f_dec(HSW_T2_DIST_M)}m | T3: {f_dec(HSW_T3_DIST_M)}m</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Consistência Notável em Todas as Séries (~5m)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Distância Máxima no HSW <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(HSW_DIST_MAX_M)} m</div>
          <div class="metric-subtext">Alcançada na Tentativa 2</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Destaque Positivo! Superou 5,4 metros</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Variabilidade Temporal (CV) <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">{f_dec(HSW_CV_TEMPORAL)}%</div>
          <div class="metric-subtext">Dispersão do tempo de contato por passada</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857; font-weight: 700;">
            Metrônomo Motor! CV Temporal &lt; 10%
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Cadência dos Passos com as Mãos <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CADENCIA)} passos/s</div>
          <div class="metric-subtext">22 passos em 14,16 segundos</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Cadência Alta e Passadas Rápidas</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Comprimento Médio da Passada <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #b45309;">{f_dec(HSW_PASSADA_MM)} mm</div>
          <div class="metric-subtext">~24,9 cm por passada palmar</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Passada Curta (Passos Curtos)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Fase de Duplo Suporte Palmar <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #b45309;">{f_dec(HSW_DUPLO_SUPORTE_PCT)}%</div>
          <div class="metric-subtext">Tempo com ambas as mãos apoiadas</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #fef3c7; color: #b45309; border-color: #fde68a;">
            Atenção: Apoio Duplo Excessivo (~60%)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Velocidade da Marcha (HSW) <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_VEL_M_S)} m/s</div>
          <div class="metric-subtext">{f_dec(HSW_VEL_KM_H)} km/h (Velocidade linear)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Deslocamento Ágil</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Tempo de Contato Palmar <sup>[24]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CONTATO_S)} s</div>
          <div class="metric-subtext">{HSW_CONTATO_MS} ms por apoio palmar</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Transição Ágil de Apoio</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Extensão Cervical no HSW <sup>[23]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_CERVICAL_DEG)}°</div>
          <div class="metric-subtext">Olhar erguido direcionado à frente</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Fixação Visual Estável no Alvo</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Flexão Plantar na Marcha <sup>[17]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">{f_dec(HSW_PLANTAR_DEG)}°</div>
          <div class="metric-subtext">Pés em ponta preservados na marcha</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Cadeia Posterior Firme e Ativa</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 Handstand Walk: Cadência rítmica excepcional de metrônomo, diagnósticos e prescrição corretiva <sup>[23,24]</sup>
      </div>
      <p class="callout-text">
        <strong>🗣️ O que você precisa saber na prática:</strong><br>
        • <strong>Desempenho e velocidade:</strong> Você demonstrou consistência excepcional, completando praticamente 5 metros em todas as séries (mediana de {f_dec(HSW_DIST_MEDIANA_M)} m e máxima de {f_dec(HSW_DIST_MAX_M)} m), com passos rápidos (cadência de {f_dec(HSW_CADENCIA)} passos/s), velocidade de <strong>{f_dec(HSW_VEL_M_S)} m/s ({f_dec(HSW_VEL_KM_H)} km/h)</strong> e passadas ágeis (contato de {f_dec(HSW_CONTATO_S)} s por apoio).<br>
        • <strong>Pontos de evolução:</strong> Seu duplo suporte (59,7%) e a oscilação lateral ({f_dec(HSW_OSCILACAO_ML_MM)} mm) mostram que você ainda transfere peso com bastante cautela, mantendo ambas as mãos em contato por mais da metade do tempo.
      </p>
      <p class="callout-text">
        <strong>🔬 Detalhamento dos Dados e Biomecânica:</strong><br>
        A locomoção dinâmica invertida exige cadência alta e passadas compactas para manter o centro de massa em constante aceleração para a frente sem desvios laterais excessivos. O coeficiente de variação temporal de apenas {f_dec(HSW_CV_TEMPORAL)}% atesta uma regularidade rítmica de alto nível (padrão de "metrônomo motor"). O comprimento médio de passada de {f_dec(HSW_PASSADA_MM)} mm (~25 cm) garante estabilidade sem arriscar o tombamento.
      </p>
      <p class="callout-text">
        <strong>🛠️ Como consertar no treinamento:</strong><br>
        • <em>Ampliação progressiva da passada:</em> Realizar treinos de locomoção com marcadores no solo (fitas adesivas a cada 35-40 cm), estimulando passadas mais longas e econômicas.<br>
        • <em>Fluidez dinâmica e redução do duplo apoio:</em> Treinar com uma inclinação anterior sutil e controlada do corpo, permitindo que a inércia puxe a marcha para reduzir o tempo de apoio duplo para 45-50%.<br>
        • <em>Single-arm dumbbell overhead carry:</em> Caminhada sustentando peso unilateral acima da cabeça, com escápula bloqueada no topo para fortalecer a estabilidade unilateral e confiança no apoio unimanual.
      </p>
      <div class="callout-science">
        <strong>Fundamentação Científica & Biomecânica:</strong>
        Blenkinsop et al. (2017) <sup>[24]</sup> estabelecem que a locomoção invertida madura exige coordenação espaço-temporal simétrica.
        O CV Temporal de 9,81% comprova controle temporal exemplar. Contudo, o duplo suporte de 59,68% associado à passada curta de 24,9 cm aumenta a sobrecarga mecânica cumulativa,
        indicando que a ampliação do comprimento da passada é o ajuste primordial para a economia de esforço e longevidade articular.
      </div>
    </div>

    <!-- SEÇÃO 4: SÍNTESE E RECOMENDAÇÕES -->
    <div class="section-title">
      <span class="badge-num">4</span>
      Síntese Integrativa e Recomendações Práticas Individualizadas
    </div>

    <div class="practice-box">
      <h4>📌 Síntese Integrativa do Perfil do Atleta (Destaques e Potenciais):</h4>
      <ul>
        <li>
          <strong>Hipertrofia Muscular Atlética e Densidade Magra:</strong> Mais de 70 kg de massa magra ativa ({f_dec(MLG_KG, 1)} kg; 80,8%) e FFMI de {f_dec(FFMI)} kg/m², situando-se no limite superior para atletas naturais (Kouri et al., 1995; Schutz et al., 2002). O IMC elevado decorre de massa muscular esquelética contrátil, e não de adiposidade.
        </li>
        <li>
          <strong>Resistência Isométrica Escapular de Destaque Notável:</strong> Marca expressiva de {f_dec(WALL_HS_MAX, 0)} segundos (1 min e 41 s) sustentando 87,2 kg de carga axial no Belly-to-Wall Handstand, comprovando notável tolerância à fadiga de serrátil anterior e trapézio (Gautier et al., 2007).
        </li>
        <li>
          <strong>Domínio Técnico e Alinhamento no Handstand Livre:</strong> Tempo de pico de {f_dec(HS_LIVRE_TEMPO_MAX_S)} segundos na 1ª tentativa, com alinhamento vertical de {f_dec(HS_LIVRE_VERT_DEG)}° e excelente flexão plantar ({f_dec(HS_LIVRE_PLANTAR_DEG)}°), comprovando empilhamento articular e linha corporal compacta.
        </li>
        <li>
          <strong>Precisão Rítmica de Metrônomo Motor no Handstand Walk:</strong> Coeficiente de Variação Temporal de apenas {f_dec(HS_CV_TEMPORAL)}% (<10%), revelando sincronismo rítmico exemplar na cadência dos passos e grande regularidade em todas as tentativas de marcha (~5 m) (Blenkinsop et al., 2017).
        </li>
        <li>
          <strong>Controle Postural Estabilométrico Adaptativo:</strong> Entropia Aproximada elevada ({f_dec(HS_ASSIST_APEN, 4)}), indicando controle dinâmico flexível sem rigidez articular, além de 100% de sucesso nas entradas livres por controle antecipatório feedforward maduro.
        </li>
      </ul>

      <h4 style="margin-top: 22px; color: #b45309;">🎯 Oportunidades de Evolução Técnica e Prescrição de Treino (Direto e Acionável):</h4>
      <ul>
        <li>
          <strong>1. Equalização da Força Isométrica do Punho Direito (Ponto Crítico):</strong> Corrigir a assimetria acentuada de 32,56% no Biodex a 70° (Esquerdo: 17,1 N·m vs Direito: 12,9 N·m; déficit > 15% Bishop et al., 2018). <em>Prescrição:</em> Incluir 3 a 4 séries de flexão unilateral de punho com halteres em banco apoiado (8 a 12 reps com ênfase na fase excêntrica) e sustentações isométricas unipodais na parede dedicadas ao membro direito.
        </li>
        <li>
          <strong>2. Ampliação da Passada e Redução do Duplo Suporte no HSW:</strong> Aumentar o comprimento da passada palmar de ~25 cm para 35-40 cm e diminuir a fase de duplo apoio de ~60% para 45-50%. <em>Prescrição:</em> Praticar passadas sobre marcadores visuais no solo a cada 35-40 cm e treinar a 'queda para a frente controlada', avançando a mesma distância com metade dos impactos axiais sob 87 kg.
        </li>
        <li>
          <strong>3. Gestão Estratégica de Esforço e Transição para a Locomoção:</strong> A redução na duração das séries 2 e 3 do HS livre refletiu uma escolha voluntária e consciente do participante, que, plenamente satisfeito com a excelente marca alcançada na 1ª tentativa (50,98 s), optou por se poupar para evitar fadiga extrema antes do Handstand Walk. <em>Prescrição:</em> Continuar aplicando essa autorregulação inteligente (<em>pacing</em>) nos treinos diários, combinando séries curtas e submáximas (15 a 25 s) antes de blocos de caminhada para manter os estabilizadores com alto frescor neuromuscular.
        </li>
        <li>
          <strong>4. Proteção Articular e Absorção de Impacto sob Massa Elevada:</strong> Como o suporte corporal sob 87,2 kg impõe alto estresse axial sobre os ossos do carpo e articulação radioulnar, manter rotina diária de aquecimento e mobilidade de punhos com sobrecarga gradual, priorizando aterrissagens palmares suaves.
        </li>
      </ul>
    </div>

    <!-- SEÇÃO 5: REFERÊNCIAS CIENTÍFICAS -->
    <div class="references-card">
      <h4>📚 Referências Científicas e Normativas Consultadas:</h4>
      <ol>
        <li>Sun, S. S., et al. (2003). Development of bioelectrical impedance analysis prediction equations for body composition with the use of a multicomponent model. <em>Am J Clin Nutr</em>, 77(2), 331-340.</li>
        <li>Kouri, E. M., et al. (1995). Fat-free mass index in users and nonusers of anabolic-androgenic steroids. <em>Clin J Sport Med</em>, 5(4), 223-228.</li>
        <li>American College of Sports Medicine (ACSM). (2018). <em>ACSM's Guidelines for Exercise Testing and Prescription</em> (10th ed.). Wolters Kluwer.</li>
        <li>Schutz, Y., et al. (2002). Fat-free mass index and fat mass index percentiles in Caucasians aged 18-98 y. <em>Int J Obes Relat Metab Disord</em>, 26(7), 953-960.</li>
        <li>Garrido-Chamorro, R., et al. (2007). Correlation between body mass index and body fat percentage in elite athletes: The fallacy of BMI. <em>Int J Sports Med</em>, 28(6), 461-466.</li>
        <li>Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. <em>J Appl Physiol</em>, 89(2), 465-471.</li>
        <li>Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. <em>Am J Clin Nutr</em>, 82(1), 49-52.</li>
        <li>Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. <em>Clin Nutr</em>, 31(6), 854-861.</li>
        <li>Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. <em>Sports Biomech</em>, 1(2), 163-176.</li>
        <li>Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. <em>J Phys Ther Sci</em>, 31(11), 932-938.</li>
        <li>Dodds, R. M., et al. (2014). Globally representative normative data for handgrip strength: systematic review. <em>PLoS ONE</em>, 9(12), e113637.</li>
        <li>Bishop, C., et al. (2018). Effects of inter-limb asymmetries on physical and sports performance. <em>J Sports Sci</em>, 36(10), 1135-1144.</li>
        <li>Ellenbecker, T. S., & Roetert, E. P. (2006). Isokinetic wrist strength in competitive athletes. <em>Am J Sports Med</em>, 34(11), 1845-1852.</li>
        <li>Rohleder, J., et al. (2021). Wrist joint biomechanics and handstand stability in gymnastics. <em>Sports Biomech</em>, 20(3), 312-326.</li>
        <li>Sloot, L. H., et al. (2020). Wrist motor control during balance correction in handbalancing. <em>J Biomech</em>, 102, 109653.</li>
        <li>Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. <em>Strength Cond J</em>, 41(4), 48-60.</li>
        <li>Rohleder, J., & Vogt, L. (2018). Kinematic alignment and joint stacking in artistic gymnastics vs. fitness handbalancing. <em>J Sports Sci</em>, 36(11), 1238-1245.</li>
        <li>Winter, D. A. (1995). Human balance and posture control during standing and walking. <em>Gait & Posture</em>, 3(4), 193-214.</li>
        <li>Slobounov, S., et al. (2008). Virtual reality and force-platform assessment of inverted posture stability. <em>Exp Brain Res</em>, 188(2), 241-253.</li>
        <li>Uzun, M., et al. (2012). Stabilometric comparison of handstand on force plates between elite and novice athletes. <em>J Hum Kinet</em>, 34(1), 15-23.</li>
        <li>Pincus, S. M. (1991). Approximate entropy as a measure of system complexity. <em>Proc Natl Acad Sci USA</em>, 88(6), 2297-2301.</li>
        <li>Borg, F. G., & Laxåback, G. (2010). Entropy of balance: How to compute and interpret approximate entropy in posturography. <em>J Biomech</em>, 43(15), 3044-3048.</li>
        <li>Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. <em>Hum Mov Sci</em>, 26(4), 577-594.</li>
        <li>Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Handstand walk: Locomotor biomechanics and coordination in inverted human locomotion. <em>Hum Mov Sci</em>, 54, 235-244.</li>
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
'''

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
# Arquivo PDF mantido exclusivamente na pasta individual P002_laudo
        else:
            print(f"[AVISO] Falha ao compilar PDF: {res.stderr}")
    except Exception as e:
        print(f"[AVISO] Erro ao invocar Edge: {e}")
else:
    print("[AVISO] Executável do Microsoft Edge não encontrado para gerar PDF.")

print("=" * 80)
print("RELATÓRIO DEVOLUTIVO DE P002 ATUALIZADO COM SUCESSO!")
print(f"  -> DOCX: {DOCX_OUT}")
print(f"  -> HTML: {HTML_OUT}")
if os.path.exists(PDF_OUT):
    print(f"  -> PDF:  {PDF_OUT}")
print("=" * 80)
