import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import folium
import os
import webview
from functions.add_file import add_file
from functions.filter import filter_data
from functions.extract_data_fields import extract_data_fields
from functions.extract_data import extraer_datos

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

# --------------------- Lista de columnas ---------------------
columnas_datos = [
    "NUM", "SAC", "SIC", "TIME", "TIME(s)", "LAT", "LON", "H", "TYP_020", "SIM_020", "RDP_020", "SPI_020", "RAB_020",
    "TST_020", "ERR_020", "XPP_020", "ME_020", "MI_020", "FOE_FRI_020", "RHO", "THETA", "V_070", "G_070", "MODE 3/A",
    "V_090", "G_090", "FL", "MODE C corrected", "SRL_130", "SSR_130", "SAM_130", "PRL_130", "PAM_130", "RPD_130",
    "APD_130", "TA", "TI", "MCP_ALT", "FMS_ALT", "BP", "VNAV", "ALT_HOLD", "APP", "TARGET_ALT_SOURCE", "RA", "TTA",
    "GS", "TAR", "TAS", "HDG", "IAS", "MACH", "BAR", "IVV", "TN", "X", "Y", "GS_KT", "HEADING", "CNF_170", "RAD_170",
    "DOU_170", "MAH_170", "CDM_170", "TRE_170", "GHO_170", "SUP_170", "TCC_170", "HEIGHT", "COM_230", "STAT_230",
    "SI_230", "MSCC_230", "ARC_230", "AIC_230", "B1A_230", "B1B_230"
]

# ⚠️ AÑADIMOS columna "Hex (Raw)" justo después de LEN
columnas_tabla = ["Paquete", "CAT", "LEN", "Hex (Raw)"] + columnas_datos

# --------------------- GUI Tabla ---------------------
frame_tabla = tk.Frame(root)
frame_tabla.pack(pady=20, fill="both", expand=True, padx=20)

scroll_x = tk.Scrollbar(frame_tabla, orient="horizontal")
scroll_y = tk.Scrollbar(frame_tabla, orient="vertical")

tabla = ttk.Treeview(
    frame_tabla,
    columns=columnas_tabla,
    show="headings",
    xscrollcommand=scroll_x.set,
    yscrollcommand=scroll_y.set
)

for col in columnas_tabla:
    tabla.heading(col, text=col)
    tabla.column(col, width=100, anchor="center")

scroll_x.config(command=tabla.xview)
scroll_y.config(command=tabla.yview)
scroll_x.pack(side="bottom", fill="x")
scroll_y.pack(side="right", fill="y")
tabla.pack(side="left", fill="both", expand=True)

# --------------------- Evento seleccionar fila ---------------------
def on_row_select(event):
    selected_item = tabla.selection()
    if selected_item:
        item_values = tabla.item(selected_item[0])['values']
        print("Fila seleccionada:", item_values)

tabla.bind("<ButtonRelease-1>", on_row_select)

# --------------------- Modificación de la función de agregar paquete ---------------------
def agregar_paquete(paquete_num, cat, length, datos_hex):
    # Ya no usamos extraer_datos, ya que la función add_file ya extrae todos los datos
    fila = [paquete_num, cat, length, datos_hex] + [datos_hex]  # datos_extraidos ya no es necesario aquí

    # Verificación para asegurarnos de que la fila contiene la cantidad correcta de columnas
    if len(fila) != len(columnas_tabla):
        print("❌ Error: cantidad de columnas no coincide.")
        print("Esperado:", len(columnas_tabla), "| Obtenido:", len(fila))
        return

    tabla.insert("", "end", values=fila)

# --------------------- Dummy extraer_datos ---------------------
def extraer_datos(datos_hex):
    return {col: "Not Found" for col in columnas_datos}

print("Lanzando interfaz...")
root.mainloop()
