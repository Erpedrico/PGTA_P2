
LETTERLIST = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
              'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',  '',  '',  '',  '',  '',
              ' ',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  '',  '',  '',  '',  '',  '']
# map type code to their decoder functions


def _6(bdsdata: bytes) -> dict:
    # 0,6 — Extended squitter surface position
    ranges = {
        "TYPE": [1, 5],
        "MOVEMENT": [6, 12],
        "STATUS": [13, 13],
        "TRACK": [14, 20],
        "TIME": [21, 21],
        "CPR_FORMAT": [22, 22],
        "LATITUDE": [23, 39],
        "LONGITUDE": [40, 56]
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)
    # TODO


def _8(bdsdata: bytes) -> dict:
    # 0,8 Extended squitter aircraft identification and category
    ranges = {
        "TYPE": [1, 5],
        "EMITTER_CATEGORY": [6, 8],
        "CHARACTER_1": [9, 14],
        "CHARACTER_2": [15, 20],
        "CHARACTER_3": [21, 26],
        "CHARACTER_4": [27, 32],
        "CHARACTER_5": [33, 38],
        "CHARACTER_6": [39, 44],
        "CHARACTER_7": [45, 50],
        "CHARACTER_8": [51, 56]
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)

    return {
        "category": [  # in D C B A order
            ["RESERVED"] * 8,  # D reserved
            ["NO INFO"
                "Surface Vehicle - emergency vehicle",
                "Surface Vehicle - service vehicle",
                "Fixed ground or tethered obstruction",
                "Cluster obstacle",
                "Line obstacle",
                "RESERVED",
                "RESERVED"],
            ["NO INFO",
                "Glider/sailplane",
                "Lighter than air",
                "Parachutist/skydiver",
                "Ultralight/handglider/paraglider",
                "RESERVED",
                "Unmanned aerial vehicle",
                "Space/Trans-atmospheric vehicle"],
            ["NO INFO",
                "Light",
                "Small",
                "Large",
                "High Vortex Large",
                "Heavy",
                "High Performance, High Speed"
                "Rotorcraft",]
        ][r["EMITTER_CATEGORY"]][r["TYPE"]-1][r["EMITTER_CATEGORY"]],
        "ID": LETTERLIST[r["CHARACTER_1"]] +
        LETTERLIST[r["CHARACTER_2"]] +
        LETTERLIST[r["CHARACTER_3"]] +
        LETTERLIST[r["CHARACTER_4"]] +
        LETTERLIST[r["CHARACTER_5"]] +
        LETTERLIST[r["CHARACTER_6"]] +
        LETTERLIST[r["CHARACTER_7"]] +
        LETTERLIST[r["CHARACTER_8"]]
    }


def _9(bdsdata: bytes) -> dict:
    # 0,9 — Extended squitter airborne velocity
    r = extract_bit(bdsdata, 6, 8)
    if r["SUBTYPE"] == 1 or r["SUBTYPE"] == 2:
        return _9a(bdsdata)
    elif r["SUBTYPE"] == 3 or r["SUBTYPE"] == 4:
        return _9b(bdsdata)
    else:
        return None


def _9a(bdsdata: bytes) -> dict:
    # 0,9a — Extended squitter airborne velocity, ground
    ranges = {
        "TYPE": [1, 5],
        "SUBTYPE": [6, 8],
        "INTENT_CHANGE_FLAG": [9, 9],
        "IFR_CAPACITY_FLAG": [10, 10],
        "NUC_R": [11, 13],
        "DIR_EW_V": [14, 14],
        "EW_V": [15, 24],
        "DIR_NS_V": [25, 25],
        "NS_V": [26, 35],
        "SOURCE_VERT_RATE": [36, 36],
        "SIGN_VERT_RATE": [37, 37],
        "VERT_RATE": [38, 46],  # 47-48 reserved
        "GNSS_ALT_SIGN": [49, 49],
        "GNSS_ALT_DIFF_FROM_BARO_ALT": [50, 56]
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)
    supersonic = r["SUBTYPE"] & 1
    speedbase = 4 if supersonic else 1
    return {
        "subtype": "Ground Speed, " + ("Normal" if supersonic else "Supersonic"),
        "intent change": r["INTENT_CHANGE_FLAG"],
        "IFR capacity": r["IFR_CAPACITY_FLAG"],
        "NUC_R": ["Unknown",
                  "H. < 10 m/s, V. < 15.2 m/s (50fps)",
                  "H. < 3 m/s, V. < 4.6 m/s (15fps)",
                  "H. < 1 m/s, V. < 1.5 m/s (5fps)",
                  "H. < 0.3 m/s, V. < 0.46 m/s (1.5fps)"][r["NUC_R"]],
        "EW Direction": ["East", "West"][r["DIR_EW_V"]],
        "EW Velocity": "NO INFO" if r["EW_V"] == 0 else "> "+str(1021.5*speedbase)+" kt" if r["EW_V"] == 1023 else str((r["EW_V"]-1)*speedbase) + " kt",
        "NS Direction": ["North", "South"][r["DIR_NS_V"]],
        "NS Velocity": "NO INFO" if r["NS_V"] == 0 else "> "+str(1021.5*speedbase)+" kt" if r["NS_V"] == 1023 else str((r["NS_V"]-1)*speedbase) + " kt",
        "Source of vertical rate": ["GNSS", "Baro"][r["SOURCE_VERT_RATE"]],
        "Sign of vertical rate": ["Up", "Down"][r["SIGN_VERT_RATE"]],
        "Vertical rate": "NO INFO" if r["VERT_RATE"] == 0 else "> 32608 ft/min" if r["VERT_RATE"] == 511 else str((r["VERT_RATE"]-1)*64) + " ft/min",
        "GNSS alt. sign": ["Above baro alt.", "Below baro alt."][r["GNSS_ALT_SIGN"]],
        "GNSS alt. difference from baro. alt.": "NO INFO" if r["GNSS_ALT_DIFF_FROM_BARO_ALT"] == 0 else "> 3137.5 ft" if r["GNSS_ALT_DIFF_FROM_BARO_ALT"] == 127 else str((r["GNSS_ALT_DIFF_FROM_BARO_ALT"]-1)*25) + " ft"
    }


