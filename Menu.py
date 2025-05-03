import customtkinter as ctk
from tkinter import filedialog, messagebox, ttk
import folium
import os
import webview
from functions.add_file import add_file
from functions.filter import aplicar_filtros
from functions.extract_data_fields import extract_data_fields
from functions.extract_data import extraer_datos
from functions.Posiciones import process_dataframe_to_trajectories
import pandas as pd
from tkinter import simpledialog
import csv
from functions.map import abrir_mapa_webview
import tkinter as tk
import threading
import time




# Apariencia y color
ctk.set_appearance_mode("System") 
ctk.set_default_color_theme("blue") 

# Crear la ventana principal
root = ctk.CTk()
root.title("Decodificador de ASTERIX")

# Establecer las dimensiones de la ventana 
root.geometry("1000x600")  

#------------------- Creación mapa web ---------------------
# Crear un mapa base (se abrirá en el navegador)
mapa = folium.Map(location=[20, 0], zoom_start=2)
mapa_path = "mapa.html"
mapa.save(mapa_path)

# Función para abrir el mapa en el navegador
def abrir_mapa():
    os.startfile(mapa_path)


#--------------- Título --------------------------
# Frame para el título
btns_frame = ctk.CTkFrame(root, fg_color="#0077B6", corner_radius=0)  # Fondo azul claro
btns_frame.pack(side="top", fill="x", padx=0, pady=0)


# Añadir título en el centro
title_label = ctk.CTkLabel(btns_frame, text="Decodificador de ASTERIX", 
                          font=("Segoe UI", 18, "bold"),
                           text_color="white")
title_label.pack(pady=12)  # Centra el título con un poco de margen superior



# --------------------- Botones --------------------
btn_frame = ctk.CTkFrame(root)
btn_frame.pack(side="top", pady=10, fill="x", padx=20)

btn_abrir = tk.Button(btn_frame, text="Abrir Mapa en Navegador", command=abrir_mapa)
btn_archivo = ctk.CTkButton(
    btn_frame,
    text="Añadir Archivo",
    command=lambda: add_file(tabla),
    fg_color="white",
    text_color="black",  # Texto en negro
    font=("Segoe UI", 14), 
    corner_radius=8
)
btn_archivo.grid(row=0, column=0, padx=5, pady=5, sticky="ew") 


def lanzar_mapa_desde_tabla():
    # Llenar current_df con todos los datos que hay en tabla
    if not extraer_datos_tabla():
        messagebox.showwarning("Error", "No hay datos en la tabla para mostrar en el mapa.")
        return
    # Al usar current_df global, simplemente lo pasamos
    abrir_mapa_webview(current_df)


btn_mapa_webview = ctk.CTkButton(
    btn_frame,
    text="Ver Mapa",
    command=lanzar_mapa_desde_tabla,
    fg_color="#2196F3",
    hover_color="#0b7dda",
    font=("Segoe UI", 14,),
    corner_radius=8
)

#############################--Creación del Dataframe--#####################################
current_df = pd.DataFrame()
def extraer_datos_tabla():
    """
    Extrae los datos de la tabla (Treeview) y los convierte en un DataFrame.
    """
    global current_df

    # Verificamos que hay filas en la tabla
    if len(tabla.get_children()) == 0:
        return False  # Si no hay datos, retorna False

    # Extraer las columnas del Treeview
    columnas = columnas_datos  # O las que estés usando en tu tabla
    datos = []

    # Recorremos cada fila de la tabla
    for row in tabla.get_children():
        fila = tabla.item(row)["values"]
        datos.append(fila)

    # Crear el DataFrame a partir de los datos extraídos
    current_df = pd.DataFrame(datos, columns=columnas)
    return True

btn_mapa_webview.grid(row=0, column=5, padx=5, pady=5, sticky="ew")

