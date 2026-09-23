# -*- coding: utf-8 -*-
"""
ATUALIZADOR AUTOMÁTICO DA PLANILHA DE CAMPO TABULAR DO LABIOCOM (COM DISTÂNCIAS HSW E MEDIANA)
"""

import os
import datetime
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter
import numpy as np
import ezc3d

def parse_data(val):
    if not val: return None
    if isinstance(val, (datetime.date, datetime.datetime)):
        return val.date() if isinstance(val, datetime.datetime) else val
    if isinstance(val, (int, float)):
        return datetime.date(1899, 12, 30) + datetime.timedelta(days=int(val))
    if isinstance(val, str):
        val = val.strip()
        for fmt in ['%d/%m/%Y', '%Y-%m-%d', '%d/%m/%y']:
            try: return datetime.datetime.strptime(val, fmt).date()
            except: pass
    return None

def classificar_hs_assistido(c3d_path):
    try:
        c = ezc3d.c3d(c3d_path)
        labels = [l.strip().split(':')[-1].upper() for l in c['parameters']['POINT']['LABELS']['value']]
        pts = c['data']['points']
        fs = c['parameters']['POINT']['RATE']['value'][0]
        num_frames = pts.shape[2]

        def gm(name):
            if name in labels:
                p = pts[:3, labels.index(name), :].copy()
                p[:, np.all(p == 0, axis=0)] = np.nan
                return p
            return np.full((3, num_frames), np.nan)

        rank = gm('RANK'); lank = gm('LANK'); rpsi = gm('RPSI'); apoio = gm('APOIO')
        z_pernas = np.nanmax([rank[2, :], lank[2, :]], axis=0)
        z_pelvis = rpsi[2, :]

        if not np.all(np.isnan(apoio)):
            dist_pesq = np.linalg.norm(apoio - (rank + lank)/2.0, axis=0)
            fl = np.where((dist_pesq > 250) & (z_pernas > z_pelvis + 300))[0]
        else:
            fl = np.where(z_pernas > z_pelvis + 300)[0]

        dur = len(fl) / fs if len(fl) else (num_frames / fs)
        status = 'OK' if dur >= 3.0 else 'Falha'
        return {'dur': dur, 'status': status}
    except Exception:
        return {'dur': 0, 'status': 'Falha'}

def classificar_hs_livre(c3d_path):
    try:
        c = ezc3d.c3d(c3d_path)
        labels = [l.strip().split(':')[-1].upper() for l in c['parameters']['POINT']['LABELS']['value']]
        pts = c['data']['points']
        fs = c['parameters']['POINT']['RATE']['value'][0]
        num_frames = pts.shape[2]

        def gm(name):
            if name in labels:
                p = pts[:3, labels.index(name), :].copy()
                p[:, np.all(p == 0, axis=0)] = np.nan
                return p
            return np.full((3, num_frames), np.nan)

        rank = gm('RANK'); lank = gm('LANK'); rwra = gm('RWRA'); lwra = gm('LWRA')
        rfin = gm('RFIN'); lfin = gm('LFIN'); rpsi = gm('RPSI')
        z_pernas = np.nanmax([rank[2, :], lank[2, :]], axis=0)
        z_pelvis = rpsi[2, :]

        hand_z_init = []
        for m_cand in [rfin, lfin, rwra, lwra]:
            v = np.where(~np.isnan(m_cand[2, :]))[0]
            if len(v):
                hand_z_init.append(np.nanmean(m_cand[2, v[:15]]))
        min_hand_z = min(hand_z_init) if hand_z_init else 1000
        pos_inicio = '2 = Mãos chão' if min_hand_z < 200 else '1 = De cima'

        is_inv = (z_pernas > z_pelvis + 300).astype(int)
        diff_inv = np.diff(is_inv, prepend=0)
        entries = np.where(diff_inv == 1)[0]

        durs = []
        for e in entries:
            end_idx = np.where(diff_inv[e:] == -1)[0]
            dur = (end_idx[0])/fs if len(end_idx) else (len(is_inv)-e)/fs
            durs.append(dur)

        max_dur = max(durs) if durs else 0
        status = 'OK (>=3s)' if max_dur >= 3.0 else 'Falha (<3s)'

        n_chutes = 1
        for i_ch, dur_ch in enumerate(durs, 1):
            if dur_ch >= 3.0:
                n_chutes = i_ch
                break
        else:
            n_chutes = max(1, len(entries))

        t_rank = np.where(rank[2, :] > 500)[0]
        t_lank = np.where(lank[2, :] > 500)[0]
        lead = 'D' if len(t_rank) and len(t_lank) and t_rank[0] < t_lank[0] else 'E'
        dt = abs(t_rank[0] - t_lank[0])/fs if len(t_rank) and len(t_lank) else 0
        forma = '1 = Kick-up' if dt > 0.15 else '2 = Tuck/Pike'

        return {
            'pos_inicio': pos_inicio,
            'forma': forma,
            'perna_lider': lead,
            'n_chutes': n_chutes,
            'max_dur': max_dur,
            'status': status
        }
    except Exception:
        return {
            'pos_inicio': None, 'forma': None, 'perna_lider': None,
            'n_chutes': 1, 'max_dur': 0, 'status': 'Falha (<3s)'
        }

