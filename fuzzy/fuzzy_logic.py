"""
Módulo de Lógica Difusa - Sistema de Recomendación de Viviendas
Implementa las funciones básicas de lógica difusa utilizadas en el sistema.
Implementa las funciones matemáticas fundamentales de la lógica difusa. Es la "caja de herramientas" matemática básica.
- triangular_membership()    # Función triangular
- trapezoidal_membership()   # Función trapezoidal  
- gaussian_membership()      # Función gaussiana
- fuzzy_and(), fuzzy_or()    # Operaciones difusas
- weighted_average()         # Defuzzificación
"""

from typing import Dict, List
import math


class FuzzyLogic:
    """Implementación de lógica difusa para el sistema de recomendación"""
    
    @staticmethod
    def triangular_membership(x: float, a: float, b: float, c: float) -> float:
        """
        Función de pertenencia triangular
        a: inicio, b: pico, c: fin
        """
        if x <= a or x >= c:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        else:  # b < x < c
            return (c - x) / (c - b)
    
    @staticmethod
    def trapezoidal_membership(x: float, a: float, b: float, c: float, d: float) -> float:
        """
        Función de pertenencia trapezoidal
        a: inicio, b: inicio plateau, c: fin plateau, d: fin
        """
        if x <= a or x >= d:
            return 0.0
        elif a < x <= b:
            return (x - a) / (b - a)
        elif b < x <= c:
            return 1.0
        else:  # c < x < d
            return (d - x) / (d - c)
    
    @staticmethod
    def gaussian_membership(x: float, center: float, sigma: float) -> float:
        """Función de pertenencia gaussiana"""
        return math.exp(-0.5 * ((x - center) / sigma) ** 2)
    
    @staticmethod
    def fuzzy_and(values: List[float]) -> float:
        """Operación AND difusa (mínimo)"""
        return min(values) if values else 0.0
    
    @staticmethod
    def fuzzy_or(values: List[float]) -> float:
        """Operación OR difusa (máximo)"""
        return max(values) if values else 0.0
    
    @staticmethod
    def weighted_average(values: List[float], weights: List[float]) -> float:
        """Promedio ponderado para defuzzificación"""
        if not values or not weights or len(values) != len(weights):
            return 0.0
        return sum(v * w for v, w in zip(values, weights)) / sum(weights)
