"""
SCRIPT DE PROCESSAMENTO E CONSOLIDAÇÃO - SESSÃO 1 (LaCiDH)
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes

Fontes de Dados Integradas:
1. PLANILHA_COLETA_CAMPO_LACIDH.xlsx (Antropometria, FPM, 1-RM SP com Estágio Final, Wall-HS)
2. Laudos de Bioimpedância Tetrapolar Sanny BIA1011-AF em PDF (Resistência, Reatância, Ângulo de Fase, %Gordura, Massa Magra)
3. Laudos e Séries Temporais do Dinamômetro Isocinético Biodex PRO a 70° (filtragem inteligente de duplicatas e relatórios redundantes)

Gera:
- variaveis_forca_processadas_lacidh.csv (Pasta resultados do LaCiDH)
- TABELA_OFICIAL_VARIAVEIS_LACIDH.xlsx (Formatada visualmente com dados consolidados de P001)
"""

import os
import sys
import csv
import glob
import re
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

try:
    import pypdf
except ImportError:
    pypdf = None


def extrair_dados_sanny_bia(caminho_pdf):
    """Extrai parâmetros de bioimpedância elétrica a partir do relatório em PDF da Sanny."""
    if not pypdf or not os.path.exists(caminho_pdf):
        return {}

    try:
        reader = pypdf.PdfReader(caminho_pdf)
        texto_total = ""
        for p in reader.pages:
            texto_total += p.extract_text() + "\n"

        dados = {}

        all_ohms = re.findall(r"([\d\.,]+)\s*ohms", texto_total, re.IGNORECASE)
        if len(all_ohms) >= 3:
            dados["Resistencia_BIA_ohms"] = float(all_ohms[0].replace(",", "."))
            dados["Reatancia_BIA_ohms"] = float(all_ohms[1].replace(",", "."))
            dados["Impedancia_BIA_ohms"] = float(all_ohms[2].replace(",", "."))

        m_af = re.search(r"(\d+\.\d+)\s*[\u00b0\u00ba\uFFFD\?]", texto_total)
        if m_af:
            dados["Angulo_Fase_deg"] = float(m_af.group(1))
        else:
            m_af2 = re.search(r"(\d+\.\d+)\s*\n\s*6\.02", texto_total)
            if m_af2:
                dados["Angulo_Fase_deg"] = float(m_af2.group(1))

        lines = [l.strip() for l in texto_total.split("\n") if l.strip()]
        kg_vals = []
        pct_vals = []
        for l in lines:
            if l.endswith("kg") and "-" not in l:
                try:
                    kg_vals.append(float(l.replace("kg", "").strip().replace(",", ".")))
                except ValueError:
                    pass
            elif l.endswith("%") and "-" not in l:
                try:
                    pct_vals.append(float(l.replace("%", "").strip().replace(",", ".")))
                except ValueError:
                    pass

        if len(kg_vals) >= 5:
            dados["BIA_Massa_Corporal_kg"] = kg_vals[0]
            dados["Agua_Corporal_Total_kg"] = kg_vals[1]
            dados["Massa_Livre_Gordura_kg"] = kg_vals[2]
            dados["Massa_Gorda_kg"] = kg_vals[3]
            dados["Massa_Muscular_Esqueletica_kg"] = kg_vals[4]

        if len(pct_vals) >= 4:
            dados["Agua_Corporal_pct"] = pct_vals[0]
            dados["Massa_Livre_Gordura_pct"] = pct_vals[1]
            dados["Percentual_Gordura_pct"] = pct_vals[2]
            dados["Massa_Muscular_Esqueletica_pct"] = pct_vals[3]

        all_kcal = re.findall(r"([\d\.,]+)\s*kcal", texto_total)
        if len(all_kcal) >= 2:
            dados["Gasto_Energetico_Total_kcal"] = float(all_kcal[0].replace(",", "."))
            dados["Taxa_Metabolica_Basal_kcal"] = float(all_kcal[1].replace(",", "."))

        # Nível de atividade física Sanny
        for level in ["Muito Ativo", "Pouco Ativo", "Atleta", "Ativo", "Sedentário", "Sedentario"]:
            if re.search(r"\b" + level + r"\b", texto_total, re.IGNORECASE):
                dados["BIA_Nivel_Atividade"] = "Sedentário" if "sedent" in level.lower() else level
                break

        return dados
    except Exception as e:
        print(f"[AVISO] Erro ao extrair PDF BIA ({caminho_pdf}): {e}")
        return {}


