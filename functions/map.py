import pandas as pd
import folium
import tempfile
import webbrowser
from datetime import datetime
import json

class MapaViewer:
    def __init__(self, df):
        self.df = df.copy()
        self.df["TIME"] = self.df["TIME"].str.strip().apply(self._to_seconds)

        for col in ("LAT", "LON", "H", "TIME"):
            self.df[col] = pd.to_numeric(self.df[col], errors="coerce")
        self.df.dropna(subset=["LAT", "LON", "H", "TIME"], inplace=True)

        # Agrupar por segundo (sin milisegundos)
        self.df["SECOND"] = self.df["TIME"].astype(int)  # Usar el tiempo en segundos completos

        if self.df.empty:
            print("Error: No hay datos válidos para el mapa.")
            return

        self._crear_y_abrir_mapa()

    def _to_seconds(self, tstr):
        try:
            t = datetime.strptime(tstr, "%H:%M:%S.%f")
            return t.hour * 3600 + t.minute * 60 + t.second  # Ignorar los milisegundos
        except:
            return float("nan")

    def _crear_y_abrir_mapa(self):
        # Agrupar por segundo (sin milisegundos)
        groups = self.df.groupby("SECOND")
        data_by_second = {
            str(int(second)): [
                {
                    "lat": row["LAT"],
                    "lon": row["LON"],
                    "address": row["Address"],
                    "popup": f"Avión: {row['Address']}<br>Altura: {row['H']} m<br>Hora: {int(second)//3600:02}:{(int(second)%3600)//60:02}:{int(second)%60:02}"
                }
                for _, row in group.iterrows()
            ]
            for second, group in groups
        }

        seconds_list = sorted(data_by_second.keys())
        center = [self.df["LAT"].mean(), self.df["LON"].mean()]
        m = folium.Map(location=center, zoom_start=6)

        m.get_root().html.add_child(folium.Element(f"""
            <div id="nav-controls" style="position: fixed; top: 10px; left: 50%; transform: translateX(-50%); z-index: 9999; background: white; padding: 8px; border-radius: 8px; box-shadow: 0 2px 6px rgba(0,0,0,0.3);">
                <button onclick="prevGroup()">⬅️</button>
                <span id="time-label">Cargando...</span>
                <button onclick="nextGroup()">➡️</button>
                <button id="pause-btn" onclick="toggleAutoChange()">Pause</button>
            </div>
            <script>
                const data = {json.dumps(data_by_second)};
                const seconds = {json.dumps(seconds_list)};
                let currentIndex = 0;
                let markers = [];
                let autoChangeInterval = null;
                let isAutoChanging = true;

                function formatSecond(s) {{
                    const h = Math.floor(s / 3600);
                    const m = Math.floor((s % 3600) / 60);
                    const sec = s % 60;
                    return ("0" + h).slice(-2) + ":" + ("0" + m).slice(-2) + ":" + ("0" + sec).slice(-2);
                }}

                function updateMarkers(map) {{
                    // Limpiar marcadores existentes
                    markers.forEach(m => map.removeLayer(m));
                    markers = [];

                    const currentSecond = parseInt(seconds[currentIndex]);
                    const startSecond = currentSecond - 3;

                    // Mostrar desde (current - 3) hasta current
                    for (let i = 0; i < seconds.length; i++) {{
                        const sec = parseInt(seconds[i]);
                        if (sec >= startSecond && sec <= currentSecond) {{
                            const group = data[seconds[i]];
                            group.forEach(info => {{
                                const htmlIcon = L.divIcon({{
                                    html: `
                                        <div style="text-align: center;">
                                            <img src="https://cdn-icons-png.flaticon.com/128/723/723955.png" style="width: 32px; height: 32px;"><br>
                                            <span style="font-size: 12px; color: black;">${{info.address}}</span>
                                        </div>
                                    `,
                                    iconSize: [32, 40],
                                    iconAnchor: [16, 16],
                                    className: ""
                                }});
                                const marker = L.marker([info.lat, info.lon], {{ icon: htmlIcon }}).addTo(map);
                                marker.bindPopup(info.popup);
                                markers.push(marker);
                            }});
                        }}
                    }}

                    document.getElementById("time-label").innerText = formatSecond(currentSecond);
                }}



                function nextGroup() {{
                    if (currentIndex < seconds.length - 1) {{
                        currentIndex++;
                        updateMarkers(window.map);
                    }}
                }}

                function prevGroup() {{
                    if (currentIndex > 0) {{
                        currentIndex--;
                        updateMarkers(window.map);
                    }}
                }}

                function toggleAutoChange() {{
                    if (isAutoChanging) {{
                        clearInterval(autoChangeInterval);
                        document.getElementById("pause-btn").innerText = "Resume";
                    }} else {{
                        autoChangeInterval = setInterval(() => {{
                            nextGroup();
                        }}, 1000);  // Cambiar cada 1 segundo
                        document.getElementById("pause-btn").innerText = "Pause";
                    }}
                    isAutoChanging = !isAutoChanging;
                }}

                setTimeout(() => {{
                    const leafletMap = Object.values(window).find(v => v instanceof L.Map);
                    if (!leafletMap) {{
                        console.error("No se pudo encontrar el mapa de Leaflet.");
                        return;
                    }}
                    window.map = leafletMap;
                    updateMarkers(window.map);
                    autoChangeInterval = setInterval(() => {{
                        nextGroup();
                    }}, 1000);  // Cambiar cada 1 segundo
                }}, 500);
            </script>
        """))

        with tempfile.NamedTemporaryFile(suffix=".html", delete=False, mode="w", encoding="utf-8") as tmp:
            m.save(tmp.name)
            webbrowser.open(f"file://{tmp.name}")

def abrir_mapa_webview(df):
    MapaViewer(df)
