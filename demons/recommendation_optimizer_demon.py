"""
Demonio de Optimización de Recomendaciones - Sistema de Recomendación de Viviendas
Optimiza continuamente las recomendaciones balanceando exploración vs explotación.

FUNCIONALIDAD:
- Balancea entre dar lo que piden vs dar lo que necesitan
- Implementa estrategias de exploración para descubrir nuevas preferencias
- Optimiza la satisfacción a largo plazo
- Adapta pesos de características basándose en feedback
- Evita sobre-especialización en recomendaciones
"""

import json
import time
import random
import math
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict, deque
from statistics import mean


class RecommendationOptimizerDemon:
    """Demonio que optimiza continuamente las estrategias de recomendación"""
    
    def __init__(self, system):
        self.system = system
        self.execution_count = 0
        self.last_execution = None
        
        # Configuración de exploración vs explotación
        self.exploration_rate = 0.2  # 20% exploración, 80% explotación
        self.exploration_decay = 0.99  # Reducir exploración gradualmente
        self.min_exploration_rate = 0.05  # Mínimo 5% exploración
        
        # Histórico de recomendaciones y resultados
        self.recommendation_history = deque(maxlen=1000)
        self.user_feedback_history = defaultdict(list)
        self.feature_performance = defaultdict(dict)
        
        # Pesos adaptativos para características
        self.adaptive_weights = {
            'price': 0.3,
            'location': 0.25,
            'amenities': 0.2,
            'transport': 0.15,
            'size': 0.1
        }
        
        # Métricas de optimización
        self.optimization_metrics = {
            'diversity_score': 0.5,
            'satisfaction_trend': 0.0,
            'novelty_rate': 0.0,
            'click_through_rate': 0.0
        }
        
    def execute(self):
        """Ejecuta el ciclo de optimización de recomendaciones"""
        self.execution_count += 1
        self.last_execution = datetime.now()
        
        print(f"🔄 DEMONIO DE OPTIMIZACIÓN DE RECOMENDACIONES (Ejecución #{self.execution_count})")
        
        # Analizar performance de recomendaciones pasadas
        performance_analysis = self._analyze_recommendation_performance()
        
        # Optimizar balance exploración/explotación
        exploration_update = self._optimize_exploration_rate()
        
        # Adaptar pesos de características
        weight_updates = self._adapt_feature_weights()
        
        # Implementar estrategias de diversificación
        diversity_improvements = self._improve_recommendation_diversity()
        
        # Detectar y corregir sesgos
        bias_corrections = self._detect_and_correct_biases()
        
        result = {
            'timestamp': self.last_execution.isoformat(),
            'performance_analysis': performance_analysis,
            'exploration_rate': self.exploration_rate,
            'weight_updates': weight_updates,
            'diversity_improvements': diversity_improvements,
            'bias_corrections': bias_corrections
        }
        
        print(f"   📊 Performance: {performance_analysis.get('avg_satisfaction', 0):.2f}")
        print(f"   🎯 Exploración: {self.exploration_rate:.2%}")
        print(f"   ⚖️ Pesos actualizados: {weight_updates}")
        print(f"   🌈 Diversidad mejorada: {diversity_improvements}")
        
        return result
        
    def _analyze_recommendation_performance(self) -> Dict[str, Any]:
        """Analiza la performance de recomendaciones pasadas"""
        if not self.recommendation_history:
            return {'avg_satisfaction': 0.5, 'total_recommendations': 0}
            
        # Calcular métricas de performance
        total_recommendations = len(self.recommendation_history)
        satisfaction_scores = []
        click_rates = []
        diversity_scores = []
        
        for rec in self.recommendation_history:
            # Simular métricas (en un sistema real vendría de feedback real)
            satisfaction = rec.get('user_satisfaction', self._simulate_satisfaction_score(rec))
            click_rate = rec.get('clicked', False)
            diversity = rec.get('diversity_score', random.uniform(0.3, 0.8))
            
            satisfaction_scores.append(satisfaction)
            click_rates.append(1.0 if click_rate else 0.0)
            diversity_scores.append(diversity)
            
        # Calcular promedios
        avg_satisfaction = mean(satisfaction_scores) if satisfaction_scores else 0.5
        avg_click_rate = mean(click_rates) if click_rates else 0.0
        avg_diversity = mean(diversity_scores) if diversity_scores else 0.5
        
        # Detectar tendencias
        recent_satisfaction = mean(satisfaction_scores[-20:]) if len(satisfaction_scores) >= 20 else avg_satisfaction
        satisfaction_trend = recent_satisfaction - avg_satisfaction
        
        # Actualizar métricas globales
        self.optimization_metrics.update({
            'diversity_score': avg_diversity,
            'satisfaction_trend': satisfaction_trend,
            'click_through_rate': avg_click_rate,
            'novelty_rate': self._calculate_novelty_rate()
        })
        
        return {
            'avg_satisfaction': avg_satisfaction,
            'avg_click_rate': avg_click_rate,
            'avg_diversity': avg_diversity,
            'satisfaction_trend': satisfaction_trend,
            'total_recommendations': total_recommendations,
            'recent_performance': recent_satisfaction
        }
        
    def _simulate_satisfaction_score(self, recommendation: Dict) -> float:
        """Simula un score de satisfacción para una recomendación"""
        # En un sistema real, esto vendría del feedback del usuario
        base_score = 0.7
        
        # Ajustar basándose en características de la recomendación
        if recommendation.get('matches_preferences', False):
            base_score += 0.2
            
        if recommendation.get('price_appropriate', False):
            base_score += 0.15
            
        if recommendation.get('location_convenient', False):
            base_score += 0.1
            
        # Añadir variación aleatoria
        noise = random.uniform(-0.1, 0.1)
        return max(0.0, min(1.0, base_score + noise))
        
    def _calculate_novelty_rate(self) -> float:
        """Calcula la tasa de novedad en las recomendaciones"""
        if len(self.recommendation_history) < 10:
            return 0.5
            
        recent_recs = list(self.recommendation_history)[-20:]
        property_ids = [rec.get('property_id', f'prop_{i}') for i, rec in enumerate(recent_recs)]
        
        unique_properties = len(set(property_ids))
        total_recommendations = len(property_ids)
        
        return unique_properties / total_recommendations if total_recommendations > 0 else 0.0
        
    def _optimize_exploration_rate(self) -> Dict[str, Any]:
        """Optimiza la tasa de exploración vs explotación"""
        # Analizar si necesitamos más exploración
        recent_performance = self.optimization_metrics.get('satisfaction_trend', 0.0)
        diversity_score = self.optimization_metrics.get('diversity_score', 0.5)
        novelty_rate = self.optimization_metrics.get('novelty_rate', 0.5)
        
        old_rate = self.exploration_rate
        
        # Aumentar exploración si performance está estancada
        if recent_performance < -0.05:  # Performance está bajando
            self.exploration_rate = min(0.4, self.exploration_rate * 1.1)
        elif diversity_score < 0.4:  # Diversidad muy baja
            self.exploration_rate = min(0.3, self.exploration_rate * 1.05)
        elif novelty_rate < 0.3:  # Muy pocas propiedades nuevas
            self.exploration_rate = min(0.35, self.exploration_rate * 1.08)
        else:
            # Reducir exploración gradualmente si todo va bien
            self.exploration_rate = max(self.min_exploration_rate, self.exploration_rate * self.exploration_decay)
            
        return {
            'old_rate': old_rate,
            'new_rate': self.exploration_rate,
            'change': self.exploration_rate - old_rate,
            'reason': self._get_exploration_adjustment_reason(recent_performance, diversity_score, novelty_rate)
        }
        
    def _get_exploration_adjustment_reason(self, performance: float, diversity: float, novelty: float) -> str:
        """Obtiene la razón del ajuste en exploración"""
        if performance < -0.05:
            return 'performance_declining'
        elif diversity < 0.4:
            return 'low_diversity'
        elif novelty < 0.3:
            return 'low_novelty'
        else:
            return 'gradual_decay'
            
    def _adapt_feature_weights(self) -> int:
        """Adapta los pesos de características basándose en performance"""
        updates = 0
        
        # Analizar qué características han funcionado mejor
        feature_performance = self._calculate_feature_performance()
        
        learning_rate = 0.05
        
        for feature, performance in feature_performance.items():
            if feature in self.adaptive_weights:
                current_weight = self.adaptive_weights[feature]
                
                # Ajustar peso basándose en performance
                if performance > 0.7:  # Característica funciona bien
                    new_weight = current_weight + learning_rate * (0.8 - current_weight)
                elif performance < 0.4:  # Característica no funciona bien
                    new_weight = current_weight - learning_rate * (current_weight - 0.1)
                else:
                    new_weight = current_weight  # Mantener peso
                    
                # Aplicar cambio si es significativo
                if abs(new_weight - current_weight) > 0.01:
                    self.adaptive_weights[feature] = max(0.05, min(0.5, new_weight))
                    updates += 1
                    
        # Normalizar pesos para que sumen 1.0
        total_weight = sum(self.adaptive_weights.values())
        if total_weight > 0:
            for feature in self.adaptive_weights:
                self.adaptive_weights[feature] /= total_weight
                
        return updates
        
    def _calculate_feature_performance(self) -> Dict[str, float]:
        """Calcula la performance de cada característica"""
        # Simular análisis de performance por característica
        # En un sistema real, esto analizaría correlaciones entre características y satisfacción
        
        performance = {}
        
        for feature in self.adaptive_weights.keys():
            # Simular performance basada en datos históricos
            if len(self.recommendation_history) > 10:
                # Calcular performance promedio cuando esta característica fue importante
                relevant_recs = [rec for rec in self.recommendation_history 
                               if rec.get(f'{feature}_importance', 0.5) > 0.6]
                
                if relevant_recs:
                    satisfactions = [self._simulate_satisfaction_score(rec) for rec in relevant_recs]
                    performance[feature] = mean(satisfactions)
                else:
                    performance[feature] = 0.5  # Performance neutra
            else:
                # Performance base para características comunes
                base_performances = {
                    'price': 0.75,     # Precio suele ser importante
                    'location': 0.7,   # Ubicación también
                    'amenities': 0.65, # Amenidades moderadamente importantes
                    'transport': 0.6,  # Transporte varía según usuario
                    'size': 0.55       # Tamaño menos crítico en promedio
                }
                performance[feature] = base_performances.get(feature, 0.5)
                
        return performance
        
    def _improve_recommendation_diversity(self) -> int:
        """Implementa mejoras en la diversidad de recomendaciones"""
        improvements = 0
        
        # Analizar diversidad actual
        current_diversity = self.optimization_metrics.get('diversity_score', 0.5)
        
        if current_diversity < 0.6:  # Diversidad baja
            # Implementar estrategias de diversificación
            
            # 1. Aumentar variación en tipos de propiedades
            if hasattr(self, 'property_type_distribution'):
                self.property_type_distribution = self._balance_property_types()
                improvements += 1
                
            # 2. Forzar inclusión de propiedades diferentes
            self.min_diversity_threshold = 0.3
            improvements += 1
            
            # 3. Implementar anti-repetición temporal
            self.anti_repetition_window = 10  # No repetir en 10 recomendaciones
            improvements += 1
            
        return improvements
        
    def _balance_property_types(self) -> Dict[str, float]:
        """Balancea la distribución de tipos de propiedades en recomendaciones"""
        # Contar tipos de propiedades en recomendaciones recientes
        recent_recs = list(self.recommendation_history)[-50:]  # Últimas 50
        type_counts = defaultdict(int)
        
        for rec in recent_recs:
            prop_type = rec.get('property_type', 'unknown')
            type_counts[prop_type] += 1
            
        total_recs = len(recent_recs)
        
        # Calcular distribución objetivo (más balanceada)
        target_distribution = {}
        available_types = set(prop.property_type for prop in self.system.properties)
        
        for prop_type in available_types:
            current_ratio = type_counts[prop_type] / total_recs if total_recs > 0 else 0
            target_ratio = 1.0 / len(available_types)  # Distribución uniforme
            
            # Ajustar hacia distribución más balanceada
            adjustment = (target_ratio - current_ratio) * 0.3
            target_distribution[prop_type] = max(0.1, min(0.6, target_ratio + adjustment))
            
        return target_distribution
        
    def _detect_and_correct_biases(self) -> List[Dict]:
        """Detecta y corrige sesgos en las recomendaciones"""
        corrections = []
        
        # Detectar sesgo de precio (solo recomendar propiedades baratas o caras)
        price_bias = self._detect_price_bias()
        if price_bias:
            corrections.append({
                'bias_type': 'price_bias',
                'description': price_bias['description'],
                'correction': 'Balancear recomendaciones de precio',
                'severity': price_bias['severity']
            })
            
        # Detectar sesgo de ubicación (favorecer ciertas zonas)
        location_bias = self._detect_location_bias()
        if location_bias:
            corrections.append({
                'bias_type': 'location_bias',
                'description': location_bias['description'],
                'correction': 'Diversificar ubicaciones recomendadas',
                'severity': location_bias['severity']
            })
            
        # Detectar sesgo de novedad (solo recomendar propiedades nuevas o viejas)
        novelty_bias = self._detect_novelty_bias()
        if novelty_bias:
            corrections.append({
                'bias_type': 'novelty_bias',
                'description': novelty_bias['description'],
                'correction': 'Balancear propiedades nuevas y conocidas',
                'severity': novelty_bias['severity']
            })
            
        return corrections
        
    def _detect_price_bias(self) -> Optional[Dict]:
        """Detecta sesgo en recomendaciones de precio"""
        if len(self.recommendation_history) < 20:
            return None
            
        recent_recs = list(self.recommendation_history)[-30:]
        prices = [rec.get('price', 0) for rec in recent_recs if rec.get('price')]
        
        if not prices:
            return None
            
        avg_price = mean(prices)
        all_prices = [prop.price for prop in self.system.properties]
        market_avg = mean(all_prices) if all_prices else avg_price
        
        price_deviation = abs(avg_price - market_avg) / market_avg if market_avg > 0 else 0
        
        if price_deviation > 0.3:  # Desviación mayor al 30%
            bias_direction = 'alto' if avg_price > market_avg else 'bajo'
            return {
                'description': f'Sesgo hacia precios {bias_direction}s detectado',
                'severity': 'high' if price_deviation > 0.5 else 'medium',
                'deviation': price_deviation
            }
            
        return None
        
    def _detect_location_bias(self) -> Optional[Dict]:
        """Detecta sesgo en recomendaciones de ubicación"""
        if len(self.recommendation_history) < 15:
            return None
            
        recent_recs = list(self.recommendation_history)[-25:]
        locations = [rec.get('location', 'unknown') for rec in recent_recs]
        
        location_counts = defaultdict(int)
        for location in locations:
            location_counts[location] += 1
            
        if location_counts:
            max_location_count = max(location_counts.values())
            total_locations = len(recent_recs)
            
            if max_location_count / total_locations > 0.6:  # Una ubicación representa >60%
                dominant_location = max(location_counts.items(), key=lambda x: x[1])[0]
                return {
                    'description': f'Sesgo hacia ubicación {dominant_location}',
                    'severity': 'medium',
                    'concentration': max_location_count / total_locations
                }
                
        return None
        
    def _detect_novelty_bias(self) -> Optional[Dict]:
        """Detecta sesgo de novedad en recomendaciones"""
        novelty_rate = self.optimization_metrics.get('novelty_rate', 0.5)
        
        if novelty_rate < 0.2:
            return {
                'description': 'Sesgo hacia propiedades repetidas (baja novedad)',
                'severity': 'high' if novelty_rate < 0.1 else 'medium',
                'novelty_rate': novelty_rate
            }
        elif novelty_rate > 0.9:
            return {
                'description': 'Sesgo hacia propiedades siempre nuevas (alta novedad)',
                'severity': 'medium',
                'novelty_rate': novelty_rate
            }
            
        return None
        
    def should_explore(self) -> bool:
        """Determina si debe explorar (recomendar algo diferente) o explotar"""
        return random.random() < self.exploration_rate
        
    def record_recommendation(self, user_id: str, property_obj, recommendation_data: Dict):
        """Registra una recomendación realizada"""
        record = {
            'timestamp': datetime.now().isoformat(),
            'user_id': user_id,
            'property_id': getattr(property_obj, 'name', 'unknown'),
            'property_type': getattr(property_obj, 'property_type', 'unknown'),
            'price': getattr(property_obj, 'price', 0),
            'location': getattr(property_obj.address, 'neighborhood', 'unknown') if hasattr(property_obj, 'address') else 'unknown',
            **recommendation_data
        }
        
        self.recommendation_history.append(record)
        
    def get_optimized_weights(self) -> Dict[str, float]:
        """Obtiene los pesos optimizados para características"""
        return self.adaptive_weights.copy()
        
    def simulate_data(self):
        """Simula datos de recomendaciones para demostración"""
        print("   🎬 Simulando histórico de recomendaciones...")
        
        # Simular 30-40 recomendaciones históricas
        for i in range(random.randint(25, 35)):
            # Simular recomendación
            prop = random.choice(self.system.properties) if self.system.properties else None
            if prop:
                rec_data = {
                    'matches_preferences': random.choice([True, False]),
                    'price_appropriate': random.choice([True, False]),
                    'location_convenient': random.choice([True, False]),
                    'clicked': random.random() < 0.4,  # 40% click rate
                    'diversity_score': random.uniform(0.3, 0.8),
                    'exploration': random.random() < self.exploration_rate
                }
                
                user_id = random.choice([user.name for user in self.system.users]) if self.system.users else 'test_user'
                self.record_recommendation(user_id, prop, rec_data)
                
        print(f"   ✅ Simuladas {len(self.recommendation_history)} recomendaciones")
        
    def get_insights(self) -> Dict[str, Any]:
        """Obtiene insights de la optimización"""
        return {
            'total_recommendations': len(self.recommendation_history),
            'current_exploration_rate': self.exploration_rate,
            'adaptive_weights': self.adaptive_weights,
            'optimization_metrics': self.optimization_metrics,
            'recommendations_last_24h': len([rec for rec in self.recommendation_history 
                                           if rec.get('timestamp') and 
                                           (datetime.now() - datetime.fromisoformat(rec['timestamp'])).days < 1]),
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }
        
    def get_state(self) -> Dict:
        """Obtiene el estado completo del demonio para persistencia"""
        return {
            'exploration_rate': self.exploration_rate,
            'adaptive_weights': self.adaptive_weights,
            'optimization_metrics': self.optimization_metrics,
            'recommendation_history': list(self.recommendation_history)[-100:],  # Solo últimas 100
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }
        
    def load_state(self, state: Dict):
        """Carga el estado del demonio desde persistencia"""
        self.exploration_rate = state.get('exploration_rate', 0.2)
        self.adaptive_weights = state.get('adaptive_weights', self.adaptive_weights)
        self.optimization_metrics = state.get('optimization_metrics', self.optimization_metrics)
        self.recommendation_history = deque(state.get('recommendation_history', []), maxlen=1000)
        self.execution_count = state.get('execution_count', 0)
        if state.get('last_execution'):
            self.last_execution = datetime.fromisoformat(state['last_execution'])
