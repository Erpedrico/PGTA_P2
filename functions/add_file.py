import struct
from tkinter import filedialog, messagebox
from functions.extract_packets import parse_binary_file
from functions.extract_data import extraer_datos

def add_file(tabla):
    file_path = filedialog.askopenfilename(filetypes=[("Archivos binarios", "*.ast"), ("Todos los archivos", "*.*")])
    if not file_path:
        return

    try:
        packets = parse_binary_file(file_path)

        if not packets:
            messagebox.showinfo("Archivo vacío", "El archivo seleccionado no contiene paquetes válidos.")
            return

        # Limpiar la tabla antes de agregar nuevos datos
        for row in tabla.get_children():
            tabla.delete(row)

        # Agregar los paquetes a la tabla
        for i, packet in enumerate(packets):
            # Asumimos que `packet` es una lista de datos donde los índices representan las columnas
            cat = packet[0]  # Primer byte = Categoría
            length = int.from_bytes(packet[1:3], byteorder='big')  # Longitud del paquete (bytes 1-2)
            datos_hex = packet.hex()[:50] + "..." if len(packet) > 25 else packet.hex()  # Recortar datos largos

            # Tomamos el resto de los datos después del índice 3 (de acuerdo con las nuevas columnas)
            packet_data = packet[3:]  # El resto de los datos que queremos extraer

            # Convertimos el paquete a hexadecimal y lo procesamos
            datos_extraidos = extraer_datos(bytes(packet_data))

            # Si no se pudo extraer correctamente los datos, usamos "Not Found" como valor por defecto
            if not isinstance(datos_extraidos, dict):
                datos_extraidos = {col: "Not Found bad" for col in datos_extraidos}

            # Agregar fila a la tabla con los nuevos datos
            fila = [i + 1, cat, length, datos_hex] + [datos_extraidos.get(col, "N/A") for col in datos_extraidos]

            # Insertamos la fila en la tabla
            tabla.insert("", "end", values=fila)

        messagebox.showinfo("Carga exitosa", f"Se han cargado {len(packets)} paquetes.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo.\n{str(e)}")


