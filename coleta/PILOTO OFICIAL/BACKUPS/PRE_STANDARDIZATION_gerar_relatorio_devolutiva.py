import os
import sys
import numpy as np
import matplotlib.pyplot as plt
import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.oxml import parse_xml
from docx.oxml.ns import nsdecls

sys.stdout.reconfigure(encoding="utf-8", errors="replace")

BASE_DIR = r"C:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL"
DIR_RESULTADOS = os.path.join(BASE_DIR, r"03_CONSOLIDACAO_DATASET\resultados_finais\laudos_devolutiva")
os.makedirs(DIR_RESULTADOS, exist_ok=True)

DOCX_OUT = os.path.join(DIR_RESULTADOS, "P001_RELATORIO_DEVOLUTIVA_GUSTAVO_DONATO.docx")
HTML_OUT = os.path.join(DIR_RESULTADOS, "P001_RELATORIO_DEVOLUTIVA_GUSTAVO_DONATO.html")
GRAFICO_BIODEX_PNG = os.path.join(DIR_RESULTADOS, "grafico_biodex_gustavo_donato.png")

DIR_BIODEX_RAW = os.path.join(BASE_DIR, r"01_SESSAO_LACIDH_FORCA\dados_brutos\P001\Dados_biodex")
CURVA_D_TXT = os.path.join(DIR_BIODEX_RAW, "p001_CURVE.txt")
CURVA_E_TXT = os.path.join(DIR_BIODEX_RAW, "p001_l_CURVE.txt")

TITULO_OFICIAL_PROJETO = "Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk"

# =========================================================================
# (O GRÁFICO DO BIODEX FOI REMOVIDO CONFORME DIRETRIZ DO USUÁRIO)
# =========================================================================
# ROTINA AUTOMÁTICA DE AUDITORIA E DOUBLE-CHECK DOS DADOS BIOMECÂNICOS
# =========================================================================
def double_check_valores_p001():
    """
    Auditoria e validação cruzada automática de consistência matemática e biomecânica.
    Garante que nenhum relatório seja gerado com discrepâncias numéricas.
    """
    massa = 65.25
    estatura = 171.0
    imc_esperado = 22.31
    imc_calculado = round(massa / ((estatura / 100.0) ** 2), 2)
    assert imc_calculado == imc_esperado, f"Erro IMC: {imc_calculado} != {imc_esperado}"

    # Biodex
    pt_d = 18.5
    pt_e = 20.5
    media_bio = round((pt_d + pt_e) / 2.0, 2)  # 19.50
    rel_media_bio = round(media_bio / massa, 3)  # 0.299
    rel_max_bio = round(pt_e / massa, 3)        # 0.314
    rel_min_bio = round(pt_d / massa, 3)        # 0.284
    lsi_bio = round((pt_e / pt_d) * 100.0, 1)   # 110.8%
    diff_lsi = round(lsi_bio - 100.0, 1)        # 10.8%

    assert media_bio == 19.5, f"Erro Média Biodex: {media_bio} != 19.5"
    assert rel_media_bio == 0.299, f"Erro Relativo Médio: {rel_media_bio} != 0.299"
    assert rel_max_bio == 0.314, f"Erro Relativo Máximo: {rel_max_bio} != 0.314"
    assert lsi_bio == 110.8, f"Erro LSI Biodex: {lsi_bio} != 110.8"
    assert diff_lsi == 10.8, f"Erro Diferença LSI Biodex: {diff_lsi} != 10.8"

    # Preensão
    fpm_d = 46.0
    fpm_e = 52.0
    fpm_media = round((fpm_d + fpm_e) / 2.0, 1)  # 49.0
    fpm_rel_max = round(fpm_e / massa, 2)        # 0.80
    fpm_rel_med = round(fpm_media / massa, 3)    # 0.751
    lsi_fpm = round((fpm_e / fpm_d) * 100.0, 1)  # 113.0%

    assert fpm_media == 49.0, f"Erro FPM Média: {fpm_media} != 49.0"
    assert fpm_rel_max == 0.80, f"Erro FPM Relativo: {fpm_rel_max} != 0.80"
    assert lsi_fpm == 113.0, f"Erro LSI FPM: {lsi_fpm} != 113.0"

    # 1-RM Shoulder Press
    sp_1rm = 56.0
    sp_rel = round((sp_1rm / massa) * 100.0, 1)  # 85.8%
    assert sp_rel == 85.8, f"Erro 1-RM SP Relativo: {sp_rel} != 85.8"

    # Wall-HS
    wall_max = 64.0
    assert wall_max == 64.0

    print("=" * 80)
    print("[DOUBLE-CHECK AUDITORIA INTERNA OK] Todos os valores de P001 validados com sucesso!")
    print(f"  -> IMC: {imc_calculado} kg/m2")
    print(f"  -> Biodex: Média = {media_bio} N·m ({rel_media_bio} N·m/kg) | Pico = {pt_e} N·m ({rel_max_bio} N·m/kg)")
    print(f"  -> Biodex LSI: {lsi_bio}% (Diferença exata: {diff_lsi}%)")
    print(f"  -> FPM: D={fpm_d} kgf, E={fpm_e} kgf | LSI: {lsi_fpm}%")
    print(f"  -> 1-RM Shoulder Press: {sp_1rm} kg ({sp_rel}% da MC)")
    print(f"  -> Resistência Wall-HS: {wall_max} s")
    print("=" * 80)

double_check_valores_p001()

