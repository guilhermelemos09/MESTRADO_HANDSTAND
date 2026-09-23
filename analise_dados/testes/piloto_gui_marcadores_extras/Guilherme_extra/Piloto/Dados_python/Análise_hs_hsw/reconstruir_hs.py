"""
Reconstrução Robusta de Marcadores - Handstand Estático (HS)
============================================================
Utiliza transformação rígida por SVD (Singular Value Decomposition) para
rastrear a orientação real do segmento torácico frame a frame, corrigindo
o problema do offset translacional simples (que ignora a rotação do corpo).

Método: Kabsch Algorithm / Procrustes via SVD
Referência: KABSCH, W. A solution for the best rotation to relate two sets
of vectors. Acta Crystallographica Section A, v. 32, n. 5, p. 922-923, 1976.
"""
import numpy as np
import ezc3d


def calcular_transformacao_rigida(pontos_ref, pontos_mov):
    """
    Calcula a matriz de rotação R e vetor de translação t que melhor
    alinha pontos_mov -> pontos_ref usando o Algoritmo de Kabsch (SVD).
    
    Args:
        pontos_ref: array (N, 3) - pontos de referência (estático)
        pontos_mov: array (N, 3) - pontos móveis (frame dinâmico)
    Returns:
        R (3x3), t (3,)
    """
    centroid_ref = np.mean(pontos_ref, axis=0)
    centroid_mov = np.mean(pontos_mov, axis=0)
    
    A = pontos_ref - centroid_ref
    B = pontos_mov - centroid_mov
    
    H = A.T @ B
    U, S, Vt = np.linalg.svd(H)
    
    # Garantir rotação direita (sem reflexão)
    d = np.linalg.det(Vt.T @ U.T)
    D = np.diag([1, 1, d])
    R = Vt.T @ D @ U.T
    t = centroid_mov - R @ centroid_ref
    
    return R, t


def pontos_validos(dados, indices):
    """Verifica se todos os pontos nos índices são válidos (sem NaN e sem zero absoluto)."""
    for idx in indices:
        p = dados[:3, idx]
        if np.any(np.isnan(p)) or np.all(p == 0):
            return False
    return True


