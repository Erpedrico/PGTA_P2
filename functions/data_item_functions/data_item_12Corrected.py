# Todas las funciones de data item deben devolver un vector de longitud variable. (de momento)
def data_item_5(packet):

    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return
    
    #Verificar la longitud del paquete
    if len(packet) != 8:  # 4 octetos = 8 caracteres hexadecimales
        print(f"Error: El paquete debe tener 4 octetos (8 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None

    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return

# Extraer X (octetos 1 y 2)
    x_bytes = packet_bytes[0:2]  # Primeros 2 octetos
    x = int.from_bytes(x_bytes, byteorder='big', signed=True)  # Convertir a entero con signo
    x_nm = x / 128.0  # Convertir a millas náuticas (1/128 NM por LSB)

    # Extraer Y (octetos 3 y 4)
    y_bytes = packet_bytes[2:4]  # Últimos 2 octetos
    y = int.from_bytes(y_bytes, byteorder='big', signed=True)  # Convertir a entero con signo
    y_nm = y / 128.0  # Convertir a millas náuticas (1/128 NM por LSB)

    # Devolver la posición en coordenadas cartesianas
    return [x_nm, y_nm]
         
    