# --------------------- Lista de columnas ---------------------
columnas_datos = [
    "NUM", "SAC", "SIC", "TIME", "TIME(s)", "Target report description", "Validated", "Garbled", "CodeSource", "Mode3ACode", "Validated_FL", "Garbled_FL", "FL", "Address", "ID", "BDS", "TRACK NUMBER", "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING","LAT", "LON", "H", "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A","B1B", "RHO", "THETA", #DATA ITEM 250
       
       #DATA ITEM 250
        "MCP_STATUS", "MCP_ALT", "FMS_STATUS", "FMS_ALT", "BP_STATUS", "BP_VALUE",
        "MODE_STATUS", "VNAV", "ALTHOLD", "APP", "TARGETALT_STATUS", "TARGETALT_SOURCE",
        "ROLL_STATUS", "ROLL_ANGLE", "TRACK_STATUS", "TRUE_TRACK", "GROUNDSPEED_STATUS", 
        "GROUNDSPEED", "TRACKRATE_STATUS", "TRACK_RATE", "AIRSPEED_STATUS", "TRUE_AIRSPEED",
        "HEADING_STATUS", "MAG_HEADING", "IAS_STATUS", "IAS", "MACH_STATUS", "MACH",
        "BARO_RATE_STATUS", "BARO_RATE", "INERTIAL_VERT_STATUS", "INERTIAL_VERT_VEL",


        "FL_Corrected"
]

# ⚠️ AÑADIMOS columna "Hex (Raw)" justo después de LEN
columnas_tabla = ["Paquete", "CAT", "LEN"] + columnas_datos

# --------------------- GUI Tabla ---------------------
frame_tabla = ctk.CTkFrame(root, fg_color="#1C1C1C")
frame_tabla.pack(pady=20, fill="both", expand=True, padx=20)

scroll_x = ttk.Scrollbar(frame_tabla, orient="horizontal")
scroll_y = ttk.Scrollbar(frame_tabla, orient="vertical")

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


# --------------------- Evento seleccionar fila -------------------
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
style = ttk.Style()
style.map("Treeview",
          background=[('selected', '#555555')])  # Fondo cuando se selecciona una fila

# --------------------- Dummy extraer_datos --------------------
def extraer_datos(datos_hex):
    return {col: "Not Found" for col in columnas_datos}

######################--FILTRADO--##############################

current_df = None  # DataFrame con los datos originales
filtro_blancos = ctk.BooleanVar(value=False)
filtro_transponder = ctk.BooleanVar(value=False)
filtro_on_ground = ctk.BooleanVar(value=False)
filtro_altitud = ctk.BooleanVar(value=False)
filtro_aeropuerto = ctk.BooleanVar(value=False)
df_filtrado = None  # DataFrame con los datos filtrados


def extraer_datos_tabla():
    global current_df
    datos = []
    
    columnas_completas = ["Paquete", "CAT", "LEN"] + [
        "NUM", "SAC", "SIC", "TIME", "TIME(s)", "Target report description",
        "Validated", "Garbled", "CodeSource", "Mode3ACode", "Validated_FL",
        "Garbled_FL", "FL", "Address", "ID", "BDS", "TRACK NUMBER", 
        "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING", "LAT", "LON",
        "H", "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A", "B1B",
        "RHO", "THETA",
        #DATA ITEM 250
        "MCP_STATUS", "MCP_ALT", "FMS_STATUS", "FMS_ALT", "BP_STATUS", "BP_VALUE",
        "MODE_STATUS", "VNAV", "ALTHOLD", "APP", "TARGETALT_STATUS", "TARGETALT_SOURCE",
        "ROLL_STATUS", "ROLL_ANGLE", "TRACK_STATUS", "TRUE_TRACK", "GROUNDSPEED_STATUS", 
        "GROUNDSPEED", "TRACKRATE_STATUS", "TRACK_RATE", "AIRSPEED_STATUS", "TRUE_AIRSPEED",
        "HEADING_STATUS", "MAG_HEADING", "IAS_STATUS", "IAS", "MACH_STATUS", "MACH",
        "BARO_RATE_STATUS", "BARO_RATE", "INERTIAL_VERT_STATUS", "INERTIAL_VERT_VEL",

        "FL_Corrected"

    ]
    
    for item in tabla.get_children():
        valores = tabla.item(item)['values']
        if len(valores) >= len(columnas_completas):
            fila = dict(zip(columnas_completas, valores))
            datos.append(fila)
    
    current_df = pd.DataFrame(datos) if datos else None
    return current_df is not None

