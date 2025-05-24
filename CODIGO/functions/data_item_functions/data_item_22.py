def data_item_22(packet):
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
    
    # Combinar los 7 bytes en un número de 56 bits
    ACASRA = 0  # Inicializamos el número como 0
    for i, byte in enumerate(packet_bytes):
        ACASRA |= byte << (8 * (6 - i))
    
    return ACASRA

