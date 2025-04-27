"""
Data Item I048/250, BDS Register Data
"""


def _4_0(bdsdata: bytes) -> dict:
    # 4,0 Selected vertical intention
    ranges = {
        "STATUS1": [1, 1],
        "MCPFCU_SELECTED_ALTITUDE": [2, 13],
        "STATUS2": [14, 14],
        "FMS_SELECTED_ALTITUDE": [15, 26],
        "STATUS3": [27, 27],
        "BARO_PRESSURE_SETTING": [28, 39],
        "STATUS_MCPFCU_MODE": [48, 48],
        "VNAV": [49, 49],
        "ALT_HOLD": [50, 50],
        "APPROACH": [51, 51],
        "STATUS_TARGET_ALT_SRC": [54, 54],
        "TARGET_ALT_SRC": [55, 56],
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)
    return {
        "name": "Selected vertical intention",
        "MCP/FCU selected altitude": str(r["MCPFCU_SELECTED_ALTITUDE"]*16) + " ft" if r["STATUS1"] else "N/A",
        "FMS selected altitude": str(r["FMS_SELECTED_ALTITUDE"]*16) + " ft" if r["STATUS2"] else "N/A",
        # added 800 as base!
        "Barometric pressure setting": str(r["BARO_PRESSURE_SETTING"] * 0.1 + 800) + " mb" if r["STATUS3"] else "N/A",
        "VNAV mode": ["Not active", "Active"][r["VNAV"]] if r["STATUS_MCPFCU_MODE"] else "N/A",
        "Altitude hold mode": ["Not active", "Active"][r["ALT_HOLD"]] if r["STATUS_MCPFCU_MODE"] else "N/A",
        "Approach mode": ["Not active", "Active"][r["APPROACH"]] if r["STATUS_MCPFCU_MODE"] else "N/A",
        "Target altitude source": ["Unknown",
                                   "Aircraft altitude",
                                   "FCU/MCP selected altitude",
                                   "FMS selected altitude"][r["TARGET_ALT_SRC"]] if r["STATUS_TARGET_ALT_SRC"] else "N/A"
    }


def _5_0(bdsdata: bytes) -> dict:
    # 5,0 Track and turn report
    ranges = {
        "STATUS1": [1, 1],
        "SIGN1": [2, 2],
        "ROLL_ANGLE": [3, 11],
        "STATUS2": [12, 12],
        "SIGN2": [13, 13],
        "TRUE_TRACK_ANGLE": [14, 23],
        "STATUS3": [24, 24],
        "GROUND_SPEED": [25, 34],
        "STATUS4": [35, 35],
        "SIGN4": [36, 36],
        "TRACK_ANGLE_RATE": [37, 45],
        "STATUS5": [46, 46],
        "TRUE_AIRSPEED": [47, 56]
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)
    return {
        "name": "Track and turn report",
        "Roll angle": ("-" if r["SIGN1"] else "") + str(r["ROLL_ANGLE"]*45/256) + "°" if r["STATUS1"] else "N/A",
        "True track angle": ("-" if r["SIGN2"] else "") + str(r["TRUE_TRACK_ANGLE"]*90/512) + "°" if r["STATUS2"] else "N/A",
        "Ground speed": str(r["GROUND_SPEED"]*2) + " kt" if r["STATUS3"] else "N/A",
        "Track angle rate": ("-" if r["SIGN4"] else "") + str(r["TRACK_ANGLE_RATE"]*8/256) + "°/s" if r["STATUS4"] else "N/A",
        "True airspeed": str(r["TRUE_AIRSPEED"]*2) + " kt" if r["STATUS5"] else "N/A"
    }


def _6_0(bdsdata: bytes) -> dict:
    # 6,0 Heading and speed report
    ranges = {
        "STATUS1": [1, 1],
        "SIGN1": [2, 2],
        "MAGNETIC_HEADING": [3, 12],
        "STATUS2": [13, 13],
        "INDICATED_AIRSPEED": [14, 23],
        "STATUS3": [24, 24],
        "MACH": [25, 34],
        "STATUS4": [35, 35],
        "SIGN4": [36, 36],
        "BARO_ALT_RATE": [37, 45],
        "STATUS5": [46, 46],
        "SIGN5": [47, 47],
        "INERTIAL_VERTICAL_VELOCITY": [48, 56]
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)
    return {
        "name": "Heading and speed report",
        "Magnetic heading": ("-" if r["SIGN1"] else "") + str(r["MAGNETIC_HEADING"]*90/512) + "°" if r["STATUS1"] else "N/A",
        "Indicated airspeed": str(r["INDICATED_AIRSPEED"]) + " kt" if r["STATUS2"] else "N/A",
        "Mach": str(r["MACH"]*0.004) if r["STATUS3"] else "N/A",  # 2.048/256
        "Barometric altitude rate": ("-" if r["SIGN4"] else "") + str(r["BARO_ALT_RATE"]*32) + " ft/min" if r["STATUS4"] else "N/A",
        "Inertial vertical velocity": ("-" if r["SIGN5"] else "") + str(r["INERTIAL_VERTICAL_VELOCITY"]*32) + " ft/min" if r["STATUS5"] else "N/A"
    }


def ranges_to_bytes(bdsdata: bytes, ranges: dict) -> dict:
    r = {}
    for key, value in ranges.items():
        start, end = value
        # Extract the relevant bits from BDSDATA
        extracted_bits = extract_bit(bdsdata, start, end)
        # Convert the extracted bits to an integer
        # Store the integer value in the dictionary
        r[key] = extracted_bits
    return r


def extract_bit(data: bytes, start: int, end: int) -> int:
    """
    Extracts bits [start,end] from a byte array and returns the value as an integer.
    """

    # Calculate which bytes are relevant
    byte_start = start // 8
    byte_end = end // 8
    relevant_bytes = data[byte_start:byte_end + 1]

    # Convert to int
    value = int.from_bytes(relevant_bytes, byteorder='big')

    # Drop trailing bits, end being odd
    trailing_bits = (8 * (byte_end + 1)) - (end + 1)
    value >>= trailing_bits

    # Mask to get exact bits
    bit_length = end - start + 1
    mask = (1 << bit_length) - 1  # bit_length number of 1s
    result_int = value & mask

    return result_int


def decode(bdsdata: bytes, bdscode: int) -> (list | None):
    """
    BDS(7bytes), BDSCODE 0-255
    """
    try:
        if bdscode == 0x40:
            return _4_0(bdsdata)
        elif bdscode == 0x50:
            return _5_0(bdsdata)
        elif bdscode == 0x60:
            return _6_0(bdsdata)
        else:
            return None
    except Exception as e:
        print(f"Error decoding BDS data: {e}")
        return None


def data_item_10(packet) -> (list | None):
    """
    input: [REP(1byte), [[BDS(7bytes), BDS1(4bit), BDS2(4bit)]...]]
    output: [REP(1byte), [BDS(decoded as dict), ...]]
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

    bds = []
    packet_bytes = packet_bytes[1:] # ignore first byte (REP)
    for i in range(0, len(packet_bytes), 8):
        bdsdata = packet_bytes[i:i+7]           # bytes
        bds12 = packet_bytes[i+7]
        # Tables are numbered A-2-X where “X” is the decimal equivalent of the BDS code Y/Z. Y is the BDS1 code and Z is the BDS2 code used to access the data format for a particular register.
        bdsdata_decoded = decode(bdsdata, bds12)
        if bdsdata_decoded is None:
            # not needed subcamp, just ignore
            continue
        bds.append(bdsdata)
    return bds