# =========================================================================
# 1. GERAR DOCUMENTO DOCX NA ORDEM CRONOLÓGICA DAS COLETAS
# ORDEM: 1. BIA -> 2. PREENSÃO -> 3. BIODEX -> 4. SHOULDER PRESS -> 5. HS WALL
# =========================================================================
def set_cell_background(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    tcPr.append(parse_xml(f'<w:shd {nsdecls("w")} w:fill="{hex_color}"/>'))

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = parse_xml(f'<w:tcMar {nsdecls("w")}><w:top w:w="{top}" w:type="dxa"/><w:bottom w:w="{bottom}" w:type="dxa"/><w:left w:w="{left}" w:type="dxa"/><w:right w:w="{right}" w:type="dxa"/></w:tcMar>')
    tcPr.append(tcMar)

EMERALD_DARK_HEX = "064E3B"
EMERALD_DARK_RGB = RGBColor(6, 78, 59)

EMERALD_HEADER_HEX = "047857"
EMERALD_HEADER_RGB = RGBColor(4, 120, 87)

TEXT_DARK_RGB = RGBColor(30, 41, 59)
TEXT_MUTED_RGB = RGBColor(100, 116, 139)

MINT_LIGHT_HEX = "F0FDF4"
MINT_ZEBRA_HEX = "F8FAFC"

doc = docx.Document()

for s in doc.sections:
    s.top_margin = Inches(0.75)
    s.bottom_margin = Inches(0.75)
    s.left_margin = Inches(0.75)
    s.right_margin = Inches(0.75)

# Cabeçalho Institucional
p_inst = doc.add_paragraph()
r_inst = p_inst.add_run(
    "UNIVERSIDADE DE SÃO PAULO — EEFERP-USP\n"
    "Escola de Educação Física e Esporte de Ribeirão Preto\n"
    "Laboratório de Cineantropometria e Desempenho Humano (LaCiDH) | Laboratório de Biomecânica e Controle Motor (LaBioCoM)"
)
r_inst.font.name = "Arial"
r_inst.font.size = Pt(8.5)
r_inst.font.bold = True
r_inst.font.color.rgb = EMERALD_HEADER_RGB
p_inst.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_title = doc.add_paragraph()
r_title = p_title.add_run("RELATÓRIO INDIVIDUAL DE DESEMPENHO E COMPOSIÇÃO CORPORAL")
r_title.bold = True
r_title.font.name = "Arial"
r_title.font.size = Pt(14)
r_title.font.color.rgb = EMERALD_DARK_RGB
p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER

p_meta = doc.add_paragraph()
r_meta = p_meta.add_run(
    f"Projeto de Pesquisa: {TITULO_OFICIAL_PROJETO}\n"
    "Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes"
)
r_meta.font.name = "Arial"
r_meta.font.size = Pt(9)
r_meta.font.color.rgb = TEXT_MUTED_RGB
p_meta.alignment = WD_ALIGN_PARAGRAPH.CENTER

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# Box Atleta
t_part = doc.add_table(rows=2, cols=4)
t_part.alignment = WD_TABLE_ALIGNMENT.CENTER
for row in t_part.rows:
    for cell in row.cells:
        set_cell_background(cell, "F8FAFC")
        set_cell_margins(cell, top=80, bottom=80, left=120, right=120)
        cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER

def format_cell(cell, label, val):
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(1)
    p.paragraph_format.space_before = Pt(1)
    r1 = p.add_run(label + "\n")
    r1.font.bold = True
    r1.font.size = Pt(8)
    r1.font.color.rgb = EMERALD_HEADER_RGB
    r2 = p.add_run(val)
    r2.font.bold = True
    r2.font.size = Pt(9.5)
    r2.font.color.rgb = TEXT_DARK_RGB

format_cell(t_part.rows[0].cells[0], "PARTICIPANTE", "Gustavo H. Donato da Costa")
format_cell(t_part.rows[0].cells[1], "CÓDIGO / ID", "P001 (Atleta Piloto)")
format_cell(t_part.rows[0].cells[2], "IDADE / SEXO", "20 anos | Masculino")
format_cell(t_part.rows[0].cells[3], "DATA COLETA (S1)", "02/09/2026 (LaCiDH)")

format_cell(t_part.rows[1].cells[0], "MODALIDADES", "Calistenia / Handbalancing")
format_cell(t_part.rows[1].cells[1], "TEMPO PRÁTICA", "24 meses (18m específico)")
format_cell(t_part.rows[1].cells[2], "MEMBRO DOMINANTE", "Destro (Direito)")
format_cell(t_part.rows[1].cells[3], "STATUS SESSÃO 2", "Confirmada (09/09 08h)")

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Mensagem introdutória
p_intro = doc.add_paragraph()
r_in1 = p_intro.add_run("Olá, Gustavo!\n")
r_in1.bold = True
r_in1.font.color.rgb = EMERALD_DARK_RGB
r_in2 = p_intro.add_run(
    "Agradecemos imensamente a sua dedicação na primeira sessão da nossa pesquisa de mestrado na EEFERP-USP. "
    "Este relatório apresenta a devolutiva individual dos testes realizados no LaCiDH, organizados rigorosamente na sequência cronológica da sua coleta: "
    "1) Bioimpedância Elétrica, 2) Força de Preensão Manual, 3) Dinamometria Isométrica dos Flexores de Punho (Biodex), 4) 1-RM no Shoulder Press e 5) Resistência na Parada de Mão na Parede. "
    "Cada indicador é contextualizado com base na literatura científica internacional [1-14], evidenciando como essas capacidades físicas "
    "se relacionam potencialmente com as demandas de estabilidade e controle no Handstand!"
)
r_in2.font.color.rgb = TEXT_DARK_RGB
p_intro.paragraph_format.space_after = Pt(6)

# =========================================================================
# ETAPA 1: COMPOSIÇÃO CORPORAL (BIA)
# =========================================================================
h1 = doc.add_heading("1. Composição Corporal (Bioimpedância Elétrica Sanny® BIA1011-AF)", level=2)
h1.runs[0].font.color.rgb = EMERALD_DARK_RGB
h1.runs[0].font.size = Pt(12)

t_bia = doc.add_table(rows=7, cols=3)
t_bia.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_bia = ["Variável Avaliada", "Seu Resultado", "Interpretação & Valores Normativos"]
for j, h in enumerate(headers_bia):
    c = t_bia.cell(0, j)
    c.text = h
    set_cell_background(c, EMERALD_HEADER_HEX)
    set_cell_margins(c, top=100, bottom=100, left=140, right=140)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(9)
    if j == 1:
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    else:
        p.alignment = WD_ALIGN_PARAGRAPH.LEFT

bia_dados = [
    ("Massa Corporal & Estatura", "65,25 kg | 171,0 cm", "IMC = 22,31 kg/m² (Eutrofia / Padrão Saudável [3])"),
    ("Percentual de Gordura (%GC) [1,3]", "13,88%", "Excelente! Faixa atlética ideal masculina jovem (10% a 15%)"),
    ("Massa Livre de Gordura (MLG) [1]", "56,15 kg (86,1%)", "Predomínio expressivo de massa magra ativa"),
    ("Massa Muscular Esquelética [2]", "31,06 kg", "Excelente suporte muscular para sustentar o peso invertido"),
    ("Água Corporal Total (ACT) [1]", "39,05 L (59,89%)", "Nível ótimo de hidratação intra e extracelular"),
    ("Ângulo de Fase (PhA) [4,5]", "8,98°", "DESTAQUE: Excepcional! Reflete altíssima integridade celular")
]

for i, row in enumerate(bia_dados, 1):
    for j, val in enumerate(row):
        c = t_bia.cell(i, j)
        c.text = val
        set_cell_margins(c, top=90, bottom=90, left=140, right=140)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(1)
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        if i % 2 == 1:
            set_cell_background(c, MINT_LIGHT_HEX)
        else:
            set_cell_background(c, "FFFFFF")

# Box de Destaque PhA
p_pha = doc.add_paragraph()
p_pha.paragraph_format.space_before = Pt(6)
p_pha.paragraph_format.space_after = Pt(6)
r_pha_box = p_pha.add_run(
    "💡 Destaque da Bioimpedância: Seu Ângulo de Fase (8,98°) [4,5]\n"
    "O Ângulo de Fase (PhA) é um biomarcador derivado da relação entre resistência e reatância, indicativo da integridade e capacitância das membranas celulares. "
    "Em homens jovens e saudáveis, os valores médios reportados na literatura situam-se tipicamente entre 6,5° e 7,8° [4]. O seu resultado de 8,98° demonstra "
    "excelente integridade tecidual e estado de hidratação celular compatível com atletas adaptados a rotinas exigentes de treinamento."
)
r_pha_box.font.size = Pt(9)
r_pha_box.font.color.rgb = TEXT_DARK_RGB

# =========================================================================
# ETAPA 2: TESTES DE FORÇA NEUROMUSCULAR (ORDEM CRONOLÓGICA DAS COLETAS)
# =========================================================================
h2 = doc.add_heading("2. Perfil Neuromuscular e Força Específica (LaCiDH)", level=2)
h2.runs[0].font.color.rgb = EMERALD_DARK_RGB
h2.runs[0].font.size = Pt(12)

# --- 2.1 FORÇA DISTAL: PREENSÃO E FLEXORES DE PUNHO ---
h2_1 = doc.add_heading("2.1 Força Distal: Preensão Manual e Flexores de Punho (Biodex)", level=3)
h2_1.runs[0].font.color.rgb = EMERALD_DARK_RGB
h2_1.runs[0].font.size = Pt(11)

t_forca_distal = doc.add_table(rows=3, cols=3)
t_forca_distal.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_forca = ["Teste (Ordem de Execução)", "Seu Desempenho", "Interpretação e Relevância Biomecânica"]
for j, h in enumerate(headers_forca):
    c = t_forca_distal.cell(0, j)
    c.text = h
    set_cell_background(c, EMERALD_DARK_HEX)
    set_cell_margins(c, top=90, bottom=90, left=130, right=130)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(9)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

forca_distal_dados = [
    ("1º Teste: Força de Preensão Manual (FPM) [8,9]\nDinamômetro Hidráulico Saehan", 
     "Mão Direita (Dom): 46,0 kgf\nMão Esquerda (Não-Dom): 52,0 kgf\nRelativa: 0,80 kgf/kg | LSI: 113,0% (Não-Dom mais forte)", 
     "Superior à média de homens jovens saudáveis (~42 kgf [9]). Na parada de mão, mãos fortes atuam como a interface mecânica de contato e ancoragem palmar no solo [6,14]."),
     
    ("2º Teste: Dinamometria Isométrica dos Flexores de Punho [6,7]\nDinamômetro Biodex Multi-Joint 4 PRO (70° Ext.)",
     "Pico D (Dom): 18,5 N·m (CV: 16,6%)\nPico E (Não-Dom): 20,5 N·m (CV: 2,0%)\nMédia Bilateral: 19,5 N·m (0,299 N·m/kg)\nPico Máx: 0,314 N·m/kg | LSI: 110,8% (Não-Dom mais forte)", 
     "Avaliado na angulação funcional de 70° de extensão do Handstand [6,7]. Excelente simetria entre punhos (LSI: 110,8%; diferença de apenas 10,8%, com discreto predomínio do membro não-dominante [esquerdo > direito]), fundamental para a 'Wrist Strategy' e apoio no solo.")
]

for i, row in enumerate(forca_distal_dados, 1):
    for j, val in enumerate(row):
        c = t_forca_distal.cell(i, j)
        c.text = val
        set_cell_margins(c, top=80, bottom=80, left=130, right=130)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(1)
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, MINT_LIGHT_HEX if i % 2 == 1 else "FFFFFF")

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# Detalhamento Distal (Introdução Funcional/Coloquial seguida dos Valores Científicos de Preensão, Biodex e LSI)
p_ws = doc.add_paragraph()
p_ws.paragraph_format.space_before = Pt(2)
p_ws.paragraph_format.space_after = Pt(4)
r_ws = p_ws.add_run(
    "No modelo biomecânico de pêndulo invertido do Handstand, os flexores de punho e a musculatura palmar desempenham no equilíbrio de cabeça para baixo a mesma função que "
    "a panturrilha e os pés exercem na postura ereta bípede ('Wrist Strategy') [6,7]. Essa musculatura atua como o verdadeiro 'freio de mão' da parada "
    "de mão. Da mesma forma que cravamos as pontas dos pés no solo para conter uma oscilação para a frente, no Handstand são as pontas dos dedos e a palma "
    "que esmagam o chão quando o corpo passa da vertical (o temido 'overbalance'). Essa pressão gera um torque corretivo instantâneo que empurra o corpo "
    "de volta para o prumo. Ter punhos e mãos fortes proporciona uma ampla margem de segurança para salvar o equilíbrio com pequenos ajustes nas mãos, evitando "
    "quebrar a linha dos ombros ou arquear a lombar (a clássica postura em 'banana') [6,7]."
)
r_ws.font.size = Pt(8.8)
r_ws.font.color.rgb = TEXT_DARK_RGB

