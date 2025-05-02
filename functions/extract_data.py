from functions.data_item_functions.data_item_1Corrected import data_item_1
from functions.data_item_functions.data_item_2Corrected import data_item_2
from functions.data_item_functions.data_item_3Corrected import data_item_3
from functions.data_item_functions.data_item_4Corrected import data_item_4
from functions.data_item_functions.data_item_5Corrected import data_item_5
from functions.data_item_functions.data_item_6Corrected import data_item_6
from functions.data_item_functions.data_item_7 import data_item_7
from functions.data_item_functions.data_item_8Corrected import data_item_8
from functions.data_item_functions.data_item_9Corrected import data_item_9
from functions.data_item_functions.data_item_10 import data_item_10
from functions.data_item_functions.data_item_11Corrected import data_item_11
from functions.data_item_functions.data_item_12Corrected import data_item_12
from functions.data_item_functions.data_item_13Corrected import data_item_13
from functions.data_item_functions.data_item_14Corrected import data_item_14
from functions.data_item_functions.data_item_15 import data_item_15
from functions.data_item_functions.data_item_16 import data_item_16
from functions.data_item_functions.data_item_17 import data_item_17
from functions.data_item_functions.data_item_19 import data_item_19
from functions.data_item_functions.data_item_21 import data_item_21
from functions.data_item_functions.data_item_22 import data_item_22
from functions.data_item_functions.data_item_23 import data_item_23
from functions.data_item_functions.data_item_24 import data_item_24
from functions.data_item_functions.data_item_25 import data_item_25
from functions.data_item_functions.data_item_26 import data_item_26
from functions.data_item_functions.data_item_28 import data_item_28

from functools import partial

from math import sin, cos, radians, degrees

DEBUG=True 

# Coordenadas del radar (convertidas de grados, minutos, segundos a grados decimales)
RADAR_LAT = 41.30070233
RADAR_LON = 2.1020582

ALTITUD_RADAR = 27.257  # metros

# Radio terrestre en metros
R = 6371000.0

def convertir_rho_theta_a_latlon(rho_nm, theta_deg):
    """
    Convierte coordenadas polares (RHO en NM, THETA en grados)
    a coordenadas geográficas (latitud, longitud), tomando como origen el radar.
    """
    # Convertimos RHO a metros
    rho_metros = rho_nm * 1852

    # Convertimos THETA a radianes (ángulo desde el norte, en sentido horario)
    theta_rad = radians(theta_deg)

    # Descomposición en desplazamiento en el plano (dx hacia el este, dy hacia el norte)
    dx = rho_metros * sin(theta_rad)
    dy = rho_metros * cos(theta_rad)

    # Aproximaciones locales para delta lat/lon (válidas para distancias pequeñas)
    delta_lat = dy / R
    delta_lon = dx / (R * cos(radians(RADAR_LAT)))

    # Coordenadas finales
    lat = RADAR_LAT + degrees(delta_lat)
    lon = RADAR_LON + degrees(delta_lon)

    return lat, lon

def calcular_altitud(rho_nm, phi_deg, alt_radar_m=27.257):
    """
    Calcula altitud del blanco si tienes RHO (en NM) y ángulo de elevación (en grados).
    alt_radar_m es la altitud de la antena (elevación + mástil)
    """
    rho_m = rho_nm * 1852
    phi_rad = radians(phi_deg)
    altitud_objetivo = sin(phi_rad) * rho_m + alt_radar_m
    return altitud_objetivo

# Constante global
CAMPOS_DEFAULT = dict.fromkeys([
    "NUM", "SAC", "SIC", "TIME", "TIME(s)", "Target report description", "Validated",
    "Garbled", "CodeSource", "Validated_FL", "Garbled_FL", "FL", "Mode3ACode", "Address",
    "ID", "BDS", "TRACK NUMBER", "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING", "LAT",
    "LON", "H", "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A", "B1B", "RHO", "THETA",
    #DATA ITEM 250
        "MCP_STATUS", "MCP_ALT", "FMS_STATUS", "FMS_ALT", "BP_STATUS", "BP_VALUE",
        "MODE_STATUS", "VNAV", "ALTHOLD", "APP", "TARGETALT_STATUS", "TARGETALT_SOURCE",
        "ROLL_STATUS", "ROLL_ANGLE", "TRACK_STATUS", "TRUE_TRACK", "GROUNDSPEED_STATUS", 
        "GROUNDSPEED", "TRACKRATE_STATUS", "TRACK_RATE", "AIRSPEED_STATUS", "TRUE_AIRSPEED",
        "HEADING_STATUS", "MAG_HEADING", "IAS_STATUS", "IAS", "MACH_STATUS", "MACH",
        "BARO_RATE_STATUS", "BARO_RATE", "INERTIAL_VERT_STATUS", "INERTIAL_VERT_VEL"
], "Not Found")

