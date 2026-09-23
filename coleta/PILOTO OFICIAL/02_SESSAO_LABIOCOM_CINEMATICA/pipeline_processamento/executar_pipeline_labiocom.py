"""
ORQUESTRADOR MASTER DO PIPELINE LABIOCOM (SESSÃO 2)
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes
"""

import os
import glob
import csv
import re
import numpy as np

from pipeline_limpeza_automatica import limpar_arquivo_c3d
from analisar_hs_oficial import analisar_hs_arquivo
from analisar_hsw_oficial import analisar_hsw_arquivo

def extrair_pid(nome_arquivo):
    """Extrai o ID do participante (ex: 'P001', 'P022') do nome do arquivo."""
    m = re.search(r'(P\d{3})', nome_arquivo, re.IGNORECASE)
    if m:
        return m.group(1).upper()
    if "_" in nome_arquivo:
        return nome_arquivo.split("_")[0].upper()
    return "DEFAULT"

def executar_pipeline_completo():
    diretorio_base = os.path.dirname(os.path.abspath(__file__))
    pasta_brutos = os.path.join(diretorio_base, "..", "dados_brutos_c3d")
    pasta_limpos = os.path.join(diretorio_base, "..", "dados_limpos_c3d")
    pasta_resultados = os.path.join(diretorio_base, "..", "resultados")

    os.makedirs(pasta_limpos, exist_ok=True)
    os.makedirs(pasta_resultados, exist_ok=True)

    print("=" * 80)
    print("EXECUTANDO PIPELINE OFICIAL LABIOCOM (VICON + PLATAFORMA BERTEC)")
    print("=" * 80)

    # 1. Localizar e mapear arquivos de Calibração por Participante (ex: P001 Cal 01.c3d, P022_cal.c3d)
    arquivos_cal = glob.glob(os.path.join(pasta_brutos, "**", "*[Cc]al*.c3d"), recursive=True)
    if not arquivos_cal:
        print(f"[AVISO] Nenhum arquivo estático de calibração (*cal*.c3d) encontrado em {pasta_brutos}.")
        print("Buscando arquivos já limpos na pasta de dados limpos...")
    else:
        # Mapeia calibração por ID do atleta (mantendo pelo menos uma por participante)
        mapa_cal = {}
        for c in arquivos_cal:
            base = os.path.basename(c)
            pid = extrair_pid(base)
            if pid not in mapa_cal:
                mapa_cal[pid] = c
                print(f"[INFO] Arquivo de calibração registrado para [{pid}]: {os.path.relpath(c, pasta_brutos)}")

        # Limpar todos os arquivos brutos dinâmicos com a calibração correta de cada sujeito
        arquivos_dinamicos = [f for f in glob.glob(os.path.join(pasta_brutos, "**", "*.c3d"), recursive=True) if f not in arquivos_cal]
        for arq_din in sorted(arquivos_dinamicos):
            nome_base = os.path.basename(arq_din)
            pid = extrair_pid(nome_base)
            
            # Prioriza arquivo de calibração na mesma pasta da sessão/tarefa
            cal_mesma_pasta = [c for c in arquivos_cal if os.path.normpath(os.path.dirname(c)) == os.path.normpath(os.path.dirname(arq_din))]
            if cal_mesma_pasta:
                arq_cal_atleta = cal_mesma_pasta[0]
            else:
                arq_cal_atleta = mapa_cal.get(pid) or mapa_cal.get("DEFAULT") or arquivos_cal[0]
            
            nome_limpo = nome_base.replace(".c3d", "_limpo.c3d")
            saida_limpa = os.path.join(pasta_limpos, nome_limpo)
            if not os.path.exists(saida_limpa):
                print(f"-> Limpando {nome_base} usando calibração de [{pid}] ({os.path.basename(arq_cal_atleta)})...")
                limpar_arquivo_c3d(arq_cal_atleta, arq_din, saida_limpa)

    # 2. Processar métricas em todos os arquivos limpos
    arquivos_limpos = glob.glob(os.path.join(pasta_limpos, "*.c3d"))
    if not arquivos_limpos:
        print("[INFO] Nenhum arquivo C3D limpo encontrado para processar no momento.")
        return

    resultados_tentativas = []
    
    for arq in sorted(arquivos_limpos):
        nome = os.path.basename(arq).lower()
        print(f"\n-> Processando métricas: {nome}")
        
        # Extrair identificadores
        pid = extrair_pid(os.path.basename(arq))
        tentativa_match = re.search(r'(?:assistid\w*|livre|walk)0?(\d+)', nome)
        tentativa_str = f"T{int(tentativa_match.group(1))}" if tentativa_match else ""
        
        if "hsw" in nome or "walk" in nome:
            try:
                res = analisar_hsw_arquivo(arq)
                res["ID_Participante"] = pid
                res["Arquivo"] = os.path.basename(arq)
                res["Tipo_Tarefa"] = "HSW"
                res["Tentativa"] = tentativa_str
                resultados_tentativas.append(res)
                print(f"   [OK HSW] Distância: {res['Distancia_Percorrida_m']} m | Velocidade: {res['Velocidade_Media_mm_s']} mm/s")
            except Exception as e:
                print(f"   [ERRO HSW] {e}")
        elif "hs" in nome:
            try:
                cond = "assistido" if ("assistid" in nome) else "livre"
                res = analisar_hs_arquivo(arq, cond)
                res["ID_Participante"] = pid
                res["Arquivo"] = os.path.basename(arq)
                res["Tipo_Tarefa"] = f"HS_{cond.upper()}"
                res["Tentativa"] = tentativa_str
                resultados_tentativas.append(res)
                print(f"   [OK HS] Condição: {cond} | Tempo: {res['Tempo_Sustentacao_s']} s | CoP-CoM: {res['Distancia_CoP_CoM_mm']} mm")
            except Exception as e:
                print(f"   [ERRO HS] {e}")

    # Salvar resultados detalhados por tentativa
    if resultados_tentativas:
        saida_tentativas = os.path.join(pasta_resultados, "variaveis_labiocom_por_tentativa.csv")
        chaves = sorted(list(set().union(*(d.keys() for d in resultados_tentativas))))
        with open(saida_tentativas, "w", newline="", encoding="utf-8-sig") as f:
            writer = csv.DictWriter(f, fieldnames=chaves)
            writer.writeheader()
            writer.writerows(resultados_tentativas)
        print(f"\n[SUCESSO] Tabela detalhada por tentativa salva em:\n{saida_tentativas}")

        # Salvar tabelas individuais por participante e tarefa
        pids = sorted(list(set(d.get("ID_Participante", "DEFAULT") for d in resultados_tentativas)))
        for p in pids:
            # HS Assistido
            hs_assist = [d for d in resultados_tentativas if d.get("ID_Participante") == p and "ASSISTID" in d.get("Tipo_Tarefa", "")]
            if hs_assist:
                out_p_assist = os.path.join(pasta_resultados, f"{p}_hs_assistida_biomecanica.csv")
                k_assist = sorted(list(set().union(*(d.keys() for d in hs_assist))))
                with open(out_p_assist, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.DictWriter(f, fieldnames=k_assist)
                    w.writeheader()
                    w.writerows(hs_assist)
                print(f"   -> Salvo: {os.path.basename(out_p_assist)} ({len(hs_assist)} tentativas)")

            # HS Livre
            hs_livre = [d for d in resultados_tentativas if d.get("ID_Participante") == p and "LIVRE" in d.get("Tipo_Tarefa", "")]
            if hs_livre:
                out_p_livre = os.path.join(pasta_resultados, f"{p}_hs_livre_biomecanica.csv")
                k_livre = sorted(list(set().union(*(d.keys() for d in hs_livre))))
                with open(out_p_livre, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.DictWriter(f, fieldnames=k_livre)
                    w.writeheader()
                    w.writerows(hs_livre)
                print(f"   -> Salvo: {os.path.basename(out_p_livre)} ({len(hs_livre)} tentativas)")

            # HSW
            hsw = [d for d in resultados_tentativas if d.get("ID_Participante") == p and d.get("Tipo_Tarefa") == "HSW"]
            if hsw:
                out_p_hsw = os.path.join(pasta_resultados, f"{p}_hsw_biomecanica.csv")
                k_hsw = sorted(list(set().union(*(d.keys() for d in hsw))))
                with open(out_p_hsw, "w", newline="", encoding="utf-8-sig") as f:
                    w = csv.DictWriter(f, fieldnames=k_hsw)
                    w.writeheader()
                    w.writerows(hsw)
                print(f"   -> Salvo: {os.path.basename(out_p_hsw)} ({len(hsw)} tentativas)")

if __name__ == "__main__":
    executar_pipeline_completo()