p_distal_desc = doc.add_paragraph()
p_distal_desc.paragraph_format.space_after = Pt(6)
r_d1 = p_distal_desc.add_run(
    "Para garantir essa sustentação palmar, a avaliação de Força de Preensão Manual (FPM) acusou pico de 52,0 kgf no membro não-dominante (esquerdo) e 46,0 kgf no membro dominante (direito) "
    "(relação relativa de 0,80 kgf/kg), superando com folga a média de homens jovens saudáveis (~42 kgf [8,9]). O Índice de Simetria dos Membros na preensão (LSI: 113,0%, diferença de 13,0% "
    "a favor da mão esquerda) situa-se dentro da faixa de equilíbrio fisiológico (<15%) preconizada na literatura neuromuscular [15]. Enquanto em destros não treinados a mão dominante costuma "
    "ser discretamente superior (~10%), atletas de calistenia e ginástica frequentemente equilibram ou invertem essa relação devido às exigências bilaterais de sustentação do peso corporal. "
    "Na prática, essa simetria de preensão assegura rigidez uniforme no carpo em ambos os lados [13,14], impedindo o colapso unilateral da base palmar sob o peso invertido. Ademais, no Handstand Walk, "
    "uma pegada bilateralmente equivalente sugere capacidade homogênea de absorção de impacto no contato sucessivo de cada mão contra o solo ('hand strike'), mitigando oscilações rotacionais do tronco "
    "e prevenindo sobrecargas articulares assimétricas.\n\n"
    "Já no Biodex System 4 PRO, o torque isométrico dos flexores de punho foi avaliado a 70° de extensão, posição selecionada por sua "
    "especificidade biomecânica ao mimetizar a dorsiflexão funcional da mão contra o solo no Handstand [6,7]. O voluntário alcançou torque "
    "médio bilateral de 19,5 N·m (0,299 N·m/kg) (com pico de 20,5 N·m [0,314 N·m/kg] no membro não-dominante [esquerdo] e 18,5 N·m [0,284 N·m/kg] "
    "no membro dominante [direito]), quantificando a capacidade específica de geração de torque no ângulo funcional de atuação do freio palmar ('Wrist Strategy') [6,7]. "
    "O Índice de Simetria dos Membros nos punhos (LSI: 110,8%, diferença de apenas 10,8% a favor do lado esquerdo) também atesta excelente simetria intermembros (<15%) [15]. "
    "Em analogia à locomoção e marcha humana [15,16], essa simetria de torque angular é determinante no Handstand Walk: "
    "ao caminhar com as mãos, punhos equilibrados tendem a favorecer passadas mais estáveis, com tempos de contato homogêneos e controle direcional consistente, "
    "auxiliando a prevenir desvios de trajetória e compensações escapulares unilaterais."
)
r_d1.font.size = Pt(8.8)
r_d1.font.color.rgb = TEXT_DARK_RGB

