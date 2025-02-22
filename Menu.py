import tkinter as tk
from tkinter import filedialog, messagebox
import folium
import pandas as pd
import os
import webview

# Crear la ventana principal
root = tk.Tk()
root.title("Visor de Mapas")
root.geometry("800x600")  # Aumenta el tamaño para visualizar mejor el mapa

# Crear un mapa base (se abrirá en el navegador)
mapa = folium.Map(location=[20, 0], zoom_start=2)
mapa_path = "mapa.html"
mapa.save(mapa_path)

# Función para abrir el mapa en el navegador
def abrir_mapa():
    os.startfile(mapa_path)

# Función para añadir un archivo
def añadir_archivo():
    file_path = filedialog.askopenfilename(filetypes=[("Archivos CSV", "*.csv"), ("Todos los archivos", "*.*")])
    if not file_path:
        return
    
    try:
        df = pd.read_csv(file_path)
        messagebox.showinfo("Carga exitosa", f"Archivo '{os.path.basename(file_path)}' cargado correctamente.")
        print(df.head())  # Para depuración
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo cargar el archivo.\n{str(e)}")

# Función de Filtrado (Placeholder)
def filtrar_datos():
    messagebox.showinfo("Filtrar", "Función de filtrado en construcción.")

# Crear botones en la interfaz
btn_abrir = tk.Button(root, text="Abrir Mapa en Navegador", command=abrir_mapa)
btn_archivo = tk.Button(root, text="Añadir Archivo", command=añadir_archivo)
btn_filtrar = tk.Button(root, text="Filtrar", command=filtrar_datos)

# Posicionar botones
btn_abrir.pack(side=tk.LEFT, padx=10, pady=10)
btn_archivo.pack(side=tk.LEFT, padx=10, pady=10)
btn_filtrar.pack(side=tk.LEFT, padx=10, pady=10)

# Iniciar una ventana emergente con el mapa dentro usando PyWebView
def abrir_mapa_webview():
    webview.create_window("Mapa Interactivo", mapa_path)
    webview.start()

# Botón para abrir el mapa dentro de la ventana webview
btn_mapa_webview = tk.Button(root, text="Ver Mapa", command=abrir_mapa_webview)
btn_mapa_webview.pack(side=tk.LEFT, padx=10, pady=10)

# Iniciar la aplicación
root.mainloop()