def extrair_dados_biodex_pasta(pasta_participante):
    """
    Varre a pasta do participante procurando relatórios em PDF e TXT do Biodex PRO.
    Identifica automaticamente o lado testado (RIGHT vs LEFT) pelo texto interno,
    eliminando relatórios duplicados e redundantes (prioriza Comprehensive Evaluation e nomes limpos),
    e extrai:
    - Pico de torque (N·m) em flexão (TOWARD) a 70°
    - Média do pico de torque das repetições (N·m)
    - Coeficiente de Variação (%)
    - Séries temporais em TXT das curvas contínuas (100 Hz)
    """
    if not pypdf or not os.path.exists(pasta_participante):
        return {}

    arquivos_pdf = glob.glob(os.path.join(pasta_participante, "**", "*.pdf"), recursive=True)
    arquivos_pdf += glob.glob(os.path.join(pasta_participante, "*.pdf"))
    arquivos_pdf = list(set(arquivos_pdf))

    testes_por_lado = {"RIGHT": [], "LEFT": []}

    for pdf_path in arquivos_pdf:
        fname = os.path.basename(pdf_path)
        if "curve" in fname.lower() or "sanny" in fname.lower():
            continue
        try:
            reader = pypdf.PdfReader(pdf_path)
            if not reader.pages:
                continue
            text = reader.pages[0].extract_text() or ""
            if "PEAK TORQUE" not in text or "Wrist" not in text:
                continue

            side_match = re.search(r"Side:\s*(RIGHT|LEFT)", text, re.IGNORECASE)
            if not side_match:
                continue
            side = side_match.group(1).upper()

            session_match = re.search(r"Session:\s*([^\n]+)", text)
            session_time = session_match.group(1).strip() if session_match else ""

            tipo_score = 2 if "Comprehensive" in text else 1
            # Bônus de nome: favorece arquivos que batem com o lado sem sufixos trocados
            fname_lower = fname.lower()
            if side == "RIGHT" and not re.search(r"[_]l\d*[_]", fname_lower) and not fname_lower.startswith("p001_l"):
                tipo_score += 1
            elif side == "LEFT" and (re.search(r"[_]l\d*[_]", fname_lower) or fname_lower.startswith("p001_l") or "esq" in fname_lower):
                tipo_score += 1

            lines = [l.strip() for l in text.split("\n") if l.strip()]
            num_pairs = []
            after_table = False
            for l in lines:
                if "AGON/ANTAG" in l:
                    after_table = True
                    continue
                if after_table:
                    if "Comments:" in l:
                        break
                    parts = l.split()
                    if len(parts) >= 2:
                        try:
                            v1 = float(parts[0].replace(",", "."))
                            v2 = float(parts[1].replace(",", "."))
                            num_pairs.append((v1, v2))
                        except ValueError:
                            pass

            peak_torque = 0.0
            avg_peak_tq = 0.0
            cv_pct = 0.0

            if len(num_pairs) >= 1:
                peak_torque = max(num_pairs[0])
            if len(num_pairs) >= 2:
                avg_peak_tq = max(num_pairs[1])

            for idx, (v1, v2) in enumerate(num_pairs):
                if v1 == 60.0 or v2 == 60.0:
                    if idx + 2 < len(num_pairs):
                        cv_pct = max(num_pairs[idx + 2])
                    break

            testes_por_lado[side].append({
                "arquivo": fname,
                "caminho": pdf_path,
                "score": tipo_score,
                "session": session_time,
                "peak_torque": peak_torque,
                "avg_peak_tq": avg_peak_tq,
                "cv_pct": cv_pct
            })
        except Exception as e:
            pass

    arquivos_txt = glob.glob(os.path.join(pasta_participante, "**", "*.txt"), recursive=True)
    arquivos_txt += glob.glob(os.path.join(pasta_participante, "*.txt"))
    arquivos_txt = list(set(arquivos_txt))
    curvas_txt = {}
    for txt_path in arquivos_txt:
        fname = os.path.basename(txt_path)
        if "curve" in fname.lower():
            if "_l_" in fname.lower() or "esq" in fname.lower() or fname.lower().startswith("p001_l"):
                curvas_txt["LEFT"] = fname
            else:
                curvas_txt["RIGHT"] = fname

    resultado = {}
    for side in ["RIGHT", "LEFT"]:
        lista = testes_por_lado[side]
        if lista:
            lista_ordenada = sorted(lista, key=lambda x: (x["score"], x["peak_torque"]), reverse=True)
            melhor = lista_ordenada[0]
            melhor["curva_txt"] = curvas_txt.get(side, "")
            melhor["total_arquivos_lado"] = len(lista)
            melhor["arquivos_duplicados_descartados"] = [x["arquivo"] for x in lista_ordenada[1:]]
            resultado[side] = melhor

    return resultado


