"""
Módulo de Evaluación de Transporte - Sistema de Recomendación de Viviendas
Implementa la evaluación de accesibilidad basada en modo de transporte.
QUÉ HACE: Evalúa accesibilidad según modo de transporte
- TransportType (WALK, BIKE, BUS, CAR)
- TransportAccessibilityEvaluator
  - evaluate_accessibility()           # Evalúa una distancia
  - compare_accessibility_modes()      # Compara varios transportes

"""

from typing import Dict, List, Any
from enum import Enum
from fuzzy.fuzzy_logic import FuzzyLogic


class TransportType(Enum):
    """Tipos de transporte disponibles"""
    WALK = "walk"
    BIKE = "bike"
    BUS = "bus"
    CAR = "car"


class TransportAccessibilityEvaluator:
    """Evaluador de accesibilidad basado en modo de transporte"""
    
    def __init__(self):
        # Definir rangos de accesibilidad por modo de transporte (en metros)
        self.accessibility_ranges = {
            TransportType.WALK: {
                'very_close': (0, 200),      # 0-200m: caminata cómoda
                'close': (200, 500),         # 200-500m: caminata aceptable
                'moderate': (500, 1000),     # 500m-1km: caminata larga
                'far': (1000, 2000),         # 1-2km: caminata muy larga
                'very_far': (2000, float('inf'))  # >2km: inaccesible caminando
            },
            TransportType.BIKE: {
                'very_close': (0, 500),      # 0-500m: bicicleta muy cómoda
                'close': (500, 1500),        # 500m-1.5km: bicicleta cómoda
                'moderate': (1500, 3000),    # 1.5-3km: bicicleta aceptable
                'far': (3000, 5000),         # 3-5km: bicicleta larga
                'very_far': (5000, float('inf'))  # >5km: inaccesible en bici
            },
            TransportType.BUS: {
                'very_close': (0, 300),      # 0-300m: parada muy cerca
                'close': (300, 800),         # 300-800m: parada cerca
                'moderate': (800, 1500),     # 800m-1.5km: parada aceptable
                'far': (1500, 3000),         # 1.5-3km: parada lejos
                'very_far': (3000, float('inf'))  # >3km: inaccesible en bus
            },
            TransportType.CAR: {
                'very_close': (0, 1000),     # 0-1km: auto muy cómodo
                'close': (1000, 3000),       # 1-3km: auto cómodo
                'moderate': (3000, 8000),    # 3-8km: auto aceptable
                'far': (8000, 15000),        # 8-15km: auto largo
                'very_far': (15000, float('inf'))  # >15km: muy lejos en auto
            }
        }
        
        # Tiempo estimado por modo de transporte (minutos por km)
        self.time_per_km = {
            TransportType.WALK: 12,    # 5 km/h
            TransportType.BIKE: 4,     # 15 km/h
            TransportType.BUS: 6,      # 10 km/h (incluyendo espera)
            TransportType.CAR: 2       # 30 km/h (incluyendo tráfico)
        }
    
    def evaluate_accessibility(self, distance: float, transport_mode: TransportType) -> Dict[str, Any]:
        """
        Evalúa la accesibilidad de una amenidad considerando la distancia y modo de transporte
        
        Args:
            distance: Distancia en metros
            transport_mode: Modo de transporte
            
        Returns:
            Dict con clasificación, score de accesibilidad, tiempo estimado y membresías difusas
        """
        ranges = self.accessibility_ranges[transport_mode]
        
        # Determinar clasificación de accesibilidad
        classification = "very_far"
        accessibility_score = 0.0
        
        if distance <= ranges['very_close'][1]:
            classification = "very_close"
            accessibility_score = 1.0
        elif distance <= ranges['close'][1]:
            classification = "close"
            accessibility_score = 0.8
        elif distance <= ranges['moderate'][1]:
            classification = "moderate"
            accessibility_score = 0.6
        elif distance <= ranges['far'][1]:
            classification = "far"
            accessibility_score = 0.3
        else:
            classification = "very_far"
            accessibility_score = 0.0
        
        # Calcular tiempo estimado
        distance_km = distance / 1000
        estimated_time = distance_km * self.time_per_km[transport_mode]
        
        # Calcular membresías difusas para el modo de transporte específico
        memberships = self._calculate_transport_specific_memberships(distance, transport_mode)
        
        return {
            'classification': classification,
            'accessibility_score': accessibility_score,
            'estimated_time_minutes': round(estimated_time, 1),
            'distance_km': round(distance_km, 2),
            'transport_mode': transport_mode.value,
            'fuzzy_memberships': memberships
        }
    
    def _calculate_transport_specific_memberships(self, distance: float, transport_mode: TransportType) -> Dict[str, float]:
        """Calcula membresías difusas específicas para el modo de transporte"""
        ranges = self.accessibility_ranges[transport_mode]
        memberships = {}
        
        # Muy cerca
        memberships['very_close'] = FuzzyLogic.triangular_membership(
            distance, ranges['very_close'][0], 
            ranges['very_close'][0] + (ranges['very_close'][1] - ranges['very_close'][0]) / 2,
            ranges['very_close'][1]
        )
        
        # Cerca
        memberships['close'] = FuzzyLogic.triangular_membership(
            distance, ranges['close'][0],
            ranges['close'][0] + (ranges['close'][1] - ranges['close'][0]) / 2,
            ranges['close'][1]
        )
        
        # Moderado
        memberships['moderate'] = FuzzyLogic.triangular_membership(
            distance, ranges['moderate'][0],
            ranges['moderate'][0] + (ranges['moderate'][1] - ranges['moderate'][0]) / 2,
            ranges['moderate'][1]
        )
        
        # Lejos
        memberships['far'] = FuzzyLogic.triangular_membership(
            distance, ranges['far'][0],
            ranges['far'][0] + (ranges['far'][1] - ranges['far'][0]) / 2,
            ranges['far'][1]
        )
        
        # Muy lejos (gaussiana centrada en el punto medio del rango)
        very_far_center = ranges['very_far'][0] + 1000  # 1km después del inicio del rango
        memberships['very_far'] = FuzzyLogic.gaussian_membership(
            distance, very_far_center, 2000
        )
        
        return memberships
    
    def compare_accessibility_modes(self, distance: float, available_transports: List[TransportType]) -> Dict[str, Dict[str, Any]]:
        """
        Compara la accesibilidad usando diferentes modos de transporte para la misma distancia
        
        Args:
            distance: Distancia en metros
            available_transports: Lista de modos de transporte disponibles
            
        Returns:
            Dict con evaluación para cada modo de transporte
        """
        comparisons = {}
        
        for transport in available_transports:
            comparisons[transport.value] = self.evaluate_accessibility(distance, transport)
        
        # Ordenar por score de accesibilidad (mejor primero)
        sorted_transports = sorted(
            comparisons.items(),
            key=lambda x: x[1]['accessibility_score'],
            reverse=True
        )
        
        return {
            'transport_comparisons': dict(comparisons),
            'best_transport': sorted_transports[0][0] if sorted_transports else None,
            'accessibility_ranking': [transport[0] for transport in sorted_transports]
        }
