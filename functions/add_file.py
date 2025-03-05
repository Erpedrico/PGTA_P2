import struct
from tkinter import filedialog, messagebox
from functions.extract_packets import parse_binary_file 

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
            cat = packet[0]  # Primer byte = Categoría
            length = int.from_bytes(packet[1:3], byteorder='big')  # Longitud del paquete
            datos_hex = packet.hex()[:50] + "..." if len(packet) > 25 else packet.hex()  # Recortar datos largos
            tabla.insert("", "end", values=(i + 1, cat, length, datos_hex))

        messagebox.showinfo("Carga exitosa", f"Se han cargado {len(packets)} paquetes.")

    except Exception as e:
        messagebox.showerror("Error", f"No se pudo procesar el archivo.\n{str(e)}")
