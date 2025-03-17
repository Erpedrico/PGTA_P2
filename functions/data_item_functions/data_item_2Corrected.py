def data_item_14(packet):
    # Verificar la longitud del paquete
    if len(packet) != 6:  # 3 octetos = 6 caracteres hexadecimales
        print(f"Error: El paquete debe tener 3 octetos (6 caracteres hexadecimales). Longitud actual: {len(packet)}")
        return None

    # Limpiar el paquete (eliminar caracteres no válidos)
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
    
    # Convertir los 3 octetos a un entero de 24 bits
    time_of_day = int.from_bytes(packet_bytes, byteorder='big')

    # Calcular el tiempo en segundos (1/128 segundos por LSB)
    time_in_seconds = time_of_day / 128.0

    # Convertir el tiempo a horas, minutos, segundos y milisegundos
    hours = int(time_in_seconds / 3600)
    minutes = int((time_in_seconds % 3600) / 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)

    # Formatear el tiempo en HH:MM:SS.sss
    time_formatted = f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    return [time_formatted]