"""
Demonio de Descubrimiento de Patrones Ocultos - Sistema de Recomendación de Viviendas
Encuentra relaciones no obvias entre características y preferencias de usuarios.

FUNCIONALIDAD:
- Encuentra correlaciones inesperadas entre características
- Descubre que "usuarios que buscan X también valoran Y"
- Identifica características que predicen satisfacción
- Detecta segmentos de usuarios con comportamientos similares
- Revela patrones ocultos en preferencias y decisiones
"""

import json
import time
import random
from typing import Dict, List, Any, Optional, Tuple, Set
from datetime import datetime, timedelta
from collections import defaultdict, Counter
from itertools import combinations
from statistics import mean, correlation


class PatternDiscoveryDemon:
    """Demonio que descubre patrones ocultos en comportamientos y preferencias"""
    
    def __init__(self, system):
        self.system = system
        self.execution_count = 0
        self.last_execution = None
        
        # Patrones descubiertos
        self.discovered_correlations = []          # Correlaciones entre características
        self.user_segments = defaultdict(list)     # Segmentos de usuarios similares
        self.satisfaction_predictors = {}          # Características que predicen satisfacción
        self.co_occurrence_patterns = defaultdict(int)  # Patrones de co-ocurrencia
        self.hidden_preferences = defaultdict(dict)     # Preferencias implícitas descubiertas
        
        # Configuración
        self.min_correlation_threshold = 0.6
        self.min_pattern_frequency = 3
        self.discovery_confidence_threshold = 0.7
        
    def execute(self):
        """Ejecuta el ciclo de descubrimiento de patrones"""
        self.execution_count += 1
        self.last_execution = datetime.now()
        
        print(f"🔍 DEMONIO DE DESCUBRIMIENTO DE PATRONES OCULTOS (Ejecución #{self.execution_count})")
        
        # Analizar correlaciones entre características de propiedades
        correlations = self._discover_property_correlations()
        
        # Descubrir segmentos de usuarios
        user_segments = self._discover_user_segments()
        
        # Encontrar predictores de satisfacción
        satisfaction_predictors = self._discover_satisfaction_predictors()
        
        # Analizar patrones de co-ocurrencia
        cooccurrence_patterns = self._analyze_cooccurrence_patterns()
        
        # Detectar preferencias implícitas
        implicit_preferences = self._detect_implicit_preferences()
        
        result = {
            'timestamp': self.last_execution.isoformat(),
            'new_correlations': len(correlations),
            'user_segments_found': len(user_segments),
            'satisfaction_predictors': len(satisfaction_predictors),
            'cooccurrence_patterns': len(cooccurrence_patterns),
            'implicit_preferences': len(implicit_preferences)
        }
        
        print(f"   🔗 Nuevas correlaciones: {len(correlations)}")
        print(f"   👥 Segmentos de usuarios: {len(user_segments)}")
        print(f"   ⭐ Predictores de satisfacción: {len(satisfaction_predictors)}")
        print(f"   🎯 Patrones de co-ocurrencia: {len(cooccurrence_patterns)}")
        
        return result
        
    def _discover_property_correlations(self) -> List[Dict]:
        """Descubre correlaciones entre características de propiedades"""
        correlations = []
        
        if len(self.system.properties) < 3:
            return correlations
            
        # Extraer características numéricas
        properties_data = []
        for prop in self.system.properties:
            prop_data = {
                'price': prop.price,
                'rooms': prop.rooms,
                'area': prop.area,
                'amenities_count': len(prop.nearby_amenities),
                'avg_distance_to_amenities': self._calculate_avg_amenity_distance(prop)
            }
            properties_data.append(prop_data)
            
        # Calcular correlaciones entre pares de características
        characteristics = ['price', 'rooms', 'area', 'amenities_count', 'avg_distance_to_amenities']
        
        for char1, char2 in combinations(characteristics, 2):
            values1 = [prop[char1] for prop in properties_data if prop[char1] is not None]
            values2 = [prop[char2] for prop in properties_data if prop[char2] is not None]
            
            if len(values1) >= 3 and len(values2) >= 3 and len(values1) == len(values2):
                try:
                    corr = self._calculate_correlation(values1, values2)
                    
                    if abs(corr) >= self.min_correlation_threshold:
                        correlation_data = {
                            'characteristic_1': char1,
                            'characteristic_2': char2,
                            'correlation': corr,
                            'strength': 'strong' if abs(corr) > 0.8 else 'moderate',
                            'direction': 'positive' if corr > 0 else 'negative',
                            'samples': len(values1),
                            'discovered_at': datetime.now().isoformat(),
                            'confidence': min(abs(corr), 0.95)
                        }
                        
                        correlations.append(correlation_data)
                        self.discovered_correlations.append(correlation_data)
                        
                except Exception as e:
                    # Correlación no calculable
                    pass
                    
        # Mantener solo últimas 50 correlaciones
        if len(self.discovered_correlations) > 50:
            self.discovered_correlations = self.discovered_correlations[-50:]
            
        return correlations
        
    def _calculate_correlation(self, values1: List[float], values2: List[float]) -> float:
        """Calcula correlación entre dos listas de valores"""
        if len(values1) != len(values2) or len(values1) < 2:
            return 0.0
            
        mean1 = mean(values1)
        mean2 = mean(values2)
        
        numerator = sum((v1 - mean1) * (v2 - mean2) for v1, v2 in zip(values1, values2))
        
        sum_sq1 = sum((v1 - mean1) ** 2 for v1 in values1)
        sum_sq2 = sum((v2 - mean2) ** 2 for v2 in values2)
        
        denominator = (sum_sq1 * sum_sq2) ** 0.5
        
        return numerator / denominator if denominator != 0 else 0.0
        
    def _calculate_avg_amenity_distance(self, prop) -> Optional[float]:
        """Calcula la distancia promedio a amenidades de una propiedad"""
        if not prop.nearby_amenities:
            return None
            
        distances = [amenity['distance'] for amenity in prop.nearby_amenities]
        return mean(distances) if distances else None
        
    def _discover_user_segments(self) -> List[Dict]:
        """Descubre segmentos de usuarios con comportamientos similares"""
        segments = []
        
        if len(self.system.users) < 2:
            return segments
            
        # Agrupar usuarios por características similares
        user_profiles = []
        for user in self.system.users:
            profile = {
                'user': user,
                'age_group': self._get_age_group(user.age),
                'transport_types': set(t.value for t in user.transport_preferences) if user.transport_preferences else set(),
                'preference_count': len(user.preferences),
                'has_education_preference': any('education' in p.get('type', '') for p in user.preferences),
                'has_transport_preference': any('transport' in p.get('type', '') or 'bus' in p.get('type', '') for p in user.preferences),
                'has_park_preference': any('park' in p.get('type', '') for p in user.preferences)
            }
            user_profiles.append(profile)
            
        # Encontrar grupos de usuarios similares
        for i, profile1 in enumerate(user_profiles):
            similar_users = [profile1['user'].name]
            
            for j, profile2 in enumerate(user_profiles[i+1:], i+1):
                similarity = self._calculate_user_similarity(profile1, profile2)
                
                if similarity >= self.discovery_confidence_threshold:
                    similar_users.append(profile2['user'].name)
                    
            if len(similar_users) >= 2:  # Al menos 2 usuarios similares
                segment = {
                    'segment_id': f'segment_{len(segments) + 1}',
                    'users': similar_users,
                    'common_characteristics': self._extract_common_characteristics(
                        [profile for profile in user_profiles if profile['user'].name in similar_users]
                    ),
                    'size': len(similar_users),
                    'discovered_at': datetime.now().isoformat()
                }
                
                segments.append(segment)
                self.user_segments[segment['segment_id']] = similar_users
                
        return segments
        
    def _get_age_group(self, age: int) -> str:
        """Clasifica edad en grupos"""
        if age < 25:
            return 'joven'
        elif age < 35:
            return 'joven_adulto'
        elif age < 50:
            return 'adulto'
        else:
            return 'adulto_mayor'
            
    def _calculate_user_similarity(self, profile1: Dict, profile2: Dict) -> float:
        """Calcula similitud entre dos perfiles de usuario"""
        similarities = []
        
        # Similitud por edad
        if profile1['age_group'] == profile2['age_group']:
            similarities.append(1.0)
        else:
            similarities.append(0.0)
            
        # Similitud por transporte
        transport1 = profile1['transport_types']
        transport2 = profile2['transport_types']
        
        if transport1 and transport2:
            intersection = len(transport1 & transport2)
            union = len(transport1 | transport2)
            transport_similarity = intersection / union if union > 0 else 0.0
        else:
            transport_similarity = 1.0 if not transport1 and not transport2 else 0.0
            
        similarities.append(transport_similarity)
        
        # Similitud por tipos de preferencias
        pref_similarities = []
        for pref_type in ['has_education_preference', 'has_transport_preference', 'has_park_preference']:
            if profile1[pref_type] == profile2[pref_type]:
                pref_similarities.append(1.0)
            else:
                pref_similarities.append(0.0)
                
        similarities.extend(pref_similarities)
        
        return mean(similarities) if similarities else 0.0
        
    def _extract_common_characteristics(self, profiles: List[Dict]) -> Dict:
        """Extrae características comunes de un grupo de perfiles"""
        if not profiles:
            return {}
            
        common = {}
        
        # Grupo de edad más común
        age_groups = [p['age_group'] for p in profiles]
        common['dominant_age_group'] = Counter(age_groups).most_common(1)[0][0]
        
        # Transportes más comunes
        all_transports = set()
        for p in profiles:
            all_transports.update(p['transport_types'])
            
        common['common_transports'] = list(all_transports)
        
        # Preferencias comunes
        education_count = sum(1 for p in profiles if p['has_education_preference'])
        transport_count = sum(1 for p in profiles if p['has_transport_preference'])
        park_count = sum(1 for p in profiles if p['has_park_preference'])
        
        common['preference_patterns'] = {
            'education_preference_ratio': education_count / len(profiles),
            'transport_preference_ratio': transport_count / len(profiles),
            'park_preference_ratio': park_count / len(profiles)
        }
        
        return common
        
    def _discover_satisfaction_predictors(self) -> List[Dict]:
        """Descubre características que predicen satisfacción (simulado)"""
        predictors = []
        
        # Simular análisis de satisfacción
        # En un sistema real, esto analizaría feedback de usuarios
        
        potential_predictors = [
            {
                'characteristic': 'nearby_amenities_count',
                'impact': 'positive',
                'strength': 0.8,
                'description': 'Usuarios con más amenidades cercanas tienden a estar más satisfechos'
            },
            {
                'characteristic': 'transport_compatibility',
                'impact': 'positive', 
                'strength': 0.75,
                'description': 'Compatibilidad con transporte preferido predice satisfacción'
            },
            {
                'characteristic': 'price_vs_expectations',
                'impact': 'negative',
                'strength': 0.7,
                'description': 'Precios muy por encima de expectativas reducen satisfacción'
            }
        ]
        
        for predictor in potential_predictors:
            if predictor['strength'] >= self.discovery_confidence_threshold:
                predictor_data = {
                    **predictor,
                    'discovered_at': datetime.now().isoformat(),
                    'confidence': predictor['strength'],
                    'samples_analyzed': len(self.system.properties)
                }
                
                predictors.append(predictor_data)
                self.satisfaction_predictors[predictor['characteristic']] = predictor_data
                
        return predictors
        
    def _analyze_cooccurrence_patterns(self) -> List[Dict]:
        """Analiza patrones de co-ocurrencia en preferencias"""
        patterns = []
        
        # Analizar qué preferencias aparecen juntas frecuentemente
        preference_combinations = defaultdict(int)
        
        for user in self.system.users:
            if len(user.preferences) >= 2:
                # Obtener tipos de preferencias del usuario
                pref_types = [p.get('type', 'unknown') for p in user.preferences]
                
                # Contar combinaciones de pares
                for pref1, pref2 in combinations(sorted(set(pref_types)), 2):
                    preference_combinations[(pref1, pref2)] += 1
                    
        # Identificar patrones frecuentes
        for (pref1, pref2), count in preference_combinations.items():
            if count >= self.min_pattern_frequency:
                pattern = {
                    'preference_1': pref1,
                    'preference_2': pref2,
                    'frequency': count,
                    'users_with_pattern': count,
                    'total_users': len(self.system.users),
                    'pattern_strength': count / len(self.system.users),
                    'discovered_at': datetime.now().isoformat()
                }
                
                patterns.append(pattern)
                self.co_occurrence_patterns[(pref1, pref2)] = count
                
        return patterns
        
    def _detect_implicit_preferences(self) -> List[Dict]:
        """Detecta preferencias implícitas no declaradas"""
        implicit_prefs = []
        
        # Analizar propiedades que usuarios tienden a preferir
        # pero que no están en sus preferencias declaradas
        
        for user in self.system.users:
            declared_prefs = set(p.get('type', '') for p in user.preferences)
            
            # Simular análisis de comportamiento implícito
            # En un sistema real, esto analizaría clicks, tiempo de visualización, etc.
            
            potential_implicit = []
            
            # Si usuario es joven pero no declaró preferencia por transporte público
            if user.age < 30 and 'bus_stop' not in declared_prefs and 'transport' not in ' '.join(declared_prefs):
                potential_implicit.append({
                    'type': 'transport_accessibility',
                    'reason': 'young_user_transport_pattern',
                    'confidence': 0.6
                })
                
            # Si usuario no declaró preferencia por parques pero edad sugiere familia
            if user.age > 30 and 'park' not in declared_prefs:
                potential_implicit.append({
                    'type': 'park_access',
                    'reason': 'family_age_pattern',
                    'confidence': 0.55
                })
                
            # Agregar preferencias implícitas con suficiente confianza
            for implicit_pref in potential_implicit:
                if implicit_pref['confidence'] >= 0.5:
                    implicit_data = {
                        'user': user.name,
                        'implicit_preference': implicit_pref['type'],
                        'reason': implicit_pref['reason'],
                        'confidence': implicit_pref['confidence'],
                        'discovered_at': datetime.now().isoformat()
                    }
                    
                    implicit_prefs.append(implicit_data)
                    
                    # Guardar en preferencias ocultas
                    if user.name not in self.hidden_preferences:
                        self.hidden_preferences[user.name] = {}
                    self.hidden_preferences[user.name][implicit_pref['type']] = implicit_data
                    
        return implicit_prefs
        
    def get_pattern_insights_for_user(self, user_name: str) -> Dict[str, Any]:
        """Obtiene insights de patrones para un usuario específico"""
        insights = {
            'user': user_name,
            'discovered_correlations': [],
            'user_segment': None,
            'implicit_preferences': self.hidden_preferences.get(user_name, {}),
            'similar_users': []
        }
        
        # Encontrar segmento del usuario
        for segment_id, users in self.user_segments.items():
            if user_name in users:
                insights['user_segment'] = segment_id
                insights['similar_users'] = [u for u in users if u != user_name]
                break
                
        # Correlaciones relevantes (últimas 10)
        insights['discovered_correlations'] = self.discovered_correlations[-10:]
        
        return insights
        
    def simulate_data(self):
        """Simula datos para descubrimiento de patrones"""
        print("   🎬 Simulando datos para descubrimiento de patrones...")
        
        # Simular algunas correlaciones conocidas
        if len(self.system.properties) >= 2:
            # Simular correlación precio-área
            self.discovered_correlations.append({
                'characteristic_1': 'price',
                'characteristic_2': 'area',
                'correlation': 0.85,
                'strength': 'strong',
                'direction': 'positive',
                'samples': len(self.system.properties),
                'discovered_at': datetime.now().isoformat(),
                'confidence': 0.85
            })
            
        # Simular algunos patrones de co-ocurrencia
        self.co_occurrence_patterns[('education_centre', 'transport')] = 3
        self.co_occurrence_patterns[('park', 'family_friendly')] = 2
        
        print("   ✅ Simulados patrones de correlación y co-ocurrencia")
        
    def get_insights(self) -> Dict[str, Any]:
        """Obtiene insights del descubrimiento de patrones"""
        strongest_correlation = None
        max_correlation = 0.0
        
        for corr in self.discovered_correlations:
            if abs(corr['correlation']) > max_correlation:
                max_correlation = abs(corr['correlation'])
                strongest_correlation = f"{corr['characteristic_1']} - {corr['characteristic_2']}"
                
        most_frequent_pattern = None
        max_frequency = 0
        
        for pattern, frequency in self.co_occurrence_patterns.items():
            if frequency > max_frequency:
                max_frequency = frequency
                most_frequent_pattern = f"{pattern[0]} + {pattern[1]}"
                
        return {
            'total_correlations_discovered': len(self.discovered_correlations),
            'strongest_correlation': strongest_correlation,
            'max_correlation_strength': max_correlation,
            'user_segments_created': len(self.user_segments),
            'most_frequent_cooccurrence': most_frequent_pattern,
            'max_cooccurrence_frequency': max_frequency,
            'users_with_implicit_preferences': len(self.hidden_preferences),
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }
        
    def get_state(self) -> Dict:
        """Obtiene el estado completo del demonio para persistencia"""
        return {
            'discovered_correlations': self.discovered_correlations[-30:],  # Solo últimas 30
            'user_segments': dict(self.user_segments),
            'satisfaction_predictors': self.satisfaction_predictors,
            'co_occurrence_patterns': dict(self.co_occurrence_patterns),
            'hidden_preferences': dict(self.hidden_preferences),
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }
        
    def load_state(self, state: Dict):
        """Carga el estado del demonio desde persistencia"""
        self.discovered_correlations = state.get('discovered_correlations', [])
        self.user_segments = defaultdict(list, state.get('user_segments', {}))
        self.satisfaction_predictors = state.get('satisfaction_predictors', {})
        self.co_occurrence_patterns = defaultdict(int, state.get('co_occurrence_patterns', {}))
        self.hidden_preferences = defaultdict(dict, state.get('hidden_preferences', {}))
        self.execution_count = state.get('execution_count', 0)
        if state.get('last_execution'):
            self.last_execution = datetime.fromisoformat(state['last_execution'])