def mostrar_dialogo_filtros():
    dialogo = ctk.CTkToplevel(root)
    dialogo.title("Configurar Filtros")
    dialogo.geometry("400x350")  # Aumentado ligeramente
    dialogo.attributes("-topmost", True)
    
    # Variables temporales
    temp_blancos = ctk.BooleanVar(value=filtro_blancos.get())
    temp_transponder = ctk.BooleanVar(value=filtro_transponder.get())
    temp_on_ground = ctk.BooleanVar(value=filtro_on_ground.get())
    temp_altitud = ctk.BooleanVar(value=filtro_altitud.get())
    temp_aeropuerto = ctk.BooleanVar(value=filtro_aeropuerto.get())
    
    # Frame contenedor
    filtros_frame = ctk.CTkFrame(dialogo)
    filtros_frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    ctk.CTkLabel(filtros_frame, text="Opciones de filtrado", 
                font=("Segoe UI Black", 16)).pack(anchor="w", pady=(0, 15))
    
    # Filtros básicos
    ctk.CTkCheckBox(filtros_frame, text="Eliminar blancos puros", 
                   variable=temp_blancos).pack(anchor="w", pady=5)
    ctk.CTkCheckBox(filtros_frame, text="Eliminar transponder fijo", 
                   variable=temp_transponder).pack(anchor="w", pady=5)
    ctk.CTkCheckBox(filtros_frame, text="Eliminar on ground", 
                   variable=temp_on_ground).pack(anchor="w", pady=5)
    
    # Separador
    ttk.Separator(filtros_frame, orient="horizontal").pack(fill="x", pady=10)
    
    # Filtros extra
    ctk.CTkCheckBox(filtros_frame, text="Limitar a 6000 pies máximo", 
                   variable=temp_altitud).pack(anchor="w", pady=5)
    ctk.CTkCheckBox(filtros_frame, text="Filtrar por aeropuerto Barcelona", 
                   variable=temp_aeropuerto).pack(anchor="w", pady=5)
    # Botones
    buttons_frame = ctk.CTkFrame(filtros_frame, fg_color="transparent")
    buttons_frame.pack(fill="x", pady=(20, 0))
    
    # Botones
    def aplicar():
        filtro_blancos.set(temp_blancos.get())
        filtro_transponder.set(temp_transponder.get())
        filtro_on_ground.set(temp_on_ground.get())
        filtro_altitud.set(temp_altitud.get())
        filtro_aeropuerto.set(temp_aeropuerto.get())
        aplicar_filtros_actuales()
        dialogo.destroy()
    
    ctk.CTkButton(buttons_frame, text="Aplicar", command=aplicar, 
                 fg_color="#4CAF50", hover_color="#45a049").pack(side="right", padx=10)
    ctk.CTkButton(buttons_frame, text="Cancelar", command=dialogo.destroy).pack(side="right")