def processar_todas_forcas_lacidh():
    base_dir = r"C:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL\01_SESSAO_LACIDH_FORCA"
    pasta_brutos = os.path.join(base_dir, "dados_brutos")
    pasta_saida = os.path.join(base_dir, "resultados")
    os.makedirs(pasta_saida, exist_ok=True)

    caminho_csv = os.path.join(pasta_saida, "variaveis_forca_processadas_lacidh.csv")
    caminho_xlsx = os.path.join(pasta_saida, "TABELA_OFICIAL_VARIAVEIS_LACIDH.xlsx")

    print("=" * 80)
    print("PROCESSADOR UNIVERSAL DE FORÇA E COMPOSIÇÃO CORPORAL - LaCiDH")
    print(f"Pasta de entrada: {pasta_brutos}")
    print(f"Pasta de saída:   {pasta_saida}")
    print("=" * 80)

    participantes = {}

    planilha_xlsx = os.path.join(pasta_brutos, "PLANILHA_COLETA_CAMPO_LACIDH.xlsx")
    if not os.path.exists(planilha_xlsx):
        planilha_xlsx = os.path.join(base_dir, "PLANILHA_COLETA_CAMPO_LACIDH.xlsx")
    if os.path.exists(planilha_xlsx):
        print(f"[1/4] Lendo Planilha de Campo: {planilha_xlsx}")
        wb = openpyxl.load_workbook(planilha_xlsx, data_only=True)
        ws = wb.active

        headers = [str(cell.value or "").strip() for cell in ws[1]]
        header_map = {h: i for i, h in enumerate(headers) if h}

        for row in ws.iter_rows(min_row=3, values_only=True):
            if not row or not any(row):
                continue
            part_id = str(row[header_map.get("ID_Participante", 0)] or "").strip().upper()
            if not part_id or not (part_id.startswith("P") or part_id.startswith("VOL")):
                continue

            def get_val(col_name, default=0.0):
                idx = header_map.get(col_name)
                if idx is not None and idx < len(row):
                    v = row[idx]
                    if v is not None and str(v).strip() != "":
                        try:
                            return float(v)
                        except ValueError:
                            return v
                return default

            massa = get_val("Massa_Corporal_kg", 0.0)
            estatura = get_val("Estatura_cm", 0.0)

            if massa == 0 and estatura == 0:
                continue

            imc = round(massa / ((estatura / 100.0) ** 2), 2) if estatura > 0 and massa > 0 else 0.0

            # FPM
            fpm_d = [get_val(f"FPM_Dom_T{i}_kgf", 0.0) for i in [1, 2, 3]]
            fpm_nd = [get_val(f"FPM_NaoDom_T{i}_kgf", 0.0) for i in [1, 2, 3]]
            fpm_d_max = max(fpm_d) if fpm_d else 0.0
            fpm_nd_max = max(fpm_nd) if fpm_nd else 0.0
            fpm_max_global = max(fpm_d_max, fpm_nd_max)
            fpm_media_bilateral = round((fpm_d_max + fpm_nd_max) / 2.0, 2) if (fpm_d_max > 0 or fpm_nd_max > 0) else 0.0
            fpm_rel_media = round(fpm_media_bilateral / massa, 4) if massa > 0 else 0.0
            fpm_rel_max = round(fpm_max_global / massa, 4) if massa > 0 else 0.0
            lsi_fpm = round((fpm_nd_max / fpm_d_max) * 100, 2) if fpm_d_max > 0 else 0.0

            # 1-RM Shoulder Press
            sp_1rm = get_val("Estagio_Final_kg", 0.0)
            if not sp_1rm:
                sp_1rm = get_val("Estágio_Final_kg", 0.0)
            if not sp_1rm:
                sp_1rm = get_val("Carga_1RM_Validada_kg", 0.0)

            sp_rel = round(sp_1rm / massa, 4) if massa > 0 and sp_1rm > 0 else 0.0

            # Wall-HS
            res_t1 = get_val("Resistencia_WallHS_T1_s", 0.0)
            res_t2 = get_val("Resistencia_WallHS_T2_s", 0.0)
            res_max = max(res_t1, res_t2)

            data_col = str(row[header_map.get("Data_Coleta", 2)] or "")
            if "TODAY" in data_col.upper() or "HOJE" in data_col.upper() or not data_col:
                data_col = "02/09/2026"

            participantes[part_id] = {
                "ID_Participante": part_id,
                "Nome_Abreviado": str(row[header_map.get("Nome_Abreviado", 1)] or ""),
                "Data_Coleta_Lacidh": data_col,
                "Sexo": str(row[header_map.get("Sexo", 3)] or "").strip().upper(),
                "Idade_anos": int(get_val("Idade_anos", 0)),
                "Massa_Corporal_kg": round(massa, 2),
                "Estatura_cm": round(estatura, 1),
                "IMC_kg_m2": imc,
                "IMLG_FFMI_kg_m2": "",
                "BIA_Nivel_Atividade": str(row[header_map.get("BIA_Nivel_Atividade", 0)] or "").strip() if "BIA_Nivel_Atividade" in header_map else "",
                "Membro_Dominante": str(row[header_map.get("Membro_Dominante", 8)] or "D").strip().upper(),
                # FPM
                "FPM_Dom_T1_kgf": fpm_d[0],
                "FPM_Dom_T2_kgf": fpm_d[1],
                "FPM_Dom_T3_kgf": fpm_d[2],
                "FPM_Dominante_Max_kgf": round(fpm_d_max, 2),
                "FPM_Dom_Max_kgf": round(fpm_d_max, 2),
                "FPM_NaoDom_T1_kgf": fpm_nd[0],
                "FPM_NaoDom_T2_kgf": fpm_nd[1],
                "FPM_NaoDom_T3_kgf": fpm_nd[2],
                "FPM_NaoDominante_Max_kgf": round(fpm_nd_max, 2),
                "FPM_NaoDom_Max_kgf": round(fpm_nd_max, 2),
                "FPM_Max_Global_kgf": round(fpm_max_global, 2),
                "FPM_Media_Bilateral_kgf": fpm_media_bilateral,
                "FPM_Relativa_kgf_kg": fpm_rel_media,
                "FPM_Relativa_Max_kgf_kg": fpm_rel_max,
                "LSI_FPM_pct": lsi_fpm,
                # 1-RM SP
                "SP_Estagio_1_kg": get_val("Estagio_1_kg", 0.0),
                "SP_Estagio_2_kg": get_val("Estagio_2_kg", 0.0),
                "SP_Estagio_3_kg": get_val("Estagio_3_kg", 0.0),
                "SP_Estagio_4_kg": get_val("Estagio_4_kg", 0.0),
                "SP_Estagio_5_kg": get_val("Estagio_5_kg", 0.0),
                "SP_Estagio_6_kg": get_val("Estagio_6_kg", 0.0),
                "1RM_ShoulderPress_Absoluta_kg": round(sp_1rm, 2),
                "SP_1RM_Estagio_Final_kg": round(sp_1rm, 2),
                "1RM_ShoulderPress_Relativa_kg_kg": sp_rel,
                # Resistência Wall-HS
                "Resistencia_WallHS_T1_s": round(res_t1, 2),
                "Resistencia_WallHS_T2_s": round(res_t2, 2),
                "Resistencia_WallHS_Max_s": round(res_max, 2),
                # Biodex Punho Inicializador (Padronizado para Master SPSS e Local)
                "FFP_Biodex_Dominante_Max_Nm": "",
                "FFP_Biodex_Dom_Max_Nm": "",
                "FFP_Biodex_NaoDominante_Max_Nm": "",
                "FFP_Biodex_NaoDom_Max_Nm": "",
                "FFP_Biodex_Max_Global_Nm": "",
                "FFP_Biodex_Media_Bilateral_Nm": "",
                "FFP_Biodex_Relativo_Nm_kg": "",
                "FFP_Biodex_Relativo_Media_Nm_kg": "",
                "FFP_Biodex_Relativo_Max_Nm_kg": "",
                "LSI_FFP_pct": "",
                "FFP_Biodex_CV_Dom_pct": "",
                "FFP_Biodex_CV_NaoDom_pct": "",
                "Relatorio_Biodex_D_PDF": "",
                "Relatorio_Biodex_E_PDF": "",
                "Curva_Biodex_D_TXT": "",
                "Curva_Biodex_E_TXT": "",
                "Status_Biodex": "Pendente",
                # Metadados
                "Relatorio_BIA_PDF": str(row[header_map.get("Relatorio_BIA_PDF", 30)] or f"{part_id}_sanny.pdf"),
                "Observacoes": str(row[header_map.get("Observacoes_Sessao", 32)] or "")
            }

    # 2. Procurar laudos de Bioimpedância Tetrapolar (Sanny) em dados_brutos
    print("[2/4] Integrando Laudos de Bioimpedância Tetrapolar (Sanny BIA1011-AF)...")
    for pid in participantes:
        padroes = [
            os.path.join(pasta_brutos, pid, f"{pid}_sanny.pdf"),
            os.path.join(pasta_brutos, pid, f"{pid}_SANNY"),
            os.path.join(pasta_brutos, pid, "*.pdf"),
            os.path.join(pasta_brutos, f"{pid}_sanny.pdf")
        ]
        bia_encontrado = None
        for p in padroes:
            arquivos = glob.glob(p)
            for f in arquivos:
                if "sanny" in f.lower():
                    bia_encontrado = f
                    break
            if bia_encontrado:
                break

        if bia_encontrado:
            print(f"  -> Encontrado laudo BIA para {pid}: {os.path.basename(bia_encontrado)}")
            dados_bia = extrair_dados_sanny_bia(bia_encontrado)
            if dados_bia:
                if not participantes[pid].get("BIA_Nivel_Atividade"):
                    participantes[pid]["BIA_Nivel_Atividade"] = dados_bia.get("BIA_Nivel_Atividade", "")
                participantes[pid].update(dados_bia)
                mlg = dados_bia.get("Massa_Livre_Gordura_kg", 0.0)
                est = participantes[pid].get("Estatura_cm", 0.0)
                if mlg > 0 and est > 0:
                    participantes[pid]["IMLG_FFMI_kg_m2"] = round(mlg / ((est / 100.0) ** 2), 2)
                print(f"     [OK] BIA extraída: Nível={participantes[pid].get('BIA_Nivel_Atividade')}, AF={dados_bia.get('Angulo_Fase_deg')}°, %Gord={dados_bia.get('Percentual_Gordura_pct')}%, MM={dados_bia.get('Massa_Livre_Gordura_kg')} kg, IMLG={participantes[pid].get('IMLG_FFMI_kg_m2')} kg/m², R={dados_bia.get('Resistencia_BIA_ohms')} Ω")
        else:
            print(f"  -> [AVISO] Laudo BIA não encontrado para {pid}")

    # 3. Procurar e integrar laudos do Dinamômetro Isocinético Biodex PRO
    print("[3/4] Integrando Laudos e Séries Isocinéticas do Biodex PRO (Flexores de Punho a 70°)...")
    for pid in participantes:
        pasta_p = os.path.join(pasta_brutos, pid)
        dados_bio = extrair_dados_biodex_pasta(pasta_p)
        if dados_bio:
            dom = participantes[pid].get("Membro_Dominante", "D")
            d_side = dados_bio.get("RIGHT")
            e_side = dados_bio.get("LEFT")

            pt_d = d_side["peak_torque"] if d_side else 0.0
            pt_e = e_side["peak_torque"] if e_side else 0.0
            cv_d = d_side["cv_pct"] if d_side else 0.0
            cv_e = e_side["cv_pct"] if e_side else 0.0

            if dom == "D":
                dom_peak = pt_d
                naodom_peak = pt_e
                dom_cv = cv_d
                naodom_cv = cv_e
            else:
                dom_peak = pt_e
                naodom_peak = pt_d
                dom_cv = cv_e
                naodom_cv = cv_d

            max_global = max(pt_d, pt_e)
            media_bilat = round((pt_d + pt_e) / 2.0, 2) if (pt_d > 0 and pt_e > 0) else max_global
            massa = participantes[pid].get("Massa_Corporal_kg", 0.0)
            rel_media = round(media_bilat / massa, 4) if massa > 0 else 0.0
            rel_max = round(max_global / massa, 4) if massa > 0 else 0.0
            lsi = round((naodom_peak / dom_peak) * 100, 2) if dom_peak > 0 else 0.0

            # Atualizar chaves padronizadas (ambos os formatos suportados)
            participantes[pid]["FFP_Biodex_Dominante_Max_Nm"] = dom_peak
            participantes[pid]["FFP_Biodex_Dom_Max_Nm"] = dom_peak
            participantes[pid]["FFP_Biodex_NaoDominante_Max_Nm"] = naodom_peak
            participantes[pid]["FFP_Biodex_NaoDom_Max_Nm"] = naodom_peak
            participantes[pid]["FFP_Biodex_Max_Global_Nm"] = max_global
            participantes[pid]["FFP_Biodex_Media_Bilateral_Nm"] = media_bilat
            participantes[pid]["FFP_Biodex_Relativo_Nm_kg"] = rel_media
            participantes[pid]["FFP_Biodex_Relativo_Media_Nm_kg"] = rel_media
            participantes[pid]["FFP_Biodex_Relativo_Max_Nm_kg"] = rel_max
            participantes[pid]["LSI_FFP_pct"] = lsi
            participantes[pid]["FFP_Biodex_CV_Dom_pct"] = dom_cv
            participantes[pid]["FFP_Biodex_CV_NaoDom_pct"] = naodom_cv
            participantes[pid]["Relatorio_Biodex_D_PDF"] = d_side["arquivo"] if d_side else ""
            participantes[pid]["Relatorio_Biodex_E_PDF"] = e_side["arquivo"] if e_side else ""
            participantes[pid]["Curva_Biodex_D_TXT"] = d_side.get("curva_txt", "") if d_side else ""
            participantes[pid]["Curva_Biodex_E_TXT"] = e_side.get("curva_txt", "") if e_side else ""
            
            total_desc = sum(len(dados_bio[s].get("arquivos_duplicados_descartados", [])) for s in dados_bio)
            participantes[pid]["Status_Biodex"] = f"Processado com Sucesso (Bilateral - {total_desc} redundâncias descartadas)"

            print(f"  -> [OK] Biodex extraído para {pid}:")
            print(f"     Lado Direito: {pt_d} N·m (CV: {cv_d}%) | Arquivo: {d_side['arquivo'] if d_side else 'N/A'}")
            print(f"     Lado Esquerdo: {pt_e} N·m (CV: {cv_e}%) | Arquivo: {e_side['arquivo'] if e_side else 'N/A'}")
            print(f"     Média Bilateral: {media_bilat} N·m | LSI: {lsi}% | Relativo: {rel_media} N·m/kg")
        else:
            print(f"  -> [AVISO] Nenhum laudo Biodex encontrado para {pid}")

    # 4. Exportar CSV
    if participantes:
        fieldnames = list(next(iter(participantes.values())).keys())
        with open(caminho_csv, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=fieldnames)
            writer.writeheader()
            for pid in sorted(participantes.keys()):
                writer.writerow(participantes[pid])
        print(f"[4/4] Arquivo CSV gerado: {caminho_csv}")

        # 5. Exportar Excel Formatado (TABELA_OFICIAL_VARIAVEIS_LACIDH.xlsx)
        wb_out = openpyxl.Workbook()
        ws_out = wb_out.active
        ws_out.title = "Variaveis_LaCiDH"
        ws_out.views.sheetView[0].showGridLines = True

        fill_header = PatternFill(start_color="1F4E78", end_color="1F4E78", fill_type="solid")
        font_header = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
        font_data = Font(name="Calibri", size=11)
        align_center = Alignment(horizontal="center", vertical="center")
        align_left = Alignment(horizontal="left", vertical="center")
        align_right = Alignment(horizontal="right", vertical="center")
        border_thin = Border(
            left=Side(style="thin", color="D9D9D9"),
            right=Side(style="thin", color="D9D9D9"),
            top=Side(style="thin", color="D9D9D9"),
            bottom=Side(style="thin", color="D9D9D9")
        )

        for col_idx, col_name in enumerate(fieldnames, start=1):
            cell = ws_out.cell(row=1, column=col_idx, value=col_name)
            cell.fill = fill_header
            cell.font = font_header
            cell.alignment = align_center

        for row_idx, pid in enumerate(sorted(participantes.keys()), start=2):
            pdata = participantes[pid]
            for col_idx, col_name in enumerate(fieldnames, start=1):
                val = pdata.get(col_name, "")
                cell = ws_out.cell(row=row_idx, column=col_idx, value=val)
                cell.font = font_data
                cell.border = border_thin
                if isinstance(val, (int, float)):
                    cell.alignment = align_right
                else:
                    cell.alignment = align_center if col_name in ["ID_Participante", "Sexo", "Membro_Dominante"] else align_left

        for col in ws_out.columns:
            max_len = max(len(str(cell.value or "")) for cell in col)
            col_letter = get_column_letter(col[0].column)
            ws_out.column_dimensions[col_letter].width = max(max_len + 4, 12)

        wb_out.save(caminho_xlsx)
        print(f"[SUCESSO] Planilha Excel Oficial LaCiDH gerada em:\n  -> {caminho_xlsx}")
    else:
        print("[AVISO] Nenhum participante processado.")


if __name__ == "__main__":
    processar_todas_forcas_lacidh()
