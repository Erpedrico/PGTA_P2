from tkinter import filedialog, messagebox
#import uap_mapping
def extract_data_fields(packet):
    data_fields = []
    data_items=[]

    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
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

    # Paso 1: Saltar los dos primeros octetos
    packet_bytes = packet_bytes[3:]

    # Paso 2: Leer el primer octeto
    first_octet = packet_bytes[0]

    # Paso 3: Verificar el último bit (LSB) del primer octeto
    # Si el último bit (LSB) es 1, analizamos más octetos
    octets_to_read = 1  # Inicia leyendo el primer octeto

    while first_octet & 1:  # Comprobamos si el último bit (LSB) es 1
        octets_to_read += 1  # Incrementamos el número de octetos a leer
        if octets_to_read > len(packet_bytes):  # Evitar desbordamiento
            break
        first_octet = packet_bytes[octets_to_read - 1]  # Leemos el siguiente octeto

    # Paso 4: Ahora que sabemos cuántos octetos debemos analizar, lo hacemos bit a bit
    bits_to_check = packet_bytes[:octets_to_read]

    # Paso 5: Analizar bit a bit de izquierda a derecha
    for octet_index, octet in enumerate(bits_to_check):
        for bit_index in range(7, -1, -1):  # Recorremos de izquierda a derecha (bit más significativo a menos)
            bit = (octet >> bit_index) & 1
            if bit == 1:
                # Si el bit es 1, lo guardamos
                data_fields.append(f"Bit 1 en el octeto {octet_index + 1}, bit {bit_index}")

    # Imprimir resultados (mostrar los bits en los que encontramos 1)
    for entry in data_fields:
        print(entry)
    '''
    packet_bytes = packet_bytes[len(bits_to_check):]  # Saltar FSPEC
    index = 0  # Reiniciar index después de FSPEC
       
    #Extraer FRNs activos
    frns_present = []
    for octet_index, octet in enumerate(bits_to_check):
        for bit_index in range(7, -1, -1):  # Recorremos de izquierda a derecha
            bit = (octet >> bit_index) & 1
            if bit == 1:
                frn = (octet_index * 8) + (7 - bit_index) + 1  # Calcular el FRN
                frns_present.append(frn)
    
    #Extraer los data item según los FRNs activos (ejemplo CAT48)
    for frn in frns_present:
        if frn in uap_mapping:
            data_item = uap_mapping[frn]
            name = data_item["name"]
            length = data_item["length"]

            # Si la longitud en octetos es fija
            if isinstance(length, int):
                data = packet_bytes[index:index + length]
                index += length
                data_items.append(f"FRN {frn}: {name} (Longitud: {length} octetos) - Datos: {data.hex()}")
            else:
                # Si la longitud en octetos es variable, (esto hay que desarollarlo más, tengo duda de qué significa cada valor de longitud en octetos y si tiene relación con el data filed)
                data_items.append(f"FRN {frn}: {name} (Longitud: {length}) - Datos variables")
        else:
            data_items.append(f"FRN {frn}: Desconocido")
    '''
    

    # Combinar todas las entradas en una sola cadena
    result_message = "\n".join(data_fields)

    # Mostrar la cadena en un messagebox
    messagebox.showinfo("Resultados del análisis", result_message)

    