def aplicar_filtros_actuales():
    """
    Aplica los filtros seleccionados utilizando el sistema de carga 
    """
    global current_df, df_filtrado
    
    if current_df is None:
        if not extraer_datos_tabla():
            messagebox.showwarning("Error", "Primero carga un archivo")
            return
    
    # Función que ejecutará en segundo plano
    def ejecutar_filtros(carga_info):
        df_procesado = current_df.copy()
        total_filtros = sum([
            filtro_blancos.get(), 
            filtro_transponder.get(), 
            filtro_on_ground.get(), 
            filtro_altitud.get(), 
            filtro_aeropuerto.get()
        ])
        
        filtros_aplicados = 0
        
        # 1. Filtro de blancos puros
        if filtro_blancos.get():
            actualizar_carga(
                carga_info, 
                estado="Eliminando blancos puros...",
                progreso=filtros_aplicados/total_filtros
            )
            time.sleep(0.2)  # Pequeña pausa para ver la actualización
            
            modos_validos = [
                "Single ModeS All-Call",
                "Single ModeS Roll-Call",
                "ModeS All-Call+PSR",
                "ModeS Roll-Call + PSR"
            ]
            df_procesado = df_procesado[
                df_procesado['Target report description'].astype(str).apply(
                    lambda x: any(m in x for m in modos_validos)
                )
            ]
            filtros_aplicados += 1
        
        # 2. Filtro de transponder
        if filtro_transponder.get():
            actualizar_carga(
                carga_info, 
                estado="Filtrando transponders fijos...",
                progreso=filtros_aplicados/total_filtros
            )
            time.sleep(0.2)
            
            mask = (df_procesado['FL'] == 'N/A') | (~df_procesado['FL'].astype(str).str.contains('7777'))
            df_procesado = df_procesado[mask]
            filtros_aplicados += 1
        
        # 3. Filtro on ground
        if filtro_on_ground.get():
            actualizar_carga(
                carga_info, 
                estado="Filtrando aeronaves en tierra...",
                progreso=filtros_aplicados/total_filtros
            )
            time.sleep(0.2)
            
            estados_tierra = [
                "No alert, no SPI, aircraft on ground",
                "Alert, no SPI, aircraft on ground"
            ]
            df_procesado = df_procesado[~df_procesado['STAT'].isin(estados_tierra)]
            filtros_aplicados += 1

        # 4. Filtros extra
        if filtro_altitud.get():
            actualizar_carga(
                carga_info, 
                estado="Aplicando filtro de altitud máxima...",
                progreso=filtros_aplicados/total_filtros
            )
            time.sleep(0.2)
            
            from functions.filter import filtrar_altitud_maxima
            df_procesado = filtrar_altitud_maxima(df_procesado)
            filtros_aplicados += 1
        
        if filtro_aeropuerto.get():
            actualizar_carga(
                carga_info, 
                estado="Aplicando filtro de aeropuerto...",
                progreso=filtros_aplicados/total_filtros
            )
            time.sleep(0.2)
            
            from functions.filter import filtrar_aeropuerto_barcelona
            df_procesado = filtrar_aeropuerto_barcelona(df_procesado)
            filtros_aplicados += 1
        
        # Completado
        actualizar_carga(
            carga_info, 
            estado="Actualizando tabla...",
            progreso=1.0
        )
        time.sleep(0.2)
        
        return df_procesado
    
    # Función que se ejecuta cuando se completa el filtrado
    def filtrado_completado(resultado):
        global df_filtrado
        df_filtrado = resultado
        actualizar_tabla(df_filtrado)
        
        # Mostrar resumen de filtros aplicados
        messagebox.showinfo(
            "Filtros aplicados", 
            f"Registros mostrados: {len(df_filtrado)}\n" +
            ("✓ Filtrado por aeropuerto Barcelona\n" if filtro_aeropuerto.get() else "") +
            ("✓ Altitud máxima 6000 pies\n" if filtro_altitud.get() else "")
        )
    
    # Ejecutar en segundo plano
    ejecutar_en_segundo_plano(
        funcion=ejecutar_filtros,
        mensaje="Aplicando filtros",
        on_complete=filtrado_completado,
        cancelable=True
    )
        
#Actualizacion de la tabla si hay filtrado
     