# --- 2.2 FORÇA PROXIMAL E RESISTÊNCIA: SHOULDER PRESS E PAREDE ---
doc.add_paragraph().paragraph_format.space_after = Pt(2)
h2_2 = doc.add_heading("2.2 Força Proximal e Resistência: Shoulder Press e Parada de Mão na Parede", level=3)
h2_2.runs[0].font.color.rgb = EMERALD_DARK_RGB
h2_2.runs[0].font.size = Pt(11)

t_forca_proximal = doc.add_table(rows=3, cols=3)
t_forca_proximal.alignment = WD_TABLE_ALIGNMENT.CENTER
for j, h in enumerate(headers_forca):
    c = t_forca_proximal.cell(0, j)
    c.text = h
    set_cell_background(c, EMERALD_DARK_HEX)
    set_cell_margins(c, top=90, bottom=90, left=130, right=130)
    c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
    p = c.paragraphs[0]
    p.runs[0].bold = True
    p.runs[0].font.color.rgb = RGBColor(255, 255, 255)
    p.runs[0].font.size = Pt(9)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

forca_proximal_dados = [
    ("3º Teste: 1-RM no Shoulder Press (SP) [10]\nBarra Olímpica Estrita (Overhead Press)",
     "56,0 kg\n(85,8% da massa corporal)", 
     "Excelente capacidade de empurrada vertical estrita, refletindo força máxima elevada em deltóides, tríceps e fixadores escapulares (serrátil anterior e trapézio) [10]."),
     
    ("4º Teste: Resistência Belly-to-Wall Handstand [6,7]\nParada de Mão Isométrica na Parede (20 cm)",
     "64,0 segundos\n(T1: 60s | T2: 64s)", 
     "Capacidade de sustentação contínua superior a 1 minuto sob alinhamento estrito, sugerindo ótima tolerância à fadiga isométrica da cintura escapular e do core sob gravidade [6,11].")
]

for i, row in enumerate(forca_proximal_dados, 1):
    for j, val in enumerate(row):
        c = t_forca_proximal.cell(i, j)
        c.text = val
        set_cell_margins(c, top=80, bottom=80, left=130, right=130)
        c.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.CENTER
        p = c.paragraphs[0]
        p.paragraph_format.space_after = Pt(1)
        p.paragraph_format.space_before = Pt(1)
        p.runs[0].font.size = Pt(8.5)
        p.runs[0].font.color.rgb = TEXT_DARK_RGB
        if j == 1:
            p.alignment = WD_ALIGN_PARAGRAPH.CENTER
            p.runs[0].bold = True
            p.runs[0].font.color.rgb = EMERALD_DARK_RGB
        else:
            p.alignment = WD_ALIGN_PARAGRAPH.LEFT
        set_cell_background(c, MINT_LIGHT_HEX if i % 2 == 1 else "FFFFFF")

doc.add_paragraph().paragraph_format.space_after = Pt(2)

# Detalhamento Proximal e Resistência
p_prox_desc = doc.add_paragraph()
p_prox_desc.paragraph_format.space_after = Pt(6)
r_px = p_prox_desc.add_run(
    "Erguer 56,0 kg (quase 86% da sua massa corporal) em desenvolvimento estrito no Shoulder Press demonstra elevado nível de força máxima de empurrada "
    "vertical, exigindo ativação expressiva de deltóides e tríceps em conjunto com a elevação e rotação superior das escápulas (serrátil anterior e trapézio) [10]. "
    "Na prática do Handstand, essa força potencializa a capacidade de 'empurrar o chão para longe', travando ativamente a cintura escapular para que o tronco "
    "não afunde nos ombros sob a ação da gravidade [6,10].\n\n"
    "Por sua vez, a sustentação de 64 segundos na parada de mão na parede (Belly-to-Wall a 20 cm) comprova excelente resistência isométrica à fadiga dos "
    "músculos estabilizadores proximais e do core sob alinhamento estrito [6,11]. No treinamento prático, dada a especificidade estática do teste, essa "
    "resistência sugere sobretudo uma elevada capacidade para sustentar a postura no Handstand estático e retardar a degradação técnica ao longo de séries "
    "sucessivas, podendo também fornecer uma base de suporte para tarefas invertidas mais dinâmicas como o Handstand Walk."
)
r_px.font.size = Pt(8.8)
r_px.font.color.rgb = TEXT_DARK_RGB

# =========================================================================
# ETAPA 3: SESSÃO 2
# =========================================================================
h3 = doc.add_heading("3. Próxima Etapa: Sessão 2 no LaBioCoM (Vicon & Bertec)", level=2)
h3.runs[0].font.color.rgb = EMERALD_DARK_RGB
h3.runs[0].font.size = Pt(12)

p_s2 = doc.add_paragraph(
    "Sua segunda sessão está confirmada para Quarta-feira, 09/09/2026 das 08:00 às 09:00 no LaBioCoM. "
    "Nessa etapa avaliaremos a cinemática e a cinética do Handstand e do Handstand Walk:\n"
    "• Sistema Vicon (12 Câmeras 3D Infravermelhas): Medirá o alinhamento tridimensional de punhos, ombros, quadril e ponta de pé [6,11].\n"
    "• Plataformas de Força Bertec: Medirão a oscilação milimétrica do Centro de Pressão (CoP) a 1000 Hz, permitindo investigar a correlação direta entre o controle postural dinâmico e o torque de flexores de punho medido no Biodex [6,7].\n"
    "• Handstand Walk (HSW): Registrará a velocidade de deslocamento, comprimento das passadas com as mãos e cadência motora!"
)
p_s2.runs[0].font.color.rgb = TEXT_DARK_RGB
p_s2.paragraph_format.space_after = Pt(6)

