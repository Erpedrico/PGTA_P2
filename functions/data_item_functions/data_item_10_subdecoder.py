
LETTERLIST = ['', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O',
              'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z',  '',  '',  '',  '',  '',
              ' ',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',  '',
              '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',  '',  '',  '',  '',  '',  '']
# map type code to their decoder functions


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


'''
def _5(bdsdata: bytes) -> dict:
    # 0,5 — Extended squitter airborne position
    ranges = {
        "TYPE": [1, 5],
        "SURVEILLANCE": [6, 7],
        "SAF": [8, 8],
        "ALTITUDE": [9, 20],
        "TIME": [21, 21],
        "CPR_FORMAT": [22, 22],
        "LATITUDE": [23, 39],
        "LONGITUDE": [40, 56]
    }
    r = ranges_to_bytes(bdsdata, ranges)

    def gray_to_binary(n):
        result = n
        while n > 0:
            n >>= 1
            result ^= n
        return result

    def ac_decode(v):
        # ignore M(6) 0, Q(8-1) 0:100ft, 1:25ft
        # Q0:  C1, A1, C2, A2, C4, A4, (ZERO,) B1, ZERO, B2, D2, B4, D4
        # D2 D4 A1 A2 A4 B1 B2 B4 Gray code, C4 C1 C2 follow decoder
        # Q1:  0 to 5, 7-1 and 9-1 to 12-1
        if v & 0x010:
            return str(25*((v & 0xFE0) >> 1 + (v & 0x00F)))
        else:
            case_odd = [None, 4, 2, 3, 0, None, 1]  # odd 4 6 2 3 1
            case_even = [None, 0, 2, 1, 4, None, 3]  # even 1 3 2 6 4
            C1 = (v & 0b100000000000) >> 11
            A1 = (v & 0b010000000000) >> 10
            C2 = (v & 0b001000000000) >> 9
            A2 = (v & 0b000100000000) >> 8
            C4 = (v & 0b000010000000) >> 7
            A4 = (v & 0b000001000000) >> 6
            B1 = (v & 0b000000100000) >> 5
            B2 = (v & 0b000000001000) >> 3
            D2 = (v & 0b000000000100) >> 2
            B4 = (v & 0b000000000010) >> 1
            D4 = (v & 0b000000000001)
            # base gray code
            G = D2 << 7 | D4 << 6 | A1 << 5 | A2 << 4 | A4 << 3 | B1 << 2 | B2 << 1 | B4
            G = gray_to_binary(G)
            # delta (inc) some special coding rule
            d = C1 << 2 | C2 << 1 | C4
            if B4:  # odd
                G = - 1200 + 500*G  # left boundary
                G += 100*case_odd[d]
            else:  # even
                G = 1200 - 500*G
                G += 100*case_even[d]
            if G <= -1000:
                return "-1000 to -950 ft"
            elif G >= 126650:
                return "126650 to 126750 ft"
            else:
                return str(G) + " to " + str(G+100) + " ft"

    return {
        "name": "Extended squitter Airborne Position",
        "Surveillance status": ["no condition", "permanent alert", "temporary alert", "SPI condition"][r["SURVEILLANCE"]],
        "SAF": ["dual antenna", "single antenna"][r["SAF"]],
        "Altitude": ac_decode(r["ALTITUDE"]),
        "Time": ["not sync. UTC", "sync. UTC"][r["TIME"]],
        "CPR format": r["CPR_FORMAT"],  # int 0 or 1
        "Latitude": r["LATITUDE"],
        "Longitude": r["LONGITUDE"]
    }


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

    def movement_decoder(m: int) -> str:
        if m == 0:
            return "No info"
        elif m == 1:
            return "Stopped (<0.125kt)"
        elif m <= 8:
            return str(0.125+(m-2)*0.125) + " kt"
        elif m <= 12:
            return str(1+(m-9)*0.25) + " kt"
        elif m <= 38:
            return str(2+(m-13)*0.5) + " kt"
        elif m <= 93:
            return str(15+(m-39)*1) + " kt"
        elif m <= 108:
            return str(70+(m-94)*2) + " kt"
        elif m <= 123:
            return str(100+(m-109)*5) + " kt"
        elif m == 124:
            return "> 175 kt"
        else:
            return "Reserved"

    return {
        "name": "Extended squitter Surface Position",
        "Movement": movement_decoder(r["MOVEMENT"]),
        "Status": ["Invalid", "Valid"][r["STATUS"]],
        "ground track": str(r["TRACK"]*360/128) + "°",
        "Time": ["not sync. UTC", "sync. UTC"][r["TIME"]],
        "CPR format": r["CPR_FORMAT"],  # int 0 or 1
        "Latitude": r["LATITUDE"],
        "Longitude": r["LONGITUDE"]
    }


def _7(bdsdata: bytes) -> dict:
    # BDS Code 0,7 — Extended squitter status
    ranges = {
        "TRANSMISSION_RATE": [1, 2],
        "ALTITUDE_TYPE": [3, 3]
        # reserved
    }
    r = ranges_to_bytes(bdsdata, ranges)
    return {
        "name": "Extended squitter status",
        "Transmission rate": ["No capacity to determine surface squitter rate",
                              "High surface squitter rate selected",
                              "Low surface squitter rate selected",
                              "Reserved"][r["TRANSMISSION_RATE"]],
        "Altitude type": ["Barometric altitude", "GNSS height"][r["ALTITUDE_TYPE"]]
    }


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
        "name": "Aircraft Identification and Category",
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
        "name": "Airborne Velocity, Ground",
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
        "name": "Airborne Velocity, Air",
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
'''


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
