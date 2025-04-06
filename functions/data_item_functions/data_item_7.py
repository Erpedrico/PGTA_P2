def data_item_7(packet): 
     # Limpiar el paquete (eliminar caracteres no válidos)
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return None
    
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
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

    octet_index=1
    radar_plot=[]
    while FX ==1:
        # Procesar subcampos si están presentes
        # Subfield #1: SSR Plot Runlength
        if SRL and octet_index < len(packet_bytes):
            srl_octet = packet_bytes[octet_index]
            srl_value = srl_octet  # Valor binario de SRL
            radar_plot.append(srl_value * 0.044)
            octet_index += 1

        # Subfield #2: Number of Received Replies for MSSR
        if SRR and octet_index < len(packet_bytes):
            srr_octet = packet_bytes[octet_index]
            srr_value = srr_octet  # Valor binario de SRR
            radar_plot.append(srr_value)
            octet_index += 1

        # Subfield #3: Amplitude of MSSR Reply
        if SAM and octet_index < len(packet_bytes):
            sam_octet = packet_bytes[octet_index]
            sam_value = sam_octet  # Valor binario de SAM
            radar_plot.append(sam_value)
            octet_index +=1

        # Subfield #4: PSR Plot Runlength
        if PRL and octet_index < len(packet_bytes):
            prl_octet = packet_bytes[octet_index]
            prl_value = prl_octet  # Valor binario de PRL
            radar_plot.append(prl_value * 0.044)
            octet_index += 1

        # Subfield #5: PSR Amplitude
        if PAM and octet_index < len(packet_bytes):
            pam_octet = packet_bytes[octet_index]
            pam_value = pam_octet  # Valor binario de PAM
            radar_plot.append(pam_value)
            octet_index += 1

        # Subfield #6: Difference in Range between PSR and SSR plot
        if RPD and octet_index < len(packet_bytes):
            rpd_octet = packet_bytes[octet_index]
            rpd_value = rpd_octet  # Valor binario de RPD
            radar_plot.append(rpd_value)
            octet_index += 1

        # Subfield #7: Difference in Azimuth between PSR and SSR plot
        if APD and octet_index < len(packet_bytes):
            apd_octet = packet_bytes[octet_index]
            apd_value = apd_octet  # Valor binario de APD
            radar_plot.append(apd_value)
            octet_index += 1
        
        current_octet = packet_bytes[octet_index]
        FX = current_octet & 0b1  # Verificar si hay más extensiones

    return radar_plot
#preguntar lo del complemento A2 (acabar esto!)

