import struct

def parse_binary_file(file_path):
    packets = []
    
    with open(file_path, "rb") as f:
        data = f.read()  # Leer todo el archivo binario
    
    index = 0  # Posición actual en los datos
    while index < len(data):
        if index + 3 > len(data):  # Verificar si hay al menos 3 bytes disponibles
            break
        
        cat = data[index]  # Primer octeto (categoría del paquete)
        length = struct.unpack_from('>H', data, index + 1)[0]  # Dos octetos siguientes (longitud total)
        
        if index + length > len(data):  # Evitar que la longitud exceda los datos disponibles
            break
        
        packet = data[index : index + length]  # Extraer el paquete completo
        packets.append(packet)  # Guardar en la lista
        
        index += length  # Moverse al siguiente paquete
    
    return packets
