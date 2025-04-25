'''
RE-Data-Item Reserved Expansion Field
'''


def MD5_decoder(packet: bytes, items_indicator: int) -> dict:
    r = {}
    SUM = items_indicator & 0b10000000
    PMN = items_indicator & 0b01000000
    POS = items_indicator & 0b00100000
    GA = items_indicator & 0b00010000
    EM1 = items_indicator & 0b00001000
    TOS = items_indicator & 0b00000100
    XP = items_indicator & 0b00000010
    if SUM:
        subfield = packet[0]
        packet = packet[1:]
        r["Summary"] = {
            "Mode 5 Interrogation":  subfield & 0b10000000 != 0,
            "Authenticated Mode 5 ID Reply/Report": subfield & 0b01000000 != 0,
            "Authenticated Mode 5 Data Reply/Report": subfield & 0b00100000 != 0,
            "Mode 1 from Mode 5 Reply/Report": subfield & 0b00010000 != 0,
            "Mode 2 from Mode 5 Reply/Report": subfield & 0b00001000 != 0,
            "Mode 3 from Mode 5 Reply/Report": subfield & 0b00000100 != 0,
            "Mode C from Mode 5 Reply/Report": subfield & 0b00000010 != 0
        }  # boolean values
    if PMN:
        subfield = packet[0:2]
        packet = packet[1:]
        PIN = int.from_bytes(subfield, byteorder='big')
        subfield = packet[0]
        packet = packet[1:]
        NAV = subfield & 0b00100000
        NAT = subfield & 0b00011111
        MIS = packet[0]
        packet = packet[1:]
        r["PNM"] = {
            "PIN": PIN,  # int
            "Validity of PIN": NAV == 0,
            "National Origin": NAT if NAV == 0 else None,
            "Mission Code": MIS
        }
    if POS:
        subfield = packet[0:3]
        packet = packet[3:]
        LAT = int.from_bytes(subfield, byteorder='big',
                             signed=True) * 2.145767e-05
        subfield = packet[0:3]
        packet = packet[3:]
        LON = int.from_bytes(subfield, byteorder='big',
                             signed=True) * 2.145767e-05
        r["Reported Position"] = {
            "Latitude": LAT,  # float
            "Longitude": LON  # float
        }
    if GA:
        subfield = packet[0:2]
        packet = packet[2:]
        RES = subfield[0] & 0b01000000
        GA = int.from_bytes(subfield, byteorder='big') & 0x3FFF
        GA *= 25 if RES else 100
        r["GNSS-derived Altitude"] = GA  # int
    if EM1:
        subfield = packet[0:2]
        packet = packet[2:]
        EM1 = int.from_bytes(subfield, byteorder='big') & 0x0FFF
        r["Extended Mode 1"] = {
            "Code validity": subfield[0] & 0b10000000 != 0,
            "Garbled code": subfield[0] & 0b01000000 != 0,
            "Mode 1 code derived": subfield[0] & 0b00100000 != 0,
            "Extended Mode 1 code": EM1
        }
    if TOS:
        subfield = packet[0]
        packet = packet[1:]
        r["Time offset"] = subfield/128  # second
    if XP:
        subfield = packet[0]
        packet = packet[1:]
        r["X Pulse"] = {
            "Mode 5 PIN": subfield & 0b00100000 != 0,
            "Mode 5 Data": subfield & 0b00010000 != 0,
            "Mode C": subfield & 0b00001000 != 0,
            "Mode 3/A": subfield & 0b00000100 != 0,
            "Mode 2": subfield & 0b00000010 != 0,
            "Mode 1": subfield & 0b00000001 != 0
        }
    return r


def M5E_decoder(packet: bytes, items_indicator: int) -> dict:
    SUM = items_indicator & 0b10000000
    PMN = items_indicator & 0b01000000
    POS = items_indicator & 0b00100000
    GA = items_indicator & 0b00010000
    EM1 = items_indicator & 0b00001000
    TOS = items_indicator & 0b00000100
    XP = items_indicator & 0b00000010
    FOM = items_indicator & 0b00000001
    r = MD5_decoder(packet, items_indicator)
    if FOM:
        r["Figure of Merit"] = packet[-1]
    return r


