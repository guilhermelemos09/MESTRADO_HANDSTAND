"""
Reconstrução Robusta de Marcadores - Handstand Walk (HSW)
==========================================================
Utiliza Algoritmo de Kabsch (SVD) com fallback inteligente de âncoras:
- Primário (4 pontos): C7 + T10 + referencia1 + referencia2
- Fallback (3 pontos): C7 + T10 + referencia2  (quando ref1 some)

3 pontos não-colineares são matematicamente suficientes para definir
um corpo rígido no espaço 3D, permitindo recuperar o ombro em frames
onde referencia1 estava ocluída (~37% dos frames do HSW).

Ref: KABSCH, W. Acta Crystallographica Section A, v. 32, n. 5, 1976.
     SÖDERKVIST & WEDIN. Journal of Biomechanics, v. 26, n. 12, 1993.
"""
import numpy as np
import ezc3d


def calcular_transformacao_rigida(pontos_ref, pontos_mov):
    """
    Algoritmo de Kabsch: calcula R e t que mapeia pontos_ref → pontos_mov.
    Funciona com qualquer número de pontos >= 3.
    """
    centroid_ref = np.mean(pontos_ref, axis=0)
    centroid_mov = np.mean(pontos_mov, axis=0)
    A = pontos_ref - centroid_ref
    B = pontos_mov - centroid_mov
    H = A.T @ B
    U, S, Vt = np.linalg.svd(H)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = centroid_mov - R @ centroid_ref
    return R, t


def ponto_valido(p):
    """Verifica se um ponto 3D é válido (sem NaN e não-zero absoluto)."""
    return not (np.any(np.isnan(p)) or np.all(p == 0))


