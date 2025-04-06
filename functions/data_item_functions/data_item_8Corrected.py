def data_item_8(packet):

    # Limpiar el paquete (eliminar caracteres no válidos)
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None
    
    # Verificar la longitud del paquete
    if len(cleaned_packet) != 6:  # 3 octetos = 6 caracteres hexadecimales
        print(f"Error: El paquete debe tener 3 octetos (6 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None
    
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None
    
    # Convertir los 3 octetos a un entero de 24 bits
    aircraft_address = int.from_bytes(packet_bytes, byteorder='big')

    # Formatear la dirección en hexadecimal (6 caracteres)
    address_hex = f"{aircraft_address:06X}"

    return [address_hex]