def RPC_decoder(packet: bytes, items_indicator: int) -> dict:
    SCO = items_indicator & 0b10000000
    SCR = items_indicator & 0b01000000
    RW = items_indicator & 0b00100000
    AR = items_indicator & 0b00010000
    r = {}
    if SCO:
        subfield = packet[0]
        packet = packet[1:]
        r["Score"] = subfield
    if SCR:
        subfield = packet[0:2]
        packet = packet[2:]
        SCR = int.from_bytes(subfield, byteorder='big')
        r["Signal/Clutter Ratio"] = SCR*0.1
    if RW:
        subfield = packet[0:2]
        packet = packet[2:]
        RW = int.from_bytes(subfield, byteorder='big')
        r["Range Width"] = RW/256
    if AR:
        subfield = packet[0:2]
        AR = int.from_bytes(subfield, byteorder='big')
        r["Ambiguous Range"] = AR/256
    return r


def data_item_28(packet) -> dict:
    cleaned_packet = "".join(
        c for c in packet if c in "0123456789abcdefABCDEF")
    packet_bytes = bytes()
    message = {}
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(
            f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None

    # Convertir la cadena hexadecimal limpia a bytes
    try:
        # Convierte la cadena hexadecimal a bytes
        packet_bytes = bytes.fromhex(cleaned_packet)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None

    length = packet_bytes[0]

    items_indicator = packet_bytes[1]
    MD5 = items_indicator & 0b10000000
    M5N = items_indicator & 0b01000000
    M4E = items_indicator & 0b00100000
    RPC = items_indicator & 0b00010000
    ERR = items_indicator & 0b00001000

    packet_bytes = packet_bytes[1:]
    if MD5:
        items_indicator = packet_bytes[0]

        SUM = items_indicator & 0b10000000 >> 7
        PMN = items_indicator & 0b01000000 >> 6
        POS = items_indicator & 0b00100000 >> 5
        GA = items_indicator & 0b00010000 >> 4
        EM1 = items_indicator & 0b00001000 >> 3
        TOS = items_indicator & 0b00000100 >> 2
        XP = items_indicator & 0b00000010 >> 1
        # assume fx is 0
        packet_bytes = packet_bytes[1:]
        MD5_length = 1*SUM+4*PMN+6*POS+2*GA+2*EM1+1*TOS+1*XP

        r = MD5_decoder(packet_bytes[:MD5_length], items_indicator)
        message["MD5"] = r
        packet_bytes = packet_bytes[MD5_length:]  # pop from the list

    if M5N:
        items_indicator = packet_bytes[0]
        packet_bytes = packet_bytes[1:]
        FOM = 0
        FX = items_indicator & 0b00000001
        if FX:
            FOM = packet_bytes[0] & 0b10000000 >> 7
            packet_bytes = packet_bytes[1:]
        SUM = items_indicator & 0b10000000 >> 7
        PMN = items_indicator & 0b01000000 >> 6
        POS = items_indicator & 0b00100000 >> 5
        GA = items_indicator & 0b00010000 >> 4
        EM1 = items_indicator & 0b00001000 >> 3
        TOS = items_indicator & 0b00000100 >> 2
        XP = items_indicator & 0b00000010 >> 1
        items_indicator |= FOM
        M5N_length = 1*SUM+4*PMN+6*POS+2*GA+2*EM1+1*TOS+1*XP+1*FOM
        r = M5E_decoder(packet_bytes[:M5N_length], items_indicator)
        message["M5E"] = r
        packet_bytes = packet_bytes[M5N_length:]

    if M4E:
        FOEFRI = packet_bytes[0] & 0b00000110 >> 1
        # assume fx is 0
        message["M4E"] = {"Indication Foe/Friend (Mode4)":
                          ["No Mode 4 identification",
                           "possibly friendly target",
                           "probably friendly target",
                           "friendly target"][FOEFRI]
                          }
        packet_bytes = packet_bytes[1:]

    if RPC:
        items_indicator = packet_bytes[0]
        packet_bytes = packet_bytes[1:]
        SCO = items_indicator & 0b10000000 >> 7
        SCR = items_indicator & 0b01000000 >> 6
        RW = items_indicator & 0b00100000 >> 5
        AR = items_indicator & 0b00010000 >> 4
        # assume fx is 0
        RPC_length = 1*SCO+2*SCR+2*RW+2*AR
        r = RPC_decoder(packet_bytes[:RPC_length], items_indicator)
        message["RPC"] = r
        packet_bytes = packet_bytes[RPC_length:]

    if ERR:
        RHO = packet_bytes[:3]
        RHO = int.from_bytes(RHO, byteorder='big')
        RHO /= 256
        message["ERR"] = RHO

        # there should be no more bytes left
    return message
