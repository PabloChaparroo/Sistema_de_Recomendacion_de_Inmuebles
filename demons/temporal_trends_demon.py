"""
Demonio de Tendencias Temporales - Sistema de Recomendación de Viviendas
Detecta y aprende patrones estacionales y tendencias a largo plazo del mercado.

FUNCIONALIDAD:
- Detecta patrones estacionales (ej: más demanda en verano)
- Aprende cómo eventos externos afectan el mercado
- Identifica ciclos de demanda por tipo de propiedad
- Predice cambios futuros basándose en tendencias históricas
- Adapta recomendaciones según el momento temporal
"""

import json
import time
import random
from typing import Dict, List, Any, Optional, Tuple
from datetime import datetime, timedelta
from collections import defaultdict
from statistics import mean
import calendar


class TemporalTrendsDemon:
    """Demonio que detecta y aprende tendencias temporales del mercado"""
    
    def __init__(self, system):
        self.system = system
        self.execution_count = 0
        self.last_execution = None
        
        # Datos temporales
        self.seasonal_patterns = defaultdict(dict)  # Por mes, tipo de propiedad, etc.
        self.weekly_patterns = defaultdict(dict)    # Por día de la semana
        self.event_impacts = []                     # Eventos que afectan el mercado
        self.demand_cycles = defaultdict(list)      # Ciclos de demanda históricos
        
        # Configuración
        self.min_data_points = 10
        self.seasonal_learning_rate = 0.05
        self.trend_sensitivity = 0.1
        
        # Inicializar patrones base
        self._initialize_base_patterns()
        
    def _initialize_base_patterns(self):
        """Inicializa patrones base conocidos del mercado inmobiliario"""
        # Patrones estacionales base (hipótesis inicial)
        months = [
            'enero', 'febrero', 'marzo', 'abril', 'mayo', 'junio',
            'julio', 'agosto', 'septiembre', 'octubre', 'noviembre', 'diciembre'
        ]
        
        # Estacionalidad hipotética para Argentina
        seasonal_multipliers = {
            'enero': 0.8,    # Vacaciones, menos actividad
            'febrero': 0.9,  # Fin de vacaciones
            'marzo': 1.2,    # Inicio escolar, más actividad
            'abril': 1.1,    # Otoño
            'mayo': 1.0,     # Normal
            'junio': 0.9,    # Invierno
            'julio': 0.8,    # Pleno invierno
            'agosto': 1.1,   # Fin de invierno
            'septiembre': 1.3, # Primavera, alta actividad
            'octubre': 1.2,  # Primavera
            'noviembre': 1.1, # Pre-verano
            'diciembre': 0.9  # Fiestas
        }
        
        for month, multiplier in seasonal_multipliers.items():
            self.seasonal_patterns[month] = {
                'demand_multiplier': multiplier,
                'confidence': 0.3,  # Baja confianza inicial
                'sample_count': 0,
                'last_updated': datetime.now().isoformat()
            }
            
        # Patrones semanales base
        weekday_patterns = {
            'lunes': 1.1,     # Inicio de semana, más actividad
            'martes': 1.2,    # Día pico
            'miércoles': 1.1, # Medio de semana
            'jueves': 1.0,    # Normal
            'viernes': 0.9,   # Fin de semana laboral
            'sábado': 1.3,    # Día pico para visitas
            'domingo': 0.8    # Día familiar, menos actividad
        }
        
        for day, multiplier in weekday_patterns.items():
            self.weekly_patterns[day] = {
                'activity_multiplier': multiplier,
                'confidence': 0.4,
                'sample_count': 0
            }
            
    def execute(self):
        """Ejecuta el ciclo de análisis de tendencias temporales"""
        self.execution_count += 1
        self.last_execution = datetime.now()
        
        print(f"📈 DEMONIO DE TENDENCIAS TEMPORALES (Ejecución #{self.execution_count})")
        
        # Analizar patrones estacionales
        seasonal_updates = self._analyze_seasonal_patterns()
        
        # Analizar patrones semanales
        weekly_updates = self._analyze_weekly_patterns()
        
        # Detectar eventos que impactan el mercado
        events_detected = self._detect_market_events()
        
        # Predecir tendencias futuras
        future_predictions = self._predict_future_trends()
        
        # Actualizar ciclos de demanda
        demand_cycles_updated = self._update_demand_cycles()
        
        result = {
            'timestamp': self.last_execution.isoformat(),
            'seasonal_updates': seasonal_updates,
            'weekly_updates': weekly_updates,
            'events_detected': len(events_detected),
            'future_predictions': len(future_predictions),
            'demand_cycles_updated': demand_cycles_updated
        }
        
        print(f"   📊 Actualizaciones estacionales: {seasonal_updates}")
        print(f"   📅 Actualizaciones semanales: {weekly_updates}")
        print(f"   🎯 Eventos detectados: {len(events_detected)}")
        print(f"   🔮 Predicciones futuras: {len(future_predictions)}")
        
        return result
        
    def _analyze_seasonal_patterns(self) -> int:
        """Analiza y actualiza patrones estacionales"""
        current_month = datetime.now().strftime('%B').lower()
        month_names = {
            'january': 'enero', 'february': 'febrero', 'march': 'marzo',
            'april': 'abril', 'may': 'mayo', 'june': 'junio',
            'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
            'october': 'octubre', 'november': 'noviembre', 'december': 'diciembre'
        }
        current_month_es = month_names.get(current_month, current_month)
        
        updates = 0
        
        # Simular actividad del mes actual
        current_activity = self._measure_current_market_activity()
        
        if current_activity is not None:
            # Actualizar patrón estacional del mes actual
            current_pattern = self.seasonal_patterns[current_month_es]
            current_multiplier = current_pattern.get('demand_multiplier', 1.0)
            
            # Suavizar actualización
            new_multiplier = current_multiplier + self.seasonal_learning_rate * (current_activity - current_multiplier)
            
            self.seasonal_patterns[current_month_es].update({
                'demand_multiplier': new_multiplier,
                'confidence': min(current_pattern.get('confidence', 0) + 0.1, 1.0),
                'sample_count': current_pattern.get('sample_count', 0) + 1,
                'last_updated': datetime.now().isoformat()
            })
            
            updates += 1
            
        return updates
        
    def _analyze_weekly_patterns(self) -> int:
        """Analiza y actualiza patrones semanales"""
        current_weekday = datetime.now().strftime('%A').lower()
        weekday_names = {
            'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miércoles',
            'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sábado', 'sunday': 'domingo'
        }
        current_weekday_es = weekday_names.get(current_weekday, current_weekday)
        
        updates = 0
        
        # Simular actividad del día actual
        current_activity = self._measure_current_daily_activity()
        
        if current_activity is not None:
            current_pattern = self.weekly_patterns[current_weekday_es]
            current_multiplier = current_pattern.get('activity_multiplier', 1.0)
            
            # Suavizar actualización
            new_multiplier = current_multiplier + self.seasonal_learning_rate * (current_activity - current_multiplier)
            
            self.weekly_patterns[current_weekday_es].update({
                'activity_multiplier': new_multiplier,
                'confidence': min(current_pattern.get('confidence', 0) + 0.05, 1.0),
                'sample_count': current_pattern.get('sample_count', 0) + 1
            })
            
            updates += 1
            
        return updates
        
    def _measure_current_market_activity(self) -> Optional[float]:
        """Mide la actividad actual del mercado (simulada)"""
        # En un sistema real, esto mediría:
        # - Número de visitas a propiedades
        # - Consultas realizadas
        # - Propiedades listadas
        # - Transacciones cerradas
        
        # Simulamos basándose en datos del sistema
        if not self.system.properties:
            return None
            
        # Simular actividad basándose en características del mes/estación
        base_activity = 1.0
        current_month = datetime.now().month
        
        # Ajustar por estacionalidad (primavera/otoño más activos)
        if current_month in [3, 4, 5, 9, 10, 11]:  # Primavera y otoño
            base_activity *= random.uniform(1.1, 1.4)
        elif current_month in [12, 1, 2]:  # Verano (vacaciones)
            base_activity *= random.uniform(0.7, 0.9)
        else:  # Invierno
            base_activity *= random.uniform(0.8, 1.0)
            
        # Añadir variación aleatoria
        activity = base_activity * random.uniform(0.9, 1.1)
        
        return min(2.0, max(0.3, activity))  # Clamp entre 0.3 y 2.0
        
    def _measure_current_daily_activity(self) -> Optional[float]:
        """Mide la actividad actual del día (simulada)"""
        current_weekday = datetime.now().weekday()  # 0=lunes, 6=domingo
        
        # Patrones típicos de actividad inmobiliaria
        if current_weekday in [0, 1, 2]:  # Lunes, martes, miércoles
            base_activity = random.uniform(1.0, 1.3)
        elif current_weekday in [3, 4]:    # Jueves, viernes
            base_activity = random.uniform(0.9, 1.1)
        elif current_weekday == 5:        # Sábado
            base_activity = random.uniform(1.2, 1.5)  # Día pico para visitas
        else:                             # Domingo
            base_activity = random.uniform(0.6, 0.9)
            
        return min(2.0, max(0.3, base_activity))
        
    def _detect_market_events(self) -> List[Dict]:
        """Detecta eventos que impactan el mercado"""
        events = []
        
        # Simular detección de eventos
        # En un sistema real, esto detectaría:
        # - Cambios súbitos en precios
        # - Noticias económicas
        # - Nuevos desarrollos urbanos
        # - Cambios en transporte público
        
        # Evento simulado: variación significativa en actividad
        recent_activity = self._measure_current_market_activity()
        if recent_activity and (recent_activity > 1.5 or recent_activity < 0.6):
            event = {
                'type': 'activity_anomaly',
                'description': f'Actividad {"alta" if recent_activity > 1.5 else "baja"} inusual detectada',
                'magnitude': recent_activity,
                'detected_at': datetime.now().isoformat(),
                'confidence': 0.7
            }
            events.append(event)
            self.event_impacts.append(event)
            
        # Mantener solo últimos 50 eventos
        if len(self.event_impacts) > 50:
            self.event_impacts = self.event_impacts[-50:]
            
        return events
        
    def _predict_future_trends(self) -> List[Dict]:
        """Predice tendencias futuras basándose en patrones aprendidos"""
        predictions = []
        
        # Predicción para próximo mes
        next_month = (datetime.now() + timedelta(days=30)).month
        next_month_name = calendar.month_name[next_month].lower()
        month_names_es = {
            'january': 'enero', 'february': 'febrero', 'march': 'marzo',
            'april': 'abril', 'may': 'mayo', 'june': 'junio',
            'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
            'october': 'octubre', 'november': 'noviembre', 'december': 'diciembre'
        }
        next_month_es = month_names_es.get(next_month_name, next_month_name)
        
        if next_month_es in self.seasonal_patterns:
            pattern = self.seasonal_patterns[next_month_es]
            prediction = {
                'type': 'monthly_forecast',
                'period': next_month_es,
                'predicted_activity_multiplier': pattern['demand_multiplier'],
                'confidence': pattern['confidence'],
                'based_on_samples': pattern['sample_count'],
                'generated_at': datetime.now().isoformat()
            }
            predictions.append(prediction)
            
        # Predicción semanal
        for i in range(1, 8):  # Próximos 7 días
            future_date = datetime.now() + timedelta(days=i)
            weekday = future_date.strftime('%A').lower()
            weekday_names = {
                'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miércoles',
                'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sábado', 'sunday': 'domingo'
            }
            weekday_es = weekday_names.get(weekday, weekday)
            
            if weekday_es in self.weekly_patterns:
                pattern = self.weekly_patterns[weekday_es]
                prediction = {
                    'type': 'daily_forecast',
                    'date': future_date.isoformat(),
                    'weekday': weekday_es,
                    'predicted_activity_multiplier': pattern['activity_multiplier'],
                    'confidence': pattern['confidence']
                }
                predictions.append(prediction)
                
        return predictions
        
    def _update_demand_cycles(self) -> int:
        """Actualiza ciclos de demanda por tipo de propiedad"""
        updates = 0
        
        # Analizar demanda por tipo de propiedad
        property_types = set(prop.property_type for prop in self.system.properties)
        
        for prop_type in property_types:
            # Simular ciclo de demanda
            current_activity = self._measure_current_market_activity()
            if current_activity:
                cycle_data = {
                    'timestamp': datetime.now().isoformat(),
                    'property_type': prop_type,
                    'demand_level': current_activity,
                    'season': self._get_current_season()
                }
                
                self.demand_cycles[prop_type].append(cycle_data)
                
                # Mantener solo últimos 100 registros por tipo
                if len(self.demand_cycles[prop_type]) > 100:
                    self.demand_cycles[prop_type] = self.demand_cycles[prop_type][-100:]
                    
                updates += 1
                
        return updates
        
    def _get_current_season(self) -> str:
        """Obtiene la estación actual"""
        month = datetime.now().month
        if month in [12, 1, 2]:
            return 'verano'
        elif month in [3, 4, 5]:
            return 'otoño'
        elif month in [6, 7, 8]:
            return 'invierno'
        else:
            return 'primavera'
            
    def get_temporal_adjustment(self, base_score: float) -> float:
        """Obtiene un ajuste temporal para un score base"""
        current_month = datetime.now().strftime('%B').lower()
        current_weekday = datetime.now().strftime('%A').lower()
        
        # Convertir a español
        month_names = {
            'january': 'enero', 'february': 'febrero', 'march': 'marzo',
            'april': 'abril', 'may': 'mayo', 'june': 'junio',
            'july': 'julio', 'august': 'agosto', 'september': 'septiembre',
            'october': 'octubre', 'november': 'noviembre', 'december': 'diciembre'
        }
        weekday_names = {
            'monday': 'lunes', 'tuesday': 'martes', 'wednesday': 'miércoles',
            'thursday': 'jueves', 'friday': 'viernes', 'saturday': 'sábado', 'sunday': 'domingo'
        }
        
        current_month_es = month_names.get(current_month, current_month)
        current_weekday_es = weekday_names.get(current_weekday, current_weekday)
        
        # Obtener multiplicadores
        seasonal_multiplier = self.seasonal_patterns.get(current_month_es, {}).get('demand_multiplier', 1.0)
        weekly_multiplier = self.weekly_patterns.get(current_weekday_es, {}).get('activity_multiplier', 1.0)
        
        # Combinar ajustes (peso mayor a estacional)
        combined_multiplier = (seasonal_multiplier * 0.7) + (weekly_multiplier * 0.3)
        
        return base_score * combined_multiplier
        
    def simulate_data(self):
        """Simula datos temporales para demostración"""
        print("   🎬 Simulando datos temporales...")
        
        # Simular datos para diferentes meses y días
        current_date = datetime.now()
        
        # Simular datos históricos (últimos 3 meses)
        for days_back in range(90, 0, -7):  # Cada semana hacia atrás
            sim_date = current_date - timedelta(days=days_back)
            
            # Simular actividad para esa fecha
            activity = random.uniform(0.6, 1.4)
            
            # Registrar en patrones correspondientes
            month = sim_date.strftime('%B').lower()
            weekday = sim_date.strftime('%A').lower()
            
            # Mapeo a español (simplificado)
            if month in ['march', 'april', 'may']:
                month_es = random.choice(['marzo', 'abril', 'mayo'])
            elif month in ['june', 'july', 'august']:
                month_es = random.choice(['junio', 'julio', 'agosto'])
            else:
                month_es = random.choice(['enero', 'febrero', 'septiembre', 'octubre', 'noviembre', 'diciembre'])
                
            # Actualizar contadores
            if month_es in self.seasonal_patterns:
                self.seasonal_patterns[month_es]['sample_count'] += 1
                
        print("   ✅ Simulados 12 semanas de datos temporales")
        
    def get_insights(self) -> Dict[str, Any]:
        """Obtiene insights de las tendencias temporales"""
        # Mes con mayor demanda
        best_month = 'none'
        max_demand = 0.0
        
        for month, pattern in self.seasonal_patterns.items():
            demand = pattern.get('demand_multiplier', 0.0)
            if demand > max_demand:
                max_demand = demand
                best_month = month
                
        # Día con mayor actividad
        best_day = 'none'
        max_activity = 0.0
        
        for day, pattern in self.weekly_patterns.items():
            activity = pattern.get('activity_multiplier', 0.0)
            if activity > max_activity:
                max_activity = activity
                best_day = day
                
        return {
            'best_demand_month': best_month,
            'max_monthly_demand': max_demand,
            'best_activity_day': best_day,
            'max_daily_activity': max_activity,
            'events_recorded': len(self.event_impacts),
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }
        
    def get_state(self) -> Dict:
        """Obtiene el estado completo del demonio para persistencia"""
        return {
            'seasonal_patterns': dict(self.seasonal_patterns),
            'weekly_patterns': dict(self.weekly_patterns),
            'event_impacts': self.event_impacts[-20:],  # Solo últimos 20 eventos
            'demand_cycles': {k: v[-50:] for k, v in self.demand_cycles.items()},  # Solo últimos 50 por tipo
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None
        }
        
    def load_state(self, state: Dict):
        """Carga el estado del demonio desde persistencia"""
        self.seasonal_patterns = defaultdict(dict, state.get('seasonal_patterns', {}))
        self.weekly_patterns = defaultdict(dict, state.get('weekly_patterns', {}))
        self.event_impacts = state.get('event_impacts', [])
        self.demand_cycles = defaultdict(list, state.get('demand_cycles', {}))
        self.execution_count = state.get('execution_count', 0)
        if state.get('last_execution'):
            self.last_execution = datetime.fromisoformat(state['last_execution'])
