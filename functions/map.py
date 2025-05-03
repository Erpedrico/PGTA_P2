import pandas as pd
import folium
import tempfile
import webbrowser
from datetime import datetime

class MapaViewer:
    def __init__(self, df):
        # 1. Copiar y preparar df
        self.df = df.copy()
        # Limpiamos TIME y convertimos a segundos
        self.df["TIME"] = self.df["TIME"].str.strip().apply(self._to_seconds)
        # Convertir columnas numéricas y eliminar filas sin datos
        for col in ("LAT", "LON", "H", "TIME"):
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
        self.df.dropna(subset=["LAT", "LON", "H", "TIME"], inplace=True)

        # 2. Quedarnos solo con la primera aparición de cada Address
        self.df.sort_values("TIME", inplace=True)
        self.df.drop_duplicates(subset="Address", keep="first", inplace=True)

        if self.df.empty:
            print("Error: No hay datos válidos para el mapa.")
            return

        # 3. Generar y abrir el mapa
        self._crear_y_abrir_mapa()

    def _to_seconds(self, tstr):
        try:
            t = datetime.strptime(tstr, "%H:%M:%S.%f")
            return t.hour*3600 + t.minute*60 + t.second + t.microsecond/1e6
        except:
            return float("nan")

    def _crear_y_abrir_mapa(self):
        # Centrar el mapa en la media de posiciones
        center = [self.df["LAT"].mean(), self.df["LON"].mean()]
        m = folium.Map(location=center, zoom_start=6)

        # Añadir marcadores
        for _, row in self.df.iterrows():
            popup = (f"Avión: {row['Address']}<br>"
                     f"Altura: {row['H']} m<br>"
                     f"Hora (s): {row['TIME']:.3f}")
            folium.Marker(
                [row["LAT"], row["LON"]],
                popup=popup,
                icon=folium.Icon(color="blue", icon="plane", prefix="fa")
            ).add_to(m)

        # Guardar en fichero temporal y abrir
        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
            m.save(tmp.name)
            url = f"file://{tmp.name}"
        webbrowser.open(url)

def abrir_mapa_webview(df):
    MapaViewer(df)

