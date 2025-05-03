from tkinter import filedialog, messagebox
from functions.extract_data import extraer_datos

DEBUG = False

def add_file(tabla):
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos binarios", "*.ast"), ("Todos los archivos", "*.*")]
    )

    if not file_path:
        return

    try:
        with open(file_path, "rb") as f:
            data = f.read()

        data_len = len(data)
        idx = 0
        packets = []

        append_packet = packets.append

        # Parsear en bloque
        while idx + 3 <= data_len:
            packet_len = int.from_bytes(data[idx+1:idx+3], byteorder="big")
            if packet_len <= 0 or idx + packet_len > data_len:
                break
            append_packet(data[idx:idx+packet_len])
            idx += packet_len


        if not packets:
            messagebox.showinfo("Archivo vacío", "El archivo seleccionado no contiene paquetes válidos.")
            return

        # Limpiar tabla
        tabla.delete(*tabla.get_children())

        insert_row = tabla.insert
        get_value = dict.get
        extend = list.extend

        columnas = [
            "NUM", "SAC", "SIC", "TIME", "TIME(s)", "Target report description", "Validated",
            "Garbled", "CodeSource", "Validated_FL", "Garbled_FL", "FL", "Mode3ACode", "Address",
            "ID", "BDS", "TRACK NUMBER", "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING", "LAT",
            "LON", "H", "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A", "B1B", "RHO", "THETA",
            "MCP_STATUS", "MCP_ALT", "FMS_STATUS", "FMS_ALT", "BP_STATUS", "BP_VALUE",
            "MODE_STATUS", "VNAV", "ALTHOLD", "APP", "TARGETALT_STATUS", "TARGETALT_SOURCE",
            "ROLL_STATUS", "ROLL_ANGLE", "TRACK_STATUS", "TRUE_TRACK", "GROUNDSPEED_STATUS", 
            "GROUNDSPEED", "TRACKRATE_STATUS", "TRACK_RATE", "AIRSPEED_STATUS", "TRUE_AIRSPEED",
            "HEADING_STATUS", "MAG_HEADING", "IAS_STATUS", "IAS", "MACH_STATUS", "MACH",
            "BARO_RATE_STATUS", "BARO_RATE", "INERTIAL_VERT_STATUS", "INERTIAL_VERT_VEL",  "FL_Corrected"
        ]

        for i, packet in enumerate(packets):
            cat = packet[0]
            length = int.from_bytes(packet[1:3], byteorder='big')
            hex_data = packet.hex()

            datos_extraidos = extraer_datos(hex_data)
            if not isinstance(datos_extraidos, dict):
                datos_extraidos = {}

            fila = [i + 1, cat, length]
            extend(fila, (get_value(datos_extraidos, col, "N/A") for col in columnas))
            insert_row("", "end", values=fila)


        messagebox.showinfo("Carga exitosa", f"Se han cargado {len(packets)} paquetes.")
        

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo.\n{e}")