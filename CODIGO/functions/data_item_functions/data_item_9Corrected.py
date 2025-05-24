from bitstring import BitArray #Para manejar bits más fácil

def data_item_9(packet):
    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None

    # Verificar si la cadena limpia tiene exactamente 6 octetos (12 caracteres hexadecimales)
    if len(cleaned_packet) != 12:
        print(f"Error: El paquete debe tener 6 octetos (12 caracteres hexadecimales). Longitud actual: {len(cleaned_packet)}")
        return None

    # Convertir la cadena hexadecimal a un objeto BitArray
    bit_array = BitArray(hex=cleaned_packet)

    # Decodificar los 6 octetos (48 bits) en 8 caracteres de 6 bits cada uno
    aircraft_id = []
    for i in range(0, 48, 6):  # 48 bits en total, 6 bits por carácter
        # Extraer 6 bits
        number = bit_array[i:i+6].uint  # Convertir a entero 6 bits
        
        # Diccionario de mapeo
        char_map = {
            0: 'A', 1: 'B', 2: 'C', 3: 'D', 4: 'E', 5: 'F',
            6: 'G', 7: 'H', 8: 'I', 9: 'J', 10: 'K', 11: 'L',
            12: 'M', 13: 'N', 14: 'O', 15: 'P', 16: 'Q', 17: 'R',
            18: 'S', 19: 'T', 20: 'U', 21: 'V', 22: 'W', 23: 'X',
            24: 'Y', 25: 'Z', 26: '0', 27: '1', 28: '2', 29: '3',
            30: '4', 31: '5', 32: '6', 33: '7', 34: '8', 35: '9'
        }

        # Decodificar el valor de 6 bits a un carácter
        aircraft_id.append(char_map.get(number, ''))  # Usar '' si el valor no está en el diccionario
    
    ID = ''.join(aircraft_id).strip()  # Unir en una cadena y eliminar espacios

    
    return ID