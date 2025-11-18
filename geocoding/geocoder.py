"""
Sistema de geocodificación usando OpenStreetMap Nominatim
Convierte direcciones en coordenadas y calcula distancias
"""
import time
import requests
from typing import Optional, Tuple
from math import radians, sin, cos, sqrt, atan2

class Geocoder:
    def __init__(self):
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self.headers = {'User-Agent': 'SistemaRecomendacionInmuebles/1.0'}
        self.cache = {}
        
    def geocode_poi(self, nombre_lugar: str) -> Optional[Tuple[float, float]]:
        """Busca coordenadas de un punto de interés"""
        # Agregar contexto solo si no está presente
        if "mendoza" not in nombre_lugar.lower() or "argentina" not in nombre_lugar.lower():
            query = f"{nombre_lugar}, Mendoza, Argentina"
        else:
            query = nombre_lugar
        
        if query in self.cache:
            return self.cache[query]
        
        params = {'q': query, 'format': 'json', 'limit': 1}
        
        try:
            time.sleep(1)  # Rate limiting
            response = requests.get(self.base_url, params=params, headers=self.headers, timeout=5)
            response.raise_for_status()
            
            results = response.json()
            if results and len(results) > 0:
                lat = float(results[0]['lat'])
                lon = float(results[0]['lon'])
                coords = (lat, lon)
                self.cache[query] = coords
                print(f"   📍 Encontrado: {nombre_lugar} → ({lat:.4f}, {lon:.4f})")
                return coords
        except Exception as e:
            print(f"   ⚠️  Error buscando '{nombre_lugar}': {e}")
        
        return None
    
    @staticmethod
    def haversine_distance(coord1: Tuple[float, float], coord2: Tuple[float, float]) -> float:
        """Calcula distancia en km usando Haversine"""
        lat1, lon1 = coord1
        lat2, lon2 = coord2
        R = 6371.0
        
        lat1_rad, lon1_rad = radians(lat1), radians(lon1)
        lat2_rad, lon2_rad = radians(lat2), radians(lon2)
        
        dlat = lat2_rad - lat1_rad
        dlon = lon2_rad - lon1_rad
        
        a = sin(dlat/2)**2 + cos(lat1_rad) * cos(lat2_rad) * sin(dlon/2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))
        
        return R * c
