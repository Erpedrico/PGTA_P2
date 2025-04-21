from functions.data_item_functions.data_item_1Corrected import data_item_1
from functions.data_item_functions.data_item_2Corrected import data_item_2
from functions.data_item_functions.data_item_3Corrected import data_item_3
from functions.data_item_functions.data_item_4Corrected import data_item_4
from functions.data_item_functions.data_item_5Corrected import data_item_5
from functions.data_item_functions.data_item_6Corrected import data_item_6
from functions.data_item_functions.data_item_7 import data_item_7
from functions.data_item_functions.data_item_8Corrected import data_item_8
from functions.data_item_functions.data_item_9Corrected import data_item_9
#from functions.data_item_functions.data_item_10 import data_item_10
from functions.data_item_functions.data_item_11Corrected import data_item_11
from functions.data_item_functions.data_item_12Corrected import data_item_12
from functions.data_item_functions.data_item_13Corrected import data_item_13
from functions.data_item_functions.data_item_14Corrected import data_item_14
from functions.data_item_functions.data_item_15 import data_item_15
from functions.data_item_functions.data_item_16 import data_item_16
from functions.data_item_functions.data_item_17 import data_item_17
from functions.data_item_functions.data_item_19 import data_item_19
from functions.data_item_functions.data_item_21 import data_item_21
from functions.data_item_functions.data_item_22 import data_item_22
from functions.data_item_functions.data_item_23 import data_item_23
from functions.data_item_functions.data_item_24 import data_item_24
from functions.data_item_functions.data_item_25 import data_item_25
from functions.data_item_functions.data_item_26 import data_item_26