# Evitar prints en loops críticos, opcional con log level si se requiere
DEBUG = True

def extraer_datos(datos_hex):
    campos = CAMPOS_DEFAULT.copy()

    try:
        cleaned_hex = limpiar_hex(datos_hex)
        packet_bytes = bytes.fromhex(cleaned_hex)
        if len(packet_bytes) < 4:
            return campos

        packet_bytes = packet_bytes[3:]

        fspec_bytes, packet_bytes = leer_fspec(packet_bytes)
        data_items = obtener_data_items(fspec_bytes)
        handlers = HANDLER_MAP  # Global, no se recrea cada vez

        for item in data_items:
            handler = handlers.get(item)
            if handler is not None:
                packet_bytes = handler(packet_bytes, campos)

        # Calcular LAT y LON a partir de RHO y THETA
        rho_str = campos.get("RHO", None)
        theta_str = campos.get("THETA", None)

        if rho_str is not None and theta_str is not None:
            try:
                rho = float(rho_str)
                theta = float(theta_str)

                lat, lon = convertir_rho_theta_a_latlon(rho, theta)
                campos["LAT"] = lat
                campos["LON"] = lon
            except Exception as e:
                print(f"Error al convertir RHO y THETA: {e}")
                campos["LAT"] = "Error"
                campos["LON"] = "Error"

        # Calcular H directamente desde FL
        fl = campos.get("FL", None)
        if fl is not None:
            try:
                fl_val = float(fl)
                campos["H"] = round(fl_val * 100 * 0.3048, 2)
            except Exception as e:
                print(f"Error al calcular altitud desde FL: {e}")
                campos["H"] = "Error"

    except Exception as e:
        print(f"Error en el procesamiento de datos hexadecimales: {e}")

    return campos






# Ejemplo de cómo llamar la función:
# datos_hex = '...'  # Aquí iría la cadena hexadecimal del paquete
# campos_extraidos = extraer_datos(datos_hex)

# Función auxiliar para los data items simples
def asignar_campos(func, longitud, nombres_campos, packet_bytes, campos):
    data_item_bytes = packet_bytes[:longitud].hex()
    resultado = func(data_item_bytes)
    if not isinstance(resultado, (list, tuple)):
        resultado = [resultado]
    for nombre, valor in zip(nombres_campos, resultado):
        campos[nombre] = str(valor)
    return packet_bytes[longitud:]

def make_simple_handler(func, longitud, campos_nombres):
    return partial(asignar_campos, func, longitud, campos_nombres)

def handler_item_variable(data_func, nombre, packet_bytes, campos):
    octets_to_read = 1
    while packet_bytes[octets_to_read - 1] & 1:
        octets_to_read += 1
    resultado = data_func(packet_bytes[:octets_to_read].hex())
    campos[nombre] = str(resultado)
    return packet_bytes[octets_to_read:]

def handler_item_3(pb, campos):
    return handler_item_variable(data_item_3, "Target report description", pb, campos)

def handler_item_14(pb, campos):
    return handler_item_variable(data_item_14, "TRACK STATUS", pb, campos)

def handler_item_7(pb, campos):
    if len(pb) < 1:
        print("Error: no hay datos suficientes para leer item 7")
        return pb

    first_octet = pb[0]
    octets_to_read = 1

    # Leer FSPEC octets
    while first_octet & 1:
        if octets_to_read >= len(pb):
            print("Error: FSPEC incompleto en item 7")
            return pb
        first_octet = pb[octets_to_read]
        octets_to_read += 1

    bits_to_check = pb[:octets_to_read]

    data_items_d7 = []
    item_counter = 1

    for octet in bits_to_check:
        for bit_index in range(7, -1, -1):
            if bit_index == 0:
                continue  # Skip LSB (extension bit)
            bit = (octet >> bit_index) & 1
            if bit == 1:
                data_items_d7.append(item_counter)
            item_counter += 1

    longitud_d7 = len(data_items_d7)

    total_length = octets_to_read + longitud_d7
    if len(pb) < total_length:
        print(f"Error: Se esperaban {total_length} bytes, pero hay {len(pb)}")
        return pb

    hex_str = pb[:total_length].hex()
    campos["TARGET IDENTIFICATION"] = data_item_7(hex_str)

    return pb[total_length:]


