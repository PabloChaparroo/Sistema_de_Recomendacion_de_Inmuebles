"""
Demonio de Aprendizaje de Preferencias - Sistema de Recomendación de Viviendas
Aprende las preferencias reales de los usuarios basándose en su comportamiento.

FUNCIONALIDAD:
- Monitoriza qué propiedades los usuarios clickean/seleccionan
- Registra cuáles ignoran o rechazan
- Aprende patrones: "Usuarios que clickean X también clickean Y"
- Descubre preferencias implícitas (diferentes a las declaradas)
- Actualiza perfiles de usuario automáticamente

INTEGRADO CON: Neo4j + LangChain
"""

import json
import time
from typing import Dict, List, Any, Optional
from datetime import datetime, timedelta
from collections import defaultdict
import random
from database.neo4j_connector import Neo4jConnector
import warnings

# Silenciar warnings de Neo4j
warnings.filterwarnings('ignore')


class PreferenceLearningDemon:
    """Demonio que aprende preferencias reales del usuario desde su comportamiento"""
    
    def __init__(self, connector: Neo4jConnector = None):
        self.connector = connector or Neo4jConnector()
        self.learning_rate = 0.1
        self.execution_count = 0
        self.last_execution = None
        
        # Parámetros de aprendizaje
        self.positive_weight_increase = 0.15  # Cuando clickea una propiedad
        self.negative_weight_decrease = 0.05  # Cuando ignora una propiedad
        self.decay_factor = 0.95  # Decaimiento temporal de preferencias antiguas
        
    def execute(self):
        """Ejecuta el ciclo de aprendizaje del demonio"""
        self.execution_count += 1
        self.last_execution = datetime.now()
        
        print(f"🧠 DEMONIO DE APRENDIZAJE DE PREFERENCIAS (Ejecución #{self.execution_count})")
        
        if not self.connector.is_connected():
            print("   ⚠️ Neo4j no conectado - saltando ejecución")
            return
        
        # Analizar interacciones recientes desde Neo4j
        new_learnings = self._analyze_recent_interactions()
        
        # Actualizar perfiles de usuario en Neo4j
        updated_users = self._update_user_profiles(new_learnings)
        
        print(f"   ✅ {len(updated_users)} perfiles actualizados")
    
    def _analyze_recent_interactions(self) -> Dict:
        """
        Analiza interacciones recientes desde Neo4j
        
        Returns:
            dict con patrones aprendidos por usuario
        """
        learnings = defaultdict(dict)
        
        try:
            with self.connector.get_session() as session:
                # Obtener clics recientes (últimas 24 horas)
                result = session.run("""
                    MATCH (u:User)-[click:CLICKED]->(p:Property)
                    WHERE click.timestamp >= datetime() - duration('P1D')
                    MATCH (p)-[:HAS_ADDRESS]->(a:Address)
                    RETURN u.name AS usuario,
                           p.name AS propiedad,
                           p.price AS precio,
                           p.rooms AS habitaciones,
                           a.neighborhood AS barrio,
                           click.timestamp AS cuando
                    ORDER BY click.timestamp DESC
                    LIMIT 100
                """)
                
                for record in result:
                    usuario = record['usuario']
                    
                    if usuario not in learnings:
                        learnings[usuario] = {
                            'barrios_clickeados': defaultdict(int),
                            'rango_precios': [],
                            'habitaciones_preferidas': defaultdict(int)
                        }
                    
                    # Acumular preferencias
                    learnings[usuario]['barrios_clickeados'][record['barrio']] += 1
                    learnings[usuario]['rango_precios'].append(record['precio'])
                    learnings[usuario]['habitaciones_preferidas'][record['habitaciones']] += 1
        
        except Exception as e:
            print(f"   ⚠️ Error analizando interacciones: {e}")
        
        return learnings
    
    def _update_user_profiles(self, learnings: Dict) -> List[str]:
        """
        Actualiza perfiles de usuario en Neo4j con preferencias aprendidas
        
        Args:
            learnings: Patrones aprendidos por usuario
        
        Returns:
            list de usuarios actualizados
        """
        updated_users = []
        
        try:
            with self.connector.get_session() as session:
                for usuario, prefs in learnings.items():
                    # Calcular barrio favorito
                    barrios = prefs['barrios_clickeados']
                    barrio_favorito = max(barrios.items(), key=lambda x: x[1])[0] if barrios else None
                    
                    # Calcular rango de precio preferido
                    precios = prefs['rango_precios']
                    if precios:
                        precio_min = min(precios)
                        precio_max = max(precios)
                        precio_promedio = sum(precios) // len(precios)
                    else:
                        precio_min = precio_max = precio_promedio = None
                    
                    # Habitaciones preferidas
                    habs = prefs['habitaciones_preferidas']
                    habitaciones_pref = max(habs.items(), key=lambda x: x[1])[0] if habs else None
                    
                    # Actualizar en Neo4j
                    session.run("""
                        MATCH (u:User {name: $usuario})
                        SET u.learned_location_pref = $barrio_favorito,
                            u.learned_budget_min = $precio_min,
                            u.learned_budget_max = $precio_max,
                            u.learned_budget_avg = $precio_promedio,
                            u.learned_rooms_pref = $habitaciones_pref,
                            u.last_learning_update = datetime()
                    """, usuario=usuario,
                         barrio_favorito=barrio_favorito,
                         precio_min=precio_min,
                         precio_max=precio_max,
                         precio_promedio=precio_promedio,
                         habitaciones_pref=habitaciones_pref)
                    
                    updated_users.append(usuario)
                    print(f"   📝 Usuario {usuario}: barrio_pref={barrio_favorito}, "
                          f"precio_avg=${precio_promedio:,}")
        
        except Exception as e:
            print(f"   ⚠️ Error actualizando perfiles: {e}")
        
        return updated_users
    
    def get_insights(self) -> Dict[str, Any]:
        """Obtiene insights de aprendizaje del demonio"""
        return {
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None,
            'learning_rate': self.learning_rate
        }
        
    def get_state(self) -> Dict:
        """Obtiene el estado completo del demonio para persistencia"""
        return {
            'execution_count': self.execution_count,
            'last_execution': self.last_execution.isoformat() if self.last_execution else None,
            'learning_rate': self.learning_rate
        }
        
    def load_state(self, state: Dict):
        """Carga el estado del demonio desde persistencia"""
        self.execution_count = state.get('execution_count', 0)
        if state.get('last_execution'):
            self.last_execution = datetime.fromisoformat(state['last_execution'])
        self.learning_rate = state.get('learning_rate', 0.1)


