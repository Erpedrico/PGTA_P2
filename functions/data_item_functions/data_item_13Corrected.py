from bitstring import BitArray  # Para manejar bits más fácil

def data_item_200(packet):
    
    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

     # Verificar si la cadena tiene exactamente 4 octetos (8 caracteres hexadecimales)
    if len(packet) != 8:
        print(f"Error: El paquete debe tener 4 octetos (8 caracteres hexadecimales). Longitud actual: {len(cleaned_packet)}")
        return None

    # Convertir la cadena hexadecimal a un objeto BitArray
    bit_array = BitArray(hex=cleaned_packet)

    # Extraer la velocidad en tierra calculada (16 bits)
    groundspeed_bits = bit_array[0:16]  # Primeros 16 bits
    groundspeed = groundspeed_bits.uint * (2 **(-14))  # Convertir a NM/s
    groundspeed_knots= groundspeed * 3600

    # Extraer el rumbo calculado (16 bits)
    heading_bits = bit_array[16:32]  # Últimos 16 bits
    heading = heading_bits.uint * (360 / (2**16))  # Convertir a grados
    
    # Devolver la velocidad y el rumbo
    return [groundspeed, groundspeed_knots, heading]
        