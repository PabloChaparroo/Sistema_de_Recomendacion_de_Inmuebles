"""
Modelo de Frames para Sistema de Recomendación de Inmuebles
Representa conocimiento sobre propiedades, usuarios, preferencias y lógica difusa
"""

from dataclasses import dataclass, field
from typing import List, Dict, Optional
from enum import Enum
from datetime import datetime

class PropertyType(Enum):
    """Tipos de propiedad"""
    HOUSE = "casa"
    APARTMENT = "departamento"
    LOFT = "loft"

class ZoneType(Enum):
    """Tipos de zona por calidad"""
    PREMIUM = "premium"
    BUENA = "buena"
    ESTANDAR = "estandar"
    ECONOMICA = "economica"

@dataclass
class RangoDifuso:
    """Slot de RANGO con facetas difusas para evaluación"""
    min_val: float
    max_val: float
    target: float
    tolerancia: float
    
    def membership_ok(self, valor: float) -> float:
        """Calcula pertenencia triangular (0.0 - 1.0)"""
        if valor < self.min_val or valor > self.max_val:
            return 0.0
        if abs(valor - self.target) <= self.tolerancia:
            return 1.0
        return max(0, 1 - abs(valor - self.target) / (self.max_val - self.min_val))

@dataclass
class PropertyFrame:
    """Frame de Propiedad inmobiliaria"""
    name: str
    property_type: str  # 'casa' | 'departamento' | 'loft'
    price: int
    area: int  # m²
    rooms: int
    bathrooms: int
    location: str  # barrio/zona
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    nearby_amenities: List[Dict] = field(default_factory=list)
    
@dataclass
class UserFrame:
    """Frame de Usuario"""
    name: str
    age: Optional[int] = None
    budget: Optional[int] = None
    location_preference: Optional[str] = None  # barrio preferido
    min_rooms: int = 1
    property_type_pref: Optional[str] = None
    preferences: List[Dict] = field(default_factory=list)  # amenidades deseadas

@dataclass 
class PreferenciaAmenidad:
    """Preferencia de usuario por amenidad"""
    amenity_type: str  # 'parque', 'hospital', 'escuela', etc.
    priority: float  # 0.0 - 1.0
    max_distance: float  # metros

# RANGOS DIFUSOS PARA EVALUACIÓN
RANGOS_PRECIO = {
    "economico": RangoDifuso(50000, 150000, 80000, 30000),
    "medio": RangoDifuso(120000, 250000, 180000, 40000),
    "premium": RangoDifuso(200000, 500000, 350000, 80000),
}

RANGOS_AREA = {
    "pequeño": RangoDifuso(20, 60, 40, 10),
    "medio": RangoDifuso(50, 100, 75, 15),
    "grande": RangoDifuso(90, 200, 130, 30),
}

# AMENIDADES IMPORTANTES Y SUS PESOS
AMENIDADES_PESOS = {
    "parque": 0.7,
    "hospital": 0.9,
    "escuela": 0.8,
    "universidad": 0.8,
    "supermercado": 0.6,
    "transporte": 0.7,
    "centro_comercial": 0.5,
}

# DISTANCIA MÁXIMA IDEAL POR AMENIDAD (metros)
DISTANCIAS_IDEALES = {
    "parque": 500,
    "hospital": 2000,
    "escuela": 1000,
    "universidad": 3000,
    "supermercado": 800,
    "transporte": 300,
    "centro_comercial": 1500,
}

def calcular_membership_distancia(distancia: float, amenity_type: str) -> float:
    """Calcula membership difuso de distancia a amenidad"""
    ideal = DISTANCIAS_IDEALES.get(amenity_type, 1000)
    
    if distancia <= ideal:
        return 1.0
    elif distancia >= ideal * 3:
        return 0.0
    else:
        return 1.0 - ((distancia - ideal) / (ideal * 2))

def calcular_score_propiedad(propiedad: Dict, usuario: UserFrame) -> float:
    """
    Calcula score difuso de una propiedad para un usuario
    Combina: precio, tamaño, amenidades cercanas
    """
    score_total = 0.0
    peso_total = 0.0
    
    # 1. PRECIO (30% del peso)
    if usuario.budget:
        diff_precio = abs(propiedad['price'] - usuario.budget)
        tolerance = usuario.budget * 0.3
        score_precio = max(0, 1 - (diff_precio / (usuario.budget + tolerance)))
        score_total += score_precio * 0.3
        peso_total += 0.3
    
    # 2. HABITACIONES (20% del peso)
    if usuario.min_rooms:
        if propiedad['rooms'] >= usuario.min_rooms:
            score_rooms = 1.0
        else:
            score_rooms = propiedad['rooms'] / usuario.min_rooms
        score_total += score_rooms * 0.2
        peso_total += 0.2
    
    # 3. AMENIDADES CERCANAS (50% del peso)
    if 'nearby_amenities' in propiedad and propiedad['nearby_amenities']:
        score_amenidades = 0.0
        for amenidad in propiedad['nearby_amenities']:
            tipo = amenidad.get('type', '')
            distancia = amenidad.get('distance', 999999)
            
            peso_amenidad = AMENIDADES_PESOS.get(tipo, 0.5)
            membership_dist = calcular_membership_distancia(distancia, tipo)
            
            score_amenidades += membership_dist * peso_amenidad
        
        # Normalizar por cantidad de amenidades importantes
        if len(propiedad['nearby_amenities']) > 0:
            score_amenidades /= len(AMENIDADES_PESOS)
        
        score_total += score_amenidades * 0.5
        peso_total += 0.5
    
    # Normalizar score final
    if peso_total > 0:
        return score_total / peso_total
    return 0.0
