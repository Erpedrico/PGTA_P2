"""
Data Item I048/250, BDS Register Data
"""
import data_item_10_subdecoder as BDS


def data_item_10(packet) -> (list | None):
    """
    input: [REP(1byte), [[BDS(7bytes), BDS1(4bit), BDS2(4bit)]...]]
    output: [REP(1byte), [BDS(decoded as dict),...]]
    """
    cleaned_packet = "".join(
        c for c in packet if c in "0123456789abcdefABCDEF")
    if len(cleaned_packet) % 2 != 0:
        print(
            f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None

    if (len(cleaned_packet) - 2) % 16 != 0:
        print(
            f"Error: El paquete debe tener 1+8x octetos. Longitud actual: {len(cleaned_packet)}")
        return None

    packet_bytes = bytes()
    # convert to bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None

    rep = packet_bytes[0]
    bds = []
    packet_bytes = packet_bytes[1:]
    for i in range(0, len(packet_bytes), 8):
        bdsdata = packet_bytes[i:i+7]           # bytes
        bds12 = packet_bytes[i+7]
                # Tables are numbered A-2-X where “X” is the decimal equivalent of the BDS code Y/Z. Y is the BDS1 code and Z is the BDS2 code used to access the data format for a particular register. 
        bdsdata_decoded = BDS.decode(bdsdata, bds12)
        if bdsdata_decoded is None:
            print("Error al decodificar BDS")
            continue
        bds.append(bdsdata)
    return [rep, bds]