def extraer_datos(datos_hex):
    """
    Extrae los datos del paquete en formato hexadecimal considerando los LSB de cada octeto.
    Si el LSB es 1, se debe tomar el siguiente octeto y los bits 1-7 de cada octeto indican 
    qué data items están presentes.
    """
    print("La longitud de los datos es:")
    print(len(datos_hex))
    campos = {
        "NUM": "Not Found",
        "SAC": "Not Found",
        "SIC": "Not Found",
        "TIME": "Not Found",
        "TIME(s)": "Not Found",
        "Target report description": "Not Found",
        "Validated": "Not Found", 
        "Garbled": "Not Found",
        "CodeSource": "Not Found", 
        "Validated_FL": "Not Found", 
        "Garbled_FL": "Not Found",
        "FL": "Not Found", 
        "Mode3ACode": "Not Found",
        "Address": "Not Found",
        "ID": "Not Found",
        "BDS": "Not Found",
        "TRACK NUMBER": "Not Found",
        "TRACK STATUS": "Not Found",
        "X": "Not Found",
        "Y": "Not Found",
        "GS": "Not Found",
        "GS_KT": "Not Found",
        "HEADING": "Not Found",
        "LAT": "Not Found",
        "LON": "Not Found",
        "H": "Not Found",
        "COM": "Not Found",
        "STAT": "Not Found",
        "SI": "Not Found", 
        "MSSC": "Not Found", 
        "ARC": "Not Found",
        "AIC": "Not Found",
        "B1A": "Not Found",
        "B1B": "Not Found",
        "RHO": "Not Found",
        "THETA": "Not Found"
    }

    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
    cleaned_packet = "".join(c for c in datos_hex if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return

    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return

    # Paso 1: Saltar los tres primeros octetos
    print("La longitud de los datos es:")
    print(len(packet_bytes))
    packet_bytes = packet_bytes[3:]
    print(len(packet_bytes))
    # Paso 2: Leer el primer octeto
    first_octet = packet_bytes[0]

    # Paso 3: Verificar el último bit (LSB) del primer octeto
    octets_to_read = 1  # Empezamos con el primer octeto

    while first_octet & 1:  # Si el LSB es 1, leemos el siguiente octeto
        octets_to_read += 1
        if octets_to_read > len(packet_bytes):  # Evitar desbordamiento
            break
        first_octet = packet_bytes[octets_to_read - 1]

    # Paso 4: Analizar los octetos seleccionados, de izquierda a derecha
    bits_to_check = packet_bytes[:octets_to_read]

    # Paso 5: Procesar los bits de cada octeto, saltando el LSB
    data_items = []  # Lista para los data items encontrados
    item_counter = 1  # Inicia en 1, porque los data items van del 1 al 28

    for octet_index, octet in enumerate(bits_to_check):
        for bit_index in range(7, -1, -1):  # De MSB a LSB (bit 7 a 0)
            if bit_index == 0:
                continue  # Saltamos el LSB

            bit = (octet >> bit_index) & 1
            if bit == 1:
                data_items.append(item_counter)

            item_counter += 1
    
    packet_bytes = packet_bytes[octets_to_read:]


    # Paso 6: Asignar valores a los campos dependiendo de los data items encontrados
    for item in data_items:
        if item == 1:
            print(len(packet_bytes))
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
            resultado = data_item_1(data_item_bytes)
            campos["SAC"] = str(resultado[0])
            campos["SIC"] = str(resultado[1])
        elif item == 2:
            data_item_bytes = packet_bytes[:3].hex()
            packet_bytes = packet_bytes[3:]
            resultado = data_item_2(data_item_bytes)
            campos["TIME"] = str(resultado)
        elif item == 3:
            first_octet = packet_bytes[0]
            octets_to_read = 1  # Empezamos con el primer octeto
            while first_octet & 1:  # Si el LSB es 1, leemos el siguiente octeto
                octets_to_read += 1
                if octets_to_read > len(packet_bytes):  # Evitar desbordamiento
                    break
                first_octet = packet_bytes[octets_to_read - 1]
            data_item_bytes = packet_bytes[:octets_to_read].hex()
            packet_bytes = packet_bytes[octets_to_read:]
            resultado = data_item_3(data_item_bytes)
            campos["Target report description"] = str(resultado)
        elif item == 4:
            data_item_bytes = packet_bytes[:4].hex()
            packet_bytes = packet_bytes[4:]
            resultado = data_item_4(data_item_bytes)
            campos["RHO"] = str(resultado[0])
            campos["THETA"] = str(resultado[1])
        elif item == 5:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
            resultado = data_item_5(data_item_bytes)
            campos["Validated"] = str(resultado[0])
            campos["Garbled"] = str(resultado[1])
            campos["CodeSource"] = str(resultado[2])
            campos["Mode3ACode"] = str(resultado[3])
        elif item == 6:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
            resultado = data_item_6(data_item_bytes)
            campos["Validated_FL"] = str(resultado[0])
            campos["Garbled_FL"] = str(resultado[1])
            campos["FL"] = str(resultado[2])
        elif item == 7:
            first_octet = packet_bytes[0]
            octets_to_read = 1  # Empezamos con el primer octeto

            # Si el LSB es 1, seguimos leyendo más octetos
            while first_octet & 1:
                octets_to_read += 1
                if octets_to_read > len(packet_bytes):
                    break
                first_octet = packet_bytes[octets_to_read - 1]

            bits_to_check = packet_bytes[:octets_to_read]

            data_items_d7 = []
            item_counter = 1  # Empezamos en 1 para que los data items coincidan con el esquema que mencionaste

            for octet_index, octet in enumerate(bits_to_check):
                for bit_index in range(7, -1, -1):  # De MSB a LSB (bit 7 a bit 0)
                    if bit_index == 0:
                        continue  # Saltamos el LSB

                    bit = (octet >> bit_index) & 1
                    if bit == 1:
                        data_items_d7.append(item_counter)

                    item_counter += 1

            longitud_d7 = len(data_items_d7)
            print(f"Longitud D7: {longitud_d7}")
            print(f"Item {item} - Bytes disponibles: {len(packet_bytes)}")

            if len(packet_bytes) >= longitud_d7:
                data_item_bytes = packet_bytes[:longitud_d7+1].hex()
                packet_bytes = packet_bytes[longitud_d7+1:]
            else:
                print(f"No hay suficientes bytes para procesar item {item}. Se requieren {longitud_d7}, pero hay {len(packet_bytes)}.")

            
        elif item == 8:
            data_item_bytes = packet_bytes[:3].hex()
            packet_bytes = packet_bytes[3:]
            resultado = data_item_8(data_item_bytes)
            campos["Address"] = str(resultado)
            
        elif item == 9:
            data_item_bytes = packet_bytes[:6].hex()
            packet_bytes = packet_bytes[6:]
            resultado = data_item_9(data_item_bytes)
            campos["ID"] = str(resultado)
            
        elif item == 10:
            # Verificamos si la longitud de packet_bytes es suficiente para evitar un error de índice
            if len(packet_bytes) > 0:  # Si hay al menos un byte disponible
                first_octet = packet_bytes[0]
                
                # Convertimos el primer octeto a int
                first_octet = int(first_octet)  # Ya es un número entero
                
                # Ajustamos el valor del primer octeto sumando 1 (según tu lógica)
                first_octet = first_octet*8+1
                
                # Verificamos que la longitud del paquete es suficiente para evitar acceso fuera de rango
                if first_octet > len(packet_bytes):
                    print(f"Error: Intentando extraer más bytes de los que el paquete tiene. Longitud del paquete: {len(packet_bytes)}")
                    continue  # Salta al siguiente ciclo en el código

                # Extraemos los primeros 'first_octet' bytes
                data_item_bytes = packet_bytes[:first_octet].hex()  # Extraemos los primeros 'first_octet' bytes en formato hexadecimal
                
                # Actualizamos packet_bytes para eliminar los bytes ya procesados
                packet_bytes = packet_bytes[first_octet:]
                
                print(f"Bytes extraídos: {data_item_bytes}")
                print(f"Bytes restantes en packet_bytes: {packet_bytes.hex()}")
                
            else:
                print("El paquete no tiene bytes suficientes para procesar el item 10.")
                print(f"Longitud actual de packet_bytes: {len(packet_bytes)}")
                continue  # Salta al siguiente ciclo en el código
            
        elif item == 11:
            print(len(packet_bytes))
            data_item_bytes_11 = packet_bytes[:2].hex()
            print(data_item_bytes_11)
            packet_bytes = packet_bytes[2:]
            resultado = data_item_11(data_item_bytes_11)
            campos["TRACK NUMBER"] = str(resultado)
            
        elif item == 12:
            data_item_bytes = packet_bytes[:4].hex()
            packet_bytes = packet_bytes[4:]
            resultado = data_item_12(data_item_bytes)
            campos["X"] = str(resultado[0])
            campos["Y"] = str(resultado[1])
        
        elif item == 13:
            data_item_bytes = packet_bytes[:4].hex()
            packet_bytes = packet_bytes[4:]
            resultado = data_item_13(data_item_bytes)
            campos["GS"] = str(resultado[0])
            campos["GS_KT"] = str(resultado[1])
            campos["HEADING"] = str(resultado[2])
        
        elif item == 14:
            first_octet = packet_bytes[0]
            octets_to_read = 1  # Empezamos con el primer octeto
            while first_octet & 1:  # Si el LSB es 1, leemos el siguiente octeto
                octets_to_read += 1
                if octets_to_read > len(packet_bytes):  # Evitar desbordamiento
                    break
                first_octet = packet_bytes[octets_to_read - 1]
            data_item_bytes = packet_bytes[:octets_to_read].hex()
            packet_bytes = packet_bytes[octets_to_read:]
            resultado = data_item_14(data_item_bytes)
            campos["TRACK STATUS"] = str(resultado)
        elif item == 15:
            data_item_bytes = packet_bytes[:4].hex()
            packet_bytes = packet_bytes[4:]
        elif item == 16:
            first_octet = packet_bytes[0]
            octets_to_read = 1  # Empezamos con el primer octeto
            while first_octet & 1:  # Si el LSB es 1, leemos el siguiente octeto
                octets_to_read += 1
                if octets_to_read > len(packet_bytes):  # Evitar desbordamiento
                    break
                first_octet = packet_bytes[octets_to_read - 1]
            data_item_bytes = packet_bytes[:octets_to_read].hex()
            packet_bytes = packet_bytes[octets_to_read:]
        elif item == 17:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
        elif item == 18:
            data_item_bytes = packet_bytes[:4].hex()
            packet_bytes = packet_bytes[4:]
        elif item == 19:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
            resultado = data_item_19(data_item_bytes)
            campos["H"] = str(resultado)
        elif item == 20:
            first_octet = packet_bytes[0]
            octets_to_read = 1  # Empezamos con el primer octeto
            while first_octet & 1:  # Si el LSB es 1, leemos el siguiente octeto
                octets_to_read += 1
                if octets_to_read > len(packet_bytes):  # Evitar desbordamiento
                    break
                first_octet = packet_bytes[octets_to_read - 1]
            data_item_bytes = packet_bytes[:octets_to_read].hex()
            packet_bytes = packet_bytes[octets_to_read:]
        elif item == 21:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
            resultado = data_item_21(data_item_bytes)
            campos["COM"] = str(resultado[0]) 
            campos["STAT"] = str(resultado[1]) 
            campos["SI"] = str(resultado[2]) 
            campos["MSSC"] = str(resultado[3]) 
            campos["ARC"] = str(resultado[4])
            campos["AIC"] = str(resultado[5])
            campos["B1A"] = str(resultado[6])
            campos["B1B"] = str(resultado[7])
        elif item == 22:
            data_item_bytes = packet_bytes[:7].hex()
            packet_bytes = packet_bytes[7:]
        elif item == 23:
            data_item_bytes = packet_bytes[:1].hex()
            packet_bytes = packet_bytes[1:]
        elif item == 24:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
        elif item == 25:
            data_item_bytes = packet_bytes[:1].hex()
            packet_bytes = packet_bytes[1:]
        elif item == 26:
            data_item_bytes = packet_bytes[:2].hex()
            packet_bytes = packet_bytes[2:]
        

    return campos  # Devolver los campos con los datos extraídos

# Ejemplo de cómo llamar la función:
# datos_hex = '...'  # Aquí iría la cadena hexadecimal del paquete
# campos_extraidos = extraer_datos(datos_hex)

