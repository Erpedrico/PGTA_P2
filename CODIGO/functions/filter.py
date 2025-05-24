import pandas as pd
from typing import Dict, Any, Optional


# FILTROS BÁSICOS (BLANCOS PUROS, TRANSPONDER FIJO, ON GROUND)

def eliminar_blancos_puros(df: pd.DataFrame) -> pd.DataFrame:
    
    #Filtramos blanco puro (Mode S o Mode S + PSR)
    
    modos_validos = [
        "Single ModeS All-Call",
        "Single ModeS Roll-Call",
        "ModeS All-Call+PSR",
        "ModeS Roll-Call + PSR"
    ]
    return df[df['TYP020'].isin(modos_validos)].copy()

# Filtrado del DataFrame:
    # 1. df['TYP020'].isin(modos_validos) -> Crea máscara booleana (True para filas válidas)
    # 2. df[mask] -> Filtra filas donde mask es True
    # 3. .copy() -> Crea copia independiente para evitar warnings de Pandas

def eliminar_transponder_fijo(df: pd.DataFrame, codigo_fijo: int = 7777) -> pd.DataFrame:
    
    #Elimina transponders con código fijo (7777).
    
    return df[(df['Mode3ACode'] == 'N/A') | (df['Mode3ACode'].astype(int) != codigo_fijo)].copy()

def eliminar_on_ground(df: pd.DataFrame) -> pd.DataFrame:
    
    #Elimina blancos marcados como 'on ground' (STAT230).
    
    estados_tierra = [
        "No alert, no SPI, aircraft on ground",
        "Alert, no SPI, aircraft on ground"
    ]
    return df[~df['STAT'].isin(estados_tierra)].copy()



# FILTROS GEOGRÁFICOS (LATITUD, LONGITUD)

def filtrar_altitud_maxima(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra hasta una altitud maxima de 6000 ft
    """
    max_altitud_ft = 6000
    try:
        # Convertir a numéricos, manejar errores con coerce
        fl_en_pies = pd.to_numeric(df['FL'], errors='coerce') * 100
        mode_c = pd.to_numeric(df['FL_Corrected'], errors='coerce')
        
        # Filtrar por cualquiera de las dos columnas
        return df[
            (mode_c.notna() & (mode_c <= max_altitud_ft)) |
            (fl_en_pies.notna() & (fl_en_pies <= max_altitud_ft))
        ].copy()
    except Exception as e:
        print(f"[ERROR] Filtro altitud: {str(e)}")
        return df.copy()

def filtrar_aeropuerto_barcelona(df: pd.DataFrame) -> pd.DataFrame:
    """
    Filtra para incluir solo datos del aeropuerto de Barcelona.
    Coordenadas aproximadas del aeropuerto.
    """
    try:
        # Convertir a numéricos si no lo están ya
        lat = pd.to_numeric(df['LAT'], errors='coerce')
        lon = pd.to_numeric(df['LON'], errors='coerce')
        
        # Aplicar filtro geográfico
        mascara = (
            lat.between(41.27963, 41.31009) & 
            lon.between(2.05787, 2.10873)
        )
        
        return df[mascara].copy()
    except Exception as e:
        print(f"[ERROR] Faltan columnas geográficas o error al filtrar: {str(e)}")
        return df.copy()


# FILTROS COMBINADOS

def aplicar_filtros(
    df: pd.DataFrame,
    config: Dict[str, Any]
) -> Optional[pd.DataFrame]:
    try:
        df_filtrado = df.copy()
        
        # 1. Filtros básicos
        if config.get("eliminar_blancos_puros", False):
            df_filtrado = eliminar_blancos_puros(df_filtrado)
        
        if config.get("eliminar_transponder_fijo", False):
            df_filtrado = eliminar_transponder_fijo(df_filtrado)
        
        if config.get("eliminar_on_ground", False):
            df_filtrado = eliminar_on_ground(df_filtrado)

        # 2. Filtros extra 
        if config.get("filtrar_altitud_maxima", False):
            df_filtrado = filtrar_altitud_maxima(df_filtrado)
        
        if config.get("filtrar_aeropuerto", False):
            df_filtrado = filtrar_aeropuerto_barcelona(df_filtrado)
        
        return df_filtrado
    
    except Exception as e:
        print(f"[ERROR] Al aplicar filtros: {str(e)}")
        return None