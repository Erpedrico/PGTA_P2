def data_item_21(packet):
    messages = []  # Cambié "mensages" por "messages" para la ortografía correcta

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
    COM_map = {
        0: "No communications capability (surveillance only)",
        1: "Comm. A and Comm. B capability",
        2: "Comm. A, Comm. B and Uplink ELM",
        3: "Comm. A, Comm. B, Uplink ELM and Downlink ELM",
        4: "Level 5 Transponder capability",
        5: "Not assigned",
        6: "Not assigned",
        7: "Not assigned"
    }

    STAT_map = {
        0: "No alert, no SPI, aircraft airborne",
        1: "No alert, no SPI, aircraft on ground",
        2: "Alert, no SPI, aircraft airborne",
        3: "Alert, no SPI, aircraft on ground",
        4: "Alert, SPI, aircraft airborne or on ground",
        5: "No alert, SPI, aircraft airborne or on ground",
        6: "Not assigned",
        7: "Unknown"
    }

    # Desplazamientos de bits para extraer valores
    COM = packet_bytes[0] >> 5
    STAT = packet_bytes[0] >> 2 & 0x7
    SI = packet_bytes[0] >> 1 & 1  # Corregido: operador de desplazamiento
    MSSC = packet_bytes[1] >> 7 & 1
    ARC = packet_bytes[1] >> 6 & 1
    AIC = packet_bytes[1] >> 5 & 1
    B1A = packet_bytes[1] >> 4 & 1
    B1B = packet_bytes[1] & 0xf  # Mascarilla para los 4 bits menos significativos

    # Obtención de los mensajes correspondientes
    COM_message = COM_map.get(COM, "Unknown COM value")
    STAT_message = STAT_map.get(STAT, "Unknown STAT value")
    SI_message = "II-Code Capable" if SI == 1 else "SI-Code Capable"
    MSSC_message = "Yes" if MSSC == 1 else "No"
    ARC_message = "25 ft resolution" if ARC == 1 else "100 ft resolution"
    AIC_message = "Yes" if AIC == 1 else "No"
    B1A_message = f"B1A: {B1A}"
    B1B_message = f"B1B: {B1B}"

    # Crear la lista de mensajes
    messages = [COM_message, STAT_message, SI_message, MSSC_message, ARC_message, AIC_message, B1A_message, B1B_message]
    
    return messages