def actualizar_tabla(df):
    for item in tabla.get_children():
        tabla.delete(item)
    
    for _, row in df.iterrows():
        valores = [
            row.get("Paquete", ""),
            row.get("CAT", ""),
            row.get("LEN", ""),
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
            row.get("THETA", ""),
            # Columnas del Data Item 250 
            row.get("BDS_REP", ""),
            # BDS 4.0
            row.get("MCP_STATUS", ""),
            row.get("MCP_ALT", ""),
            row.get("FMS_STATUS", ""),
            row.get("FMS_ALT", ""),
            row.get("BP_STATUS", ""),
            row.get("BP_VALUE", ""),
            row.get("MODE_STATUS", ""),
            row.get("VNAV", ""),
            row.get("ALTHOLD", ""),
            row.get("APP", ""),
            row.get("TARGETALT_STATUS", ""),
            row.get("TARGETALT_SOURCE", ""),
            # BDS 5.0
            row.get("ROLL_STATUS", ""),
            row.get("ROLL_ANGLE", ""),
            row.get("TRACK_STATUS", ""),
            row.get("TRUE_TRACK", ""),
            row.get("GROUNDSPEED_STATUS", ""),
            row.get("GROUNDSPEED", ""),
            row.get("TRACKRATE_STATUS", ""),
            row.get("TRACK_RATE", ""),
            row.get("AIRSPEED_STATUS", ""),
            row.get("TRUE_AIRSPEED", ""),
            # BDS 6.0
            row.get("HEADING_STATUS", ""),
            row.get("MAG_HEADING", ""),
            row.get("IAS_STATUS", ""),
            row.get("IAS", ""),
            row.get("MACH_STATUS", ""),
            row.get("MACH", ""),
            row.get("BARO_RATE_STATUS", ""),
            row.get("BARO_RATE", ""),
            row.get("INERTIAL_VERT_STATUS", ""),
            row.get("INERTIAL_VERT_VEL", ""),


            row.get("FL_Corrected","")
        ]
        tabla.insert("", "end", values=valores)

# Botón de filtros
btn_filtrar = ctk.CTkButton(
    btn_frame,
    text="Filtrar Datos",
    command=mostrar_dialogo_filtros,
    fg_color="white", 
    text_color="black",  # Texto negro
    font=("Segoe UI", 14), 
    corner_radius=8
)
btn_filtrar.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

def reset_filtros():
    """Reset all filters and apply the reset to update the table"""
    filtro_blancos.set(False)
    filtro_transponder.set(False)
    filtro_on_ground.set(False)
    filtro_altitud.set(False)
    filtro_aeropuerto.set(False)
    
    # If we have data in the table, update with no filters
    if current_df is not None:
        # Update the table with the original data
        actualizar_tabla(current_df)
        messagebox.showinfo("Filtros reseteados", "Todos los filtros han sido desactivados")
    else:
        messagebox.showinfo("Filtros reseteados", "Todos los filtros han sido desactivados")

# Update the reset button's command
btn_reset = ctk.CTkButton(
    btn_frame,
    text="Resetear Filtros",
    command=reset_filtros,  # Use the dedicated function
    fg_color="white", 
    text_color="black",
    font=("Segoe UI", 14),
    corner_radius=8
)
btn_reset.grid(row=0, column=2, padx=5, pady=5, sticky="ew")


