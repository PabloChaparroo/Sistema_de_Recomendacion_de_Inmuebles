"""
Módulo de Evaluadores Difusos - Sistema de Recomendación de Viviendas
Implementa los evaluadores difusos para precios, distancias y amenidades.
QUÉ HACE: Evaluadores específicos para cada criterio
- PriceFuzzyEvaluator          # "¿Es barato/caro este precio?"
- DistanceFuzzyEvaluator       # "¿Está cerca/lejos?"
- AmenityImportanceFuzzyEvaluator  # "¿Qué tan importante es esta amenidad?"
"""

from typing import Dict, List, Any
from fuzzy.fuzzy_logic import FuzzyLogic
from fuzzy.transport_evaluation import TransportType, TransportAccessibilityEvaluator


class PriceFuzzyEvaluator:
    """Evaluador difuso para precios de propiedades"""
    
    def __init__(self):
        # Definir rangos de precios para Mendoza (en pesos argentinos)
        self.very_cheap_max = 40000
        self.cheap_max = 70000
        self.moderate_max = 120000
        self.expensive_max = 200000
        
    def evaluate_price_membership(self, price: float) -> Dict[str, float]:
        """
        Evalúa el grado de pertenencia de un precio a categorías difusas
        Retorna: {'very_cheap': 0.8, 'cheap': 0.2, 'moderate': 0.0, 'expensive': 0.0}
        """
        memberships = {}
        
        # Muy barato (triangular: 0, 20000, 40000)
        memberships['very_cheap'] = FuzzyLogic.triangular_membership(
            price, 0, 20000, self.very_cheap_max
        )
        
        # Barato (triangular: 20000, 55000, 70000)
        memberships['cheap'] = FuzzyLogic.triangular_membership(
            price, 20000, 55000, self.cheap_max
        )
        
        # Moderado (triangular: 55000, 95000, 120000)
        memberships['moderate'] = FuzzyLogic.triangular_membership(
            price, 55000, 95000, self.moderate_max
        )
        
        # Caro (trapezoidal: 95000, 120000, 160000, 200000+)
        memberships['expensive'] = FuzzyLogic.trapezoidal_membership(
            price, 95000, 120000, 160000, self.expensive_max
        )
        
        return memberships


class DistanceFuzzyEvaluator:
    """Evaluador difuso para distancias a amenidades (versión mejorada con transporte)"""
    
    def __init__(self):
        self.transport_evaluator = TransportAccessibilityEvaluator()
        
    def evaluate_distance_membership(self, distance: float, transport_mode: TransportType = None) -> Dict[str, float]:
        """
        Evalúa el grado de pertenencia de una distancia a categorías difusas
        Si se especifica modo de transporte, usa rangos específicos para ese modo
        """
        if transport_mode:
            # Usar evaluador específico por transporte
            evaluation = self.transport_evaluator.evaluate_accessibility(distance, transport_mode)
            return evaluation['fuzzy_memberships']
        else:
            # Usar rangos genéricos (compatible con código existente)
            memberships = {}
            
            # Muy cerca (triangular: 0, 100, 200)
            memberships['very_close'] = FuzzyLogic.triangular_membership(distance, 0, 100, 200)
            
            # Cerca (triangular: 100, 350, 500)
            memberships['close'] = FuzzyLogic.triangular_membership(distance, 100, 350, 500)
            
            # Moderado (triangular: 350, 750, 1000)
            memberships['moderate'] = FuzzyLogic.triangular_membership(distance, 350, 750, 1000)
            
            # Lejos (gaussiana centrada en 1500, sigma=500)
            memberships['far'] = FuzzyLogic.gaussian_membership(distance, 1500, 500)
            
            return memberships


class AmenityImportanceFuzzyEvaluator:
    """Evaluador difuso para importancia de amenidades"""
    
    def __init__(self):
        self.amenity_weights = {
            'education_centre': 0.9,  # Muy importante para estudiantes
            'commercial_centre': 0.7,  # Importante para comodidad
            'hospital': 0.8,  # Importante para salud
            'park': 0.6,  # Moderadamente importante
            'bus_stop': 0.8  # Importante para transporte
        }
    
    def evaluate_amenity_importance(self, amenity_type: str, user_preferences: List[Dict]) -> float:
        """
        Evalúa la importancia difusa de una amenidad para un usuario específico
        """
        base_weight = self.amenity_weights.get(amenity_type, 0.5)
        
        # Verificar si el usuario tiene preferencias específicas por esta amenidad
        user_interest = 0.0
        for pref in user_preferences:
            if pref['type'] == amenity_type:
                # Prioridad 1 = máximo interés, prioridad 5 = mínimo interés
                user_interest = (6 - pref['priority']) / 5.0
                break
        
        # Combinar peso base con interés del usuario
        return FuzzyLogic.fuzzy_or([base_weight, user_interest])
