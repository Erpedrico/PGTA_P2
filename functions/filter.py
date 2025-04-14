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
    
    return df[(df['Mode_3A'] == 'N/A') | (df['Mode_3A'].astype(int) != codigo_fijo)].copy()

def eliminar_on_ground(df: pd.DataFrame) -> pd.DataFrame:
    
    #Elimina blancos marcados como 'on ground' (STAT230).
    
    estados_tierra = [
        "No alert, no SPI, aircraft on ground",
        "Alert, no SPI, aircraft on ground"
    ]
    return df[~df['STAT230'].isin(estados_tierra)].copy()


# FILTROS DE ALTITUD (MODE C, FLIGHT LEVEL, QNH)

def filtrar_altitud_maxima(df: pd.DataFrame, max_altitud_ft: float) -> pd.DataFrame:
    
    #Filtra por altitud máxima (Mode C o Flight Level).
    #FL se convierte a ft (FL100 = 10,000 ft).

    condicion = (
        (df['ModeC_corrected'].notna() & (df['ModeC_corrected'] <= max_altitud_ft)) |
        (df['Flight_Level'].notna() & (df['Flight_Level'] * 100 <= max_altitud_ft))
    )
    return df[condicion].copy()

def corregir_qnh(df: pd.DataFrame, qnh_actual: float = 1013.25) -> pd.DataFrame:

    #Corrige la altitud Mode C usando QNH 
    #Fórmula: Altitud_real = Altitud_ModeC + (QNH_actual - 1013.25) * 30
    
    df_corregido = df.copy()
    qnh_estandar = 1013.25
    
    # Aplicar corrección solo si está por debajo de 6000 ft 
    condicion = (df['ModeC_corrected'].notna()) & (df['ModeC_corrected'] <= 6000)
    
    df_corregido.loc[condicion, 'ModeC_corrected'] = (
        df.loc[condicion, 'ModeC_corrected'] + (qnh_actual - qnh_estandar) * 30
    )
    
    return df_corregido


# FILTROS GEOGRÁFICOS (LATITUD, LONGITUD)

def filtrar_por_area(
    df: pd.DataFrame,
    lat_min: float,
    lat_max: float,
    lon_min: float,
    lon_max: float
) -> pd.DataFrame:
    
    #Filtra datos dentro de un área geográfica (lat/lon).
    
    return df[
        df['Latitud'].between(lat_min, lat_max) & 
        df['Longitud'].between(lon_min, lon_max)
    ].copy()

def filtrar_aeropuerto_barcelona(df: pd.DataFrame) -> pd.DataFrame:
    
    #Filtro para el área del Aeropuerto de Barcelona (coordenadas).
    
    return filtrar_por_area(
        df,
        lat_min=41.27964,
        lat_max=41.31008,
        lon_min=2.05789,
        lon_max=2.10870
    )


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
        
        # 2. Corrección QNH (antes de filtrar por altitud)
        if "qnh_correccion" in config:
            df_filtrado = corregir_qnh(df_filtrado, config["qnh_correccion"])
        
        # 3. Filtro de altitud
        if "altitud_maxima_ft" in config:
            df_filtrado = filtrar_altitud_maxima(df_filtrado, config["altitud_maxima_ft"])
        
        # 4. Filtro geográfico
        if config.get("filtrar_por_area", {}).get("activo", False):
            area = config["filtrar_por_area"]
            df_filtrado = filtrar_por_area(
                df_filtrado,
                area["lat_min"],
                area["lat_max"],
                area["lon_min"],
                area["lon_max"]
            )
        
        return df_filtrado
    
    except Exception as e:
        print(f"[ERROR] Al aplicar filtros: {str(e)}")
        return None