def _9b(bdsdata: bytes) -> dict:
    # 0,9b — Extended squitter airborne velocity, air
    ranges = {
        "TYPE": [1, 5],
        "SUBTYPE": [6, 8],
        "INTENT_CHANGE_FLAG": [9, 9],
        "IFR_CAPACITY_FLAG": [10, 10],
        "NUC_R": [11, 13],
        "STATUS": [14, 14],
        "MAGNETIC_HEADING": [15, 24],
        "AIRSPEED_TYPE": [25, 25],
        "AIRSPEED": [26, 35],
        "SOURCE_VERT_RATE": [36, 36],
        "SIGN_VERT_RATE": [37, 37],
        "VERT_RATE": [38, 46],  # 47-48 reserved
        "DIFF_SIGN": [49, 49],
        "GEO_HEIGHT_DIFF_FROM_BARO_ALT": [50, 56]
    }
    # info in number format
    r = ranges_to_bytes(bdsdata, ranges)
    supersonic = r["SUBTYPE"] & 1
    speedbase = 4 if supersonic else 1
    return {
        "subtype": "Air Speed, " + ("Normal" if supersonic else "Supersonic"),
        "intent change": r["INTENT_CHANGE_FLAG"],
        "IFR capacity": r["IFR_CAPACITY_FLAG"],
        "NUC_R": ["Unknown",
                  "H. < 10 m/s, V. < 15.2 m/s (50fps)",
                  "H. < 3 m/s, V. < 4.6 m/s (15fps)",
                  "H. < 1 m/s, V. < 1.5 m/s (5fps)",
                  "H. < 0.3 m/s, V. < 0.46 m/s (1.5fps)"][r["NUC_R"]],
        "Status": ["Magnetic heading not available", "Available"][r["STATUS"]],
        "Magnetic heading": str((r["MAGNETIC_HEADING"])*360/1024) + "°",
        "Airspeed type": ["IAS", "TAS"][r["AIRSPEED_TYPE"]],
        "Airspeed": "NO INFO" if r["AIRSPEED"] == 0 else "> "+str(1021.5*speedbase)+" kt" if r["AIRSPEED"] == 1023 else str((r["AIRSPEED"]-1)*speedbase) + " kt",
        "Source of vertical rate": ["GNSS", "Baro"][r["SOURCE_VERT_RATE"]],
        "Sign of vertical rate": ["Up", "Down"][r["SIGN_VERT_RATE"]],
        "Vertical rate": "NO INFO" if r["VERT_RATE"] == 0 else "> 32608 ft/min" if r["VERT_RATE"] == 511 else str((r["VERT_RATE"]-1)*64) + " ft/min",
        "Diff sign": ["Above baro alt.", "Below baro alt."][r["DIFF_SIGN"]],
        "Geo height diff. from baro. alt.": "NO INFO" if r["GEO_HEIGHT_DIFF_FROM_BARO_ALT"] == 0 else "> 3137.5 ft" if r["GEO_HEIGHT_DIFF_FROM_BARO_ALT"] == 127 else str((r["GEO_HEIGHT_DIFF_FROM_BARO_ALT"]-1)*25) + " ft"
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


BDS_TYPE_MAPPING = [
    None, None, None, None, None, _5, _6, _7, _8, _9, _10, _11, _12, None, None, None,
    _16, None, None, None, None, None, None, _23, _24, _25, _26, _27, _28, _29, _30, _31,
    _32, _33, _34, None, None, _37, None, None, None, None, None, None, None, None, None, None,
    _48, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    _64, _65, _66, _67, _68, _69, None, None, _72, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None,
    None, None, None, None, None, None, None, None, None, None, None, None, None, None, None, None
]


def decode(bdsdata: bytes, bdscode: int) -> (list | None):
    """
    BDS(7bytes), BDSCODE 0-255
    """
    f = BDS_TYPE_MAPPING[bdscode]
    if f is None:
        print(f"Error: BDS {bdscode} no soportado")
        return None
    message = f(bdsdata)
    if message is None:
        print("Error: error en decodificación")
        return None
    return message