def classificar_hsw(c3d_path):
    try:
        c = ezc3d.c3d(c3d_path)
        labels = [l.strip().split(':')[-1].upper() for l in c['parameters']['POINT']['LABELS']['value']]
        pts = c['data']['points']
        fs = c['parameters']['POINT']['RATE']['value'][0]
        num_frames = pts.shape[2]

        def gm(name):
            if name in labels:
                p = pts[:3, labels.index(name), :].copy()
                p[:, np.all(p == 0, axis=0)] = np.nan
                return p
            return np.full((3, num_frames), np.nan)

        rwra = gm('RWRA'); lwra = gm('LWRA'); rfin = gm('RFIN'); lfin = gm('LFIN')
        rank = gm('RANK'); lank = gm('LANK')
        m_r = rwra if not np.all(np.isnan(rwra)) else rfin
        m_l = lwra if not np.all(np.isnan(lwra)) else lfin

        hand_z_init = []
        for m_cand in [rfin, lfin, rwra, lwra]:
            v = np.where(~np.isnan(m_cand[2, :]))[0]
            if len(v):
                hand_z_init.append(np.nanmean(m_cand[2, v[:15]]))
        min_hand_z = min(hand_z_init) if hand_z_init else 1000
        modo_inicio = '2 = Mãos chão' if min_hand_z < 200 else '1 = De cima'

        # Forma de subida baseada na assimetria dos tornozelos
        t_rank = np.where(rank[2, :] > 500)[0]
        t_lank = np.where(lank[2, :] > 500)[0]
        dt = abs(t_rank[0] - t_lank[0])/fs if len(t_rank) and len(t_lank) else 0
        forma = '1 = Kick-up' if dt > 0.15 else '2 = Tuck/Pike'

        from scipy.signal import find_peaks
        vz_r = np.diff(m_r[2, :], prepend=m_r[2, 0])
        vz_l = np.diff(m_l[2, :], prepend=m_l[2, 0])
        peaks_r, _ = find_peaks(-vz_r, height=1.0, distance=int(fs*0.3))
        peaks_l, _ = find_peaks(-vz_l, height=1.0, distance=int(fs*0.3))
        num_passos = len(peaks_r) + len(peaks_l)

        # Distância em metros no eixo Y
        y_r = m_r[1, ~np.isnan(m_r[1, :])]
        y_l = m_l[1, ~np.isnan(m_l[1, :])]
        dist_r = (np.max(y_r) - np.min(y_r))/1000.0 if len(y_r) else 0
        dist_l = (np.max(y_l) - np.min(y_l))/1000.0 if len(y_l) else 0
        dist_m = round(float(max(dist_r, dist_l)), 2)

        status = 'OK (>=3 passos)' if num_passos >= 3 else 'Falha (<3 passos)'
        return {
            'modo_inicio': modo_inicio,
            'forma': forma,
            'n_entradas': 1,
            'num_passos': num_passos,
            'distancia_m': dist_m if num_passos >= 3 else 0.0,
            'status': status
        }
    except Exception:
        return {
            'modo_inicio': None, 'forma': None, 'n_entradas': 1,
            'num_passos': 0, 'distancia_m': 0.0, 'status': 'Falha (<3 passos)'
        }