def reconstruir_teste(c3d_static_path, c3d_dynamic_path, output_path):
    print(f"\n--- Iniciando reconstrução (SVD) para: {c3d_dynamic_path} ---")
    
    try:
        # ── 1. CARREGAR ESTÁTICO (CALIBRAÇÃO) ───────────────────────────────
        static = ezc3d.c3d(c3d_static_path)
        labels_static = [l.strip() for l in static['parameters']['POINT']['LABELS']['value']]
        data_static = static['data']['points']
        
        # Marcadores âncora do bloco torácico (para calcular rotação)
        ancora_nomes = ['C7', 'T10', 'referencia1', 'referencia2']
        ancora_idx_static = []
        for nome in ancora_nomes:
            if nome in labels_static:
                ancora_idx_static.append(labels_static.index(nome))
            else:
                raise ValueError(f"Marcador âncora '{nome}' não encontrado no estático!")
        
        # Posições âncora no frame 0 do estático (Nx3)
        ancora_estatico = np.array([data_static[:3, i, 0] for i in ancora_idx_static])
        
        # Marcadores alvo a reconstruir
        marcadores_alvo = ['LSHO', 'RSHO']
        offsets_local = {}  # Posição de cada alvo no sistema local do estático
        
        for m in marcadores_alvo:
            if m in labels_static:
                idx_m = labels_static.index(m)
                pos_m = data_static[:3, idx_m, 0]
                # Offset = posição do alvo no sistema de coordenadas LOCAL do frame 0
                offsets_local[m] = pos_m.copy()
                print(f"-> Vetor de calibração SVD para '{m}' mapeado.")
            else:
                print(f"   Alerta: '{m}' não encontrado no arquivo estático - será ignorado.")

        # ── 2. CARREGAR DINÂMICO ─────────────────────────────────────────────
        dynamic = ezc3d.c3d(c3d_dynamic_path)
        labels_dyn = [l.strip() for l in dynamic['parameters']['POINT']['LABELS']['value']]
        data_dyn = dynamic['data']['points']
        num_frames = data_dyn.shape[2]
        
        # Backup analógico
        analogs_backup = dynamic['data']['analogs'].copy() if 'analogs' in dynamic['data'] else None
        
        # Índices das âncoras no dinâmico
        ancora_idx_dyn = []
        for nome in ancora_nomes:
            if nome in labels_dyn:
                ancora_idx_dyn.append(labels_dyn.index(nome))
            else:
                raise ValueError(f"Marcador âncora '{nome}' ausente no arquivo dinâmico!")
        
        # Trajetórias unlabeled para busca na nuvem
        unlabeled_indices = [i for i, label in enumerate(labels_dyn)
                             if '*' in label or label.lower().startswith('unlabeled')]
        
        # ── 3. RECONSTRUÇÃO FRAME A FRAME ────────────────────────────────────
        correcoes = {m: 0 for m in marcadores_alvo}
        skips_ancora = 0
        
        for frame in range(num_frames):
            # Verificar se TODAS as âncoras estão válidas neste frame
            ancora_frame = np.array([data_dyn[:3, i, frame] for i in ancora_idx_dyn])
            
            if not all(not np.any(np.isnan(p)) and not np.all(p == 0) for p in ancora_frame):
                skips_ancora += 1
                continue
            
            # Calcular transformação rígida: estático → frame atual (SVD)
            R, t = calcular_transformacao_rigida(ancora_estatico, ancora_frame)
            
            # Tentar reconstruir cada marcador alvo
            for m in marcadores_alvo:
                if m not in labels_dyn or m not in offsets_local:
                    continue
                
                idx_m_dyn = labels_dyn.index(m)
                pos_atual = data_dyn[:3, idx_m_dyn, frame]
                
                # Só reconstruir se estiver ausente
                if np.any(np.isnan(pos_atual)) or np.all(pos_atual == 0):
                    # Posição prevista = transformação rígida do offset calibrado
                    pos_prevista = R @ offsets_local[m] + t
                    
                    # Buscar candidato na nuvem de pontos não rotulados (< 50mm)
                    melhor_idx = None
                    menor_dist = 50.0  # threshold em mm
                    for idx_un in unlabeled_indices:
                        pos_cand = data_dyn[:3, idx_un, frame]
                        if np.any(np.isnan(pos_cand)) or np.all(pos_cand == 0):
                            continue
                        dist = np.linalg.norm(pos_cand - pos_prevista)
                        if dist < menor_dist:
                            menor_dist = dist
                            melhor_idx = idx_un
                    
                    if melhor_idx is not None:
                        # Achou na nuvem: usar posição real da câmera
                        data_dyn[:3, idx_m_dyn, frame] = data_dyn[:3, melhor_idx, frame]
                    else:
                        # Gap fill matemático com posição prevista pelo SVD
                        data_dyn[:3, idx_m_dyn, frame] = pos_prevista
                    
                    data_dyn[3, idx_m_dyn, frame] = 1.0  # Marcar como válido
                    correcoes[m] += 1
        
        print(f"\nReconstrução SVD concluída!")
        print(f"   Frames ignorados (âncoras ausentes): {skips_ancora}/{num_frames} "
              f"({skips_ancora/num_frames*100:.1f}%)")
        for m in marcadores_alvo:
            print(f"   - {m}: {correcoes[m]} frames corrigidos.")
        
        # ── 4. SALVAR ─────────────────────────────────────────────────────────
        dynamic['data']['points'] = data_dyn
        if analogs_backup is not None:
            dynamic['data']['analogs'] = analogs_backup
            
        if 'meta_points' in dynamic['data']:
            del dynamic['data']['meta_points']
            
        dynamic.write(output_path)
        print(f"-> Arquivo salvo em: {output_path}")
        
    except FileNotFoundError:
        print(f"Erro: Arquivo não encontrado. Verifique os nomes dos arquivos.")
    except Exception as e:
        print(f"Erro inesperado: {e}")
        import traceback; traceback.print_exc()


if __name__ == "__main__":
    reconstruir_teste("cal.c3d", "hs01.c3d", "hs01_limpo.c3d")
    reconstruir_teste("cal.c3d", "hs02.c3d", "hs02_limpo.c3d")