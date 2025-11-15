"""
Módulo de Modelos de Marcos - Sistema de Recomendación de Viviendas
Implementa los marcos (frames) que representan las entidades del sistema.
"""

from typing import Dict, List, Any, Optional
from dataclasses import dataclass, field
from enum import Enum
from fuzzy.transport_evaluation import TransportType


class AmenityType(Enum):
    """Tipos de amenidades/servicios"""
    PARK = "park"
    COMMERCIAL_CENTRE = "commercial_centre"
    HOSPITAL = "hospital"
    EDUCATION_CENTRE = "education_centre"
    BUS_STOP = "bus_stop"


@dataclass
class Address:
    """Marco para representar direcciones"""
    street: str
    number: str
    neighborhood: str
    city: str = "Mendoza"
    province: str = "Mendoza"
    postal_code: Optional[str] = None
    coordinates: Optional[Dict[str, float]] = None  # {lat, lng}
    
    def __str__(self):
        return f"{self.street} {self.number}, {self.neighborhood}, {self.city}"


@dataclass
class PropertyFrame:
    """Marco principal para propiedades inmobiliarias"""
    # Slots principales
    name: str
    address: Address
    property_type: str  # casa, departamento, oficina, etc.
    price: Optional[float] = None
    area: Optional[float] = None  # metros cuadrados
    rooms: Optional[int] = None
    bathrooms: Optional[int] = None
    
    # Slots de relación con amenidades
    nearby_amenities: List[Dict[str, Any]] = field(default_factory=list)
    
    # Facets (restricciones y validaciones)
    def validate_price(self) -> bool:
        """Valida que el precio sea positivo"""
        return self.price is None or self.price > 0
    
    def validate_area(self) -> bool:
        """Valida que el área sea positiva"""
        return self.area is None or self.area > 0
    
    def add_amenity(self, amenity_type: str, amenity_name: str, distance: float):
        """Agrega una amenidad cercana con su distancia"""
        self.nearby_amenities.append({
            "type": amenity_type,
            "name": amenity_name,
            "distance": distance  # en metros
        })
    
    def __str__(self):
        return f"Property: {self.name} at {self.address}"


@dataclass
class UserFrame:
    """Marco para usuarios del sistema"""
    # Slots principales
    name: str
    age: int
    preferences: List[Dict[str, Any]] = field(default_factory=list)
    transport_preferences: List[TransportType] = field(default_factory=list)
    
    # Facets (restricciones y validaciones)
    def validate_age(self) -> bool:
        """Valida que la edad sea válida"""
        return 0 < self.age < 150
    
    def add_preference(self, amenity_type: str, amenity_name: str, priority: int = 1):
        """Agrega una preferencia de amenidad con prioridad"""
        self.preferences.append({
            "type": amenity_type,
            "name": amenity_name,
            "priority": priority
        })
    
    def add_transport(self, transport: TransportType):
        """Agrega un medio de transporte preferido"""
        if transport not in self.transport_preferences:
            self.transport_preferences.append(transport)
    
    def __str__(self):
        return f"User: {self.name}, Age: {self.age}"


@dataclass
class AmenityFrame:
    """Marco base para amenidades/servicios"""
    # Slots principales
    name: str
    amenity_type: AmenityType
    address: Address
    
    # Slots específicos por tipo
    area: Optional[float] = None  # para parques
    stores_count: Optional[int] = None  # para centros comerciales
    education_type: Optional[str] = None  # para centros educativos
    is_terminal: Optional[bool] = None  # para paradas de bus
    
    # Facets (restricciones y validaciones)
    def validate_type_specific_data(self) -> bool:
        """Valida datos específicos según el tipo de amenidad"""
        if self.amenity_type == AmenityType.PARK:
            return self.area is None or self.area > 0
        elif self.amenity_type == AmenityType.COMMERCIAL_CENTRE:
            return self.stores_count is None or self.stores_count > 0
        elif self.amenity_type == AmenityType.BUS_STOP:
            return isinstance(self.is_terminal, bool)
        return True
    
    def __str__(self):
        return f"{self.amenity_type.value.title()}: {self.name}"


@dataclass
class TransportFrame:
    """Marco para medios de transporte"""
    # Slots principales
    transport_type: TransportType
    cost_per_km: Optional[float] = None
    max_speed: Optional[float] = None  # km/h
    availability: str = "always"  # always, schedule, limited
    
    # Facets (restricciones y validaciones)
    def validate_cost(self) -> bool:
        """Valida que el costo sea no negativo"""
        return self.cost_per_km is None or self.cost_per_km >= 0
    
    def validate_speed(self) -> bool:
        """Valida que la velocidad sea positiva"""
        return self.max_speed is None or self.max_speed > 0
    
    def __str__(self):
        return f"Transport: {self.transport_type.value}"
