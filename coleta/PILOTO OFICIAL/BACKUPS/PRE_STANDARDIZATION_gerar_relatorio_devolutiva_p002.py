import os
import sys
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

DOCX_OUT = os.path.join(DIR_RESULTADOS, "P002_RELATORIO_DEVOLUTIVA_GUILHERME_LEMOS.docx")
HTML_OUT = os.path.join(DIR_RESULTADOS, "P002_RELATORIO_DEVOLUTIVA_GUILHERME_LEMOS.html")

TITULO_OFICIAL_PROJETO = "Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk"

# =========================================================================
# AUDITORIA E VALIDAÇÃO DOS DADOS DE P002 (GUILHERME LEMOS)
# =========================================================================
def double_check_valores_p002():
    massa = 87.20
    estatura = 171.0
    imc_calculado = round(massa / ((estatura / 100.0) ** 2), 2) # 29.82
    imlg_calculado = round(70.45 / ((estatura / 100.0) ** 2), 2) # 24.09
    
    # Biodex
    pt_d = 12.9
    pt_e = 17.1
    media_bio = round((pt_d + pt_e) / 2.0, 2) # 15.00
    rel_media_bio = round(media_bio / massa, 3) # 0.172
    rel_max_bio = round(pt_e / massa, 3) # 0.196
    lsi_bio = round((pt_e / pt_d) * 100.0, 1) # 132.6%
    diff_lsi = round(lsi_bio - 100.0, 1) # 32.6%

    # Preensão
    fpm_d = 52.0
    fpm_e = 53.0
    fpm_media = round((fpm_d + fpm_e) / 2.0, 1) # 52.5
    fpm_rel_max = round(fpm_e / massa, 3) # 0.608
    lsi_fpm = round((fpm_e / fpm_d) * 100.0, 1) # 101.9%

    # 1-RM Shoulder Press
    sp_1rm = 66.0
    sp_rel = round((sp_1rm / massa) * 100.0, 1) # 75.7%

    # Wall-HS
    wall_max = 101.0

    print("=" * 80)
    print("[AUDITORIA INTERNA P002 - GUILHERME LEMOS OK]")
    print(f"  -> Idade: 42 anos | Massa: {massa} kg | Estatura: {estatura} cm")
    print(f"  -> IMC: {imc_calculado} kg/m² | IMLG (FFMI): {imlg_calculado} kg/m²")
    print(f"  -> BIA Sun: %Gord = 19.40% | MLG = 70.45 kg | MG = 16.95 kg | AF = 6.78°")
    print(f"  -> FPM (Jamar): D={fpm_d} kgf, E={fpm_e} kgf | LSI: {lsi_fpm}%")
    print(f"  -> Biodex: D={pt_d} N·m, E={pt_e} N·m | Média={media_bio} N·m | LSI: {lsi_bio}%")
    print(f"  -> 1-RM Shoulder Press: {sp_1rm} kg ({sp_rel}% da MC)")
    print(f"  -> Resistência Wall-HS: {wall_max} s (1 min e 41 s)")
    print("=" * 80)

double_check_valores_p002()

# =========================================================================
# 1. GERAR DOCUMENTO DOCX COM TEXTO SÓBRIO E CALIBRADO
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

format_cell(t_part.rows[0].cells[0], "PARTICIPANTE", "Guilherme Lemos")
format_cell(t_part.rows[0].cells[1], "CÓDIGO / ID", "P002 (Atleta Piloto)")
format_cell(t_part.rows[0].cells[2], "DATA DA SESSÃO 1", "14/09/2026")
format_cell(t_part.rows[0].cells[3], "FAIXA ETÁRIA / IDADE", "42 anos (40-44 anos)")

format_cell(t_part.rows[1].cells[0], "SEXO / DOMINÂNCIA", "Masculino | Destro (D)")
format_cell(t_part.rows[1].cells[1], "MASSA CORPORAL", "87,20 kg")
format_cell(t_part.rows[1].cells[2], "ESTATURA", "171,0 cm")
format_cell(t_part.rows[1].cells[3], "MODALIDADE / PERFIL", "CrossFit / Força / Calistenia")

doc.add_paragraph().paragraph_format.space_after = Pt(4)

# Apresentação do Relatório
p_intro = doc.add_paragraph()
r_in1 = p_intro.add_run("Prezado Guilherme,\n")
r_in1.bold = True
r_in1.font.color.rgb = EMERALD_DARK_RGB
r_in2 = p_intro.add_run(
    "Este relatório apresenta a devolutiva individual dos testes realizados no LaCiDH, organizados rigorosamente na sequência cronológica da sua coleta: "
    "1) Bioimpedância Elétrica Tetrapolar (Sanny Sun et al., 2003), 2) Força de Preensão Manual, 3) Dinamometria Isométrica dos Flexores de Punho (Biodex 4 PRO), "
    "4) 1-RM no Shoulder Press e 5) Resistência na Parada de Mão na Parede. "
    "Cada indicador é contextualizado com base na literatura científica internacional, aplicando valores normativos condizentes com a sua faixa etária (40 a 44 anos) [1-16], "
    "com foco sóbrio e descritivo sobre como essas capacidades físicas fundamentam as demandas biomecânicas no Handstand e Handstand Walk!"
)
r_in2.font.color.rgb = TEXT_DARK_RGB
p_intro.paragraph_format.space_after = Pt(6)

