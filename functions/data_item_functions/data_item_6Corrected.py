def data_item_6(packet):

    # Limpiar el paquete (eliminar caracteres no válidos)
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")


     # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None

    # Verificar la longitud del paquete
    if len(cleaned_packet) != 4:  # 2 octetos = 4 caracteres hexadecimales
        print(f"Error: El paquete debe tener 2 octetos (4 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None
      
    
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None
    
    # Convertir los 2 octetos a un entero de 16 bits
    flight_level_data = int.from_bytes(packet_bytes, byteorder='big')

    # Extraer los bits relevantes
    V = (flight_level_data >> 15) & 0b1  # Bit 16 (Validated)
    G = (flight_level_data >> 14) & 0b1  # Bit 15 (Garbled)
    flight_level = (flight_level_data & 0x3FFF)  # Bits 14-1 (Flight Level)

    # Calcular el nivel de vuelo en unidades de 1/4 de FL
    flight_level_value = flight_level * 0.25  # Convertir a Flight Level (FL)

    # Nota 3: Verificar si el valor del nivel de vuelo está dentro del rango permitido por ICAO Annex 10 (esto no se si hace falta)
    if flight_level_value < -12 or flight_level_value > 1267.75:
        print(f"Advertencia: El valor del nivel de vuelo ({flight_level_value} FL) está fuera del rango permitido por ICAO Annex 10.")

    # Devolver la información del nivel de vuelo
    Validated="Yes" if V == 0 else "No"
    Garbled="Yes" if G == 1 else "No"
    FlightLevel=f"{flight_level_value}"
    
    return [Validated, Garbled, FlightLevel]
        