def handler_item_10(packet_bytes, campos):
    if len(packet_bytes) < 1:
        return packet_bytes  # No hay suficiente para leer REP

    rep = packet_bytes[0]
    total_length = 1 + rep * 8

    if len(packet_bytes) < total_length:
        return packet_bytes  # No hay suficientes datos

    hex_str = packet_bytes[:total_length].hex()
    packet_bytes = packet_bytes[total_length:]

    bds_data = data_item_10(hex_str)

    if len(bds_data) >= 33:
        campos.update({
            "BDS_REP": bds_data[0],
            # BDS 4,0
            "MCP_STATUS": bds_data[1],
            "MCP_ALT": bds_data[2],
            "FMS_STATUS": bds_data[3],
            "FMS_ALT": bds_data[4],
            "BP_STATUS": bds_data[5],
            "BP_VALUE": bds_data[6],
            "MODE_STATUS": bds_data[7],
            "VNAV": bds_data[8],
            "ALTHOLD": bds_data[9],
            "APP": bds_data[10],
            "TARGETALT_STATUS": bds_data[11],
            "TARGETALT_SOURCE": bds_data[12],
            # BDS 5,0
            "ROLL_STATUS": bds_data[13],
            "ROLL_ANGLE": bds_data[14],
            "TRACK_STATUS": bds_data[15],
            "TRUE_TRACK": bds_data[16],
            "GROUNDSPEED_STATUS": bds_data[17],
            "GROUNDSPEED": bds_data[18],
            "TRACKRATE_STATUS": bds_data[19],
            "TRACK_RATE": bds_data[20],
            "AIRSPEED_STATUS": bds_data[21],
            "TRUE_AIRSPEED": bds_data[22],
            # BDS 6,0
            "HEADING_STATUS": bds_data[23],
            "MAG_HEADING": bds_data[24],
            "IAS_STATUS": bds_data[25],
            "IAS": bds_data[26],
            "MACH_STATUS": bds_data[27],
            "MACH": bds_data[28],
            "BARO_RATE_STATUS": bds_data[29],
            "BARO_RATE": bds_data[30],
            "INERTIAL_VERT_STATUS": bds_data[31],
            "INERTIAL_VERT_VEL": bds_data[32]
        })

    return packet_bytes

# Items que solo consumen bytes pero no se procesan aún
def skip_bytes(packet_bytes, n, campos):
    return packet_bytes[n:]

def limpiar_hex(hex_string):
    hex_chars = set("0123456789abcdefABCDEF")
    cleaned = ''.join(c for c in hex_string if c in hex_chars)
    if len(cleaned) % 2 != 0:
        raise ValueError("Longitud impar en el string hexadecimal.")
    return cleaned

def leer_fspec(packet_bytes):
    fspec_end = 0
    for i, byte in enumerate(packet_bytes):
        fspec_end += 1
        if (byte & 0x01) == 0:
            break
    return packet_bytes[:fspec_end], packet_bytes[fspec_end:]

def obtener_data_items(fspec_bytes):
    items = []
    counter = 1
    for b in fspec_bytes:
        for bit in range(7, 0, -1):
            if b & (1 << bit):
                items.append(counter)
            counter += 1
    return items

HANDLER_MAP = {
    1: make_simple_handler(data_item_1, 2, ["SAC", "SIC"]),
    2: make_simple_handler(data_item_2, 3, ["TIME"]),
    3: handler_item_3,
    4: make_simple_handler(data_item_4, 4, ["RHO", "THETA"]),
    5: make_simple_handler(data_item_5, 2, ["Validated", "Garbled", "CodeSource", "Mode3ACode"]),
    6: make_simple_handler(data_item_6, 2, ["Validated_FL", "Garbled_FL", "FL"]),
    7: handler_item_7,
    8: make_simple_handler(data_item_8, 3, ["Address"]),
    9: make_simple_handler(data_item_9, 6, ["ID"]),
    10: handler_item_10,
    11: make_simple_handler(data_item_11, 2, ["TRACK NUMBER"]),
    12: make_simple_handler(data_item_12, 4, ["X", "Y"]),
    13: make_simple_handler(data_item_13, 4, ["GS", "GS_KT", "HEADING"]),
    14: handler_item_14,
    15: lambda pb, c: pb[4:],
    16: handler_item_14,
    17: lambda pb, c: pb[2:],
    18: lambda pb, c: pb[4:],
    19: make_simple_handler(data_item_19, 2, ["H"]),
    20: handler_item_14,
    21: make_simple_handler(data_item_21, 2, ["COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A", "B1B"]),
    22: lambda pb, c: pb[7:],
    23: lambda pb, c: pb[1:],
    24: lambda pb, c: pb[2:],
    25: lambda pb, c: pb[1:],
    26: lambda pb, c: pb[2:]
}
