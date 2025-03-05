def data_item_18(packet):

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

    sigma_X = int.from_bytes(packet_bytes[0:1], byteorder='big') / 128
    sigma_Y = int.from_bytes(packet_bytes[1:2], byteorder='big') / 128
    sigma_V = int.from_bytes(packet_bytes[2:3], byteorder='big') * 2 ** (-14) 
    sigma_H = int.from_bytes(packet_bytes[3:4], byteorder='big') * 360 / (2 ** 12)

    sigma = [sigma_X, sigma_Y, sigma_V, sigma_H]  

    return sigma
