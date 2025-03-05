def data_item_24(packet):
    messages = []  # Lista para almacenar los mensajes

    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return

    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
        print(packet_bytes)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return
    
    # Verificar que tenemos al menos un byte en el paquete
    if len(packet_bytes) < 1:
        print("Error: El paquete debe tener al menos un byte.")
        return

    # Extraemos los bits correspondientes a V, G, L, A, B
    V = packet_bytes[0] >> 7  # Primer bit del primer byte
    G = packet_bytes[0] >> 6 & 0x1  # Segundo bit del primer byte
    L = packet_bytes[0] >> 5 & 0x1  # Tercer bit del primer byte

    # Juntamos los dos bytes para formar un número de 16 bits
    combined = (packet_bytes[0] << 8) | packet_bytes[1]  # Desplazamos el primer byte 8 bits a la izquierda y lo combinamos con el segundo byte
    
    # Obtenemos los 12 bits menos significativos (máscara para los 12 bits)
    masked = combined & 0xFFF  # 0xFFF es 0000111111111111 en binario

    A = masked >> 9 & 0x7  
    B = masked >> 6 & 0x7  
    C = masked >> 3 & 0x7  
    D = masked & 0x7  

    # Mensajes según los valores de V, G y L
    V_message = "Code validated" if V == 0 else "Code not validated"
    G_message = "Default" if G == 0 else "Garbled Code"
    L_message = "Mode-2 code as derived from the reply of the transponder" if L == 0 else "Smoothed Mode-2 code as provided by a local tracker"
    ABCD_message = f"A: {A}, B: {B}, C: {C}, D: {D}, total: {A}{B}{C}{D}"

    # Añadir los mensajes a la lista de mensajes
    messages.extend([V_message, G_message, L_message, ABCD_message])

    return messages


