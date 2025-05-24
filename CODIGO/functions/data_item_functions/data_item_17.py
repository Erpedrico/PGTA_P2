def data_item_17(packet):
    
    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
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

    # Verificar que el paquete tenga al menos 2 bytes
    if len(packet_bytes) < 2:
        print(f"Error: El paquete debe tener al menos 2 bytes.")
        return

    # Juntamos los dos bytes para formar un número de 16 bits
    combined = (packet_bytes[0] << 8) | packet_bytes[1]  # Desplazamos el primer byte 8 bits a la izquierda y lo combinamos con el segundo byte
    
    # Obtenemos los 12 bits menos significativos (máscara para los 12 bits)
    masked = combined & 0xFFF  # 0xFFF es 0000111111111111 en binario
    
    # Dividimos los 12 bits en grupos de 3
    grupos = []
    for i in range(4):
        # Extraemos 3 bits a partir de la posición i*3
        grupo = (masked >> (3 * (3 - i))) & 0x7  # 0x7 es 00000111 en binario, para obtener 3 bits
        grupos.append(grupo)
    
    # Juntamos los 4 grupos en un número de 4 cifras
    resultado = ''.join(str(grupo) for grupo in grupos)
    
    return resultado

