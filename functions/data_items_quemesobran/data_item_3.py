# Todas las funciones de data item deben devolver un vector de longitud variable. (de momento)
def data_item_3(packet):
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return
    
    
    # Mapeo de Warning/Error Conditions and Target Classification
    code_mapping = {
        0: "Not defined; never used.",
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
        16: "Duplicated or Illegal Mode S Aircraft Address",
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
        33: "Transponder anomaly (MS XPD replies with Mode A/C to Mode A/C-only all-call)",
        34: "Transponder anomaly (SI capability report wrong)",
        35: "Potential IC Conflict",
        36: "IC Conflict detection possible – no conflict currently detected",
    }

    # Lista para almacenar las condiciones de advertencia/error
    warning_conditions = []

    octet_index = 0
    while octet_index < len(packet_bytes):
        current_octet = packet_bytes[octet_index]
        
        # Extraer el código (bits 8-2)
        code = (current_octet >> 1) & 0b1111111 # bits 8-2
        
        # Extraer el bit FX (bit 1)
        FX = current_octet & 0b1 #bit FX

        # Obtener la descripción del código y el mensaje de FX
        code_description = code_mapping.get(code, f"Unknown code: {code}")
        fx_message = "Extension into first extent" if FX else "End of Data Item"

       
        warning_conditions.append(code_description)
        warning_conditions.append(fx_message)

        # NOTA 4: Si el código es 33 o 34, también se debe enviar el código 15 PREGUNTAR
        if code in [33, 34]:
            if 15 not in [c >> 1 for c in packet_bytes]:
                print("Transponder anomaly detected")


        # Verificar si hay extensión al siguiente octeto
        if FX == 0:
            break  # Fin del ítem
        octet_index += 1

    return warning_conditions