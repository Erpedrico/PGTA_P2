import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from functions.GeoUtils import GeoUtils, CoordinatesWGS84, CoordinatesXYZ
from functions.GeneralMatrix_v2 import GeneralMatrix
from functions.extract_data import extraer_datos
import folium
import webbrowser
import os
import pandas as pd


def process_dataframe_to_trajectories(df: pd.DataFrame) -> Dict[str, GeneralMatrix]:
    """
    Procesa un DataFrame y devuelve trayectorias que se actualizan
    
    """
    global geo_utils, aircraft_data
    
    trajectories = {}
    
    for _, row in df.iterrows():
        
        try:
            # Construir packet_data desde el DataFrame usado 
            packet_data = {
                'LAT': safe_float(row, 'LAT'),
                'LON': safe_float(row, 'LON'),
                'H': safe_float(row, 'H', default=0.0),
                'Mode3ACode': row.get('Mode3ACode', 'UNKNOWN'),
                'Address': row.get('Address', 'XXXXXX'),
                'GS_KT': safe_float(row, 'GS_KT'),
                'HEADING': safe_float(row, 'HEADING'),
                'timestamp': row.get('TIMESTAMP', datetime.now()),
                'SAC': row.get('SAC', 'N/A'),
                'SIC': row.get('SIC', 'N/A')
            }

            #Conversión de coordenadas geodeasianas a cartesianas
            if packet_data["LAT"] != "Not Found" and packet_data["LON"] != "Not Found":
                coord_wgs = CoordinatesWGS84(
                    np.radians(packet_data["LAT"]),
                    np.radians(packet_data["LON"]),
                    packet_data["H"]
                )
                coord_xyz = geo_utils.change_geodesic_to_geocentric(coord_wgs)
                packet_data.update({
                    "X": coord_xyz.X,
                    "Y": coord_xyz.Y,
                    "Z": coord_xyz.Z
                })

            # Generar ID y actualizar aircraft_data
            aircraft_id = generate_aircraft_id(packet_data)
            
            if aircraft_id not in aircraft_data:
                aircraft_data[aircraft_id] = {
                    'metadata': {
                        'mode_3a': packet_data['Mode3ACode'],
                        'address': packet_data['Address'],
                        'callsign': packet_data.get('ID')
                    },
                    'track': {
                        'timestamps': np.array([], dtype='datetime64[ms]'),
                        'geo_coords': np.empty((0, 3), dtype=float),
                        'cartesian_coords': np.empty((0, 3), dtype=float)
                    },
                    'movement': {
                        'speed': np.array([], dtype=float),
                        'heading': np.array([], dtype=float)
                    }
                }

                #Actualizar posición en construccion

        except Exception as e:
            print(f"Error procesando fila {_}: {str(e)}")
            continue
        
    return trajectories

#No se si esta bien

def generate_aircraft_id(packet_data: Dict[str, Any]) -> str:
    """
    Genera un ID único para el avión combinando Mode3A y dirección ICAO
    
    """
    # Extraer valores con valores por defecto seguros
    mode_3a = str(packet_data.get('Mode3ACode', 'UNKNOWN')).strip()
    address = str(packet_data.get('Address', 'XXXXXX')).strip()
    
    # Limpiar valores inválidos
    mode_3a = mode_3a if mode_3a not in ['', 'Not Found'] else 'UNKNOWN'
    address = address if address not in ['', 'Not Found'] else 'XXXXXX'
    
    return f"{mode_3a}_{address}"

def safe_float(value: Any, default: float = 0.0) -> float:
    """
    Convierte un valor a float de forma segura
    """
    if isinstance(value, (int, float)):
        return float(value)
    if isinstance(value, str):
        value = value.strip()
        if value in ['', 'Not Found', 'N/A']:
            return default
        try:
            return float(value)
        except ValueError:
            return default
    return default