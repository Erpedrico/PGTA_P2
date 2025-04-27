import numpy as np
from datetime import datetime
from typing import Dict, Any, Optional, Tuple
from functions.GeoUtils import GeoUtils, CoordinatesWGS84, CoordinatesXYZ
from functions.GeneralMatrix_v2 import GeneralMatrix
from functions.extract_data import extraer_datos
import folium
import webbrowser
import os

# ---------------------------------------------------------------
# CONFIGURACIÓN GLOBAL
# ---------------------------------------------------------------
geo_utils = GeoUtils()  # Instancia para conversiones geodésicas
aircraft_data: Dict[str, Dict[str, Any]] = {}  # Estructura principal para almacenar todos los datos de aviones
# ---------------------------------------------------------------

def process_aircraft_packet(hex_data: str) -> Tuple[str, Dict[str, Any], Optional[GeneralMatrix]]:
    """
    Procesa un paquete ASTERIX completo:
    1. Decodifica los datos delpaquet pasado
    2. Genera ID único del avión
    3. Actualiza el historial de tracking
    4. Calcula la matriz de trayectoria
    """
    
    # DECODIFICACIÓN
    packet_data = decode_packet_data(hex_data)  # Extrae campos básicos
    
    # Gestión de timestamps
    if 'TIME' not in packet_data or packet_data['TIME'] == "Not Found":
        packet_data['timestamp'] = datetime.now()  # Usa hora actual si no hay timestamp
    else:
        try:
            # Parsea el formato HH:MM:SS.mmm
            packet_data['timestamp'] = datetime.strptime(packet_data['TIME'], "%H:%M:%S.%f")
        except ValueError:
            packet_data['timestamp'] = datetime.now()  

    # IDENTIFICACIÓN
    aircraft_id = generate_aircraft_id(packet_data)  # Crea ID único
    
    # POSICION ACTUAL Y ACTUALIZACIÓN DE DATOS
    #En construcción
    
    # GENERACIÓN DE TRAYECTORIA
    trajectory = create_trajectory_matrix(aircraft_id)
    
    return aircraft_id, packet_data, trajectory

def decode_packet_data(hex_data: str) -> Dict[str, Any]:
    
    #Decodifica el paquete  y convierte coordenadas geodésicas a cartesianas.
    
    raw_data = extraer_datos(hex_data)  

    # CONVERSIÓN COORDENADAS (si están disponibles)
    if raw_data["LAT"] != "Not Found" and raw_data["LON"] != "Not Found":
        lat = float(raw_data["LAT"])
        lon = float(raw_data["LON"])
        alt = float(raw_data["H"]) if raw_data["H"] != "Not Found" else 0.0
        
        # Conversión a coordenadas cartesianas ECEF (Earth-Centered, Earth-Fixed)
        coord_wgs = CoordinatesWGS84(np.radians(lat), np.radians(lon), alt)
        coord_xyz = geo_utils.change_geodesic_to_geocentric(coord_wgs)
        
        # Añade las nuevas coordenadas al registro
        raw_data.update({
            "X": coord_xyz.X,  # Coordenada xX (metros)
            "Y": coord_xyz.Y,  # Coordenada Y (metros)
            "Z": coord_xyz.Z   # Coordenada Z (metros)
        })
    
    return raw_data

def generate_aircraft_id(packet_data: Dict[str, Any]) -> str:
    
    #Genera un ID único combinando Mode3A y dirección ICAO.
    
    return f"{packet_data.get('Mode3ACode', 'UNKNOWN')}_{packet_data.get('Address', 'XXXXXX')}"



def create_trajectory_matrix(aircraft_id: str) -> Optional[GeneralMatrix]:
#Crea una matriz GeneralMatrix con la trayectoria de la aeronave
    if aircraft_id not in aircraft_data:
        return None
    
    coords = aircraft_data[aircraft_id]['track']['cartesian_coords']
    if coords.size == 0:
        return None
    
    return GeneralMatrix(coords)

#EN CONTRUCCION
"""
def get_aircraft_position(aircraft_id: str, timestamp: datetime = None) -> Optional[Dict[str, Any]]:
    
    #Obtiene la posición de un avión en un momento específico.
    
    # Validaciones iniciales
    if aircraft_id not in aircraft_data:
        return None
    
    data = aircraft_data[aircraft_id]
    if data['track']['timestamps'].size == 0:
        return None
    
    # Lógica de búsqueda
    if timestamp is None:
        idx = -1  # Última posición
    else:
        # Encuentra el índice más cercano al timestamp solicitado
        np_time = np.datetime64(timestamp)
        time_diffs = np.abs(data['track']['timestamps'] - np_time)
        idx = np.argmin(time_diffs)
    
    # Construye el resultado
    return {
        'timestamp': data['track']['timestamps'][idx],
        'latitude': data['track']['geo_coords'][idx][0],
        'longitude': data['track']['geo_coords'][idx][1],
        'altitude': data['track']['geo_coords'][idx][2],
        'x': data['track']['cartesian_coords'][idx][0],
        'y': data['track']['cartesian_coords'][idx][1],
        'z': data['track']['cartesian_coords'][idx][2],
        'speed': data['movement']['speed'][idx] if data['movement']['speed'].size > idx else None,
        'heading': data['movement']['heading'][idx] if data['movement']['heading'].size > idx else None
    }

"""