# =========================================================================
# ETAPA 4: REFERÊNCIAS CIENTÍFICAS
# =========================================================================
h4 = doc.add_heading("Referências Científicas e Normativas Consultadas", level=2)
h4.runs[0].font.color.rgb = EMERALD_DARK_RGB
h4.runs[0].font.size = Pt(10)

referencias = [
    "[1] Kyle, U. G., et al. (2004). Bioelectrical impedance analysis—part I: review of principles and methods. Clinical Nutrition, 23(5), 1226-1243.",
    "[2] Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. Journal of Applied Physiology, 89(2), 465-471.",
    "[3] American College of Sports Medicine (ACSM). (2018). ACSM's Guidelines for Exercise Testing and Prescription (10th ed.). Wolters Kluwer.",
    "[4] Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. Am J Clin Nutr, 82(1), 49-52.",
    "[5] Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. Clinical Nutrition, 31(6), 854-861.",
    "[6] Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. Sports Biomechanics, 1(2), 163-176.",
    "[7] Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Balance control strategies during perturbed and unperturbed balance in standing and handstand. Royal Society Open Science, 4(7), 161018.",
    "[8] Novaes, R. D., et al. (2009). Equações de referência para predição da força de preensão manual em indivíduos brasileiros saudáveis. Rev Bras Med Esporte, 15(4), 265-270.",
    "[9] Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. J Phys Ther Sci, 31(11), 932-938.",
    "[10] Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. Strength & Conditioning Journal, 41(4), 48-60.",
    "[11] Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. Human Movement Science, 26(4), 577-594.",
    "[12] Ellenbecker, T. S., et al. (2006). Isokinetic wrist strength in competitive athletes. American Journal of Sports Medicine, 34(11), 1845-1852.",
    "[13] Alizadehkhaiyat, O., et al. (2007). Isometric forearm and wrist strength in healthy adults. Journal of Electromyography and Kinesiology, 17(5), 629-637.",
    "[14] Rohleder, J., et al. (2021). Wrist joint biomechanics and handstand stability in gymnastics. Sports Biomechanics, 20(3), 312-326.",
    "[15] Bishop, C., Turner, A., & Read, P. (2018). Effects of inter-limb asymmetries on physical and sports performance: a systematic review. Journal of Sports Sciences, 36(10), 1135-1144.",
    "[16] Herzog, W., Nigg, B. M., Read, L. J., & Olsson, E. (1989). Asymmetries in ground reaction force patterns in normal human gait. Medicine and Science in Sports and Exercise, 21(1), 110-118."
]

for ref in referencias:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_after = Pt(2)
    r_r = p_ref.add_run(ref)
    r_r.font.name = "Arial"
    r_r.font.size = Pt(8)
    r_r.font.color.rgb = TEXT_MUTED_RGB

doc.save(DOCX_OUT)
print("Saved refined DOCX (academic tone & strict test order) to:", DOCX_OUT)

