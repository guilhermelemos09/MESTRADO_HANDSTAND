"""
SCRIPT MASTER DE CONSOLIDAÇÃO DO DATASET COMPLETO DO MESTRADO
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes

Integra:
1. Identificação e Perfil de Prática (Tabela Mestre / Formulários Oficiais)
2. Sessão 1 - LaCiDH (Força, Composição Corporal BIA, 1-RM Shoulder Press, Resistência)
3. Sessão 2 - LaBioCoM (Cinemática 3D Vicon + Cinética Bertec de HS e HSW)

Gera:
- dataset_mestrado_completo_SPSS.csv (Planilha estruturada pronta para importação no SPSS)
"""

import os
import csv
import re
import glob
import openpyxl
import numpy as np

def consolidar_dataset():
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    pasta_raiz_piloto = os.path.abspath(os.path.join(diretorio_base, "..", ".."))

    tabela_mestre_path = os.path.join(pasta_raiz_piloto, "00_CADASTRO_TRIAGEM_E_TCLE", "TABELA_MESTRE_IDENTIFICACAO_PARTICIPANTES.xlsx")
    caminho_lacidh = os.path.join(pasta_raiz_piloto, "01_SESSAO_LACIDH_FORCA", "resultados", "variaveis_forca_processadas_lacidh.csv")
    caminho_labiocom = os.path.join(pasta_raiz_piloto, "02_SESSAO_LABIOCOM_CINEMATICA", "resultados", "variaveis_labiocom_por_tentativa.csv")
    
    pasta_saida = os.path.join(diretorio_base, "..", "dataset_final")
    os.makedirs(pasta_saida, exist_ok=True)
    caminho_saida = os.path.join(pasta_saida, "dataset_mestrado_completo_SPSS.csv")

    print("=" * 80)
    print("CONSOLIDAÇÃO MASTER DO DATASET DO MESTRADO (SPSS READY)")
    print("=" * 80)

    participantes = {}

    # 1. Carregar Identificação e Perfil da Tabela Mestre Oficial
    if os.path.exists(tabela_mestre_path):
        print(f"[1/3] Lendo Perfil dos Participantes da Tabela Mestre...")
        wb = openpyxl.load_workbook(tabela_mestre_path, data_only=True)
        ws_of = wb["02_Participantes_Oficiais"]
        ws_bc = wb["01_Banco_Interessados_Forms"]

        banco_info = {}
        for r in range(2, ws_bc.max_row + 1):
            nome = str(ws_bc.cell(r, 2).value or "").strip().lower()
            if nome:
                banco_info[nome] = {
                    "Tempo_Pratica_Total_meses": ws_bc.cell(r, 10).value or "",
                    "Tempo_Treino_Especifico_HS_meses": ws_bc.cell(r, 10).value or "",
                    "Frequencia_Semanal_treinos": ws_bc.cell(r, 11).value or ""
                }

        for r in range(2, ws_of.max_row + 1):
            pid = ws_of.cell(r, 1).value
            nome = ws_of.cell(r, 2).value
            if pid and nome:
                nome_l = str(nome).strip().lower()
                id_nasc = str(ws_of.cell(r, 4).value or "")
                m_idade = re.search(r'\((\d+)\s*anos\)', id_nasc)
                idade = m_idade.group(1) if m_idade else id_nasc
                
                b = banco_info.get(nome_l, {})
                participantes[pid] = {
                    "ID_Participante": pid,
                    "Nome_Abreviado": ws_of.cell(r, 3).value or "",
                    "Idade_anos": idade,
                    "Sexo": ws_of.cell(r, 5).value or "",
                    "Modalidade_Principal": ws_of.cell(r, 6).value or "",
                    "Tempo_Pratica_Total_meses": b.get("Tempo_Pratica_Total_meses", ""),
                    "Tempo_Treino_Especifico_HS_meses": b.get("Tempo_Treino_Especifico_HS_meses", ""),
                    "Frequencia_Semanal_treinos": b.get("Frequencia_Semanal_treinos", "")
                }
    else:
        print(f"[AVISO] Tabela Mestre não encontrada em: {tabela_mestre_path}")

    # 2. Carregar Dados de Força LaCiDH
    if os.path.exists(caminho_lacidh):
        print(f"[2/3] Lendo Dados do LaCiDH: {os.path.basename(caminho_lacidh)}")
        with open(caminho_lacidh, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                pid = row.get("ID_Participante", "").strip()
                if not pid:
                    continue
                if pid not in participantes:
                    participantes[pid] = {"ID_Participante": pid}
                
                campos_lacidh = [
                    "Massa_Corporal_kg", "Estatura_cm", "IMC_kg_m2", "IMLG_FFMI_kg_m2",
                    "Percentual_Gordura_pct", "Massa_Livre_Gordura_kg", "Massa_Gorda_kg", "Angulo_Fase_deg", "Resistencia_BIA_ohms",
                    "FPM_Dominante_Max_kgf", "FPM_NaoDominante_Max_kgf", "FPM_Max_Global_kgf", "FPM_Relativa_kgf_kg", "LSI_FPM_pct",
                    "FFP_Biodex_Dominante_Max_Nm", "FFP_Biodex_NaoDominante_Max_Nm", "FFP_Biodex_Max_Global_Nm", "FFP_Biodex_Relativo_Nm_kg", "LSI_FFP_pct",
                    "1RM_ShoulderPress_Absoluta_kg", "1RM_ShoulderPress_Relativa_kg_kg", "Resistencia_WallHS_Max_s"
                ]
                for campo in campos_lacidh:
                    participantes[pid][campo] = row.get(campo, "")
    else:
        print(f"[AVISO] Dados de força LaCiDH não encontrados em: {caminho_lacidh}")

    # 3. Carregar Dados Cinemáticos/Cinéticos LaBioCoM (se houver)
    if os.path.exists(caminho_labiocom):
        print(f"[3/3] Lendo Dados do LaBioCoM: {os.path.basename(caminho_labiocom)}")
        tentativas_por_part = {}
        with open(caminho_labiocom, "r", encoding="utf-8-sig") as f:
            reader = csv.DictReader(f)
            for row in reader:
                nome_arq = row.get("Arquivo", "")
                pid = nome_arq.split("_")[0].upper() if "_" in nome_arq else "P001"
                if pid not in tentativas_por_part:
                    tentativas_por_part[pid] = []
                tentativas_por_part[pid].append(row)
        
        for pid, trials in tentativas_por_part.items():
            if pid not in participantes:
                participantes[pid] = {"ID_Participante": pid}
            
            hs_assist = [t for t in trials if "HS_ASSISTIDO" in t.get("Tipo_Tarefa", "")]
            hs_livre = [t for t in trials if "HS_LIVRE" in t.get("Tipo_Tarefa", "")]
            hsw = [t for t in trials if "HSW" in t.get("Tipo_Tarefa", "")]

            if hs_assist:
                tempos = [float(t.get("Tempo_Sustentacao_s", 0) or 0) for t in hs_assist]
                melhor_tempo = round(float(np.max(tempos)), 2) if tempos else 0.0
                idx_pico_assist = int(np.argmax(tempos)) if tempos else 0
                t_pico = hs_assist[idx_pico_assist]
                
                participantes[pid]["HS_Assist_Tempo_Sustentacao_Pico_s"] = melhor_tempo
                participantes[pid]["HS_Assist_Tempo_Sustentacao_Max_s"] = melhor_tempo
                participantes[pid]["HS_Assist_Tentativa_Pico"] = f"T{idx_pico_assist + 1}"
                participantes[pid]["HS_Assist_Distancia_CoP_CoM_Media_mm"] = float(t_pico.get("Distancia_CoP_CoM_mm", 0) or 0)
                participantes[pid]["HS_Assist_Velocidade_CoP_mm_s"] = float(t_pico.get("Velocidade_CoP_mm_s", 0) or 0)
                participantes[pid]["HS_Assist_ApEn_CoP"] = float(t_pico.get("ApEn_CoP", 0) or 0)
                participantes[pid]["HS_Assist_Indice_Verticalidade_deg"] = float(t_pico.get("Indice_Verticalidade_deg", 0) or 0)
                participantes[pid]["HS_Assist_Extensao_Cervical_deg"] = float(t_pico.get("Extensao_Cervical_deg", 0) or 0)
                participantes[pid]["HS_Assist_Flexao_Plantar_deg"] = float(t_pico.get("Flexao_Plantar_deg", 0) or 0)
                participantes[pid]["HS_Assist_Base_Apoio_mm"] = float(t_pico.get("Base_Apoio_mm", 0) or 0)
                participantes[pid]["HS_Assist_Rotacao_Maos_deg"] = float(t_pico.get("Rotacao_Maos_deg", 0) or 0)
                participantes[pid]["HS_Altura_CoM_mm"] = float(t_pico.get("Altura_CoM_mm", 0) or 0)
                participantes[pid]["HS_Comprimento_Bracos_mm"] = float(t_pico.get("Comprimento_Braco_mm", 0) or 0)

            if hs_livre:
                tempos_livre = [float(t.get("Tempo_Sustentacao_s", 0) or 0) for t in hs_livre]
                acertos = sum(1 for tempo in tempos_livre if tempo >= 3.0)
                sucesso = 1 if acertos > 0 else 0
                idx_pico_livre = int(np.argmax(tempos_livre)) + 1 if tempos_livre else ""
                participantes[pid]["HS_Livre_Sucesso_Binario"] = sucesso
                participantes[pid]["HS_Livre_Qtd_Acertos"] = acertos
                participantes[pid]["HS_Livre_Taxa_Sucesso_pct"] = round((acertos / len(tempos_livre)) * 100, 1) if tempos_livre else 0.0
                participantes[pid]["HS_Livre_Tempo_Max_s"] = round(float(np.max(tempos_livre)), 2) if tempos_livre else 0.0
                participantes[pid]["HS_Livre_Tentativa_Pico"] = f"T{idx_pico_livre}" if idx_pico_livre else ""

            if hsw:
                distancias = [float(t.get("Distancia_Percorrida_m", 0) or 0) for t in hsw]
                # Mantém a MEDIANA conforme protocolo metodológico
                participantes[pid]["HSW_Distancia_Percorrida_Mediana_m"] = round(float(np.median(distancias)), 3) if distancias else 0.0
                participantes[pid]["HSW_Distancia_Percorrida_Max_m"] = round(float(np.max(distancias)), 3) if distancias else 0.0
                
                # Dados da tentativa mais longa / representativa
                idx_max = int(np.argmax(distancias)) if distancias else 0
                t_best = hsw[idx_max]
                participantes[pid]["HSW_Variabilidade_Espacial_CV_pct"] = float(t_best.get("Variabilidade_Espacial_CV_pct", 0) or 0)
                participantes[pid]["HSW_Variabilidade_Temporal_CV_pct"] = float(t_best.get("Variabilidade_Temporal_CV_pct", 0) or 0)
                participantes[pid]["HSW_Comprimento_Passada_Medio_mm"] = float(t_best.get("Comprimento_Passada_Medio_mm", 0) or 0)
                participantes[pid]["HSW_Cadencia_passos_s"] = float(t_best.get("Cadencia_passos_s", 0) or 0)
                participantes[pid]["HSW_Indice_Verticalidade_deg"] = float(t_best.get("Indice_Verticalidade_deg", 0) or 0)
                participantes[pid]["HSW_Extensao_Cervical_deg"] = float(t_best.get("Extensao_Cervical_deg", 0) or 0)
                participantes[pid]["HSW_Flexao_Plantar_deg"] = float(t_best.get("Flexao_Plantar_deg", 0) or 0)
                participantes[pid]["HSW_Base_Apoio_mm"] = float(t_best.get("Base_Apoio_mm", 0) or 0)
                participantes[pid]["HSW_Rotacao_Maos_deg"] = float(t_best.get("Rotacao_Maos_deg", 0) or 0)
                
                v_mm = float(t_best.get("Velocidade_Media_mm_s", 0) or 0)
                participantes[pid]["HSW_Velocidade_Media_m_s"] = round(v_mm / 1000.0, 2)
                t_exec = float(t_best.get("Tempo_Execucao_s", 0) or 0)
                n_passos = float(t_best.get("Num_Passos", 1) or 1)
                participantes[pid]["HSW_Tempo_Contato_Maos_s"] = round(t_exec / max(1.0, n_passos), 2)
                participantes[pid]["HSW_Tempo_Duplo_Suporte_pct"] = float(t_best.get("Duplo_Suporte_pct", 0) or 0)

    # 4. Gravar arquivo consolidado
    if participantes:
        todas_chaves = []
        for p in participantes.values():
            for k in p.keys():
                if k not in todas_chaves:
                    todas_chaves.append(k)

        with open(caminho_saida, "w", newline="", encoding="utf-8-sig") as f_out:
            writer = csv.DictWriter(f_out, fieldnames=todas_chaves)
            writer.writeheader()
            for pid in sorted(participantes.keys()):
                writer.writerow(participantes[pid])
        
        print("=" * 80)
        print(f"[SUCESSO] Dataset unificado com {len(participantes)} participante(s) salvo em:\n{caminho_saida}")
        print("=" * 80)

if __name__ == "__main__":
    consolidar_dataset()
