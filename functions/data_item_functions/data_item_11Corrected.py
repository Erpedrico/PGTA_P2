# Todas las funciones de data item deben devolver un vector de longitud variable. (de momento)
def data_item_11(packet):   
    # Limpiar la entrada asegurando solo caracteres hexadecimales
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    print(packet)
    # Verificar si la cadena limpia tiene una longitud correcta
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None
    
    # Verificar la longitud del paquete
    if len(cleaned_packet) != 4:  # 2 octetos = 4 caracteres hexadecimales
        print(f"Error: El paquete debe tener 2 octetos (4 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None

    # Convertir la cadena hexadecimal a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None

    # Convertir los bytes en un entero de 16 bits
    track_data = int.from_bytes(packet_bytes, byteorder='big')

    # Extraer el número de pista (12 bits menos significativos)
    track_number = track_data & 0x0FFF  # 0x0FFF = 0000111111111111 en binario

    return [track_number]