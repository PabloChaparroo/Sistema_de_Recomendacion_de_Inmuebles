"""
Generador de mapas interactivos con Folium
"""
import folium
from typing import List, Dict, Tuple, Optional
import os

class MapGenerator:
    def create_map(self, properties: List[Dict], poi_coords: Tuple[float, float], poi_name: str) -> str:
        """Crea mapa con propiedades cercanas"""
        center = poi_coords
        m = folium.Map(location=center, zoom_start=13, tiles='OpenStreetMap')
        
        # Marcador del POI
        folium.Marker(
            location=poi_coords,
            popup=f"<b>📍 {poi_name}</b>",
            icon=folium.Icon(color='red', icon='star', prefix='fa')
        ).add_to(m)
        
        # Círculo de radio
        folium.Circle(
            location=poi_coords,
            radius=5000,
            color='red',
            fill=True,
            fillOpacity=0.1
        ).add_to(m)
        
        # Marcadores de propiedades
        for idx, prop in enumerate(properties, 1):
            dist = prop.get('distance_km', 999)
            color = 'green' if dist <= 1 else ('blue' if dist <= 3 else 'orange')
            
            popup_html = f"""
            <b>🏠 Propiedad #{idx}</b><br>
            <b>Precio:</b> ${prop.get('price', 0):,.0f}<br>
            <b>Habitaciones:</b> {int(prop.get('rooms', 0))}<br>
            <b>📏 Distancia:</b> {dist:.2f} km
            """
            
            folium.Marker(
                location=(prop['lat'], prop['lon']),
                popup=popup_html,
                icon=folium.Icon(color=color, icon='home', prefix='fa')
            ).add_to(m)
        
        output_path = os.path.abspath("mapa_propiedades_cercanas.html")
        m.save(output_path)
        return output_path
