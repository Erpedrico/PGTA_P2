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
import csv
from functions.Aviones import mostrar_mapa_aviones, process_aircraft_packet
import threading
import time

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

    # Primero procesar todos los paquetes para construir las trayectorias
    procesar_paquetes_para_mapa()
    
    # Luego mostrar el mapa con los aviones
    mostrar_mapa_aviones()
    
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

# --------------------- Botones --------------------
btn_frame = tk.Frame(root)
btn_frame.pack(side="top", pady=10, fill="x", padx=20)


btn_abrir = tk.Button(btn_frame, text="Abrir Mapa en Navegador", command=abrir_mapa)
btn_archivo = ttk.Button(
    btn_frame,
    text="Añadir Archivo",
    command=lambda: add_file(tabla),
    style='Accent.TButton'
)
btn_archivo.grid(row=0, column=0, padx=5, pady=5, sticky="ew") 

btn_mapa_webview = ttk.Button(
    btn_frame,
    text="Ver Mapa",
    command=abrir_mapa_webview
)
btn_mapa_webview.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

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

# --------------------- FILTRADO  ---------------------
current_df = None  # DataFrame con los datos originales
filtro_blancos = tk.BooleanVar(value=False)
filtro_transponder = tk.BooleanVar(value=False)
filtro_on_ground = tk.BooleanVar(value=False)
df_filtrado=None #DataFrame con los datos filtrados


def extraer_datos_tabla():
    global current_df
    datos = []
    
    columnas_completas = ["Paquete", "CAT", "LEN", "Hex (Raw)"] + [
        "NUM", "SAC", "SIC", "TIME", "TIME(s)", "Target report description",
        "Validated", "Garbled", "CodeSource", "Mode3ACode", "Validated_FL",
        "Garbled_FL", "FL", "Address", "ID", "BDS", "TRACK NUMBER", 
        "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING", "LAT", "LON",
        "H", "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A", "B1B",
        "RHO", "THETA"
    ]
    
    for item in tabla.get_children():
        valores = tabla.item(item)['values']
        if len(valores) >= len(columnas_completas):
            fila = dict(zip(columnas_completas, valores))
            datos.append(fila)
    
    current_df = pd.DataFrame(datos) if datos else None
    return current_df is not None

def mostrar_dialogo_filtros():
    dialogo = tk.Toplevel(root)
    dialogo.title("Configurar Filtros")
    dialogo.geometry("400x300")
    
    # Variables temporales
    temp_blancos = tk.BooleanVar(value=filtro_blancos.get())
    temp_transponder = tk.BooleanVar(value=filtro_transponder.get())
    temp_on_ground = tk.BooleanVar(value=filtro_on_ground.get())
    
    # Controles
    ttk.Checkbutton(dialogo, text="Eliminar blancos puros", variable=temp_blancos).pack(anchor="w", pady=5)
    ttk.Checkbutton(dialogo, text="Eliminar transponder fijo", variable=temp_transponder).pack(anchor="w", pady=5)
    ttk.Checkbutton(dialogo, text="Eliminar on ground", variable=temp_on_ground).pack(anchor="w", pady=5)
       
    
    def aplicar():
        filtro_blancos.set(temp_blancos.get())
        filtro_transponder.set(temp_transponder.get())
        filtro_on_ground.set(temp_on_ground.get())
        aplicar_filtros_actuales()
        dialogo.destroy()
    
    ttk.Button(dialogo, text="Aplicar", command=aplicar).pack(side="right", padx=5)
    ttk.Button(dialogo, text="Cancelar", command=dialogo.destroy).pack(side="right")

