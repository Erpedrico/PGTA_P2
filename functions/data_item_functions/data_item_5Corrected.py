def data_item_10(packet):

    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return
    
    # Verificar la longitud del paquete
    if len(packet) != 4:  # 2 octetos = 4 caracteres hexadecimales
        print(f"Error: El paquete debe tener 2 octetos (4 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None
    
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return
    
    # Convertir los 2 octetos a un entero de 16 bits
    mode3a_code = int.from_bytes(packet_bytes, byteorder='big')

   
    V = (mode3a_code >> 15) & 0b1  # Bit 16
    G = (mode3a_code >> 14) & 0b1  # Bit 15
    L = (mode3a_code >> 13) & 0b1  # Bit 14
    spare = (mode3a_code >> 12) & 0b1  # Bit 13 (debe ser 0)
    code_octal = mode3a_code & 0xFFF  # Bits 12-1 (código Mode-3/A en octal)

    # Verificar el bit de reserva (debe ser 0)
    if spare != 0:
        print("Advertencia: El bit de reserva (bit 13) no es 0.")

    # NOTA 1: Si el código es suavizado (L = 1), el bit G no tiene significado y debe ser 0
    if L == 1 and G != 0:
        print("El bit G (garbled) no tiene significado para un código suavizado. Se corrige a 0.")
        G = 0  # Corregir el bit G a 0

    # NOTA 2: Para Mode S, el bit V puede ser 1 si el código no está validado
    Validated="Yes" if V == 0 else "No"
    Garbled="Yes" if G == 1 else "No"
    CodeSource="Not extracted in last scan" if L == 1 else "Transponder"
    Mode3ACode =f"{code_octal:04o}"  # Formato octal de 4 dígitos

    # Devolver la información del código Mode-3/A
    return [Validated, Garbled, CodeSource, Mode3ACode]
        
    