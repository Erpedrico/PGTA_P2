from tkinter import filedialog, messagebox
from functions.extract_data import extraer_datos
import threading
import time
import customtkinter as ctk

DEBUG = False

def mostrar_carga(parent, mensaje, cancelable=False):
   
    #Muestra una pantalla de carga simple.
    
    carga = ctk.CTkToplevel(parent)
    carga.title("Procesando")
    carga.geometry("400x150")
    carga.resizable(False, False)
    carga.attributes("-topmost", True)
    carga.grab_set()  # Bloquea interacción con ventana principal
    
    # Centrar en la pantalla
    posicionx = parent.winfo_x() + (parent.winfo_width() // 2) - 200
    posiciony = parent.winfo_y() + (parent.winfo_height() // 2) - 75
    carga.geometry(f"+{posicionx}+{posiciony}")
    
    # Contenido
    frame = ctk.CTkFrame(carga)
    frame.pack(fill="both", expand=True, padx=20, pady=20)
    
    # Título
    mensaje_label = ctk.CTkLabel(frame, text=mensaje, font=("Segoe UI", 16))
    mensaje_label.pack(pady=10)
    
    # Estado actual
    estado_label = ctk.CTkLabel(frame, text="Iniciando...", font=("Segoe UI", 12))
    estado_label.pack(pady=5)
    
    # Barra de progreso
    pb = ctk.CTkProgressBar(frame)
    pb.pack(fill="x", padx=20, pady=10)
    pb.set(0)
    
    # Forzar actualizaciones
    carga.update_idletasks()
    carga.update()
    
    return {
        "ventana": carga,
        "barra": pb,
        "estado": estado_label
    }

def actualizar_carga(carga_info, estado=None, progreso=None):
    
    #Actualiza el estado y progreso de la pantalla de carga.
    
    if carga_info["ventana"].winfo_exists():
        if estado is not None:
            carga_info["estado"].configure(text=estado)
        
        if progreso is not None:
            carga_info["barra"].set(progreso)
        
        # Actualizar la interfaz
        carga_info["ventana"].update_idletasks()
        carga_info["ventana"].update()

def cerrar_carga(carga_info):
    """
    Cierra la ventana de carga.
    """
    if carga_info["ventana"].winfo_exists():
        carga_info["ventana"].grab_release()
        carga_info["ventana"].destroy()

def add_file(tabla):
    """
    Función para añadir y procesar un archivo con pantalla de carga.
    """
    # Obtener la ventana principal (parent)
    parent = tabla.winfo_toplevel()
    
    # Seleccionar archivo
    file_path = filedialog.askopenfilename(
        filetypes=[("Archivos binarios", "*.ast"), ("Todos los archivos", "*.*")]
    )

    if not file_path:
        return
    
    # Crear y mostrar la pantalla de carga
    carga_info = mostrar_carga(parent, "Procesando archivo ASTERIX")
    
    def procesar_archivo():
        try:
            # Actualizar estado inicial
            actualizar_carga(carga_info, estado="Leyendo archivo...", progreso=0.1)
            time.sleep(0.2)  # Pequeña pausa para visualización
            
            with open(file_path, "rb") as f:
                data = f.read()

            actualizar_carga(carga_info, estado="Analizando estructura...", progreso=0.3)
            time.sleep(0.2)
            
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
                parent.after(0, lambda: cerrar_carga(carga_info))
                parent.after(10, lambda: messagebox.showinfo("Archivo vacío", 
                                            "El archivo seleccionado no contiene paquetes válidos."))
                return

            # Actualizar progreso
            actualizar_carga(carga_info, estado="Decodificando datos...", progreso=0.5)
            time.sleep(0.2)
            
            # Limpiar tabla (en el hilo principal)
            parent.after(0, lambda: tabla.delete(*tabla.get_children()))

            # Funciones locales
            insert_row = tabla.insert
            get_value = dict.get
            extend = list.extend

            columnas = [
                "SAC", "SIC", "TIME", "LAT",
                "LON", "H", "TYP020", "SIM020", "RDP020", "SPI020", "RAB020", "Validated",
                "Garbled", "CodeSource", "Validated_FL", "Garbled_FL", "FL", "FL_Corrected", "Mode3ACode", "Address",
                "ID", "BDS", "TRACK NUMBER", "TRACK STATUS", "X", "Y", "GS", "GS_KT", "HEADING",
                "COM", "STAT", "SI", "MSSC", "ARC", "AIC", "B1A", "B1B", "RHO", "THETA",
                "MCP_STATUS", "MCP_ALT", "FMS_STATUS", "FMS_ALT", "BP_STATUS", "BP_VALUE",
                "MODE_STATUS", "VNAV", "ALTHOLD", "APP", "TARGETALT_STATUS", "TARGETALT_SOURCE",
                "ROLL_STATUS", "ROLL_ANGLE", "TRACK_STATUS", "TRUE_TRACK", "GROUNDSPEED_STATUS", 
                "GROUNDSPEED", "TRACKRATE_STATUS", "TRACK_RATE", "AIRSPEED_STATUS", "TRUE_AIRSPEED",
                "HEADING_STATUS", "MAG_HEADING", "IAS_STATUS", "IAS", "MACH_STATUS", "MACH",
                "BARO_RATE_STATUS", "BARO_RATE", "INERTIAL_VERT_STATUS", "INERTIAL_VERT_VEL"
            ]

            # Preparar datos para la tabla
            filas_para_insertar = []
            total_packets = len(packets)
            
            actualizar_carga(carga_info, estado=f"Procesando {total_packets} paquetes...", progreso=0.6)
            
            # Procesar cada paquete
            for i, packet in enumerate(packets):
                # Actualizar progreso cada cierto número de paquetes
                if i % max(1, total_packets // 10) == 0:
                    progress = 0.6 + (0.3 * (i / total_packets))
                    actualizar_carga(carga_info, progreso=progress)
                
                cat = packet[0]
                length = int.from_bytes(packet[1:3], byteorder='big')
                hex_data = packet.hex()

                datos_extraidos = extraer_datos(hex_data)
                if not isinstance(datos_extraidos, dict):
                    datos_extraidos = {}

                fila = [i + 1, cat, length]
                extend(fila, (get_value(datos_extraidos, col, "N/A") for col in columnas))
                filas_para_insertar.append(fila)

            # Insertar filas en la tabla (en el hilo principal)
            def insertar_filas():
                for fila in filas_para_insertar:
                    insert_row("", "end", values=fila)
            
            parent.after(0, insertar_filas)
            
            # Finalizar con éxito
            actualizar_carga(carga_info, estado="¡Archivo cargado con éxito!", progreso=1.0)
            time.sleep(0.5)  # Breve pausa para mostrar el mensaje de éxito
            
            parent.after(0, lambda: cerrar_carga(carga_info))
            parent.after(10, lambda: messagebox.showinfo("Carga exitosa", 
                                          f"Se han cargado {len(packets)} paquetes."))

        except Exception as e:
            parent.after(0, lambda: cerrar_carga(carga_info))
            parent.after(10, lambda: messagebox.showerror("Error", 
                                          f"No se pudo procesar el archivo.\n{e}"))

    # Ejecutar en segundo plano
    thread = threading.Thread(target=procesar_archivo)
    thread.daemon = True
    thread.start()