def aplicar_filtros_actuales():
    global current_df, df_filtrado
    if current_df is None:
        if not extraer_datos_tabla():
            messagebox.showwarning("Error", "Primero carga un archivo")
            return
        
    # Mostrar pantalla de carga
    carga = mostrar_carga("Aplicando filtros...")
    root.update()
    
    try:
        df_filtrado = current_df.copy()
        
        # 1. Filtro de blancos puros (conservando nombres Python)
        if filtro_blancos.get():

            modos_validos = [
                "Single ModeS All-Call",
                "Single ModeS Roll-Call",
                "ModeS All-Call+PSR",
                "ModeS Roll-Call + PSR"
            ]
            # Convertimos a string y aplicamos filtro
            df_filtrado = df_filtrado[
                df_filtrado['Target report description'].astype(str).apply(lambda x: any(m in x for m in modos_validos)  )
            ]
        
        # 2. Filtro de transponder 
        if filtro_transponder.get():
            mask = (df_filtrado['FL'] == 'N/A') | (~df_filtrado['FL'].astype(str).str.contains('7777'))
            df_filtrado = df_filtrado[mask]
        
        # 3. Filtro on ground 
        if filtro_on_ground.get():
            estados_tierra = [
                "No alert, no SPI, aircraft on ground",
                "Alert, no SPI, aircraft on ground"
            ]
            df_filtrado = df_filtrado[~df_filtrado['STAT'].isin(estados_tierra)]
        
        # Actualizar tabla
        root.update()
        actualizar_tabla(df_filtrado)
        ocultar_carga(carga)  
        messagebox.showinfo("Filtros aplicados",
                          f"Registros mostrados: {len(df_filtrado)}\n"
                          )       
        
    except Exception as e:
        messagebox.showerror("Error", f"Fallo al filtrar:\n{str(e)}")
   
    
      
        
def actualizar_tabla(df):
    for item in tabla.get_children():
        tabla.delete(item)
    
    for _, row in df.iterrows():
        valores = [
            row.get("Paquete", ""),
            row.get("CAT", ""),
            row.get("LEN", ""),
            row.get("Hex (Raw)", ""),
            row.get("NUM", ""),
            row.get("SAC", ""),
            row.get("SIC", ""),
            row.get("TIME", ""),
            row.get("TIME(s)", ""),
            row.get("Target report description", ""),
            row.get("Validated", ""),
            row.get("Garbled", ""),
            row.get("CodeSource", ""),
            row.get("Mode3ACode", ""),
            row.get("Validated_FL", ""),
            row.get("Garbled_FL", ""),
            row.get("FL", ""),
            row.get("Address", ""),
            row.get("ID", ""),
            row.get("BDS", ""),
            row.get("TRACK NUMBER", ""),
            row.get("TRACK STATUS", ""),
            row.get("X", ""),
            row.get("Y", ""),
            row.get("GS", ""),
            row.get("GS_KT", ""),
            row.get("HEADING", ""),
            row.get("LAT", ""),
            row.get("LON", ""),
            row.get("H", ""),
            row.get("COM", ""),
            row.get("STAT", ""),
            row.get("SI", ""),
            row.get("MSSC", ""),
            row.get("ARC", ""),
            row.get("AIC", ""),
            row.get("B1A", ""),
            row.get("B1B", ""),
            row.get("RHO", ""),
            row.get("THETA", "")
        ]
        tabla.insert("", "end", values=valores)

# Botón de filtros
btn_filtrar = ttk.Button(
    btn_frame,
    text="Filtrar Datos",
    command=mostrar_dialogo_filtros
)
btn_filtrar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

# Botón de reset
btn_reset = ttk.Button(
    btn_frame,
    text="Resetear Filtros",
    command=lambda: [filtro_blancos.set(False), filtro_transponder.set(False), 
                    filtro_on_ground.set(False), aplicar_filtros_actuales()]
)
btn_reset.grid(row=0, column=2, padx=5, pady=5, sticky="ew")


