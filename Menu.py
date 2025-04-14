import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import folium
import os
import webview
from functions.add_file import add_file
from functions.filter import aplicar_filtros
from functions.extract_data_fields import extract_data_fields
from functions.extract_data import extraer_datos
import pandas as pd
from tkinter import simpledialog

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
    "NUM", "SAC", "SIC", "TIME", "TIME(s)", "Target report description", "Validated", "Garbled", "CodeSource", "Mode3ACode", "Validated_FL", "Garbled_FL", "FL", "Address", "ID", "BDS", "TRACK NUMBER", "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING","LAT", "LON", "H", "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A","B1B", "RHO", "THETA"
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

# --------------------- Dummy extraer_datos ---------------------
def extraer_datos(datos_hex):
    return {col: "Not Found" for col in columnas_datos}

#####    BOTÓN FILTRAR     ####################################################################
current_df = None  # Almacenará el DataFrame con los datos 


#Prueba menú simple con solo 3 filtros

# Variables para los filtros (globales)
filtro_blancos = tk.BooleanVar(value=True)
filtro_transponder = tk.BooleanVar(value=True)
qnh_valor = tk.DoubleVar(value=1013.25)

def mostrar_menu_filtros(event):
    menu_filtros = tk.Menu(root, tearoff=0)
   
    # Opciones de filtro con variables de control
    menu_filtros.add_checkbutton(label="Eliminar blancos puros", 
                               variable=filtro_blancos,
                               command=aplicar_filtros_actuales)
    menu_filtros.add_checkbutton(label="Eliminar transponder fijo (7777)", 
                               variable=filtro_transponder,
                               command=aplicar_filtros_actuales)
    
    # Submenú para QNH
    submenu_qnh = tk.Menu(menu_filtros, tearoff=0)
    submenu_qnh.add_radiobutton(label="QNH estándar (1013.25 hPa)", 
                              variable=qnh_valor, 
                              value=1013.25,
                              command=aplicar_filtros_actuales)
    submenu_qnh.add_command(label="Ajustar manualmente...", 
                          command=pedir_qnh_manual)
    menu_filtros.add_cascade(label="Corrección QNH", menu=submenu_qnh)
    
    # Mostrar menú
    try:
        menu_filtros.tk_popup(event.x_root, event.y_root)
    finally:
        menu_filtros.grab_release()
    
    
def pedir_qnh_manual():
    nuevo_qnh = simpledialog.askfloat("QNH", "Ingrese valor QNH (hPa):", 
                                     initialvalue=qnh_valor.get())
    if nuevo_qnh:
        qnh_valor.set(nuevo_qnh)
        aplicar_filtros_actuales()

def aplicar_filtros_actuales():
    if current_df is None:
        messagebox.showwarning("Error", "Primero carga un archivo")
        return
    
    config = {
        "eliminar_blancos_puros": filtro_blancos.get(),
        "eliminar_transponder_fijo": filtro_transponder.get(),
        "qnh_correccion": qnh_valor.get()
    }
    
    try:
        df_filtrado = aplicar_filtros(current_df, config)
        actualizar_tabla(df_filtrado)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron aplicar los filtros:\n{str(e)}")

def actualizar_tabla(df):
    # Limpiar tabla existente
    for item in tabla.get_children():
        tabla.delete(item)
    
    # Insertar nuevos datos (ejemplo con columnas básicas)
    for _, row in df.iterrows():
        tabla.insert("", "end", values=(
            row.get("NUM", ""),
            row.get("TYP020", ""),
            row.get("Mode_3A", ""),
              
        ))

# Botón de Filtrar con menú contextual
btn_filtrar = ttk.Button(btn_frame, text="Filtrar")
btn_filtrar.grid(row=0, column=2, padx=10, pady=5, sticky="ew")  # Añadido al frame de botones
btn_filtrar.bind("<Button-1>", mostrar_menu_filtros)

#Botón de carga de archivo (ejemplo muy pequeño)
def cargar_archivo():
    global current_df
    # Simulación de datos 
    current_df = pd.DataFrame({
        "NUM": [1, 2, 3],
        "TYP020": ["Single ModeS All-Call", "Primary", "ModeS Roll-Call + PSR"],
        "Mode_3A": [1234, 5678, 7777],
        "ModeC_corrected": [5000, 3000, 6000]
    })
    messagebox.showinfo("Éxito", "Datos cargados")
btn_cargar = ttk.Button(root, text="Cargar Archivo", command=cargar_archivo)
btn_cargar.pack(pady=10)




print("Lanzando interfaz...")
root.mainloop()
