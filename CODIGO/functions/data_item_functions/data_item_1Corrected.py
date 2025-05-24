# Todas las funciones de data item deben devolver un vector de longitud variable. (de momento)
def data_item_1(packet):
    
    # Limpiar el paquete (eliminar caracteres no válidos)
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
    
    # Verificar que haya al menos 2 bytes para extraer SAC y SIC
    if len(packet_bytes) < 2:
        print("Paquete demasiado corto") # Paquete demasiado corto
        return None
    
    sac = packet_bytes[0]  # Primer byte (SAC)
    sic =packet_bytes[1]  # Segundo byte (SIC)
    

    return [sac, sic]

    



    
    