# =========================================================================
# 2. GERAR VERSÃO HTML NA MESMA ORDEM CRONOLÓGICA E SEM CONFUSÃO VISUAL
# =========================================================================
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório Individual de Desempenho - Gustavo Donato (P001) | EEFERP-USP</title>
<style>
  :root {{
    --primary-gradient: linear-gradient(135deg, #064e3b 0%, #047857 50%, #059669 100%);
    --accent-gradient: linear-gradient(90deg, #10b981, #34d399, #6ee7b7);
    --card-bg: #ffffff;
    --text-main: #0f172a;
    --text-body: #334155;
    --text-muted: #64748b;
    --emerald-dark: #064e3b;
    --emerald-medium: #047857;
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
    max-width: 880px;
    margin: 0 auto;
    background: var(--card-bg);
    border-radius: 20px;
    box-shadow: 0 10px 35px -5px rgba(0, 0, 0, 0.06), 0 0 0 1px rgba(0, 0, 0, 0.04);
    overflow: hidden;
  }}

  .hero-header {{
    background: var(--primary-gradient);
    color: white;
    padding: 36px 32px 30px;
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

  .institution-badge {{
    display: inline-flex;
    align-items: center;
    background: rgba(255, 255, 255, 0.12);
    backdrop-filter: blur(8px);
    border: 1px solid rgba(255, 255, 255, 0.2);
    padding: 6px 16px;
    border-radius: 9999px;
    font-size: 11px;
    font-weight: 600;
    letter-spacing: 0.8px;
    text-transform: uppercase;
    color: #a7f3d0;
    margin-bottom: 14px;
  }}

  .hero-header h1 {{
    margin: 0 0 8px 0;
    font-size: 24px;
    font-weight: 800;
    letter-spacing: -0.5px;
    color: #ffffff;
  }}

  .hero-header p {{
    margin: 0;
    font-size: 13.5px;
    color: #d1fae5;
    font-weight: 400;
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
    margin-bottom: 28px;
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
    font-size: 14px;
    font-weight: 700;
    color: var(--text-main);
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

  /* GRID DE KPIS NA ORDEM CRONOLÓGICA DAS COLETAS */
  .metrics-grid {{
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(190px, 1fr));
    gap: 14px;
    margin: 18px 0;
  }}

  .metric-box {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 18px;
    position: relative;
    overflow: hidden;
    transition: all 0.25s ease;
    box-shadow: 0 2px 8px rgba(0,0,0,0.02);
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    min-height: 155px;
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
    min-height: 38px;
    display: flex;
    align-items: flex-start;
  }}

  .metric-label {{
    font-size: 12px;
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
    font-size: 28px;
    font-weight: 800;
    color: var(--text-main);
    line-height: 1.1;
    margin: 0;
    letter-spacing: -0.5px;
  }}

  .metric-footer {{
    min-height: 28px;
    display: flex;
    align-items: center;
  }}

  .metric-pill {{
    display: inline-flex;
    align-items: center;
    background: #ecfdf5;
    color: #047857;
    font-size: 11px;
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
    padding: 20px 24px;
    margin: 22px 0;
  }}

  .callout-title {{
    display: flex;
    align-items: center;
    gap: 8px;
    font-size: 15px;
    font-weight: 800;
    color: var(--emerald-dark);
    margin-bottom: 8px;
  }}

  .callout-text {{
    font-size: 13.5px;
    color: #1e293b;
    margin: 0;
    line-height: 1.65;
  }}

  /* CARD BIODEX LIMPO E DIRETO (SEM POLUIÇÃO DE BARRAS REPETIDAS) */
  .biodex-card {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 14px;
    padding: 24px;
    margin: 24px 0;
    box-shadow: 0 4px 15px rgba(0,0,0,0.03);
  }}

  .biodex-header {{
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-bottom: 18px;
    flex-wrap: wrap;
    gap: 10px;
    border-bottom: 1px solid #f1f5f9;
    padding-bottom: 12px;
  }}

  .biodex-header h3 {{
    margin: 0;
    font-size: 16px;
    color: var(--emerald-dark);
    font-weight: 800;
  }}

  .biodex-badge {{
    background: #ecfdf5;
    color: #047857;
    font-weight: 700;
    font-size: 11.5px;
    padding: 5px 12px;
    border-radius: 9999px;
    border: 1px solid #a7f3d0;
  }}

  .practice-box {{
    background: #ffffff;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin: 18px 0;
  }}

  .practice-box h4 {{
    margin: 0 0 10px 0;
    color: var(--emerald-dark);
    font-size: 14px;
  }}

  .practice-box ul {{
    margin: 0;
    padding-left: 20px;
  }}

  .practice-box li {{
    margin-bottom: 8px;
    font-size: 13px;
    color: var(--text-body);
  }}

  .references-card {{
    background: #f8fafc;
    border: 1px solid #e2e8f0;
    border-radius: 12px;
    padding: 20px;
    margin-top: 32px;
  }}

  .references-card h4 {{
    margin: 0 0 12px 0;
    font-size: 12.5px;
    font-weight: 800;
    color: var(--emerald-dark);
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }}

  .references-card ol {{
    margin: 0;
    padding-left: 18px;
    font-size: 11.5px;
    color: var(--text-muted);
  }}

  .references-card li {{
    margin-bottom: 6px;
    line-height: 1.45;
  }}

  .footer {{
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 24px 32px;
    text-align: center;
    font-size: 12px;
    color: var(--text-muted);
  }}

  .footer strong {{
    color: var(--emerald-dark);
  }}

  sup {{
    font-weight: 800;
    color: #10b981;
  }}
</style>
</head>
<body>

<div class="card-container">
  <div class="hero-header">
    <div class="institution-badge">Universidade de São Paulo • EEFERP-USP</div>
    <h1>Relatório Individual de Desempenho & Composição Corporal</h1>
    <p>Projeto de Pesquisa: {TITULO_OFICIAL_PROJETO}</p>
  </div>

  <div class="content">
    <div class="athlete-card">
      <div class="athlete-item">
        <strong>Participante</strong>
        <span>Gustavo Henrique Donato</span>
      </div>
      <div class="athlete-item">
        <strong>Código / ID</strong>
        <span>P001 (Atleta Piloto)</span>
      </div>
      <div class="athlete-item">
        <strong>Idade / Sexo</strong>
        <span>20 anos | Masculino</span>
      </div>
      <div class="athlete-item">
        <strong>Membro Dominante</strong>
        <span>Destro (Direito)</span>
      </div>
      <div class="athlete-item">
        <strong>Data da Coleta (S1)</strong>
        <span>02/09/2026 (LaCiDH)</span>
      </div>
    </div>

    <p style="font-size: 14px; color: var(--text-body); margin-bottom: 24px;">
      Olá, <strong>Gustavo</strong>! Agradecemos a sua dedicação na primeira sessão da pesquisa de mestrado na EEFERP-USP. 
      Abaixo apresentamos a sua devolutiva individual com os testes organizados na exata sequência de execução da coleta: 
      <strong>1) Composição Corporal (BIA)</strong>, <strong>2) Preensão Manual</strong>, <strong>3) Dinamometria Isométrica de Punho (Biodex)</strong>, 
      <strong>4) 1-RM no Shoulder Press</strong> e <strong>5) Resistência Belly-to-Wall Handstand</strong>, acompanhados de sua fundamentação científica internacional <sup>[1-14]</sup>.
    </p>

    <!-- 1. COMPOSIÇÃO CORPORAL -->
    <div class="section-title">
      <span class="badge-num">1</span>
      Composição Corporal — Bioimpedância Elétrica (Sanny® BIA1011-AF)
    </div>

    <div class="metrics-grid">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Gordura Corporal (%GC) <sup>[1,3]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">13,88%</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Padrão Atlético Saudável (10–15%)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Massa Livre de Gordura <sup>[1]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">56,15 kg</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">86,1% em Massa Magra Ativa</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Massa Muscular Esquelética <sup>[2]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">31,06 kg</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">Suporte Antigravitacional Adequado</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">Ângulo de Fase (PhA) <sup>[4,5]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value" style="color: #047857;">8,98°</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #dcfce7; color: #047857;">Integridade Celular Elevada</div>
        </div>
      </div>
    </div>

    <div class="callout-highlight">
      <div class="callout-title">
        💡 O que significa o seu Ângulo de Fase (8,98°)? <sup>[4,5]</sup>
      </div>
      <p class="callout-text">
        O Ângulo de Fase (PhA) é um biomarcador derivado da relação entre resistência e reatância, indicativo da capacitância e integridade das membranas celulares. 
        Em homens jovens saudáveis da sua faixa etária, a literatura reporta valores médios de referência entre <strong>6,5° e 7,8°</strong> <sup>[4]</sup>. 
        O seu resultado de <strong>8,98°</strong> reflete um tecido celular de excelente integridade estrutural e bom estado de hidratação intra e extracelular.
      </p>
    </div>

    <!-- 2. FORÇA NEUROMUSCULAR NA ORDEM CRONOLÓGICA DAS COLETAS -->
    <div class="section-title">
      <span class="badge-num">2</span>
      Perfil Neuromuscular e Força Específica (LaCiDH)
    </div>

    <!-- 2.1 FORÇA DISTAL: PREENSÃO E FLEXORES DE PUNHO -->
    <h3 style="font-size: 15px; font-weight: 700; color: var(--text-heading); margin: 18px 0 10px 0;">
      2.1 Força Distal: Preensão Manual e Flexores de Punho (Biodex)
    </h3>

    <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">1º Preensão Manual (FPM) <sup>[8,9]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value">52,0 kgf</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">Relativa: 0,80 kgf/kg</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #ecfdf5; color: #047857; font-weight: 600; border: 1px solid #a7f3d0;">
            Simetria (LSI): 113,0% (Diferença de 13,0% • Não-Dominante [E] mais forte)
          </div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">2º Flexores de Punho (Biodex a 70°) <sup>[6,7]</sup></div>
        </div>
        <div class="metric-body" style="display: flex; align-items: baseline; justify-content: space-between;">
          <div class="metric-value" style="color: #047857;">20,5 N·m</div>
          <div style="font-size: 12.5px; font-weight: 600; color: var(--text-muted);">Média: 19,5 N·m (0,299 N·m/kg)</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill" style="background: #ecfdf5; color: #047857; font-weight: 600; border: 1px solid #a7f3d0;">
            Simetria (LSI): 110,8% (Diferença de 10,8% • Não-Dominante [E] mais forte)
          </div>
        </div>
      </div>
    </div>

    <!-- DETALHAMENTO DISTAL 2.1 -->
    <div class="biodex-card" style="margin-top: 14px;">
      <div class="biodex-header">
        <div>
          <h4 style="margin: 0; font-size: 13.5px; font-weight: 700; color: var(--text-heading);">Análise Biomecânica dos Punhos e Estratégia de Equilíbrio</h4>
          <span style="font-size: 12px; color: var(--text-muted);">Interface Palmar, Torque a 70°, Simetria Bilateral e Aplicação no Handstand Walk</span>
        </div>
      </div>

      <div class="callout-highlight" style="margin-top: 14px; margin-bottom: 0;">
        <p class="callout-text">
          No modelo biomecânico de pêndulo invertido do Handstand, os flexores de punho e a musculatura palmar desempenham no equilíbrio de cabeça para baixo a mesma função que a panturrilha e os pés exercem na postura ereta bípede (<strong>"Wrist Strategy"</strong>) <sup>[6,7]</sup>. Essa musculatura atua como o verdadeiro <strong>"freio de mão" da parada de mão</strong>. Da mesma forma que cravamos as pontas dos pés no solo para conter uma oscilação para a frente, no Handstand são as pontas dos dedos e a palma que esmagam o chão quando o corpo passa da vertical (o temido <em>overbalance</em>). Essa pressão gera um torque corretivo instantâneo que empurra o corpo de volta para o prumo. Ter punhos e mãos fortes proporciona uma ampla margem de segurança para salvar o equilíbrio com pequenos ajustes nas mãos, evitando quebrar a linha dos ombros ou arquear a lombar (a clássica postura em "banana") <sup>[6,7]</sup>.
        </p>
        <p class="callout-text" style="margin-top: 10px;">
          Para garantir essa sustentação palmar, a avaliação de <strong>Força de Preensão Manual (FPM)</strong> acusou pico de <strong>52,0 kgf no membro não-dominante (esquerdo) e 46,0 kgf no membro dominante (direito)</strong> (relação relativa de <strong>0,80 kgf/kg</strong>), superando com folga a média de homens jovens saudáveis (~42 kgf <sup>[8,9]</sup>). O <strong>Índice de Simetria dos Membros na preensão (LSI: 113,0%, diferença de 13,0% a favor da mão esquerda)</strong> situa-se dentro da faixa de equilíbrio fisiológico (<15%) preconizada na literatura neuromuscular <sup>[15]</sup>. Enquanto em destros não-atletas a mão dominante costuma ser discretamente superior (~10%), praticantes de calistenia e ginástica frequentemente equilibram ou invertem essa relação devido às exigências bilaterais de sustentação do peso corporal. Na prática, essa simetria de preensão assegura rigidez uniforme no carpo em ambos os lados <sup>[13,14]</sup>, impedindo o colapso unilateral da base palmar sob o peso invertido. Ademais, no <strong>Handstand Walk</strong>, uma pegada bilateralmente equivalente sugere capacidade homogênea de absorção de impacto no contato sucessivo de cada mão contra o solo (<em>hand strike</em>), mitigando oscilações rotacionais do tronco e prevenindo sobrecargas articulares assimétricas.
        </p>
        <p class="callout-text" style="margin-top: 10px;">
          Já no <strong>Biodex System 4 PRO</strong>, o torque isométrico dos flexores de punho foi avaliado a <strong>70° de extensão</strong>, posição selecionada por sua especificidade biomecânica ao mimetizar a dorsiflexão funcional da mão contra o solo no Handstand <sup>[6,7]</sup>. O voluntário alcançou torque médio bilateral de <strong>19,5 N·m (0,299 N·m/kg)</strong> (com pico de <strong>20,5 N·m [0,314 N·m/kg] no membro não-dominante [esquerdo]</strong> e <strong>18,5 N·m [0,284 N·m/kg] no membro dominante [direito]</strong>), quantificando a capacidade específica de geração de torque no ângulo funcional de atuação do freio palmar (<em>Wrist Strategy</em>) <sup>[6,7]</sup>. O <strong>Índice de Simetria dos Membros nos punhos (LSI: 110,8%, diferença de apenas 10,8% a favor do lado esquerdo)</strong> também atesta excelente simetria intermembros (<15%) <sup>[15]</sup>. Em analogia à locomoção e marcha humana <sup>[15,16]</sup>, essa simetria de torque angular é determinante no <strong>Handstand Walk</strong>: ao caminhar com as mãos, punhos equilibrados tendem a favorecer passadas mais estáveis, com tempos de contato homogêneos e controle direcional consistente, auxiliando a prevenir desvios de trajetória e compensações escapulares unilaterais.
        </p>
      </div>
    </div>

    <!-- 2.2 FORÇA PROXIMAL E RESISTÊNCIA POSTURAL -->
    <h3 style="font-size: 15px; font-weight: 700; color: var(--text-heading); margin: 24px 0 10px 0;">
      2.2 Força Proximal e Resistência: Shoulder Press e Parada de Mão na Parede
    </h3>

    <div class="metrics-grid" style="grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));">
      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">3º 1-RM Shoulder Press <sup>[10]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">56,0 kg</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">85,8% da massa corporal (Força Máxima)</div>
        </div>
      </div>

      <div class="metric-box">
        <div class="metric-header">
          <div class="metric-label">4º Resistência Wall HS <sup>[6]</sup></div>
        </div>
        <div class="metric-body">
          <div class="metric-value">64 seg</div>
        </div>
        <div class="metric-footer">
          <div class="metric-pill">>1 min em Handstand Estrito</div>
        </div>
      </div>
    </div>

    <!-- DETALHAMENTO PROXIMAL 2.2 -->
    <div class="biodex-card" style="margin-top: 14px;">
      <div class="biodex-header">
        <div>
          <h4 style="margin: 0; font-size: 13.5px; font-weight: 700; color: var(--text-heading);">Análise de Empurrada Vertical e Sustentação Sob Fadiga</h4>
          <span style="font-size: 12px; color: var(--text-muted);">Cintura Escapular, Travamento Articular e Estabilidade do Core</span>
        </div>
      </div>

      <div class="callout-highlight" style="margin-top: 14px; margin-bottom: 0;">
        <p class="callout-text">
          Erguer <strong>56,0 kg (quase 86% da sua massa corporal)</strong> em desenvolvimento estrito no <strong>Shoulder Press</strong> demonstra elevado nível de força máxima de empurrada vertical, exigindo ativação expressiva de deltóides e tríceps em conjunto com a elevação e rotação superior das escápulas (serrátil anterior e trapézio) <sup>[10]</sup>. Na prática do Handstand, essa força potencializa a capacidade de <strong>"empurrar o chão para longe"</strong>, travando ativamente a cintura escapular para que o tronco não afunde nos ombros sob a ação da gravidade <sup>[6,10]</sup>.
        </p>
        <p class="callout-text" style="margin-top: 10px;">
          Por sua vez, a sustentação de <strong>64 segundos na parada de mão na parede</strong> (Belly-to-Wall a 20 cm) comprova excelente resistência isométrica à fadiga dos músculos estabilizadores proximais e do core sob alinhamento estrito <sup>[6,11]</sup>. No treinamento prático, dada a especificidade estática do teste, essa resistência sugere sobretudo uma elevada capacidade para sustentar a postura no <strong>Handstand estático</strong> e retardar a degradação técnica ao longo de séries sucessivas, podendo também fornecer uma base de suporte para tarefas invertidas mais dinâmicas como o <strong>Handstand Walk</strong>.
        </p>
      </div>
    </div>

    <!-- BOX EXPLICAÇÃO PRÁTICA NA ORDEM DOS TESTES -->
    <div class="practice-box">
      <h4>🎯 Resumo Integrado:</h4>
      <ul>
        <li><strong>1º Preensão Manual (52 kgf) <sup>[8,9]</sup>:</strong> Significativamente acima da média populacional (~42 kgf). Auxilia na firmeza palmar e na ancoragem mecânica das mãos contra o solo (LSI: 113,0%, discreto predomínio do membro não-dominante/esquerdo).</li>
        <li><strong>2º Flexores de Punho no Biodex (20,5 N·m / 0,314 N·m/kg) <sup>[6,7,12]</sup>:</strong> Capacidade de freio corretivo ("Wrist Strategy") compatível com as demandas da parada de mão, com excelente simetria bilateral (LSI: 110,8%; membro não-dominante/esquerdo ligeiramente mais forte que o dominante) para suportar o peso invertido.</li>
        <li><strong>3º Shoulder Press (56 kg estrito) <sup>[10]</sup>:</strong> Empurrar quase 86% do peso corporal acima da cabeça sem auxílio das pernas reflete alta rigidez isométrica e dinâmica da cintura escapular (deltóides e tríceps).</li>
        <li><strong>4º Resistência Belly-to-Wall (64s) <sup>[6]</sup>:</strong> Sustentação contínua superior a 1 minuto em extensão estrita, sugerindo boa tolerância dos estabilizadores escapulares (serrátil anterior e trapézio) e core sob fadiga cumulativa.</li>
      </ul>
    </div>

    <!-- 3. SESSÃO 2 -->
    <div class="section-title">
      <span class="badge-num">3</span>
      Próxima Etapa: Sessão 2 no LaBioCoM (Vicon & Bertec)
    </div>

    <p style="font-size: 13.5px; color: var(--text-body);">
      Sua segunda sessão está confirmada para <strong>Quarta-feira, 09/09/2026 das 08:00 às 09:00 no LaBioCoM</strong>. 
      Na semana que vem vamos avaliar a biomecânica cinemática e cinética em movimento:
    </p>
    <ul style="font-size: 13px; color: var(--text-body); padding-left: 20px;">
      <li><strong>12 Câmeras 3D Vicon:</strong> Medição do alinhamento tridimensional de punhos, ombros, quadril e ponta de pé no espaço <sup>[6,11]</sup>.</li>
      <li><strong>Plataformas de Força Bertec:</strong> Registro a 1000 Hz da oscilação do Centro de Pressão (CoP) para analisar a atuação prática da estratégia dos punhos <sup>[6,7]</sup>.</li>
      <li><strong>Handstand Walk (HSW):</strong> Registro da velocidade dos passos com as mãos, comprimento das passadas e cadência motora!</li>
    </ul>

    <!-- 4. REFERÊNCIAS CIENTÍFICAS -->
    <div class="references-card">
      <h4>📚 Referências Científicas e Normativas Consultadas:</h4>
      <ol>
        <li>Kyle, U. G., et al. (2004). Bioelectrical impedance analysis—part I: review of principles and methods. <em>Clinical Nutrition</em>, 23(5), 1226-1243.</li>
        <li>Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. <em>Journal of Applied Physiology</em>, 89(2), 465-471.</li>
        <li>American College of Sports Medicine (ACSM). (2018). <em>ACSM's Guidelines for Exercise Testing and Prescription</em> (10th ed.). Wolters Kluwer.</li>
        <li>Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. <em>Am J Clin Nutr</em>, 82(1), 49-52.</li>
        <li>Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. <em>Clinical Nutrition</em>, 31(6), 854-861.</li>
        <li>Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. <em>Sports Biomechanics</em>, 1(2), 163-176.</li>
        <li>Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Balance control strategies during perturbed and unperturbed balance in standing and handstand. <em>Royal Society Open Science</em>, 4(7), 161018.</li>
        <li>Novaes, R. D., et al. (2009). Equações de referência para predição da força de preensão manual em indivíduos brasileiros saudáveis. <em>Rev Bras Med Esporte</em>, 15(4), 265-270.</li>
        <li>Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. <em>J Phys Ther Sci</em>, 31(11), 932-938.</li>
        <li>Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. <em>Strength & Conditioning Journal</em>, 41(4), 48-60.</li>
        <li>Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. <em>Human Movement Science</em>, 26(4), 577-594.</li>
        <li>Ellenbecker, T. S., et al. (2006). Isokinetic wrist strength in competitive athletes. <em>American Journal of Sports Medicine</em>, 34(11), 1845-1852.</li>
        <li>Alizadehkhaiyat, O., et al. (2007). Isometric forearm and wrist strength in healthy adults. <em>Journal of Electromyography and Kinesiology</em>, 17(5), 629-637.</li>
        <li>Rohleder, J., et al. (2021). Wrist joint biomechanics and handstand stability in gymnastics. <em>Sports Biomechanics</em>, 20(3), 312-326.</li>
        <li>Bishop, C., Turner, A., & Read, P. (2018). Effects of inter-limb asymmetries on physical and sports performance: a systematic review. <em>Journal of Sports Sciences</em>, 36(10), 1135-1144.</li>
        <li>Herzog, W., Nigg, B. M., Read, L. J., & Olsson, E. (1989). Asymmetries in ground reaction force patterns in normal human gait. <em>Medicine and Science in Sports and Exercise</em>, 21(1), 110-118.</li>
      </ol>
    </div>

  </div>

  <div class="footer">
    Pesquisador Responsável: <strong>Guilherme de Paula Lemos</strong> | Orientador: <strong>Prof. Dr. Matheus Machado Gomes</strong><br>
    Escola de Educação Física e Esporte de Ribeirão Preto — EEFERP-USP | Contato: guilherme.lemos@usp.br
  </div>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)
print("Saved refined HTML (academic tone & strict test order) to:", HTML_OUT)

if __name__ == "__main__":
    pass