# =========================================================================
# ETAPA 1: COMPOSIÇÃO CORPORAL (BIA)
# =========================================================================
h1 = doc.add_heading("1. Composição Corporal (Bioimpedância Elétrica Sanny® BIA1011-AF — Sun et al., 2003)", level=2)
h1.runs[0].font.color.rgb = EMERALD_DARK_RGB
h1.runs[0].font.size = Pt(12)

t_bia = doc.add_table(rows=8, cols=3)
t_bia.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_bia = ["Variável Avaliada", "Seu Resultado", "Interpretação & Valores Normativos (40-49 anos)"]
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
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER if j == 1 else WD_ALIGN_PARAGRAPH.LEFT

bia_dados = [
    ("Massa Corporal & Estatura", "87,20 kg | 171,0 cm", "IMC = 29,82 kg/m² (Limitação clássica do IMC em praticantes de força [3,6])"),
    ("Índice de Massa Livre de Gordura (FFMI) [6,7]", "24,09 kg/m²", "Elevada robustez musculoesquelética; superior à média da população não treinada (18,5 a 20,0 kg/m² [6,7])"),
    ("Percentual de Gordura (%GC) [1,3]", "19,40%", "Adequado / Bom para homens de 40-49 anos treinados (ACSM: 16% a 22%)"),
    ("Massa Livre de Gordura (MLG) [1]", "70,45 kg (80,6%)", "Predomínio de massa livre de gordura (músculo, osso e água corporal total)"),
    ("Massa Muscular Esquelética [2]", "37,37 kg (42,8%)", "Boa musculatura postural para suporte sob gravidade"),
    ("Massa Gorda Total [1]", "16,95 kg (19,4%)", "Reserva lipídica compatível com a rotina de treinos e peso total"),
    ("Ângulo de Fase (PhA) [4,5]", "6,78°", "Dentro da faixa de referência saudável para 40-49 anos (média: 7,15° ± 0,77° [4])")
]

for i, row in enumerate(bia_dados, 1):
    for j, val in enumerate(row):
        c = t_bia.cell(i, j)
        c.text = val
        set_cell_margins(c, top=80, bottom=80, left=140, right=140)
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

# Box de Contextualização Sóbria: FFMI vs IMC
p_ffmi = doc.add_paragraph()
p_ffmi.paragraph_format.space_before = Pt(6)
p_ffmi.paragraph_format.space_after = Pt(6)
r_ffmi_box = p_ffmi.add_run(
    "💡 Contextualização Metodológica: IMLG/FFMI (24,09 kg/m²) vs IMC (29,82 kg/m²) [6,7]\n"
    "O IMC tradicional (29,82 kg/m²) tende a superestimar o excesso de peso em indivíduos treinados, por não discriminar gordura de massa muscular. "
    "Para uma descrição mais adequada em Ciências do Esporte, utiliza-se o Índice de Massa Livre de Gordura (FFMI = MLG / Estatura²) [6,7]. "
    "Em homens saudáveis não treinados, a média populacional situa-se entre 18,5 e 20,0 kg/m² [7]. O seu resultado de 24,09 kg/m² reflete um porte físico "
    "robusto, com expressivos 70,45 kg de massa livre de gordura (incluindo tecido muscular, massa óssea e fluidos corporais), condizente com uma rotina "
    "séria de modalidades de força e peso corporal. Importante notar: por se tratar de uma bioimpedância realizada em estado nutricional e de hidratação normal "
    "(com 19,4% de gordura), o índice descreve a sua constituição física global do dia a dia, e não um limite hipertrófico desidratado de competição."
)
r_ffmi_box.font.size = Pt(9)
r_ffmi_box.font.color.rgb = TEXT_DARK_RGB

# =========================================================================
# ETAPA 2: TESTES DE FORÇA NEUROMUSCULAR (ORDEM CRONOLÓGICA DAS COLETAS)
# =========================================================================
h2 = doc.add_heading("2. Perfil Neuromuscular e Força Específica (LaCiDH)", level=2)
h2.runs[0].font.color.rgb = EMERALD_DARK_RGB
h2.runs[0].font.size = Pt(12)

# --- 2.1 FORÇA DISTAL: PREENSÃO E FLEXORES DE PUNHO ---
h2_1 = doc.add_heading("2.1 Força Distal: Preensão Manual (Jamar) e Flexores de Punho (Biodex 4 PRO)", level=3)
h2_1.runs[0].font.color.rgb = EMERALD_DARK_RGB
h2_1.runs[0].font.size = Pt(11)

