def data_item_26(packet):
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

    # Juntamos los dos bytes para formar un número de 16 bits
    combined = (packet_bytes[0] << 8) | packet_bytes[1]  # Desplazamos el primer byte 8 bits a la izquierda y lo combinamos con el segundo byte
    
    # Obtenemos los 12 bits menos significativos (máscara para los 12 bits)
    masked = combined & 0xFFF  # 0xFFF es 0000111111111111 en binario

    # Extraemos los valores de cada bit según los requisitos
    QA4 = masked >> 11 & 0x1  
    QA2 = masked >> 10 & 0x1
    QA1 = masked >> 9 & 0x1
    QB4 = masked >> 8 & 0x1
    QB2 = masked >> 7 & 0x1
    QB1 = masked >> 6 & 0x1
    QC4 = masked >> 5 & 0x1
    QC2 = masked >> 4 & 0x1
    QC1 = masked >> 3 & 0x1
    QD4 = masked >> 2 & 0x1
    QD2 = masked >> 1 & 0x1
    QD1 = masked & 0x1  

    # Crear los mensajes
    QA4_message = "High quality pulse" if QA4 == 0 else "Low quality pulse"
    QA2_message = "High quality pulse" if QA2 == 0 else "Low quality pulse"
    QA1_message = "High quality pulse" if QA1 == 0 else "Low quality pulse"
    QB4_message = "High quality pulse" if QB4 == 0 else "Low quality pulse"
    QB2_message = "High quality pulse" if QB2 == 0 else "Low quality pulse"
    QB1_message = "High quality pulse" if QB1 == 0 else "Low quality pulse"
    QC4_message = "High quality pulse" if QC4 == 0 else "Low quality pulse"
    QC2_message = "High quality pulse" if QC2 == 0 else "Low quality pulse"
    QC1_message = "High quality pulse" if QC1 == 0 else "Low quality pulse"
    QD4_message = "High quality pulse" if QD4 == 0 else "Low quality pulse"
    QD2_message = "High quality pulse" if QD2 == 0 else "Low quality pulse"
    QD1_message = "High quality pulse" if QD1 == 0 else "Low quality pulse"

    # Añadir los mensajes a la lista de mensajes
    messages.extend([QA4_message, QA2_message, QA1_message, QB4_message, QB2_message, QB1_message, QC4_message, QC2_message, QC1_message, QD4_message, QD2_message, QD1_message])

    return messages


