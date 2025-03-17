def data_item_7(packet):

    # Verificar la longitud del paquete
    if len(packet) != 2:  # 1 octeto = 2 caracteres hexadecimales
        print(f"Error: El paquete debe tener 1 octeto (2 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None
    
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
    
     # Convertir el octeto a un entero de 8 bits
    mode1_code = int.from_bytes(packet_bytes, byteorder='big')

  
    V = (mode1_code >> 7) & 0b1  # Bit 8
    G = (mode1_code >> 6) & 0b1  # Bit 7
    L = (mode1_code >> 5) & 0b1  # Bit 6
    code_octal = mode1_code & 0b11111  # Bits 5-1 (código Mode-1 en octal)

    # NOTA 1: Si el código es suavizado (L = 1), el bit G no tiene significado y debe ser 0
    if L == 1 and G != 0:
        print("El bit G (garbled) no tiene significado para un código suavizado y debe ser 0.")

   

    Validated = "Yes" if V == 0 else "No"
    Garbled= "Yes" if G == 1 else "No"
    CodeSource="Local Tracker" if L == 1 else "Transponder"
    Mode1Code = f"{code_octal:03o}"  # Formato octal de 3 dígitos

    return [Validated, Garbled, CodeSource, Mode1Code]
       
    