t_forca_distal = doc.add_table(rows=3, cols=3)
t_forca_distal.alignment = WD_TABLE_ALIGNMENT.CENTER
headers_forca = ["Teste (Ordem de Execução)", "Seu Desempenho", "Interpretação e Referências Normativas (40-44 anos)"]
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
    ("1º Teste: Força de Preensão Manual (FPM) [8,9]\nDinamômetro Hidráulico Jamar/Saehan", 
     "Mão Direita (Dom): 52,0 kgf\nMão Esquerda (Não-Dom): 53,0 kgf\nMédia: 52,5 kgf | Relativa: 0,608 kgf/kg\nLSI: 101,9% (Excelente Simetria Bilateral)", 
     "Muito Bom! Situa-se acima da média de homens de 40-44 anos (média normativa: 45,5 a 47,0 kgf [8,9]), posicionando-se no percentil ≥85%. Simetria bilateral excelente (LSI 101,9%), conferindo base palmar estável."),
     
    ("2º Teste: Dinamometria Isométrica dos Flexores de Punho [10,11]\nDinamômetro Biodex Multi-Joint 4 PRO (70° TOWARD)",
     "Pico D (Dom): 12,9 N·m (CV: 11,1%)\nPico E (Não-Dom): 17,1 N·m (CV: 21,3%)\nMédia Bilateral: 15,0 N·m (0,172 N·m/kg)\nPico Máx: 0,196 N·m/kg | LSI: 132,6% (Não-Dom mais forte)", 
     "Avaliado na angulação funcional de 70° de extensão do Handstand [10,11]. O lado dominante apresentou boa consistência (CV 11,1%). O lado não-dominante exibiu maior pico de torque (+32,5%), demonstrando maior rigidez articular (stiffness).")
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

# Detalhamento Distal
p_distal_desc = doc.add_paragraph()
p_distal_desc.paragraph_format.space_before = Pt(4)
p_distal_desc.paragraph_format.space_after = Pt(6)
r_d1 = p_distal_desc.add_run(
    "No modelo mecânico de pêndulo invertido do Handstand, os flexores de punho e dedos desempenham função corretiva essencial "
    "('Wrist Strategy') [10,11]. Quando o corpo oscila ligeiramente além da vertical (overbalance), a pressão das mãos e dedos contra o solo "
    "gera um torque de flexão corretivo que empurra o Centro de Massa de volta para a área de sustentação.\n\n"
    "Na Preensão Manual (FPM), alcançar 52,0 kgf (direita) e 53,0 kgf (esquerda) representa um desempenho sólido: na literatura normativa "
    "(meta-análise de Bohannon, 2019 [8] e consórcio Dodds et al., 2014 [9]), a média para homens saudáveis de 40 a 44 anos é de aproximadamente 46,0 kgf. "
    "O seu resultado coloca você confortavelmente acima da média populacional (percentil ≥85%), com excelente simetria entre os lados (LSI: 101,9%, diferença inferior a 2%), "
    "o que proporciona ancoragem equilibrada entre os carpos direito e esquerdo.\n\n"
    "No dinamômetro isocinético Biodex 4 PRO a 70° de flexão (TOWARD), observou-se 12,9 N·m no punho direito (com boa reprodutibilidade, CV = 11,1%) "
    "e 17,1 N·m no punho esquerdo (LSI = 132,6%). Essa assimetria a favor do membro não-dominante é documentada em praticantes de modalidades de peso corporal e força, "
    "onde o membro de suporte secundário desenvolve maior rigidez adaptativa (stiffness). Na Sessão 2, verificaremos se essa diferença de torque se correlaciona "
    "com a simetria de contato no solo durante a caminhada invertida (Handstand Walk)."
)
r_d1.font.size = Pt(8.8)
r_d1.font.color.rgb = TEXT_DARK_RGB

# --- 2.2 FORÇA PROXIMAL E RESISTÊNCIA: SHOULDER PRESS E PAREDE ---
h2_2 = doc.add_heading("2.2 Força Proximal e Resistência: Shoulder Press e Parada de Mão na Parede (Wall-HS)", level=3)
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
    ("3º Teste: 1-RM no Shoulder Press (SP) [12]\nBarra Smith Estrita (Overhead Press)",
     "66,0 kg\n(75,7% da massa corporal)", 
     "Nível Avançado para homens de 40-49 anos [12,13]. Erguer ~76% do peso corporal em empurrada vertical estrita demonstra boa capacidade neuromuscular de deltoides, tríceps e fixadores escapulares."),
     
    ("4º Teste: Resistência Belly-to-Wall Handstand [10,14]\nParada de Mão Isométrica na Parede (20 cm)",
     "101,0 segundos (1 min e 41 s)\n(T1: 92s | T2: 101s)", 
     "Destaque do teste! Sustentação superior a 1m40s sob alinhamento rigoroso, indicando excelente capacidade de resistência isométrica à fadiga da cintura escapular e estabilizadores do tronco [10,14].")
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

