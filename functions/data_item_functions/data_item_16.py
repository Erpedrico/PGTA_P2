def data_item_16(packet):
    mensajes = []

    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return

    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
        print(packet_bytes)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return
    
    # Diccionario que mapea los valores a los mensajes correspondientes
    mensajes_map = {
        0: "Not defined; never used",
        1: "Multipath Reply (Reflection)",
        2: "Reply due to sidelobe interrogation/reception",
        3: "Split plot",
        4: "Second time around reply",
        5: "Angel",
        6: "Slow moving target correlated with road infrastructure (terrestrial vehicle)",
        7: "Fixed PSR plot",
        8: "Slow PSR target",
        9: "Low quality PSR plot",
        10: "Phantom SSR plot",
        11: "Non-Matching Mode-3/A Code",
        12: "Mode C code / Mode S altitude code abnormal value compared to the track",
        13: "Target in Clutter Area",
        14: "Maximum Doppler Response in Zero Filter",
        15: "Transponder anomaly detected",
        16: "Duplicated or Illegal Mode S Aircraft Address ",
        17: "Mode S error correction applied",
        18: "Undecodable Mode C code / Mode S altitude code",
        19: "Birds",
        20: "Flock of Birds",
        21: "Mode-1 was present in original reply",
        22: "Mode-2 was present in original reply",
        23: "Plot potentially caused by Wind Turbine",
        24: "Helicopter",
        25: "Maximum number of re-interrogations reached (surveillance information)",
        26: "Maximum number of re-interrogations reached (BDS Extractions)",
        27: "BDS Overlay Incoherence",
        28: "Potential BDS Swap Detected",
        29: "Track Update in the Zenithal Gap",
        30: "Mode S Track re-acquired",
        31: "Duplicated Mode 5 Pair NO/PIN detected",
        32: "Wrong DF reply format detected",
        33: "Transponder anomaly (MS XPD replies with Mode A/C to Mode A/Conly all-call)",
        34: "Transponder anomaly (SI capability report wrong)",
        35: "Potential IC Conflict",
        36: "IC Conflict detection possible, no conflict currently detected"
    }

    for byte in packet_bytes:
        # Extraemos los 7 bits más significativos (desplazamos 1 bit a la derecha)
        primeros_7_bits = byte >> 1
        
        # Si el valor está en el rango de 0 a 36, obtenemos el mensaje
        if 0 <= primeros_7_bits <= 36:
            # Si el valor está en el diccionario, usamos el mensaje mapeado
            mensaje = mensajes_map.get(primeros_7_bits, f"Mensaje para el valor {primeros_7_bits}")
            mensajes.append(mensaje)
        else:
            mensajes.append(f"Valor fuera de rango: {primeros_7_bits}")
    
    return mensajes
