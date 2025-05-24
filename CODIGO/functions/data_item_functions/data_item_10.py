def data_item_10(packet: str) -> list:
    """
    Procesa el Data Item I048/250 (BDS Register Data)
    Devuelve: [REP, (12 campos BDS4.0), (10 campos BDS5.0), (10 campos BDS6.0)]
    """
    try:
        cleaned = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
        if len(cleaned) % 2 != 0:
            return ["0"] + ["NA"]*32
        
        packet_bytes = bytes.fromhex(cleaned)
        if len(packet_bytes) < 1:
            return ["0"] + ["NA"]*32

        rep = packet_bytes[0]
        result = [str(rep)] + ["NA"]*32  # Inicializa con "NA"

        packet_bytes = packet_bytes[1:]

        for _ in range(rep):
            if len(packet_bytes) < 8:
                break

            bds_data = packet_bytes[:7]
            bds_code = packet_bytes[7]
            packet_bytes = packet_bytes[8:]

            bds1 = (bds_code >> 4) & 0x0F
            bds2 = bds_code & 0x0F

            if bds1 == 4 and bds2 == 0:
                data = int.from_bytes(bds_data, 'big')
                result[1:13] = [
                    "1" if (data >> 55) & 0b1 else "0",
                    str(((data >> 43) & 0xFFF) * 16),
                    "1" if (data >> 42) & 0b1 else "0",
                    str(((data >> 30) & 0xFFF) * 16),
                    "1" if (data >> 29) & 0b1 else "0",
                    f"{((data >> 17) & 0xFFF) * 0.1 + 800.0:.1f}",
                    "1" if (data >> 8) & 0b1 else "0",
                    "1" if (data >> 7) & 0b1 else "0",
                    "1" if (data >> 6) & 0b1 else "0",
                    "1" if (data >> 5) & 0b1 else "0",
                    "1" if (data >> 2) & 0b1 else "0",
                    ["Unknown", "Aircraft", "FCU/MCP", "FMS"][data & 0b11]
                ]

            elif bds1 == 5 and bds2 == 0:
                data = int.from_bytes(bds_data, 'big')

                # Bit 55: ROLL_STATUS
                roll_status = "1" if (data >> 55) & 0b1 else "0"

                # Bits 54-45: ROLL_ANGLE (10 bits signed)
                raw_roll = (data >> 45) & 0x3FF
                if raw_roll & (1 << 9):  # check sign bit
                    raw_roll -= (1 << 10)
                roll_angle = f"{raw_roll * (45.0 / 256.0):.3f}"

                # Bit 44: TRACK_STATUS
                track_status = "1" if (data >> 44) & 0b1 else "0"

                # Bits 43-33: TRUE_TRACK (11 bits signed)
                raw_track = (data >> 33) & 0x7FF
                if raw_track & (1 << 10):
                    raw_track -= (1 << 11)
                true_track = f"{raw_track * (90.0 / 512.0):.3f}"

                # Bit 32: GROUNDSPEED_STATUS
                gs_status = "1" if (data >> 32) & 0b1 else "0"

                # Bits 22–31: GROUNDSPEED
                groundspeed = str(((data >> 22) & 0x3FF) * 2)

                # Bit 21: TRACKRATE_STATUS
                tr_status = "1" if (data >> 21) & 0b1 else "0"

                # Bits 20–11: TRACK_RATE (10 bits signed)
                raw_tr = (data >> 11) & 0x3FF
                if raw_tr & (1 << 9):
                    raw_tr -= (1 << 10)
                track_rate = f"{raw_tr * (8.0 / 256.0):.3f}"

                # Bit 10: AIRSPEED_STATUS
                airspeed_status = "1" if (data >> 10) & 0b1 else "0"

                # Bits 0–9: TRUE_AIRSPEED
                true_airspeed = str((data & 0x3FF) * 2)

                result[13:23] = [
                    roll_status,
                    roll_angle,
                    track_status,
                    true_track,
                    gs_status,
                    groundspeed,
                    tr_status,
                    track_rate,
                    airspeed_status,
                    true_airspeed
                ]



            elif bds1 == 6 and bds2 == 0:
                data = int.from_bytes(bds_data, 'big')

                # Bit 55: HEADING_STATUS
                heading_status = "1" if (data >> 55) & 0b1 else "0"

                # Bits 54–44: MAG_HEADING (11-bit signed)
                raw_heading = (data >> 44) & 0x7FF
                if raw_heading & (1 << 10):  # check sign bit
                    raw_heading -= (1 << 11)
                mag_heading = f"{raw_heading * (90.0 / 512.0):.6f}"

                # Bit 43: IAS_STATUS
                ias_status = "1" if (data >> 43) & 0b1 else "0"

                # Bits 42–33: IAS (10 bits unsigned)
                ias = str((data >> 33) & 0x3FF)

                # Bit 32: MACH_STATUS
                mach_status = "1" if (data >> 32) & 0b1 else "0"

                # Bits 31–22: MACH (10 bits unsigned)
                mach = f"{((data >> 22) & 0x3FF) * (2.048 / 512.0):.3f}"

                # Bit 21: BARO_RATE_STATUS
                baro_status = "1" if (data >> 21) & 0b1 else "0"

                # Bits 20–11: BARO_RATE (10-bit signed)
                raw_baro = (data >> 11) & 0x3FF
                if raw_baro & (1 << 9):
                    raw_baro -= (1 << 10)
                baro_rate = str(int(raw_baro * 32))

                # Bit 10: INERTIAL_V_STATUS
                iv_status = "1" if (data >> 10) & 0b1 else "0"

                # Bits 9–0: INERTIAL_VERTICAL (10-bit signed)
                raw_iv = data & 0x3FF
                if raw_iv & (1 << 9):
                    raw_iv -= (1 << 10)
                inertial_v = str(int(raw_iv * 32))

                result[23:33] = [
                    heading_status,
                    mag_heading,
                    ias_status,
                    ias,
                    mach_status,
                    mach,
                    baro_status,
                    baro_rate,
                    iv_status,
                    inertial_v
                ]


        return result

    except Exception:
        return ["0"] + ["NA"]*32















