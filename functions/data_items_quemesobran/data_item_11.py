def data_item_11(packet):
    # Verificar la longitud del paquete
    if len(packet) != 4:  # 2 octetos = 4 caracteres hexadecimales
        print(f"Error: El paquete debe tener 2 octetos (4 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None
    
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None
    
    # Convertir los 2 octetos a un entero de 16 bits
    confidence_indicator = int.from_bytes(packet_bytes, byteorder='big')

    # Extraer la calidad de cada pulso (bits 12-1)
    pulse_quality = []
    i=0
    while i < 12:
        bit = (confidence_indicator >> i) & 0b1
        pulse_quality.append("Low quality pulse Xi" if bit == 1 else "High quality pulse Xi")
        i+=1
    # Verificar si al menos un pulso es de baja calidad
    if "Low quality pulse Xi" not in pulse_quality:
        print("Todos los pulsos son de alta calidad.")
        return None
    else:
        return pulse_quality