def atualizar_planilha_campo_oficial():
    diretorio_base = r"C:\Users\Gui\Documents\MESTRADO_HANDSTAND\coleta\PILOTO OFICIAL\02_SESSAO_LABIOCOM_CINEMATICA\pipeline_processamento"
    caminho_oficial = os.path.join(diretorio_base, "..", "PLANILHA_COLETA_CAMPO_LABIOCOM.xlsx")
    pasta_brutos = os.path.join(diretorio_base, "..", "dados_brutos_c3d")
    pasta_limpos = os.path.join(diretorio_base, "..", "dados_limpos_c3d")
    caminho_mestre = os.path.join(diretorio_base, "..", "..", "00_CADASTRO_TRIAGEM_E_TCLE", "TABELA_MESTRE_IDENTIFICACAO_PARTICIPANTES.xlsx")
    caminho_lacidh = os.path.join(diretorio_base, "..", "..", "01_SESSAO_LACIDH_FORCA", "PLANILHA_COLETA_CAMPO_LACIDH.xlsx")

    datas_s1 = {}
    if os.path.exists(caminho_mestre):
        wb_m = openpyxl.load_workbook(caminho_mestre, data_only=True)
        if '02_Participantes_Oficiais' in wb_m.sheetnames:
            ws_of = wb_m['02_Participantes_Oficiais']
            for r in range(2, ws_of.max_row + 1):
                pid = ws_of.cell(r, 1).value
                d1 = ws_of.cell(r, 7).value
                if pid and d1:
                    datas_s1[str(pid).strip()] = d1

    if os.path.exists(caminho_lacidh):
        wb_l = openpyxl.load_workbook(caminho_lacidh, data_only=True)
        if 'Coleta_LaCiDH' in wb_l.sheetnames:
            ws_l = wb_l['Coleta_LaCiDH']
            for r in range(3, ws_l.max_row + 1):
                pid = ws_l.cell(r, 1).value
                d1 = ws_l.cell(r, 3).value
                if pid and d1:
                    datas_s1[str(pid).strip()] = d1

    dados_existentes = {}
    if os.path.exists(caminho_oficial):
        wb_old = openpyxl.load_workbook(caminho_oficial, data_only=True)
        if 'Coleta_LaBioCoM' in wb_old.sheetnames:
            ws_old = wb_old['Coleta_LaBioCoM']
            headers_old = [cell.value for cell in ws_old[1]]
            for r in range(3, ws_old.max_row + 1):
                pid_val = ws_old.cell(r, 1).value
                if pid_val:
                    pid_str = str(pid_val).strip()
                    dados_existentes[pid_str] = {}
                    for c_idx, col_name in enumerate(headers_old, 1):
                        val = ws_old.cell(r, c_idx).value
                        if val is not None and col_name:
                            dados_existentes[pid_str][col_name] = val

    wb = openpyxl.Workbook()
    font_family = "Calibri"

    colunas = [
        # 1. Identificação (Azul Escuro 1F4E78)
        ("ID_Participante", "ex: P001", "1F4E78", 12),
        ("Nome_Abreviado", "ex: Gustavo Donato", "1F4E78", 22),
        ("Data_Sessao2", "DD/MM/AAAA", "1F4E78", 13),
        ("Intervalo_pos_S1_dias", "Dias pós-LaCiDH (48h-7d)", "1F4E78", 14),
        ("Membro_Dominante", "D ou E", "1F4E78", 10),

        # 2. Medidas Vicon Oficiais LaBioCoM (9 Medidas Bilaterais em mm - Verde Floresta 065F46)
        ("Ombro_Offset_D_mm", "Ombro D (Acromioclavicular-Sulco mm)", "065F46", 16),
        ("Ombro_Offset_E_mm", "Ombro E (Acromioclavicular-Sulco mm)", "065F46", 16),
        ("Cotovelo_Largura_D_mm", "Cotovelo D (Epicôndilos mm)", "065F46", 14),
        ("Cotovelo_Largura_E_mm", "Cotovelo E (Epicôndilos mm)", "065F46", 14),
        ("Punho_Largura_D_mm", "Punho D (Entre estilóides mm)", "065F46", 14),
        ("Punho_Largura_E_mm", "Punho E (Entre estilóides mm)", "065F46", 14),
        ("Mao_Espessura_D_mm", "Mão D (3º dedo e palma mm)", "065F46", 14),
        ("Mao_Espessura_E_mm", "Mão E (3º dedo e palma mm)", "065F46", 14),
        ("Joelho_Largura_D_mm", "Joelho D (Côndilos femorais mm)", "065F46", 14),
        ("Joelho_Largura_E_mm", "Joelho E (Côndilos femorais mm)", "065F46", 14),
        ("Tornozelo_Largura_D_mm", "Tornozelo D (Maléolos mm)", "065F46", 14),
        ("Tornozelo_Largura_E_mm", "Tornozelo E (Maléolos mm)", "065F46", 14),
        ("Comp_Real_MMII_EIAS_D_mm", "Comp Real MMII D (EIAS-Maléolo mm)", "065F46", 16),
        ("Comp_Real_MMII_EIAS_E_mm", "Comp Real MMII E (EIAS-Maléolo mm)", "065F46", 16),
        ("Comp_Membro_Trocanter_D_mm", "Comp Membro D (Trocânter-Maléolo mm)", "065F46", 16),
        ("Comp_Membro_Trocanter_E_mm", "Comp Membro E (Trocânter-Maléolo mm)", "065F46", 16),
        ("Comp_Braco_Acromio_Dedo3_D_mm", "Comp Braço D (Acrômio-3ºdedo mm)", "065F46", 16),
        ("Comp_Braco_Acromio_Dedo3_E_mm", "Comp Braço E (Acrômio-3ºdedo mm)", "065F46", 16),

        # 3. Morfologia das Mãos no Solo (Azul Petróleo 0E7490)
        ("Posicao_Dedos", "1=Afastados | 2=Unidos", "0E7490", 14),
        ("Cupula_Garra_Cambering", "1=Garra (Cambering) | 2=Plana", "0E7490", 15),

        # 4. Handstand Estático — Assistido (Azul Royal 1D4ED8)
        ("HS_Assist_T1_Status", "OK / Falha / Disp", "1D4ED8", 12),
        ("HS_Assist_T2_Status", "OK / Falha / Disp", "1D4ED8", 12),
        ("HS_Assist_T3_Status", "OK / Falha / Disp", "1D4ED8", 12),
        ("HS_Assist_Tentativa_Pico", "T1, T2 ou T3 (Pico)", "1D4ED8", 14),

        # 5. Handstand Estático — Livre (Púrpura 6B21A8)
        ("HS_Livre_Posicao_Inicio", "1=De cima | 2=Mãos chão", "6B21A8", 15),
        ("HS_Livre_Forma_Subida", "1=Kick | 2=Strad | 3=Pike | 4=Tuck | 5=Press", "6B21A8", 18),
        ("HS_Livre_Perna_Lider", "D ou E", "6B21A8", 10),
        ("HS_Livre_T1_N_Chutes", "Nº chutes até parar (máx 5)", "6B21A8", 13),
        ("HS_Livre_T1_Status", "OK (>=3s) / Falha", "6B21A8", 12),
        ("HS_Livre_T2_N_Chutes", "Nº chutes até parar (máx 5)", "6B21A8", 13),
        ("HS_Livre_T2_Status", "OK (>=3s) / Falha", "6B21A8", 12),
        ("HS_Livre_T3_N_Chutes", "Nº chutes até parar (máx 5)", "6B21A8", 13),
        ("HS_Livre_T3_Status", "OK (>=3s) / Falha", "6B21A8", 12),
        ("HS_Livre_Tentativa_Pico", "T1, T2 ou T3 (Pico)", "6B21A8", 14),
        ("HS_Livre_Obs", "Estabilidade / Correções punho", "6B21A8", 22),

        # 6. Handstand Walk — Dinâmico (Laranja C2410C - com Distâncias e Mediana)
        ("HSW_Modo_Inicio", "1=De cima | 2=Mãos chão | 3=Stop&Go", "C2410C", 16),
        ("HSW_Forma_Subida", "1=Kick | 2=Strad | 3=Pike | 4=Tuck | 5=Press", "C2410C", 18),
        ("HSW_T1_N_Entradas", "Subidas (máx 3)", "C2410C", 13),
        ("HSW_T1_Status", "OK (>=3 passos) / Falha", "C2410C", 14),
        ("HSW_T1_Distancia_m", "Distância linear T1 (m)", "C2410C", 14),
        ("HSW_T2_N_Entradas", "Subidas (máx 3)", "C2410C", 13),
        ("HSW_T2_Status", "OK (>=3 passos) / Falha", "C2410C", 14),
        ("HSW_T2_Distancia_m", "Distância linear T2 (m)", "C2410C", 14),
        ("HSW_T3_N_Entradas", "Subidas (máx 3)", "C2410C", 13),
        ("HSW_T3_Status", "OK (>=3 passos) / Falha", "C2410C", 14),
        ("HSW_T3_Distancia_m", "Distância linear T3 (m)", "C2410C", 14),
        ("HSW_Distancia_Mediana_m", "Mediana dos trials válidos (m)", "C2410C", 16),
        ("HSW_Obs_Ocorrencias", "Passadas, quedas, toques, cotovelo", "C2410C", 25),

        # 7. Rastreabilidade Técnica (Cinza 475569)
        ("Marcadores_Descolados", "Nenhum / Quais e tentativa", "475569", 20),
        ("Observacoes_Gerais_Sessao2", "Intercorrências / Notas gerais", "475569", 25)
    ]

    ws = wb.active
    ws.title = "Coleta_LaBioCoM"
    ws.views.sheetView[0].showGridLines = True

    thin_side = Side(border_style="thin", color="CBD5E1")
    cell_border = Border(left=thin_side, right=thin_side, top=thin_side, bottom=thin_side)

    for col_idx, (col_name, sub_hint, color_hex, width) in enumerate(colunas, 1):
        col_letter = get_column_letter(col_idx)
        ws.column_dimensions[col_letter].width = width

        c1 = ws.cell(1, col_idx)
        c1.value = col_name
        c1.font = Font(name=font_family, size=11, bold=True, color="FFFFFF")
        c1.fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")
        c1.alignment = Alignment(horizontal="center", vertical="center", wrap_text=False)
        c1.border = cell_border

        c2 = ws.cell(2, col_idx)
        c2.value = sub_hint
        c2.font = Font(name=font_family, size=9, italic=True, color="E2E8F0")
        c2.fill = PatternFill(start_color=color_hex, end_color=color_hex, fill_type="solid")
        c2.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c2.border = cell_border

    ws.row_dimensions[1].height = 26
    ws.row_dimensions[2].height = 24

    fill_even = PatternFill(start_color="F8FAFC", end_color="F8FAFC", fill_type="solid")
    fill_odd = PatternFill(start_color="FFFFFF", end_color="FFFFFF", fill_type="solid")

    mapa_colunas = {col_name: idx for idx, (col_name, _, _, _) in enumerate(colunas, 1)}

    for p_idx in range(1, 41):
        row_num = p_idx + 2
        pid = f"P{p_idx:03d}"
        row_fill = fill_even if p_idx % 2 == 0 else fill_odd
        ws.row_dimensions[row_num].height = 20

        for col_idx in range(1, len(colunas) + 1):
            c = ws.cell(row_num, col_idx)
            c.border = cell_border
            c.fill = row_fill
            c.font = Font(name=font_family, size=10, color="1E293B")
            c.alignment = Alignment(horizontal="center", vertical="center")

        ws.cell(row_num, 1).value = pid
        ws.cell(row_num, 1).font = Font(name=font_family, size=10, bold=True, color="0F172A")

        if pid in dados_existentes:
            for col_name, val in dados_existentes[pid].items():
                if col_name in mapa_colunas:
                    ws.cell(row_num, mapa_colunas[col_name]).value = val

        data_s2_val = ws.cell(row_num, mapa_colunas["Data_Sessao2"]).value
        d2 = parse_data(data_s2_val)
        d1 = parse_data(datas_s1.get(pid))
        if d1 and d2:
            ws.cell(row_num, mapa_colunas["Intervalo_pos_S1_dias"]).value = (d2 - d1).days

        pasta_pid_bruto = os.path.join(pasta_brutos, pid)
        if os.path.exists(pasta_pid_bruto):
            print(f"[PROCESSANDO CINEMÁTICA AUTOMÁTICA] {pid}...")

            # --- A. Handstand Assistido ---
            durs_assist = {}
            for t_num in [1, 2, 3]:
                col_st = f"HS_Assist_T{t_num}_Status"
                f_limpo = os.path.join(pasta_limpos, f"{pid}_hs_assistida{t_num:02d}_limpo.c3d")
                f_bruto = os.path.join(pasta_pid_bruto, "handstand_assistido", f"{pid}_hs_assistida{t_num:02d}.c3d")
                alvo = f_limpo if os.path.exists(f_limpo) else (f_bruto if os.path.exists(f_bruto) else None)

                if alvo:
                    res_a = classificar_hs_assistido(alvo)
                    ws.cell(row_num, mapa_colunas[col_st]).value = res_a['status']
                    durs_assist[f"T{t_num}"] = res_a['dur']
                else:
                    ws.cell(row_num, mapa_colunas[col_st]).value = "Dispensado"

            if durs_assist:
                pico_assist = max(durs_assist, key=durs_assist.get)
                ws.cell(row_num, mapa_colunas["HS_Assist_Tentativa_Pico"]).value = pico_assist

            # --- B. Handstand Livre ---
            durs_livre = {}
            inicio_detectado = None
            forma_detectada = None
            perna_detectada = None

            for t_num in [1, 2, 3]:
                col_st = f"HS_Livre_T{t_num}_Status"
                col_ch = f"HS_Livre_T{t_num}_N_Chutes"
                f_livre_limpo = os.path.join(pasta_limpos, f"{pid}_hs_livre{t_num:02d}_limpo.c3d")
                f_livre_bruto = os.path.join(pasta_pid_bruto, "handstand_livre", f"{pid}_hs_livre{t_num:02d}.c3d")
                alvo_l = f_livre_limpo if os.path.exists(f_livre_limpo) else (f_livre_bruto if os.path.exists(f_livre_bruto) else None)

                if alvo_l:
                    res_l = classificar_hs_livre(alvo_l)
                    ws.cell(row_num, mapa_colunas[col_st]).value = res_l['status']
                    ws.cell(row_num, mapa_colunas[col_ch]).value = res_l['n_chutes']
                    durs_livre[f"T{t_num}"] = res_l['max_dur']

                    if inicio_detectado is None and res_l['pos_inicio']:
                        inicio_detectado = res_l['pos_inicio']
                    if forma_detectada is None and res_l['forma']:
                        forma_detectada = res_l['forma']
                    if perna_detectada is None and res_l['perna_lider']:
                        perna_detectada = res_l['perna_lider']
                else:
                    ws.cell(row_num, mapa_colunas[col_st]).value = "Dispensado"

            if inicio_detectado:
                ws.cell(row_num, mapa_colunas["HS_Livre_Posicao_Inicio"]).value = inicio_detectado
            if forma_detectada:
                ws.cell(row_num, mapa_colunas["HS_Livre_Forma_Subida"]).value = forma_detectada
            if perna_detectada:
                ws.cell(row_num, mapa_colunas["HS_Livre_Perna_Lider"]).value = perna_detectada
            if durs_livre:
                pico_livre = max(durs_livre, key=durs_livre.get)
                ws.cell(row_num, mapa_colunas["HS_Livre_Tentativa_Pico"]).value = pico_livre

            # --- C. Handstand Walk ---
            modos_walk = []
            formas_walk = []
            dists_walk = []

            for t_num in [1, 2, 3]:
                col_st = f"HSW_T{t_num}_Status"
                col_ent = f"HSW_T{t_num}_N_Entradas"
                col_dist = f"HSW_T{t_num}_Distancia_m"
                f_walk_limpo = os.path.join(pasta_limpos, f"{pid}_hs_walk{t_num:02d}_limpo.c3d")
                f_walk_bruto = os.path.join(pasta_pid_bruto, "handstand_walk", f"{pid}_hs_walk{t_num:02d}.c3d")
                alvo_w = f_walk_limpo if os.path.exists(f_walk_limpo) else (f_walk_bruto if os.path.exists(f_walk_bruto) else None)

                if alvo_w:
                    res_w = classificar_hsw(alvo_w)
                    ws.cell(row_num, mapa_colunas[col_st]).value = res_w['status']
                    ws.cell(row_num, mapa_colunas[col_ent]).value = res_w['n_entradas']
                    ws.cell(row_num, mapa_colunas[col_dist]).value = res_w['distancia_m']

                    if res_w['status'] == 'OK (>=3 passos)':
                        dists_walk.append(res_w['distancia_m'])

                    if res_w['modo_inicio']:
                        modos_walk.append(res_w['modo_inicio'])
                    if res_w['forma']:
                        formas_walk.append(res_w['forma'])
                else:
                    ws.cell(row_num, mapa_colunas[col_st]).value = "Dispensado"

            if modos_walk:
                ws.cell(row_num, mapa_colunas["HSW_Modo_Inicio"]).value = max(set(modos_walk), key=modos_walk.count)
            if formas_walk:
                forma_final = '1 = Kick-up' if '1 = Kick-up' in formas_walk else formas_walk[0]
                ws.cell(row_num, mapa_colunas["HSW_Forma_Subida"]).value = forma_final
            if dists_walk:
                mediana_m = round(float(np.median(dists_walk)), 2)
                ws.cell(row_num, mapa_colunas["HSW_Distancia_Mediana_m"]).value = mediana_m

    # ABA 2: Dicionario_Codigos
    ws_dic = wb.create_sheet(title="Dicionario_Codigos")
    ws_dic.views.sheetView[0].showGridLines = True

    dic_widths = {"A": 22, "B": 30, "C": 40, "D": 42, "E": 18}
    for col, width in dic_widths.items():
        ws_dic.column_dimensions[col].width = width

    ws_dic.merge_cells("A1:E1")
    ws_dic["A1"] = "DICIONÁRIO DE VARIÁVEIS E CÓDIGOS DA COLETA DE CAMPO - SESSÃO 2 (LaBioCoM)"
    ws_dic["A1"].font = Font(name=font_family, size=12, bold=True, color="FFFFFF")
    ws_dic["A1"].fill = PatternFill(start_color="064E3B", end_color="064E3B", fill_type="solid")
    ws_dic["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_dic.row_dimensions[1].height = 26

    dic_headers = [("A", "Bloco"), ("B", "Variável"), ("C", "Descrição"), ("D", "Critérios / Códigos"), ("E", "Tipo")]
    for col, text in dic_headers:
        c = ws_dic[f"{col}2"]
        c.value = text
        c.font = Font(name=font_family, size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill(start_color="047857", end_color="047857", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center")
        c.border = cell_border
    ws_dic.row_dimensions[2].height = 20

    dic_itens = [
        ("1. Identificação", "ID_Participante", "Código identificador do atleta", "P001, P002 ... P040", "Texto / ID"),
        ("1. Identificação", "Nome_Abreviado", "Nome de referência em laboratório", "Texto livre", "Texto"),
        ("1. Identificação", "Data_Sessao2", "Data da coleta de cinemática/cinética", "DD/MM/AAAA", "Data"),
        ("1. Identificação", "Intervalo_pos_S1_dias", "Dias corridos entre S1 (LaCiDH) e S2 (LaBioCoM)", "Calculado automaticamente (48h a 7 dias)", "Numérico (Int)"),
        ("1. Identificação", "Membro_Dominante", "Membro superior dominante relatado", "D = Destro | E = Canhoto", "Categórico"),

        ("2. Medidas Vicon", "Ombro_Offset_D/E_mm", "Art. acromioclavicular ao sulco bicipital", "mm no paquímetro (Shoulder Offset)", "Numérico"),
        ("2. Medidas Vicon", "Cotovelo_Largura_D/E_mm", "Diâmetro biepicondilar do úmero", "mm no paquímetro", "Numérico"),
        ("2. Medidas Vicon", "Punho_Largura_D/E_mm", "Meio entre os processos estilóides rádio-ulna", "mm no paquímetro", "Numérico"),
        ("2. Medidas Vicon", "Mao_Espessura_D/E_mm", "Dorso do 3º dedo à palma da mão", "mm no paquímetro", "Numérico"),
        ("2. Medidas Vicon", "Joelho_Largura_D/E_mm", "Côndilos femorais medial-lateral", "mm no paquímetro", "Numérico"),
        ("2. Medidas Vicon", "Tornozelo_Largura_D/E_mm", "Bimaleolar (maléolo medial e lateral)", "mm no paquímetro", "Numérico"),
        ("2. Medidas Vicon", "Comp_Real_MMII_EIAS_D/E_mm", "Distância EIAS ao maléolo medial da tíbia", "mm com fita métrica (Leg Length)", "Numérico"),
        ("2. Medidas Vicon", "Comp_Membro_Trocanter_D/E_mm", "Trocânter maior ao maléolo lateral da fíbula", "mm com fita métrica", "Numérico"),
        ("2. Medidas Vicon", "Comp_Braco_Acromio_Dedo3_D/E_mm", "Acrômio à ponta do 3º quirodáctilo", "mm com fita métrica (Arm Length)", "Numérico"),

        ("3. Morfologia Mãos", "Posicao_Dedos", "Afastamento lateral dos dedos no chão", "1 = Afastados/Espalmados | 2 = Unidos", "Categórico"),
        ("3. Morfologia Mãos", "Cupula_Garra_Cambering", "Padrão de acoplamento palmar/falângico", "1 = Dedos em Garra (Cambering) | 2 = Plana", "Categórico"),

        ("4. HS Assistido", "HS_Assist_T[1-3]_Status", "Validação técnica da tentativa assistida (Vicon)", "OK = Válido | Falha = Desabou | Dispensado", "Texto"),
        ("4. HS Assistido", "HS_Assist_Tentativa_Pico", "Tentativa onde ocorreu o tempo máximo (pico)", "T1, T2 ou T3", "Texto"),

        ("5. HS Livre", "HS_Livre_Posicao_Inicio", "Posição corporal de partida (detectada no Vicon)", "1 = De cima (Em pé/Lunge) | 2 = Mãos chão", "Categórico"),
        ("5. HS Livre", "HS_Livre_Forma_Subida", "Estratégia motora de entrada no Handstand", "1=Kick | 2=Straddle | 3=Pike | 4=Tuck | 5=Press", "Categórico"),
        ("5. HS Livre", "HS_Livre_Perna_Lider", "Membro que sobe primeiro no chute", "D = Direita | E = Esquerda", "Categórico"),
        ("5. HS Livre", "HS_Livre_T[1-3]_N_Chutes", "Nº chutes até estabilizar (detectado no Vicon)", "Contagem de impulsos (máx 5 chutes)", "Numérico"),
        ("5. HS Livre", "HS_Livre_T[1-3]_Status", "Validação técnica da tentativa livre (>=3s)", "OK (>=3s) | Falha (<3s) | Dispensado", "Texto"),
        ("5. HS Livre", "HS_Livre_Tentativa_Pico", "Tentativa onde ocorreu o tempo máximo (pico)", "T1, T2 ou T3", "Texto"),
        ("5. HS Livre", "HS_Livre_Obs", "Estabilidade estática e ajustes palmares", "Texto livre", "Texto"),

        ("6. HSW Dinâmico", "HSW_Modo_Inicio", "Estratégia de início da marcha", "1 = De cima (Flying) | 2 = Mãos chão | 3 = Stop&Go", "Categórico"),
        ("6. HSW Dinâmico", "HSW_Forma_Subida", "Estratégia de subida no Handstand Walk", "1=Kick | 2=Straddle | 3=Pike | 4=Tuck | 5=Press", "Categórico"),
        ("6. HSW Dinâmico", "HSW_T[1-3]_N_Entradas", "Tentativas de subida na tentativa (máx 3)", "Contagem de subidas", "Numérico"),
        ("6. HSW Dinâmico", "HSW_T[1-3]_Status", "Validação técnica da marcha (mín 3 passos)", "OK (>=3 passos) | Falha (<3 passos) | Dispensado", "Texto"),
        ("6. HSW Dinâmico", "HSW_T[1-3]_Distancia_m", "Distância linear útil percorrida na tentativa", "Metros (m) no Vicon (eixo Y)", "Numérico"),
        ("6. HSW Dinâmico", "HSW_Distancia_Mediana_m", "Mediana das distâncias das tentativas válidas", "Metros (m) - Desfecho primário SPSS", "Numérico"),
        ("6. HSW Dinâmico", "HSW_Obs_Ocorrencias", "Passadas, quedas, toques, cotovelo", "Texto livre", "Texto"),

        ("7. Rastreabilidade", "Marcadores_Descolados", "Marcadores retrorreflexivos soltos na sessão", "Nenhum | Quais e tentativa correspondente", "Texto"),
        ("7. Rastreabilidade", "Observacoes_Gerais_Sessao2", "Intercorrências laboratoriais e do Vicon", "Texto livre", "Texto")
    ]

    for idx, r in enumerate(dic_itens, 3):
        r_fill = fill_even if idx % 2 == 0 else fill_odd
        for c_idx, val in enumerate(r, 1):
            col_let = get_column_letter(c_idx)
            c = ws_dic[f"{col_let}{idx}"]
            c.value = val
            c.font = Font(name=font_family, size=9.5, color="1E293B")
            c.fill = r_fill
            c.border = cell_border
            c.alignment = Alignment(horizontal="center" if c_idx in [1, 5] else "left", vertical="center")
        ws_dic.row_dimensions[idx].height = 18

    try:
        wb.save(caminho_oficial)
        print(f"\n[SUCESSO] Planilha de Campo Oficial do LaBioCoM atualizada com sucesso em:\n{caminho_oficial}")
    except PermissionError:
        caminho_alt = os.path.join(diretorio_base, "..", "PLANILHA_COLETA_CAMPO_LABIOCOM_ATUALIZADA.xlsx")
        wb.save(caminho_alt)
        print(f"\n[AVISO] O arquivo principal está aberto no Excel. Salvo com sucesso em:\n{caminho_alt}")

if __name__ == "__main__":
    atualizar_planilha_campo_oficial()
