def data_item_28(packet) -> dict:
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    result = {"name": "Data Item 28", "Latitude": None, "Longitude": None}

    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return result

    try:
        packet_bytes = bytes.fromhex(cleaned_packet)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return result

    if len(packet_bytes) < 2:
        return result

    total_length = packet_bytes[0]
    items_indicator = packet_bytes[1]

    MD5 = items_indicator & 0b10000000
    packet_bytes = packet_bytes[1:]  # Eliminamos byte de longitud

    if MD5:
        if len(packet_bytes) < 1:
            return result

        md5_header = packet_bytes[0]
        packet_bytes = packet_bytes[1:]

        SUM = (md5_header >> 7) & 1
        PMN = (md5_header >> 6) & 1
        POS = (md5_header >> 5) & 1

        skip_bytes = 0
        if SUM:
            skip_bytes += 1
        if PMN:
            skip_bytes += 4

        if len(packet_bytes) < skip_bytes:
            return result

        packet_bytes = packet_bytes[skip_bytes:]

        if POS:
            if len(packet_bytes) < 6:
                return result

            lat_bytes = packet_bytes[0:3]
            lon_bytes = packet_bytes[3:6]

            lat = int.from_bytes(lat_bytes, byteorder='big', signed=True) * 2.145767e-05
            lon = int.from_bytes(lon_bytes, byteorder='big', signed=True) * 2.145767e-05

            result["Latitude"] = round(lat,6)
            result["Longitude"] = round(lon,6)

            print("---------------------------------------------Estamos aqui 1------------------------------------------------")
            print(result)
            print("---------------------------------------------Estamos aqui 2------------------------------------------------")
            

    return result
