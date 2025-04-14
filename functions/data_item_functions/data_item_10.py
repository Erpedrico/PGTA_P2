"""
Data Item I048/250, BDS Register Data
"""
import data_item_10_subdecoder as BDS


def data_item_10(packet) -> (list | None):
    """
    [REP(1byte), [[BDS(7bytes), BDS1(4bit), BDS2(4bit)]...]]
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
        bds1 = (packet_bytes[i+7] & 0xF0) >> 4  # Extract upper 4 bits #int
        bds2 = packet_bytes[i+7] & 0x0F         # Extract lower 4 bits #int
        bdsdata_decoded = BDS.decode(bdsdata)
        if bdsdata_decoded is None:
            print("Error al decodificar BDS")
            continue
        bds.append([bdsdata, bds1, bds2])

    return [rep, bds]
