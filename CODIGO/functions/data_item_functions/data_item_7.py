def data_item_7(packet):
    # Limpiar el paquete (eliminar caracteres no válidos)
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None
    
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return None
    
    # Verificar que hay al menos 1 octeto
    if len(packet_bytes) < 1:
        print("Error: Paquete demasiado corto")
        return None

    # Procesar el primer octeto (Primary Subfield)
    first_octet = packet_bytes[0]
    SRL = (first_octet >> 7) & 0b1  # bit 8
    SRR = (first_octet >> 6) & 0b1  # bit 7
    SAM = (first_octet >> 5) & 0b1  # bit 6
    PRL = (first_octet >> 4) & 0b1  # bit 5
    PAM = (first_octet >> 3) & 0b1  # bit 4
    RPD = (first_octet >> 2) & 0b1  # bit 3
    APD = (first_octet >> 1) & 0b1  # bit 2
    FX = first_octet & 0b1          # bit 1

    # Diccionario para almacenar los resultados
    radar_plot_characteristics = {
        "SRL": "Subfield #1 (SSR Plot Runlength) present" if SRL else "Subfield #1 absent",
        "SRR": "Subfield #2 (Number of Received Replies for MSSR) present" if SRR else "Subfield #2 absent",
        "SAM": "Subfield #3 (Amplitude of MSSR Reply) present" if SAM else "Subfield #3 absent",
        "PRL": "Subfield #4 (PSR Plot Runlength) present" if PRL else "Subfield #4 absent",
        "PAM": "Subfield #5 (PSR Amplitude) present" if PAM else "Subfield #5 absent",
        "RPD": "Subfield #6 (Difference in Range between PSR and SSR plot) present" if RPD else "Subfield #6 absent",
        "APD": "Subfield #7 (Difference in Azimuth between PSR and SSR plot) present" if APD else "Subfield #7 absent",
        "FX": "Extension into next octet" if FX else "End of Primary Subfield"
    }

    print(radar_plot_characteristics)

    radar_plot = []
    octet_index = 1
    
    # Procesar extensiones si FX=1
    while FX == 1 and octet_index < len(packet_bytes):
        current_octet = packet_bytes[octet_index]
        FX = current_octet & 0b1  # Verificar si hay más extensiones
        
        # Procesar subcampos si están presentes
        # Subfield #1: SSR Plot Runlength (0.044 * N, donde N es el valor del octeto)
        if SRL and octet_index < len(packet_bytes):
            srl_value = packet_bytes[octet_index]
            radar_plot.append(srl_value * 0.044)  # Convertir a microsegundos
            octet_index += 1

        # Subfield #2: Number of Received Replies for MSSR
        if SRR and octet_index < len(packet_bytes):
            srr_value = packet_bytes[octet_index]
            radar_plot.append(srr_value)
            octet_index += 1

        # Subfield #3: Amplitude of MSSR Reply (en complemento A2)
        if SAM and octet_index < len(packet_bytes):
            sam_value = packet_bytes[octet_index]
            if sam_value & 0b10000000:  # Si el bit de signo está activo
                sam_value = sam_value - 256  # Convertir a negativo (complemento A2)
            radar_plot.append(sam_value)  # Valor en dBm
            octet_index += 1

        # Subfield #4: PSR Plot Runlength (0.044 * N)
        if PRL and octet_index < len(packet_bytes):
            prl_value = packet_bytes[octet_index]
            radar_plot.append(prl_value * 0.044)  # Convertir a microsegundos
            octet_index += 1

        # Subfield #5: PSR Amplitude (en complemento A2)
        if PAM and octet_index < len(packet_bytes):
            pam_value = packet_bytes[octet_index]
            if pam_value & 0b10000000:  # Si el bit de signo está activo
                pam_value = pam_value - 256  # Convertir a negativo (complemento A2)
            radar_plot.append(pam_value)  # Valor en dBm
            octet_index += 1

        # Subfield #6: Difference in Range between PSR and SSR plot (en complemento A2)
        if RPD and octet_index < len(packet_bytes):
            rpd_value = packet_bytes[octet_index]
            if rpd_value & 0b10000000:  # Si el bit de signo está activo
                rpd_value = rpd_value - 256  # Convertir a negativo (complemento A2)
            radar_plot.append(rpd_value / 256.0)  # Convertir a NM
            octet_index += 1

        # Subfield #7: Difference in Azimuth between PSR and SSR plot (en complemento A2)
        if APD and octet_index < len(packet_bytes):
            apd_value = packet_bytes[octet_index]
            if apd_value & 0b10000000:  # Si el bit de signo está activo
                apd_value = apd_value - 256  # Convertir a negativo (complemento A2)
            radar_plot.append(apd_value * (360.0 / 16384.0))  # Convertir a grados
            octet_index += 1

    return radar_plot