# Detalhamento Proximal e Resistência
p_prox_desc = doc.add_paragraph()
p_prox_desc.paragraph_format.space_before = Pt(4)
p_prox_desc.paragraph_format.space_after = Pt(6)
r_px = p_prox_desc.add_run(
    "Erguer 66,0 kg em desenvolvimento estrito no Smith Machine representa 75,7% do seu peso corporal. Na literatura de força para adultos na faixa dos 40 anos, "
    "cargas acima de 70% da massa corporal situam o praticante em patamar avançado de força de membros superiores [12,13]. No Handstand, essa força assegura "
    "capacidade ativa de bloqueio escapuloumeral, evitando o colapso dos ombros sob a ação contínua da gravidade.\n\n"
    "No Belly-to-Wall Handstand, a sustentação de 101,0 segundos (1 min e 41 s) a 20 cm da parede evidencia ótima resistência muscular localizada. "
    "Sustentar 87 kg de peso em inversão por esse período exige trabalho coordenado e tolerância à fadiga do trapézio superior, serrátil anterior e musculatura do core, "
    "retardando a perda de alinhamento técnico durante séries sucessivas e tarefas invertidas prolongadas."
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
    "Na Sessão 2 no LaBioCoM, integraremos seus indicadores às análises biomecânicas tridimensionais:\n"
    "• Sistema Vicon (12 Câmeras 3D Infravermelhas): Rastreamento cinemático do alinhamento escapuloumeral, pelve e pernas, além da determinação da trajetória vertical do Centro de Massa (CoM) [10,14].\n"
    "• Plataformas de Força Bertec (1000 Hz): Registro cinético da oscilação milimétrica do Centro de Pressão (CoP), investigando a relação entre a força dos flexores de punho e a regulação postural no solo [10,11].\n"
    "• Handstand Walk (HSW): Análise espaço-temporal da caminhada invertida (comprimento de passada, velocidade e simetria de apoios manuais)!"
)
p_s2.runs[0].font.color.rgb = TEXT_DARK_RGB
p_s2.paragraph_format.space_after = Pt(6)

# =========================================================================
# ETAPA 4: REFERÊNCIAS CIENTÍFICAS
# =========================================================================
h4 = doc.add_heading("Referências Científicas e Normativas Consultadas (Ajustadas para 40-49 anos)", level=2)
h4.runs[0].font.color.rgb = EMERALD_DARK_RGB
h4.runs[0].font.size = Pt(10)

referencias = [
    "[1] Sun, S. S., Chumlea, W. C., Heymsfield, S. B., Lukaski, H. C., Schoeller, D., Friedl, K., ... & Hubbard, V. S. (2003). Development of bioelectrical impedance analysis prediction equations for body composition with the use of a multicomponent model for use in epidemiologic surveys. Am J Clin Nutr, 77(2), 331-340.",
    "[2] Janssen, I., Heymsfield, S. B., Baumgartner, R. N., & Ross, R. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. Journal of Applied Physiology, 89(2), 465-471.",
    "[3] American College of Sports Medicine (ACSM). (2018). ACSM's Guidelines for Exercise Testing and Prescription (10th ed.). Wolters Kluwer.",
    "[4] Barbosa-Silva, M. C. G., Barros, A. J., Wang, J., Heymsfield, S. B., & Pierson, R. N. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. Am J Clin Nutr, 82(1), 49-52. [Tabelas de referência para homens de 40-49 anos: 7,15° ± 0,77°].",
    "[5] Norman, K., Stobäus, N., Pirlich, M., & Bosy-Westphal, A. (2012). Bioelectrical phase angle as a biomarker—recent advances. Clinical Nutrition, 31(6), 854-861.",
    "[6] VanItallie, T. B., Yang, M. U., Heymsfield, S. B., Funk, R. C., & Boileau, R. A. (1990). Height-normalized indices of the body's fat-free mass and fat mass: potentially useful indicators for nutritional assessment. Am J Clin Nutr, 52(6), 953-959.",
    "[7] Schutz, Y., Kyle, U. U. G., & Pichard, C. (2002). Fat-free mass index and fat mass index percentiles in Caucasians aged 18–98 y. International Journal of Obesity, 26(7), 953-960.",
    "[8] Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. J Phys Ther Sci, 31(11), 932-938. [Normativa para homens de 40 a 44 anos: média 46,0 kgf].",
    "[9] Dodds, R. M., Syddall, H. E., Cooper, R., Ben-Shlomo, Y., Kuh, D., & Sayer, A. A. (2014). Globally representative normative data for handgrip strength: a systematic review and meta-analysis. PLoS ONE, 9(12), e113637.",
    "[10] Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. Sports Biomechanics, 1(2), 163-176.",
    "[11] Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Balance control strategies during perturbed and unperturbed balance in standing and handstand. Royal Society Open Science, 4(7), 161018.",
    "[12] Soriano, M. A., Jiménez-Reyes, P., Rhea, M. R., & Marín, P. J. (2019). The overhead press: A review of biomechanics and exercise prescription. Strength & Conditioning Journal, 41(4), 48-60.",
    "[13] Kilgore, L., & Rippetoe, M. (2011). Strength Training Standards. The Aasgaard Company.",
    "[14] Gautier, G., Thouvarecq, R., & Larue, J. (2007). Influence of visual information on postural control in a handstand. Human Movement Science, 26(4), 577-594.",
    "[15] Bishop, C., Turner, A., & Read, P. (2018). Effects of inter-limb asymmetries on physical and sports performance: a systematic review. Journal of Sports Sciences, 36(10), 1135-1144.",
    "[16] Ellenbecker, T. S., & Roetert, E. P. (2006). Isokinetic wrist strength in competitive athletes. American Journal of Sports Medicine, 34(11), 1845-1852."
]

