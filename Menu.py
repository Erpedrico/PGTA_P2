import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import folium
import os
import webview
from functions.add_file import add_file
from functions.filter import filter_data
from functions.extract_data_fields import extract_data_fields

# Crear la ventana principal
root = tk.Tk()
root.title("Decodificador de ASTERIX")

# Abrir ventana en pantalla completa
root.attributes("-fullscreen", True)

# Quitar la barra de título predeterminada de la ventana
root.overrideredirect(True)

# Crear un mapa base (se abrirá en el navegador)
mapa = folium.Map(location=[20, 0], zoom_start=2)
mapa_path = "mapa.html"
mapa.save(mapa_path)

# Función para abrir el mapa en el navegador
def abrir_mapa():
    os.startfile(mapa_path)

# Función para abrir el mapa en ventana emergente
def abrir_mapa_webview():
    webview.create_window("Mapa Interactivo", mapa_path)
    webview.start()

# --------------------- Botones de control ---------------------
def cerrar_ventana():
    root.quit()

def minimizar_ventana():
    root.iconify()

def restaurar_ventana():
    if root.attributes("-fullscreen"):
        root.attributes("-fullscreen", False)
    else:
        root.attributes("-fullscreen", True)

# Frame para los botones de control
btns_frame = tk.Frame(root, bg="gray", relief="raised", bd=2)
btns_frame.pack(side="top", fill="x", padx=10)

# Botones de control de ventana (minimizar, restaurar y cerrar)
btn_minimizar = tk.Button(btns_frame, text="_", command=minimizar_ventana)
btn_restaurar = tk.Button(btns_frame, text="[]", command=restaurar_ventana)
btn_cerrar = tk.Button(btns_frame, text="X", command=cerrar_ventana)

# Posicionar los botones en el frame superior
btn_cerrar.pack(side="right", padx=5)
btn_restaurar.pack(side="right", padx=5)
btn_minimizar.pack(side="right", padx=5)

# --------------------- Función para cerrar la ventana ---------------------
def filtrar_datos():
    messagebox.showinfo("Filtrar", "Función de filtrado en construcción.")

# --------------------- Botones ---------------------
btn_frame = tk.Frame(root)
btn_frame.pack(side="top", pady=10, fill="x", padx=20)

btn_abrir = tk.Button(btn_frame, text="Abrir Mapa en Navegador", command=abrir_mapa)
btn_archivo = tk.Button(btn_frame, text="Añadir Archivo", command=lambda: add_file(tabla))  
btn_filtrar = tk.Button(btn_frame, text="Filtrar", command=filter_data)
btn_mapa_webview = tk.Button(btn_frame, text="Ver Mapa", command=abrir_mapa_webview)

# Posicionar botones de manera profesional
btn_abrir.grid(row=0, column=0, padx=10, pady=5, sticky="ew")
btn_archivo.grid(row=0, column=1, padx=10, pady=5, sticky="ew")
btn_filtrar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")
btn_mapa_webview.grid(row=0, column=3, padx=10, pady=5, sticky="ew")

# --------------------- Tabla para mostrar paquetes ---------------------
frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=20, fill="both", expand=True, padx=20)

# Crear tabla con Treeview
tabla = ttk.Treeview(frame_tabla, columns=("Paquete", "CAT", "LEN", "Datos"), show="headings")
tabla.heading("Paquete", text="N°")
tabla.heading("CAT", text="Categoría")
tabla.heading("LEN", text="Longitud")
tabla.heading("Datos", text="Datos (Hex)")

# Definir tamaños de columnas
tabla.column("Paquete", width=60, anchor="center")
tabla.column("CAT", width=80, anchor="center")
tabla.column("LEN", width=80, anchor="center")
tabla.column("Datos", width=400, anchor="w")

# Crear barra de desplazamiento vertical
scrollbar = tk.Scrollbar(frame_tabla, orient="vertical", command=tabla.yview)
tabla.configure(yscrollcommand=scrollbar.set)
scrollbar.pack(side="right", fill="y")
tabla.pack(side="left", fill="both", expand=True)

# Función para llamar a extract_data_fields cuando se selecciona una fila
def on_row_select(event):
    # Obtener el ID de la fila seleccionada
    selected_item = tabla.selection()
    if not selected_item:
        return  # No hacer nada si no hay fila seleccionada
    
    # Obtener los valores de la fila seleccionada
    item_values = tabla.item(selected_item[0])['values']
    
    # Verificar que la fila tenga al menos 4 columnas
    if len(item_values) >= 4:
        # Llamar a la función extract_data_fields con los datos de la cuarta columna
        extract_data_fields(item_values[3])

# Asociar la función al evento de seleccionar una fila
tabla.bind("<ButtonRelease-1>", on_row_select)

# Iniciar la aplicación
root.mainloop()
