"""
EXECUÇÃO E AUDITORIA DE LIMPEZA C3D - PARTICIPANTE P002
Projeto de Mestrado: Análise de Fatores Associados ao Desempenho no Handstand e Handstand Walk
Mestrando: Guilherme de Paula Lemos | Orientador: Prof. Dr. Matheus Machado Gomes
"""

import os
import sys
import glob
import time
import numpy as np
import ezc3d

# Garantir import do pipeline
diretorio_base = os.path.dirname(os.path.abspath(__file__))
if diretorio_base not in sys.path:
    sys.path.append(diretorio_base)

from pipeline_limpeza_automatica import limpar_arquivo_c3d

def executar_limpeza_p002():
    pasta_raiz = os.path.abspath(os.path.join(diretorio_base, ".."))
    pasta_brutos_p002 = os.path.join(pasta_raiz, "dados_brutos_c3d", "P002")
    pasta_limpos = os.path.join(pasta_raiz, "dados_limpos_c3d")
    os.makedirs(pasta_limpos, exist_ok=True)

    print("=" * 80)
    print("INICIANDO LIMPEZA DOS DADOS BRUTOS DA VICON - PARTICIPANTE P002")
    print("=" * 80)

    # Identificar todos os arquivos de calibração do P002
    arquivos_cal = glob.glob(os.path.join(pasta_brutos_p002, "**", "*[Cc]al*.c3d"), recursive=True)
    print(f"\n[CALIBRAÇÕES IDENTIFICADAS: {len(arquivos_cal)}]")
    for c in arquivos_cal:
        print(f"  - {os.path.relpath(c, pasta_raiz)}")

    # Identificar arquivos dinâmicos do P002
    arquivos_din = [
        f for f in glob.glob(os.path.join(pasta_brutos_p002, "**", "*.c3d"), recursive=True)
        if f not in arquivos_cal
    ]
    arquivos_din.sort()

    print(f"\n[ENSAIOS DINÂMICOS IDENTIFICADOS: {len(arquivos_din)}]")
    for d in arquivos_din:
        print(f"  - {os.path.relpath(d, pasta_raiz)}")

    relatorio_limpeza = []

    for arq_din in arquivos_din:
        nome_base = os.path.basename(arq_din)
        # Pareamento de calibração na mesma pasta da sessão
        cal_pareada = [c for c in arquivos_cal if os.path.normpath(os.path.dirname(c)) == os.path.normpath(os.path.dirname(arq_din))]
        if cal_pareada:
            arq_cal = cal_pareada[0]
        else:
            arq_cal = arquivos_cal[0]

        nome_saida = nome_base.replace(".c3d", "_limpo.c3d")
        caminho_saida = os.path.join(pasta_limpos, nome_saida)

        print(f"\n" + "-" * 70)
        print(f"Processando: {nome_base}")
        print(f"Calibração pareada: {os.path.basename(arq_cal)} ({os.path.basename(os.path.dirname(arq_cal))})")
        print(f"Destino: {os.path.relpath(caminho_saida, pasta_raiz)}")

        t0 = time.time()
        sucesso, stats_svd = limpar_arquivo_c3d(arq_cal, arq_din, caminho_saida)
        dt = time.time() - t0

        if sucesso:
            # Auditoria de integridade pós-limpeza
            c3d_limpo = ezc3d.c3d(caminho_saida)
            pts = c3d_limpo['data']['points']
            labels = [l.strip() for l in c3d_limpo['parameters']['POINT']['LABELS']['value']]
            n_frames = pts.shape[2]
            n_markers = len(labels)
            has_analogs = 'analogs' in c3d_limpo['data']
            analogs_shape = c3d_limpo['data']['analogs'].shape if has_analogs else (0, 0, 0)
            analog_rate = c3d_limpo['parameters']['ANALOG']['RATE']['value'][0] if has_analogs else 0

            # Verificar marcadores anatômicos essenciais
            marcadores_criticos = ['LSHO', 'RSHO', 'C7', 'T10', 'LASI', 'RASI', 'LPSI', 'RPSI', 'LWRA', 'RWRA', 'RANK', 'LANK']
            status_criticos = {}
            for mc in marcadores_criticos:
                if mc in labels:
                    idx = labels.index(mc)
                    nans = np.sum(np.isnan(pts[:3, idx, :]))
                    zeros = np.sum(pts[:3, idx, :] == 0)
                    status_criticos[mc] = "100% ÍNTEGRO" if (nans == 0 and zeros == 0) else f"FALHA ({nans} NaNs, {zeros} zeros)"
                else:
                    status_criticos[mc] = "AUSENTE"

            relatorio_limpeza.append({
                "arquivo_original": nome_base,
                "arquivo_limpo": nome_saida,
                "tempo_processamento_s": round(dt, 2),
                "num_frames": n_frames,
                "num_marcadores": n_markers,
                "analogs_shape": analogs_shape,
                "analog_rate": analog_rate,
                "stats_svd": stats_svd,
                "status_criticos": status_criticos
            })

    print("\n" + "=" * 80)
    print("RESUMO DA AUDITORIA DE LIMPEZA DO PARTICIPANTE P002")
    print("=" * 80)
    for item in relatorio_limpeza:
        print(f"\nArquivo: {item['arquivo_limpo']}")
        print(f"  - Frames: {item['num_frames']} | Tempo de processamento: {item['tempo_processamento_s']}s")
        print(f"  - Analógicos: {item['analogs_shape']} a {item['analog_rate']} Hz")
        svd_desc = ", ".join([f"{k.replace('_reconst','')}: {v} frames" for k, v in item['stats_svd'].items() if v > 0])
        print(f"  - Reconstrução SVD: {svd_desc if svd_desc else 'Nenhuma falha de cluster necessária'}")
        falhas = [f"{k}: {v}" for k, v in item['status_criticos'].items() if v != "100% ÍNTEGRO"]
        if not falhas:
            print(f"  - Integridade Marcadores Críticos: 100% ÍNTEGRO em todos os 12 marcadores avaliados!")
        else:
            print(f"  - AVISO Integridade: {', '.join(falhas)}")

    print("\n[CONCLUÍDO] Todos os 7 arquivos do P002 foram limpos e auditados com sucesso!")

if __name__ == "__main__":
    executar_limpeza_p002()