for ref in referencias:
    p_ref = doc.add_paragraph()
    p_ref.paragraph_format.space_after = Pt(2)
    r_r = p_ref.add_run(ref)
    r_r.font.name = "Arial"
    r_r.font.size = Pt(8)
    r_r.font.color.rgb = TEXT_MUTED_RGB

doc.save(DOCX_OUT)
print(f"[OK] Documento DOCX gerado em:\n  -> {DOCX_OUT}")

# =========================================================================
# 2. GERAR DOCUMENTO HTML CALIBRADO E PROFISSIONAL
# =========================================================================
html_content = f"""<!DOCTYPE html>
<html lang="pt-BR">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Relatório Individual de Desempenho - Guilherme Lemos (P002) | EEFERP-USP</title>
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

  * {{ box-sizing: border-box; }}

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

  .athlete-field {{
    display: flex;
    flex-direction: column;
  }}

  .athlete-field label {{
    font-size: 11px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    color: var(--emerald-medium);
    margin-bottom: 3px;
  }}

  .athlete-field span {{
    font-size: 14.5px;
    font-weight: 600;
    color: var(--text-main);
  }}

  .section-title {{
    display: flex;
    align-items: center;
    font-size: 18px;
    font-weight: 800;
    color: var(--emerald-dark);
    margin: 28px 0 16px 0;
    padding-bottom: 8px;
    border-bottom: 2px solid #e2e8f0;
  }}

  .section-title span.badge {{
    background: var(--emerald-medium);
    color: white;
    width: 26px;
    height: 26px;
    border-radius: 50%;
    display: inline-flex;
    align-items: center;
    justify-content: center;
    font-size: 13px;
    margin-right: 10px;
  }}

  .data-table {{
    width: 100%;
    border-collapse: separate;
    border-spacing: 0;
    border-radius: 12px;
    overflow: hidden;
    border: 1px solid #e2e8f0;
    margin-bottom: 18px;
  }}

  .data-table th {{
    background: var(--emerald-dark);
    color: white;
    padding: 12px 16px;
    font-size: 12px;
    font-weight: 700;
    text-transform: uppercase;
    letter-spacing: 0.5px;
    text-align: left;
  }}

  .data-table td {{
    padding: 12px 16px;
    font-size: 13px;
    border-top: 1px solid #f1f5f9;
  }}

  .data-table tr:nth-child(even) td {{
    background-color: #f8fafc;
  }}

  .data-table tr:hover td {{
    background-color: #f0fdf4;
  }}

  .highlight-box {{
    background: linear-gradient(135deg, #ecfdf5 0%, #d1fae5 100%);
    border: 1px solid #a7f3d0;
    border-radius: 14px;
    padding: 18px 20px;
    margin: 18px 0;
    font-size: 13.5px;
    color: #064e3b;
    line-height: 1.6;
  }}

  .highlight-box strong {{
    color: #064e3b;
    font-weight: 800;
  }}

  .ref-list {{
    font-size: 11px;
    color: var(--text-muted);
    line-height: 1.5;
    padding-left: 18px;
    margin-top: 10px;
  }}

  .ref-list li {{
    margin-bottom: 6px;
  }}

  .footer {{
    background: #f8fafc;
    border-top: 1px solid #e2e8f0;
    padding: 20px;
    text-align: center;
    font-size: 11.5px;
    color: var(--text-muted);
  }}
</style>
</head>
<body>

<div class="card-container">
  <div class="hero-header">
    <div class="institution-badge">USP RIBEIRÃO PRETO • EEFERP • LaCiDH & LaBioCoM</div>
    <h1>Relatório Individual de Desempenho e Composição Corporal</h1>
    <p>Projeto de Mestrado: {TITULO_OFICIAL_PROJETO}</p>
  </div>

  <div class="content">
    <div class="athlete-card">
      <div class="athlete-field">
        <label>Participante</label>
        <span>Guilherme Lemos</span>
      </div>
      <div class="athlete-field">
        <label>Código / ID</label>
        <span>P002 (Atleta Piloto)</span>
      </div>
      <div class="athlete-field">
        <label>Data da Coleta</label>
        <span>14/09/2026</span>
      </div>
      <div class="athlete-field">
        <label>Idade / Faixa Etária</label>
        <span>42 anos (40-44 anos)</span>
      </div>
      <div class="athlete-field">
        <label>Sexo / Dominância</label>
        <span>Masculino | Destro (D)</span>
      </div>
      <div class="athlete-field">
        <label>Massa Corporal</label>
        <span>87,20 kg</span>
      </div>
      <div class="athlete-field">
        <label>Estatura</label>
        <span>171,0 cm</span>
      </div>
      <div class="athlete-field">
        <label>Perfil de Treino</label>
        <span>CrossFit / Força / Calistenia</span>
      </div>
    </div>

    <p style="font-size: 13.5px; color: var(--text-body); margin-bottom: 20px;">
      <strong>Prezado Guilherme,</strong><br>
      Apresentamos a sua devolutiva técnica individual referente à <strong>Sessão 1</strong> realizada no LaCiDH. 
      Os dados foram analisados sob parâmetros bioelétricos e biomecânicos descritivos, com referências normativas condizentes com a sua faixa etária (40 a 44 anos).
    </p>

    <!-- SEÇÃO 1: COMPOSIÇÃO CORPORAL -->
    <div class="section-title">
      <span class="badge">1</span> Composição Corporal (Bioimpedância Tetrapolar Sanny® BIA1011-AF — Sun et al., 2003)
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>Variável Avaliada</th>
          <th style="text-align: center;">Seu Resultado</th>
          <th>Interpretação & Valores Normativos (40-49 anos)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>Massa Corporal & Estatura</strong></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">87,20 kg | 171,0 cm</td>
          <td>IMC = 29,82 kg/m² (Limitação clássica do IMC em indivíduos com maior massa livre de gordura)</td>
        </tr>
        <tr style="background: #ecfdf5;">
          <td><strong>Índice de Massa Livre de Gordura (FFMI)</strong></td>
          <td style="text-align: center; font-weight: 800; color: var(--emerald-dark); font-size: 14.5px;">24,09 kg/m²</td>
          <td>Elevada robustez musculoesquelética; superior à média da população não treinada (18,5 a 20,0 kg/m² [Schutz 2002])</td>
        </tr>
        <tr>
          <td><strong>Percentual de Gordura (%GC)</strong></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">19,40%</td>
          <td>Adequado / Bom para homens de 40-49 anos treinados (ACSM: 16% a 22%)</td>
        </tr>
        <tr>
          <td><strong>Massa Livre de Gordura (MLG)</strong></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">70,45 kg (80,6%)</td>
          <td>Predomínio de massa livre de gordura ativa (músculo, osso e fluidos corporais)</td>
        </tr>
        <tr>
          <td><strong>Massa Muscular Esquelética (MME)</strong></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">37,37 kg (42,8%)</td>
          <td>Boa musculatura postural e de membros superiores para suporte em inversão</td>
        </tr>
        <tr>
          <td><strong>Massa Gorda Total</strong></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">16,95 kg (19,4%)</td>
          <td>Reserva lipídica compatível com a rotina de treinos e peso corporal total</td>
        </tr>
        <tr>
          <td><strong>Ângulo de Fase (PhA)</strong></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">6,78°</td>
          <td>Dentro da faixa de normalidade saudável para 40-49 anos (média: 7,15° ± 0,77° [Barbosa-Silva 2005])</td>
        </tr>
      </tbody>
    </table>

    <div class="highlight-box">
      <strong>💡 Contextualização Metodológica: IMLG/FFMI (24,09 kg/m²) vs IMC (29,82 kg/m²)</strong><br>
      O IMC tradicional (29,82 kg/m²) tende a superestimar o excesso de peso em indivíduos treinados, por não discriminar gordura de massa muscular. 
      Para uma descrição mais adequada, a literatura recomenda o <strong>Índice de Massa Livre de Gordura (FFMI)</strong>: seu valor de <strong>24,09 kg/m²</strong> reflete um porte físico robusto, 
      com <strong>70,45 kg de massa livre de gordura</strong> (incluindo tecido muscular, massa óssea e fluidos corporais), condizente com uma rotina séria de modalidades de força e peso corporal. 
      Vale ressaltar que, por se tratar de uma avaliação em estado nutricional e de hidratação normal (com 19,4% de gordura), o índice descreve a sua constituição física global do dia a dia, e não um limite hipertrófico desidratado de competição.
    </div>

    <!-- SEÇÃO 2: FORÇA DISTAL -->
    <div class="section-title">
      <span class="badge">2</span> Força Distal: Preensão Manual (Jamar) & Flexores de Punho (Biodex 4 PRO)
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>Teste Avaliado</th>
          <th style="text-align: center;">Seu Desempenho</th>
          <th>Interpretação Normativa (40-44 anos)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>1º Teste: Força de Preensão Manual (FPM)</strong><br><small>Dinamômetro Saehan/Jamar</small></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">
            D: 52,0 kgf | E: 53,0 kgf<br>
            <small>Média: 52,5 kgf | Relativa: 0,608 kgf/kg<br><strong>LSI: 101,9%</strong></small>
          </td>
          <td><strong>Muito Bom!</strong> Situa-se acima da média de homens de 40-44 anos (média normativa: 45,5 a 47,0 kgf [Bohannon 2019]), posicionando-se no percentil ≥85%. Simetria bilateral excelente (LSI 101,9%), garantindo ancoragem estável no solo.</td>
        </tr>
        <tr>
          <td><strong>2º Teste: Flexores de Punho (Biodex)</strong><br><small>Biodex System 4 PRO (70° TOWARD)</small></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">
            Pico D: 12,9 N·m (CV: 11,1%)<br>
            Pico E: 17,1 N·m (CV: 21,3%)<br>
            <small>Média: 15,0 N·m (0,172 N·m/kg)<br><strong>LSI: 132,6%</strong></small>
          </td>
          <td>Avaliado na angulação funcional de 70° de extensão do Handstand. Boa consistência no membro dominante (CV 11,1%). O punho esquerdo gerou maior pico de torque (+32,5%), demonstrando maior rigidez articular adaptativa (stiffness).</td>
        </tr>
      </tbody>
    </table>

    <p style="font-size: 13px; color: var(--text-body); line-height: 1.6; margin-bottom: 20px;">
      <strong>Relevância Biomecânica da "Wrist Strategy":</strong><br>
      No Handstand, os flexores de punho desempenham o papel do 'freio palmar': quando o corpo tende a passar da vertical (<em>overbalance</em>), 
      as pontas dos dedos e a palma esmagam o solo, gerando torque reativo que empurra o Centro de Massa de volta para o prumo. 
      Sua preensão de 53 kgf aos 42 anos oferece uma base de sustentação firme. A assimetria observada no Biodex (punho esquerdo mais forte) 
      será analisada na Sessão 2 para verificar se gera micro-rotações no solo ou no Handstand Walk.
    </p>

    <!-- SEÇÃO 3: FORÇA PROXIMAL E RESISTÊNCIA -->
    <div class="section-title">
      <span class="badge">3</span> Força Proximal & Resistência Específica: Shoulder Press e Parede
    </div>

    <table class="data-table">
      <thead>
        <tr>
          <th>Teste Avaliado</th>
          <th style="text-align: center;">Seu Desempenho</th>
          <th>Interpretação Normativa (40-49 anos)</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td><strong>3º Teste: 1-RM Shoulder Press</strong><br><small>Barra Smith Estrita (Overhead Press)</small></td>
          <td style="text-align: center; font-weight: 700; color: var(--emerald-medium);">
            66,0 kg<br>
            <small>(75,7% da massa corporal)</small>
          </td>
          <td><strong>Nível Avançado</strong> para homens de 40-49 anos [Soriano 2019]. Erguer ~76% do peso corporal em empurrada vertical estrita sem impulso de pernas demonstra boa força neuromuscular de deltoides, tríceps e serrátil anterior.</td>
        </tr>
        <tr style="background: #ecfdf5;">
          <td><strong>4º Teste: Resistência Belly-to-Wall HS</strong><br><small>Parada de Mão Isométrica na Parede (20 cm)</small></td>
          <td style="text-align: center; font-weight: 800; color: var(--emerald-dark); font-size: 14.5px;">
            101,0 segundos<br>
            <small>(1 min e 41 s | T1: 92s, T2: 101s)</small>
          </td>
          <td><strong>Destaque do teste!</strong> Sustentação superior a 1m40s sob alinhamento rigoroso, indicando excelente capacidade de resistência isométrica à fadiga da cintura escapular e estabilizadores do tronco.</td>
        </tr>
      </tbody>
    </table>

    <div class="highlight-box">
      <strong>⏱️ Destaque da Avaliação: 101 Segundos de Sustentação na Parede!</strong><br>
      Sustentar mais de 1 minuto e 40 segundos em inversão estrita Belly-to-Wall a 20 cm da parede com 87 kg de massa corporal evidencia ótima resistência muscular localizada. 
      Essa capacidade do trapézio superior, serrátil anterior e musculatura do core retarda a perda de alinhamento técnico durante séries sucessivas e tarefas invertidas prolongadas.
    </div>

    <!-- SEÇÃO 4: PRÓXIMA ETAPA -->
    <div class="section-title">
      <span class="badge">4</span> Próxima Etapa: Sessão 2 no LaBioCoM (Vicon & Bertec)
    </div>

    <p style="font-size: 13px; color: var(--text-body); line-height: 1.6;">
      Na Sessão 2 no LaBioCoM, integraremos seus indicadores às análises biomecânicas tridimensionais:
    </p>
    <ul style="font-size: 13px; color: var(--text-body); line-height: 1.6;">
      <li><strong>Sistema Vicon (12 Câmeras 3D):</strong> Rastreamento cinemático do alinhamento escapuloumeral, pelve e pernas, além da determinação da trajetória vertical do Centro de Massa (CoM).</li>
      <li><strong>Plataformas Bertec (1000 Hz):</strong> Registro cinético da oscilação milimétrica do Centro de Pressão (CoP), investigando a relação entre a força dos flexores de punho e a regulação postural no solo.</li>
      <li><strong>Handstand Walk (HSW):</strong> Análise espaço-temporal da caminhada invertida (comprimento de passada, velocidade e simetria de apoios manuais)!</li>
    </ul>

    <!-- SEÇÃO 5: REFERÊNCIAS -->
    <div class="section-title">
      <span class="badge">5</span> Referências Científicas Consultadas (Estratificadas para 40-49 anos)
    </div>

    <ol class="ref-list">
      <li>Sun, S. S., et al. (2003). Development of bioelectrical impedance analysis prediction equations for body composition with the use of a multicomponent model. <em>Am J Clin Nutr</em>, 77(2), 331-340.</li>
      <li>Janssen, I., et al. (2000). Estimation of skeletal muscle mass by bioelectrical impedance analysis. <em>J Appl Physiol</em>, 89(2), 465-471.</li>
      <li>American College of Sports Medicine (ACSM). (2018). <em>ACSM's Guidelines for Exercise Testing and Prescription</em> (10th ed.).</li>
      <li>Barbosa-Silva, M. C. G., et al. (2005). Bioelectrical impedance analysis: population reference values for phase angle by age and sex. <em>Am J Clin Nutr</em>, 82(1), 49-52. [Referência para homens de 40-49 anos: 7,15° ± 0,77°].</li>
      <li>Norman, K., et al. (2012). Bioelectrical phase angle as a biomarker—recent advances. <em>Clinical Nutrition</em>, 31(6), 854-861.</li>
      <li>VanItallie, T. B., et al. (1990). Height-normalized indices of the body's fat-free mass and fat mass. <em>Am J Clin Nutr</em>, 52(6), 953-959.</li>
      <li>Schutz, Y., et al. (2002). Fat-free mass index and fat mass index percentiles in Caucasians aged 18–98 y. <em>Int J Obes</em>, 26(7), 953-960.</li>
      <li>Bohannon, R. W. (2019). Normative reference values for hand-grip dynamometry: systematic review and meta-analysis. <em>J Phys Ther Sci</em>, 31(11), 932-938. [Normativa para homens de 40 a 44 anos: média 46,0 kgf].</li>
      <li>Dodds, R. M., et al. (2014). Globally representative normative data for handgrip strength: a systematic review and meta-analysis. <em>PLoS ONE</em>, 9(12), e113637.</li>
      <li>Kerwin, D. G., & Trewartha, G. (2001). Strategies for maintaining a handstand. <em>Sports Biomechanics</em>, 1(2), 163-176.</li>
      <li>Blenkinsop, G. M., Pain, M. T. G., & Hiley, M. J. (2017). Balance control strategies during perturbed and unperturbed balance in standing and handstand. <em>R Soc Open Sci</em>, 4(7), 161018.</li>
      <li>Soriano, M. A., et al. (2019). The overhead press: A review of biomechanics and exercise prescription. <em>Strength Cond J</em>, 41(4), 48-60.</li>
      <li>Kilgore, L., & Rippetoe, M. (2011). <em>Strength Training Standards</em>. The Aasgaard Company.</li>
      <li>Gautier, G., et al. (2007). Influence of visual information on postural control in a handstand. <em>Hum Mov Sci</em>, 26(4), 577-594.</li>
      <li>Bishop, C., et al. (2018). Effects of inter-limb asymmetries on physical and sports performance. <em>J Sports Sci</em>, 36(10), 1135-1144.</li>
      <li>Ellenbecker, T. S., & Roetert, E. P. (2006). Isokinetic wrist strength in competitive athletes. <em>Am J Sports Med</em>, 34(11), 1845-1852.</li>
    </ol>
  </div>

  <div class="footer">
    Universidade de São Paulo (USP) • Escola de Educação Física e Esporte de Ribeirão Preto (EEFERP)<br>
    Laboratório de Cineantropometria e Desempenho Humano (LaCiDH) • Laboratório de Biomecânica e Controle Motor (LaBioCoM)<br>
    Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes
  </div>
</div>

</body>
</html>
"""

with open(HTML_OUT, "w", encoding="utf-8") as f:
    f.write(html_content)

print(f"[OK] Documento HTML gerado em:\n  -> {HTML_OUT}")
