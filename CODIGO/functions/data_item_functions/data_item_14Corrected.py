from bitstring import BitArray  # Importar la librería bitstring

def data_item_14(packet):
    # Limpiar la cadena hexadecimal: eliminar espacios y caracteres no válidos
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")

    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None

    # Convertir la cadena hexadecimal a un objeto BitArray
    bit_array = BitArray(hex=cleaned_packet)

    # Mapeo de valores
    CNF_mapping = {0: "Tentative Track", 1: "Confirmed Track"}
    RAD_mapping = {0: "Combined Track", 1: "PSR Track", 2: "SSR/Mode S Track", 3: "Invalid"}
    CDM_mapping = {0: "Maintaining", 1: "Climbing", 2: "Descending", 3: "Unknown"}

    # Crear una lista para almacenar los resultados
    track_status = []

    # Procesar el primer octeto
    first_octet = bit_array[0:8]  # Extraer los primeros 8 bits
    CNF = first_octet[0:1].uint  # bit 8
    RAD = first_octet[1:3].uint  # bits 7-6
    DOU = first_octet[3:4].uint  # bit 5
    MAH = first_octet[4:5].uint  # bit 4
    CDM = first_octet[5:7].uint  # bits 3-2
    FX = first_octet[7:8].uint   # bit 1

    # Procesar los campos del primer octeto
    track_status.append(CNF_mapping.get(CNF, "Unknown CNF value"))
    track_status.append(RAD_mapping.get(RAD, "Unknown RAD value"))
    track_status.append("Low confidence in plot to track association" if DOU else "Normal confidence")
    track_status.append("Horizontal manoeuvre sensed" if MAH else "No horizontal manoeuvre sensed")
    track_status.append(CDM_mapping.get(CDM, "Unknown CDM value"))
    track_status.append("Extension into first extent" if FX else "End of Data Item")

    # Procesar la siguiente extensión FX (octeto adicional)
    index = 8   # Empezar después del primer octeto
    if FX == 1 and index < len(bit_array):
        current_octet = bit_array[index:index + 8]  # Extraer el siguiente octeto

        # Procesar el primer octeto de extensión
        TRE = current_octet[0:1].uint  # bit 8
        GHO = current_octet[1:2].uint  # bit 7
        SUP = current_octet[2:3].uint  # bit 6
        TCC = current_octet[3:4].uint  # bit 5
        FX = current_octet[7:8].uint  # bit 1 (FX de la extensión)

        track_status.append("End of track lifetime" if TRE else "Track still alive")
        track_status.append("Ghost target track" if GHO else "True target track")
        track_status.append("Track maintained with neighbouring Node B" if SUP else "Track not maintained with neighbouring Node B")
        track_status.append("Slant range correction applied" if TCC else "No slant range correction")
        track_status.append("Extension into next extent" if FX else "End of Data Item")


    return track_status