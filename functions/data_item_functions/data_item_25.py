def data_item_25(packet):
    messages = []  # Lista para almacenar los mensajes

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
    
    # Verificar que tenemos al menos un byte en el paquete
    if len(packet_bytes) < 1:
        print("Error: El paquete debe tener al menos un byte.")
        return

    # Extraemos los bits correspondientes
    QA4 = packet_bytes[0] >> 4 
    QA2 = packet_bytes[0] >> 3 & 0x1  
    QA1 = packet_bytes[0] >> 2 & 0x1  
    QB2 = packet_bytes[0] >> 1 & 0x1  
    QB1 = packet_bytes[0] & 0x1  

    # Crear los mensajes
    QA4_message = " High quality pulse" if QA4 == 0 else "Low quality pulse"
    QA2_message = " High quality pulse" if QA2 == 0 else "Low quality pulse"
    QA1_message = " High quality pulse" if QA1 == 0 else "Low quality pulse"
    QB2_message = " High quality pulse" if QB2 == 0 else "Low quality pulse"
    QB1_message = " High quality pulse" if QB1 == 0 else "Low quality pulse"

    # Añadir los mensajes a la lista de mensajes
    messages.extend([QA4_message,QA2_message,QA1_message,QB2_message,QB1_message])

    return messages