#............Exportar a CSV............................
def exportar_a_csv():
    """Exporta los datos actuales (filtrados o sin filtrar)"""
    global current_df, df_filtrado
    # Mostrar pantalla de carga
    

    # Verificar si hay datos disponibles
    datos_a_exportar = df_filtrado if (df_filtrado is not None and not df_filtrado.empty) else current_df 

    # Verificar si hay datos filtrados
    if df_filtrado is None or df_filtrado.empty:
        messagebox.showwarning("Advertencia", "No hay datos filtrados para exportar")
        return
    
    try:
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
            title="Guardar datos como CSV"
        )
        
        if file_path:
            carga = mostrar_carga("Preparando datos para exportación...")
            root.update()  # Forzar actualización de la UI
    
            #Exportar a Excel de manera óptima
            datos_a_exportar.to_csv(
                file_path,
                index=False,
                sep=';',  # Punto y coma para mejor compatibilidad
                encoding='utf-8-sig',  # BOM para Excel
                quoting=csv.QUOTE_MINIMAL
            )
            ocultar_carga(carga)
            messagebox.showinfo("Éxito", f"Datos exportados correctamente:\n{file_path}")
    
    except Exception as e:
        messagebox.showerror("Error", f"Error al exportar:\n{str(e)}")
    
       

# Botón exportar
btn_exportar = ttk.Button(
    btn_frame,
    text="Exportar a CSV",
    command=exportar_a_csv,
    style='Accent.TButton'
)
btn_exportar.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

# --------------------- ESTILOS Y APARIENCIA ---------------------
style = ttk.Style()
style.theme_use('clam')

# Configurar colores y estilos
style.configure('TFrame', background='#2d2d2d')
style.configure('TButton', 
               font=('Arial', 10, 'bold'),
               padding=6,
               background='#4CAF50',
               foreground='white')
style.map('TButton',
         background=[('active', '#45a049')])

style.configure('Header.TLabel', 
               font=('Arial', 12, 'bold'),
               background='#333',
               foreground='white')

# --------------------- PANTALLA DE CARGA ---------------------
def mostrar_carga(mensaje):
    carga = tk.Toplevel(root)
    carga.title("Procesando")
    carga.geometry("300x100")
    carga.resizable(False, False)
    carga.attributes("-topmost", True)
    carga.grab_set()
    
    tk.Label(carga, text=mensaje, font=('Arial', 11)).pack(pady=10)
    pb = ttk.Progressbar(carga, mode='indeterminate')
    pb.pack(pady=5, padx=20, fill='x')
    pb.start()
    
    return carga

def ocultar_carga(ventana_carga):
    ventana_carga.grab_release()
    ventana_carga.destroy()
#MAPA PRUEBA##########################################################################3
def procesar_paquetes_para_mapa():
    """Procesa todos los paquetes de la tabla para construir las trayectorias"""
    carga = mostrar_carga("Procesando paquetes para el mapa...")
    
    try:
        # Limpiar datos anteriores
        from functions.Aviones import aircraft_data
        aircraft_data.clear()
        
        # Procesar cada paquete en la tabla
        for item in tabla.get_children():
            valores = tabla.item(item)['values']
            if len(valores) > 3:  # Asegurarse que hay datos hex
                hex_data = valores[3]
                try:
                    # Procesar el paquete en un hilo secundario
                    t = threading.Thread(target=process_aircraft_packet, args=(hex_data,))
                    t.start()
                    # Pequeña pausa para no saturar
                    time.sleep(0.01)
                except Exception as e:
                    print(f"Error procesando paquete: {e}")
        
        messagebox.showinfo("Proceso completado", "Datos de aviones listos para visualización")
    finally:
        ocultar_carga(carga)

# Modificar el botón del mapa de aviones para que procese primero los datos
btn_mapa_aviones = ttk.Button(
    btn_frame,
    text="Mapa de Aviones",
    command=lambda: [procesar_paquetes_para_mapa(), mostrar_mapa_aviones()],
    style='Accent.TButton'
)
btn_mapa_aviones.grid(row=0, column=6, padx=5, pady=5, sticky="ew")

######################################################################################################
print("Lanzando interfaz...")
root.mainloop()




