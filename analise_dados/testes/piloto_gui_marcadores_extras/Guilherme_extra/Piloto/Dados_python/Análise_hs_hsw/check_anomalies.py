import ezc3d
import numpy as np
import glob

def check_file(c3d_file):
    print(f"=== Analisando {c3d_file} ===")
    try:
        c = ezc3d.c3d(c3d_file)
    except Exception as e:
        print(f"Erro ao abrir {c3d_file}: {e}")
        return
        
    labels = [l.strip() for l in c['parameters']['POINT']['LABELS']['value']]
    points = c['data']['points']
    num_frames = points.shape[2]
    
    threshold_salto = 80.0  # mm entre frames consecutivos
    
    anomalias_encontradas = []
    
    for idx, marker in enumerate(labels):
        if marker.startswith('*') or marker.lower().startswith('unlabeled'):
            continue
            
        z = points[2, idx, :]
        
        validos = ~np.isnan(z) & (z != 0)
        num_invalidos = num_frames - np.sum(validos)
        
        z_validos = z[validos]
        saltos = 0
        if len(z_validos) > 1:
            diffs = np.abs(np.diff(z_validos))
            saltos = np.sum(diffs > threshold_salto)
            
        if num_invalidos > 0 or saltos > 0:
            pct_invalido = (num_invalidos / num_frames) * 100
            anomalias_encontradas.append({
                'marker': marker,
                'invalidos': num_invalidos,
                'pct': pct_invalido,
                'saltos': saltos
            })
            
    anomalias_encontradas.sort(key=lambda x: x['invalidos'], reverse=True)
    
    for a in anomalias_encontradas:
        print(f"Marcador: {a['marker']:<15} | Gaps: {a['invalidos']:>4} ({a['pct']:>4.1f}%) | Saltos > {threshold_salto}mm: {a['saltos']}")
        
    if not anomalias_encontradas:
        print("Nenhuma anomalia encontrada!")
    print("")

if __name__ == "__main__":
    arquivos = sorted(glob.glob("*_limpo.c3d"))
    for arq in arquivos:
        check_file(arq)
