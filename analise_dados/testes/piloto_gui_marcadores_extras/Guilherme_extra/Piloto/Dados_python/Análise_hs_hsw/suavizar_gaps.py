import ezc3d
import numpy as np
import pandas as pd
import glob

def aplicar_suavizacao(c3d_file):
    print(f"Suavizando {c3d_file}...")
    try:
        c = ezc3d.c3d(c3d_file)
    except Exception as e:
        print(f"Erro ao abrir {c3d_file}: {e}")
        return
        
    points = c['data']['points']
    labels = [l.strip() for l in c['parameters']['POINT']['LABELS']['value']]
    num_frames = points.shape[2]
    
    for idx, marker in enumerate(labels):
        if marker.startswith('*') or marker.lower().startswith('unlabeled'):
            continue
            
        # Buracos (NaNs ou Zeros)
        is_gap = np.isnan(points[0, idx, :]) | (np.all(points[:3, idx, :] == 0, axis=0))
        
        # Filtro de picos (Spike removal): compara com a mediana móvel
        z_serie = pd.Series(np.where(is_gap, np.nan, points[2, idx, :]))
        rolling_med = z_serie.rolling(window=7, center=True, min_periods=1).median()
        # Se divergir mais de 60mm da mediana móvel, é considerado um pico artificial (ruído)
        spike_mask = np.abs(z_serie - rolling_med) > 60.0
        
        is_gap = is_gap | spike_mask.values
        
        if np.all(is_gap):
            continue
            
        if np.any(is_gap):
            for coord in range(3):
                serie = points[coord, idx, :].copy()
                serie[is_gap] = np.nan
                s = pd.Series(serie)
                # Interpola linearmente os buracos e picos removidos
                s_interp = s.interpolate(method='linear', limit_direction='both')
                points[coord, idx, :] = s_interp.values
                
            points[3, idx, is_gap] = 1.0
            
    c['data']['points'] = points
    if 'meta_points' in c['data']:
        del c['data']['meta_points']
        
    c.write(c3d_file)
    print(f"-> Salvo com sucesso.")

if __name__ == "__main__":
    for f in sorted(glob.glob("*_limpo.c3d")):
        aplicar_suavizacao(f)
