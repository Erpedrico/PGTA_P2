"""
Data Item I048/250 - BDS Register Data
Implementación exacta según estructura C# con tus nombres de campos
"""

def data_item_10(packet: str) -> list:
    """
    Procesa el Data Item I048/250 (BDS Register Data)
    Devuelve: [REP, (12 campos BDS4.0), (10 campos BDS5.0), (10 campos BDS6.0)]

    """
    try:
        # Limpieza básica del paquete
        cleaned = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
        if len(cleaned) % 2 != 0:
            return ["0"] + ["Not found"]*32
        
        packet_bytes = bytes.fromhex(cleaned)
        if len(packet_bytes) < 1:
            return ["0"] + ["Not found"]*32

        rep = packet_bytes[0]
        result = [str(rep)]
        packet_bytes = packet_bytes[1:]

        # Bandera para cada BDS
        has_bds40, has_bds50, has_bds60 = False, False, False

        for _ in range(rep):
            if len(packet_bytes) < 8:
                break

            bds_data = packet_bytes[:7]
            bds_code = packet_bytes[7]
            packet_bytes = packet_bytes[8:]

            bds1 = (bds_code >> 4) & 0x0F
            bds2 = bds_code & 0x0F

            if bds1 == 4 and bds2 == 0 and not has_bds40:
                # Decodificación BDS 4.0 
                data = int.from_bytes(bds_data, 'big')
                result.extend([
                    "1" if (data >> 55) & 0b1 else "0",       # MCP_STATUS (bit 55)
                    str(((data >> 43) & 0xFFF) * 16),         # MCP_ALT (bits 43-54)
                    "1" if (data >> 42) & 0b1 else "0",       # FMS_STATUS (bit 42)
                    str(((data >> 30) & 0xFFF) * 16),         # FMS_ALT (bits 30-41)
                    "1" if (data >> 29) & 0b1 else "0",       # BP_STATUS (bit 29)
                    f"{((data >> 17) & 0xFFF) * 0.1 + 800.0:.1f}",  # BP_VALUE (bits 17-28)
                    "1" if (data >> 8) & 0b1 else "0",        # MODE_STATUS (bit 8)
                    "1" if (data >> 7) & 0b1 else "0",        # VNAV (bit 7)
                    "1" if (data >> 6) & 0b1 else "0",        # ALTHOLD (bit 6)
                    "1" if (data >> 5) & 0b1 else "0",        # APP (bit 5)
                    "1" if (data >> 2) & 0b1 else "0",        # TARGETALT_STATUS (bit 2)
                    ["Unknown", "Aircraft", "FCU/MCP", "FMS"][data & 0b11]  # TARGETALT_SOURCE (bits 0-1)
                ])
                has_bds40 = True

            elif bds1 == 5 and bds2 == 0 and not has_bds50:
                # Decodificación BDS 5.0 
                data = int.from_bytes(bds_data, 'big')
                result.extend([
                    "1" if (data >> 55) & 0b1 else "0",       # ROLL_STATUS (bit 55)
                    f"{(-1 if (data >> 54) & 0b1 else 1) * ((data >> 45) & 0x1FF) * (45.0/256.0):.3f}",  # ROLL_ANGLE (bits 45-53 + signo 54)
                    "1" if (data >> 44) & 0b1 else "0",       # TRACK_STATUS (bit 44)
                    f"{(-1 if (data >> 43) & 0b1 else 1) * ((data >> 33) & 0x3FF) * (90.0/512.0):.3f}",  # TRUE_TRACK (bits 33-42 + signo 43)
                    "1" if (data >> 32) & 0b1 else "0",       # GROUNDSPEED_STATUS (bit 32)
                    str(((data >> 22) & 0x3FF) * 2),          # GROUNDSPEED  (bits 22-31)
                    "1" if (data >> 21) & 0b1 else "0",       # TRACKRATE_STATUS (bit 21)
                    f"{(-1 if (data >> 20) & 0b1 else 1) * ((data >> 11) & 0x1FF) * (8.0/256.0):.3f}",  # TRACK_RATE (bits 11-19 + signo 20)
                    "1" if (data >> 10) & 0b1 else "0",       # AIRSPEED_STATUS (bit 10)
                    str((data & 0x3FF) * 2)                   # TRUE_AIRSPEED (bits 0-9)
                ])
                has_bds50 = True

            elif bds1 == 6 and bds2 == 0 and not has_bds60:
                # Decodificación BDS 6.0
                data = int.from_bytes(bds_data, 'big')
                result.extend([
                    "1" if (data >> 55) & 0b1 else "0",       # HEADING_STATUS (bit 55)
                    f"{(-1 if (data >> 54) & 0b1 else 1) * ((data >> 44) & 0x3FF) * (90.0/512.0):.6f}",  # MAG_HEADING (bits 44-53 + signo 54)
                    "1" if (data >> 43) & 0b1 else "0",       # IAS_STATUS (bit 43)
                    str((data >> 33) & 0x3FF),                # IAS (bits 33-42)
                    "1" if (data >> 32) & 0b1 else "0",       # MACH_STATUS (bit 32)
                    f"{((data >> 22) & 0x3FF) * (2.048/512.0):.3f}",  # MACH (bits 22-31)
                    "1" if (data >> 21) & 0b1 else "0",       # BARO_RATE_STATUS (bit 21)
                    str(int((-1 if (data >> 20) & 0b1 else 1) * ((data >> 11) & 0x1FF) * 32)),  # BARO_RATE (bits 11-19 + signo 20)
                    "1" if (data >> 10) & 0b1 else "0",       # INERTIAL_VERT_STATUS (bit 10)
                    str(int((-1 if (data >> 9) & 0b1 else 1) * (data & 0x1FF) * 32))  # INERTIAL_VERT_VEL (bits 0-8 + signo 9)
                ])
                has_bds60 = True

        # Rellenar con Not found los BDS no encontrados
        if not has_bds40:
            result.extend(["Not found"]*12)
        if not has_bds50:
            result.extend(["Not found"]*10)
        if not has_bds60:
            result.extend(["Not found"]*10)

        return result

    except Exception:
        return ["0"] + ["Not found"]*32  # REP=0 + 32 campos Not found en caso de error