#########################--Exportar a CSV--#################################
def exportar_a_csv():
    """
    Exporta los datos actuales (filtrados o sin filtrar) con barra de progreso
    """
    global current_df, df_filtrado

    # Primero intentamos extraer los datos si no están cargados
    if current_df is None:
        if not extraer_datos_tabla():
            messagebox.showwarning("Advertencia", "No hay datos para exportar")
            return
    
    # Verificar si hay datos disponibles
    datos_a_exportar = df_filtrado if (df_filtrado is not None and not df_filtrado.empty) else current_df 
    
    # Solicitar ubicación para guardar
    file_path = filedialog.asksaveasfilename(
        defaultextension=".csv",
        filetypes=[("CSV Files", "*.csv"), ("All Files", "*.*")],
        title="Guardar datos como CSV"
    )
    
    if not file_path:
        return  # Usuario canceló
    
    # Función para ejecutar en segundo plano
    def procesar_exportacion(carga_info):
        # Simular pasos de exportación
        total_filas = len(datos_a_exportar)
        chunk_size = max(1, total_filas // 10)  # Dividir en 10 partes como máximo
        
        # Paso 1: Preparar datos
        actualizar_carga(carga_info, estado="Preparando datos...", progreso=0.1)
        time.sleep(0.3)
        
        # Paso 2: Formateando columnas
        actualizar_carga(carga_info, estado="Formateando columnas...", progreso=0.3)
        time.sleep(0.3)
        
        # Paso 3: Exportando a CSV
        actualizar_carga(carga_info, estado=f"Exportando {total_filas} registros...", progreso=0.5)
        
        # Exportar en chunks para simular progreso
        with open(file_path, 'w', newline='', encoding='utf-8-sig') as f:
            datos_a_exportar.to_csv(
                f,
                index=False,
                sep=';',  # Punto y coma para mejor compatibilidad
                quoting=csv.QUOTE_MINIMAL
            )
        
        # Paso 4: Finalizando
        actualizar_carga(carga_info, estado="Finalizando...", progreso=0.9)
        time.sleep(0.3)
        
        # Completado
        actualizar_carga(carga_info, estado="¡Exportación completada!", progreso=1.0)
        time.sleep(0.5)
        
        return file_path
    
    # Función que se ejecuta cuando se completa la exportación
    def exportacion_completada(ruta_archivo):
        # Mostrar mensaje de éxito
        messagebox.showinfo(
            "Exportación exitosa", 
            f"Datos exportados correctamente a:\n{ruta_archivo}"
        )
    
    # Ejecutar en segundo plano
    ejecutar_en_segundo_plano(
        funcion=procesar_exportacion,
        mensaje="Exportando datos",
        on_complete=exportacion_completada
    )
       

# Botón exportar
btn_exportar = ctk.CTkButton(
    btn_frame,
    text="Exportar a CSV",
    command=exportar_a_csv,
    fg_color="#2196F3",
    hover_color="#0b7dda",
    font=("Segoe UI", 14,),
    corner_radius=8
)
btn_exportar.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

##########################--Posiciones--######################################
#Le pasamos la dataframe que se esta usando en el momento a Posiciones
def iniciarPosiciones():
   
    global current_df  
    
    if current_df is None or current_df.empty:
        messagebox.showerror("Error", "No hay datos cargados")
        return
    
    # Procesa el DataFrame completo
    posiciones_df = process_dataframe_to_trajectories(current_df)


##################################ESTILOS Y APARIENCIA ########################################
# --------------------- NOTIFICACIONES ---------------------
def mostrar_notificacion(titulo, mensaje):
    notif = ctk.CTkToplevel(root)
    notif.title(titulo)
    notif.geometry("300x150")
    notif.resizable(False, False)
    notif.attributes("-topmost", True)
    
    # Ubicar en esquina inferior derecha
    posicionx = root.winfo_screenwidth() - 350
    posiciony = root.winfo_screenheight() - 200
    notif.geometry(f"+{posicionx}+{posiciony}")
    
    # Contenido
    frame = ctk.CTkFrame(notif)
    frame.pack(fill="both", expand=True, padx=15, pady=15)
    
    # Título
    ctk.CTkLabel(frame, text=titulo, font=("Segoe UI", 16)).pack(anchor="w")
    
    # Mensaje
    ctk.CTkLabel(frame, text=mensaje, font=("Segoe UI", 12)).pack(anchor="w", pady=10)
    
    # Botón cerrar
    ctk.CTkButton(frame, text="Aceptar", command=notif.destroy, 
                 width=80, height=30).pack(side="right")
    
    # Auto-cerrar después de 5 segundos
    notif.after(5000, notif.destroy)

# --------------------- BARRA DE ESTADO ---------------------
estado_frame = ctk.CTkFrame(root, height=25, corner_radius=0)
estado_frame.pack(side="bottom", fill="x")

estado_texto = ctk.CTkLabel(estado_frame, text="Listo", anchor="w")
estado_texto.pack(side="left", padx=10)

# --------------------- PANTALLA DE CARGA MEJORADA ---------------------
def mostrar_carga(mensaje, cancelable=False):
    """
    Muestra una pantalla de carga con barra de progreso y mensajes actualizables.
    """
    carga = ctk.CTkToplevel()
    carga.title("Procesando")
    carga.geometry("450x200")
    carga.resizable(False, False)
    carga.attributes("-topmost", True)
    carga.grab_set()  # Bloquea interacción con ventana principal
    
    # Variable para controlar la cancelación
    cancelar_operacion = ctk.BooleanVar(value=False)
    
    # Centrar en la pantalla
    posicionx = root.winfo_x() + (root.winfo_width() // 2) - 225
    posiciony = root.winfo_y() + (root.winfo_height() // 2) - 100
    carga.geometry(f"+{posicionx}+{posiciony}")
    
    # Contenido
    frame = ctk.CTkFrame(carga)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título principal
    mensaje_label = ctk.CTkLabel(frame, text=mensaje, font=("Segoe UI Black", 16))
    mensaje_label.pack(pady=(10, 5))
    
    # Etiqueta para mostrar el estado actual
    estado_label = ctk.CTkLabel(frame, text="Iniciando...", font=("Segoe UI", 12))
    estado_label.pack(pady=(0, 10))
    
    # Progress bar
    progress_container = ctk.CTkFrame(frame, fg_color="transparent")
    progress_container.pack(pady=10, fill="x")
    
    pb = ctk.CTkProgressBar(progress_container)
    pb.pack(fill="x", padx=20)
    
    # Por defecto, indeterminado
    pb.configure(mode="indeterminate")
    pb.start()
    
    # Botón para cancelar si es necesario
    if cancelable:
        btn_cancelar = ctk.CTkButton(
            frame, 
            text="Cancelar", 
            command=lambda: cancelar_operacion.set(True),
            fg_color="#e74c3c",
            hover_color="#c0392b", 
            width=100
        )
        btn_cancelar.pack(pady=10)
    
    # Forzar actualizaciones de la interfaz
    carga.update_idletasks()
    carga.update()
    
    return {
        "ventana": carga, 
        "barra": pb, 
        "mensaje": mensaje_label,
        "estado": estado_label,
        "cancelar": cancelar_operacion
    }

def actualizar_carga(carga_info, mensaje=None, estado=None, progreso=None):
    """
    Actualiza la pantalla de carga
    """
    if carga_info["ventana"].winfo_exists():
        if mensaje is not None:
            carga_info["mensaje"].configure(text=mensaje)
        
        if estado is not None:
            carga_info["estado"].configure(text=estado)
        
        if progreso is not None:
            # Cambiar a modo determinado si no lo está ya
            if carga_info["barra"].cget("mode") == "indeterminate":
                carga_info["barra"].stop()
                carga_info["barra"].configure(mode="determinate")
            
            carga_info["barra"].set(progreso)
        
        # Actualizar la interfaz
        carga_info["ventana"].update_idletasks()
        carga_info["ventana"].update()

def ocultar_carga(carga_info):
    """Cierra la ventana de carga"""
    if carga_info["ventana"].winfo_exists():
        carga_info["ventana"].grab_release()
        carga_info["ventana"].destroy()

# --------------------- EJECUCIÓN EN SEGUNDO PLANO ---------------------
def ejecutar_en_segundo_plano(funcion, args=(), kwargs={}, on_complete=None, mensaje="Procesando", cancelable=False):
    """
    Ejecuta una función en segundo plano mostrando pantalla de carga
    """
    carga_info = mostrar_carga(mensaje, cancelable=cancelable)
    resultado = [None]  # Usamos lista para poder modificar desde el hilo
    error = [None]
    
    def worker():
        try:
            # Variable para controlar estado
            kwargs['carga_info'] = carga_info
            resultado[0] = funcion(*args, **kwargs)
        except Exception as e:
            error[0] = e
        finally:
            # Ejecutamos en el hilo principal
            root.after(100, lambda: finalizar())
    
    def finalizar():
        ocultar_carga(carga_info)
        if error[0] is not None:
            messagebox.showerror("Error", f"Se produjo un error:\n{str(error[0])}")
        elif on_complete:
            on_complete(resultado[0])
    
    # Iniciar hilo
    thread = threading.Thread(target=worker)
    thread.daemon = True
    thread.start()
    
    return carga_info  # Por si se necesita acceder

print("Lanzando interfaz...")
root.mainloop()




