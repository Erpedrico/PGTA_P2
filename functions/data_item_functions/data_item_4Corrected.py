# Todas las funciones de data item deben devolver un vector de longitud variable. (de momento)
def data_item_4(packet):

    #Verificar la longitud del paquete
    if len(packet) != 8:  # 4 octetos = 8 caracteres hexadecimales
        print(f"Error: El paquete debe tener 4 octetos (8 caracteres hexadecimales). Longitud actual: {len(packet)}")
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
    
     # Extraer RHO (octetos 1 y 2)
    rho_bytes = packet_bytes[0:2]  # Primeros 2 octetos
    rho = int.from_bytes(rho_bytes, byteorder='big')  # Convertir a entero
    rho_nm = rho / 256.0  # Convertir a NM (1/256 NM por LSB)

    # Extraer THETA (octetos 3 y 4)
    theta_bytes = packet_bytes[2:4]  # Últimos 2 octetos
    theta = int.from_bytes(theta_bytes, byteorder='big')  # Convertir a entero
    theta_deg = theta * (360.0 / 65536)  # Convertir a grados (360° / 2^16)

    # Verificar si RHO está en rango extendido 
    if rho_nm >= 256:  # RHO >= 256 NM
        print("Advertencia: RHO está en rango extendido. Se debe enviar el ítem 'Extended Range Report'.")

    # Devolver la posición en coordenadas polares
    return [rho_nm, theta_deg] 
    
    