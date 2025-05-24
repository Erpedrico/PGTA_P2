#Lo puedo mejorar con la librería bitstring
def data_item_3(packet):
    
    cleaned_packet = "".join(c for c in packet if c in "0123456789abcdefABCDEF")
    # Verificar si la cadena limpia tiene una longitud par
    if len(cleaned_packet) % 2 != 0:
        print(f"Error: La cadena hexadecimal tiene longitud impar: {cleaned_packet}")
        return
    # Convertir la cadena hexadecimal limpia a bytes
    try:
        packet_bytes = bytes.fromhex(cleaned_packet)  # Convierte la cadena hexadecimal a bytes
    except ValueError as e:
        print(f"Error al convertir el paquete hexadecimal: {e}")
        return
  
    
    first_octet= packet_bytes[0]
    TYP = (first_octet >> 5) & 0b111  # bits 8-6
    SIM = (first_octet >> 4) & 0b1    # bit 5
    RDP = (first_octet >> 3) & 0b1    # bit 4
    SPI = (first_octet >> 2) & 0b1    # bit 3
    RAB = (first_octet >> 1) & 0b1    # bit 2
    FX = first_octet & 0b1            # bit 1     


    TYP_mapping = {
        0: "No detection", 
        1: "Single PSR detection", 
        2: "Single SSR detection", 
        3: "SSR + PSR detection", 
        4: "Single ModeS All-Call",
        5: "Single ModeS Roll-Call",
        6: "ModeS All-Call + PSR",
        7: "ModeS Roll-Call + PSR"
    }
   
    TargetReportDescriptor=[]

    #Procesar los campos del primer octeto
    TargetReportDescriptor.append(TYP_mapping.get(TYP, "Unknown TYP value"))
    TargetReportDescriptor.append("Simulated" if SIM else "Actual Target Report")
    TargetReportDescriptor.append("RDP Chain 2" if RDP else "RDP Chain 1")
    TargetReportDescriptor.append("Special Position Identification" if SPI else "Absence of SPI")
    TargetReportDescriptor.append("Report from field monitor" if RAB else "Report from aircraft transponder")
    TargetReportDescriptor.append("Extension into first extent" if FX else "End of Data Item")

    
    octet_index =1
    # Procesar extensiones FX (octetos adicionales) 
    while FX == 1 and octet_index < len(packet_bytes):  
            current_octet = packet_bytes[octet_index]
            if octet_index ==1:

                # Extraer bits específicos del octeto actual
                TST = (current_octet >> 7) & 0b1    # bit 8
                ERR = (current_octet >> 6) & 0b1    # bit 7
                XPP = (current_octet >> 5) & 0b1    # bit 6
                ME  = (current_octet >> 4) & 0b1    # bit 5
                MI  = (current_octet >> 3) & 0b1    # bit 4
                FOE_FRI = (current_octet >> 1) & 0b11  # bits 3-2
                FX_ext = current_octet & 0b1        # bit 1 (FX de la extensión)

                # Mapeo de FOE/FRI
                FOE_FRI_mapping = {
                    0: "No Mode 4 interrogation",
                    1: "Friendly target",
                    2: "Unknown target",
                    3: "No reply"
                }

                # Agregar los valores de la extensión a Target Report Descriptor
                TargetReportDescriptor.append("Test target report" if TST else "Real target report")
                TargetReportDescriptor.append("Extended Range present" if ERR else "No Extended Range")
                TargetReportDescriptor.append("X-Pulse present" if XPP else "No X-Pulse present")
                TargetReportDescriptor.append("Military emergency" if ME else "No military emergency")
                TargetReportDescriptor.append("Military identification" if MI else "No military identification")
                TargetReportDescriptor.append(FOE_FRI_mapping.get(FOE_FRI, "Unknown FOE/FRI value"))
                TargetReportDescriptor.append("Extension into next extent" if FX_ext else "End of Data Item")
                
                FX=FX_ext
                
                       
            else:
                # Extraer bits específicos del tercer octeto
                ADSB = (current_octet >> 7) & 0b1    # bit 8
                SCN = (current_octet >> 6) & 0b1     # bit 7
                PAI = (current_octet >> 5) & 0b1     # bit 6
                FX_second_ext = current_octet & 0b1  # bit 1 (FX de la segunda extensión)

                # Agregar los valores de la segunda extensión a Target Report Descriptor
                TargetReportDescriptor.append("On-Site ADS-B Information available" if ADSB else "On-Site ADS-B Information not available")
                TargetReportDescriptor.append("Surveillance Cluster Network Information available" if SCN else "Surveillance Cluster Network Information not available")
                TargetReportDescriptor.append("Passive Acquisition Interface Information available" if PAI else "Passive Acquisition Interface Information not available")
                TargetReportDescriptor.append("Extension into next extent" if FX_second_ext else "End of Data Item")
                FX=FX_second_ext

            
            # Incrementar el índice para procesar el siguiente octeto
            octet_index += 1   
                
        
    return TargetReportDescriptor



        
        


   


    