def reconstruir_teste(c3d_static_path, c3d_dynamic_path, output_path):
    print(f"\n--- Iniciando reconstrução (SVD + fallback 3pts) para: {c3d_dynamic_path} ---")

    try:
        # ── 1. ESTÁTICO ───────────────────────────────────────────────────────
        static = ezc3d.c3d(c3d_static_path)
        labels_static = [l.strip() for l in static['parameters']['POINT']['LABELS']['value']]
        data_static = static['data']['points']

        # Âncoras: 4 primárias + 1 fallback subset (sem ref1)
        ancora_nomes_4 = ['C7', 'T10', 'referencia1', 'referencia2']
        ancora_nomes_3 = ['C7', 'T10', 'referencia2']  # fallback sem ref1

        def get_static_idx(nome):
            if nome in labels_static:
                return labels_static.index(nome)
            raise ValueError(f"Âncora '{nome}' não encontrada no estático!")

        ancora_idx_static_4 = [get_static_idx(n) for n in ancora_nomes_4]
        ancora_idx_static_3 = [get_static_idx(n) for n in ancora_nomes_3]

        # Posições no frame 0 do estático
        ancora_est_4 = np.array([data_static[:3, i, 0] for i in ancora_idx_static_4])
        ancora_est_3 = np.array([data_static[:3, i, 0] for i in ancora_idx_static_3])

        # Marcadores alvo
        marcadores_alvo = ['CLAV', 'LSHO', 'RSHO', 'LASI', 'LFIN']
        offsets_local = {}
        for m in marcadores_alvo:
            if m in labels_static:
                idx_m = labels_static.index(m)
                offsets_local[m] = data_static[:3, idx_m, 0].copy()
                print(f"-> Vetor SVD para '{m}' mapeado.")
            else:
                print(f"   Alerta: '{m}' não encontrado no estático — ignorado.")

        # ── 2. DINÂMICO ───────────────────────────────────────────────────────
        dynamic = ezc3d.c3d(c3d_dynamic_path)
        labels_dyn = [l.strip() for l in dynamic['parameters']['POINT']['LABELS']['value']]
        data_dyn = dynamic['data']['points']
        num_frames = data_dyn.shape[2]

        analogs_backup = dynamic['data']['analogs'].copy() if 'analogs' in dynamic['data'] else None

        # Índices dinâmicos das âncoras
        def get_dyn_idx(nome):
            if nome in labels_dyn:
                return labels_dyn.index(nome)
            raise ValueError(f"Âncora '{nome}' ausente no dinâmico!")

        ancora_idx_dyn_4 = [get_dyn_idx(n) for n in ancora_nomes_4]
        ancora_idx_dyn_3 = [get_dyn_idx(n) for n in ancora_nomes_3]

        unlabeled_indices = [i for i, label in enumerate(labels_dyn)
                             if '*' in label or label.lower().startswith('unlabeled')]

        # Residual real de pontos válidos (usado para marcar reconstruídos como válidos)
        # O ezc3d usa residual = -1.0 para pontos inválidos; positivo = válido
        residuals_nativos = dynamic.c3d_swig.get_point_residuals()  # shape (1, N_markers, N_frames)
        residual_padrao = {}
        for m in marcadores_alvo:
            if m in labels_dyn:
                idx_m = labels_dyn.index(m)
                res_validos = residuals_nativos[0, idx_m, :]
                res_pos = res_validos[res_validos > 0]
                residual_padrao[m] = float(np.mean(res_pos)) if len(res_pos) > 0 else 1.0

        # ── 3. RECONSTRUÇÃO FRAME A FRAME ────────────────────────────────────
        correcoes = {m: 0 for m in marcadores_alvo}
        stats = {'4pts': 0, '3pts': 0, 'skip': 0}

        for frame in range(num_frames):

            # --- Tentar 4 âncoras (primário) ---
            ancora_frame_4 = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn_4])
            usa_4 = all(ponto_valido(p) for p in ancora_frame_4)

            if usa_4:
                R, t = calcular_transformacao_rigida(ancora_est_4, ancora_frame_4)
                stats['4pts'] += 1

            else:
                # --- Tentar 3 âncoras (fallback: C7 + T10 + ref2) ---
                ancora_frame_3 = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn_3])
                usa_3 = all(ponto_valido(p) for p in ancora_frame_3)

                if usa_3:
                    R, t = calcular_transformacao_rigida(ancora_est_3, ancora_frame_3)
                    stats['3pts'] += 1
                else:
                    # Nenhuma combinação disponível
                    stats['skip'] += 1
                    continue

            # Reconstruir marcadores ausentes
            for m in marcadores_alvo:
                if m not in labels_dyn or m not in offsets_local:
                    continue

                idx_m_dyn = labels_dyn.index(m)
                pos_atual = data_dyn[:3, idx_m_dyn, frame]

                if np.any(np.isnan(pos_atual)) or np.all(pos_atual == 0):
                    pos_prevista = R @ offsets_local[m] + t

                    # Busca na nuvem de pontos não rotulados (< 50mm)
                    melhor_idx = None
                    menor_dist = 50.0
                    for idx_un in unlabeled_indices:
                        pos_cand = data_dyn[:3, idx_un, frame]
                        if not ponto_valido(pos_cand):
                            continue
                        dist = np.linalg.norm(pos_cand - pos_prevista)
                        if dist < menor_dist:
                            menor_dist = dist
                            melhor_idx = idx_un

                    if melhor_idx is not None:
                        data_dyn[:3, idx_m_dyn, frame] = data_dyn[:3, melhor_idx, frame]
                    else:
                        data_dyn[:3, idx_m_dyn, frame] = pos_prevista

                    data_dyn[3, idx_m_dyn, frame] = 1.0  # Marcar como válido
                    correcoes[m] += 1

        print(f"\nReconstrução SVD concluída!")
        print(f"   Frames com 4 âncoras (primário):  {stats['4pts']:5d} ({stats['4pts']/num_frames*100:.1f}%)")
        print(f"   Frames com 3 âncoras (fallback):  {stats['3pts']:5d} ({stats['3pts']/num_frames*100:.1f}%)")
        print(f"   Frames ignorados (sem âncoras):   {stats['skip']:5d} ({stats['skip']/num_frames*100:.1f}%)")
        for m in marcadores_alvo:
            if m in correcoes:
                print(f"   - {m}: {correcoes[m]} frames corrigidos.")

        # ── 4. SALVAR ─────────────────────────────────────────────────────────
        dynamic['data']['points'] = data_dyn
        if analogs_backup is not None:
            dynamic['data']['analogs'] = analogs_backup
        
        # O ezc3d mantém um cache de metadados dos pontos lidos (incluindo o status invalid).
        # É obrigatório deletar meta_points para forçar a reconstrução do array de residuais 
        # baseado na nossa modificação (onde 1.0 na 4ª linha significa válido).
        if 'meta_points' in dynamic['data']:
            del dynamic['data']['meta_points']
            
        dynamic.write(output_path)
        print(f"-> Arquivo salvo em: {output_path}")

    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        import traceback; traceback.print_exc()


if __name__ == "__main__":
    reconstruir_teste("Guilherme_extra Cal 01.c3d", "hsw01.c3d", "hsw01_limpo.c3d")
    reconstruir_teste("Guilherme_extra Cal 01.c3d", "hsw02.c3d", "hsw02_limpo.c3d")
