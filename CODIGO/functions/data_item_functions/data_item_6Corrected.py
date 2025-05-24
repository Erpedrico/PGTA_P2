def data_item_6(packet):
    """
    Data Item 6: Flight Level (Mode C)
    """
    
    # Limpiar el paquete (eliminar caracteres no válidos)
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None

    # Verificar la longitud del paquete
    if len(cleaned_packet) != 4:  # 2 octetos = 4 caracteres hexadecimales
        print(f"Error: El paquete debe tener 2 octetos (4 caracteres hexadecimales). Longitud actual: {len(cleaned_packet)}")
        return None
      
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None
    
    # Extraer los bits del primer octeto
    first_octet = packet_bytes[0]
    
    # Bit V (validación) - bit 7 del primer octeto
    V = (first_octet & 0b10000000) >> 7
    
    # Bit G (garbled) - bit 6 del primer octeto  
    G = (first_octet & 0b01000000) >> 6
    
    # Extraer los últimos 14 bits para el Flight Level
    # Combinar los 6 bits restantes del primer octeto con los 8 bits del segundo octeto
    last_14_bits = ((first_octet & 0b00111111) << 8) | packet_bytes[1]
    
    # Manejar el signo (complemento a dos para 14 bits)
    if (last_14_bits & 0x2000) != 0:  # Si el bit 13 (bit de signo) está activado
        last_14_bits = last_14_bits - 0x4000  # Restamos 2^14 para obtener el valor negativo 
    
    # Calcular el nivel de vuelo en unidades de 1/4 de FL
    flight_level_value = last_14_bits * 0.25
    
    # Interpretar los flags 
    validated = "Code validated" if V == 0 else "Code not validated"
    garbled = "Default" if G == 0 else "Garbled code"
    
    return [validated, garbled, str(flight_level_value)]


# Función de prueba para verificar el funcionamiento
def test_data_item_6():
    """
    Función de prueba con algunos casos de ejemplo
    """
    # Casos de prueba
    test_cases = [
        "8000",  # V=1, G=0, FL=0
        "4000",  # V=0, G=1, FL=0  
        "0064",  # V=0, G=0, FL=100 (25.0 FL)
        "3FFF",  # Valor máximo positivo
        "2000",  # Valor mínimo negativo
    ]
    
    for test_case in test_cases:
        print(f"Testing: {test_case}")
        result = data_item_6(test_case)
        if result:
            print(f"  Validated: {result[0]}")
            print(f"  Garbled: {result[1]}")
            print(f"  Flight Level: {result[2]}")
        print()

# Ejecutar pruebas si se ejecuta directamente
if __name__ == "__main__":
    test_data_item_6()