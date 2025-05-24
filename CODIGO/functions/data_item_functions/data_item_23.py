def data_item_23(packet):
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
    A = packet_bytes[0] >> 2 & 0x7  # Los 3 bits siguientes para A (de 0 a 7)
    B = packet_bytes[0] & 0x3  # Los 2 últimos bits para B (de 0 a 3)

    # Crear los mensajes para V, G y L
    V_message = "Code validated" if V == 0 else "Code not validated"
    G_message = "Default" if G == 0 else "Garbled Code"
    L_message = "Mode-1 code as derived from the reply of the transponder" if L == 0 else "Smoothed Mode-1 code as provided by a local tracker."

    # Crear el mensaje para A y B sin juntarlos, sino simplemente con sus valores decimales
    AB_message = f"A: {A}, B: {B}, total: {A}{B}"

    # Añadir los mensajes a la lista de mensajes
    messages.extend([V_message, G_message, L_message, AB_message])

    return messages



