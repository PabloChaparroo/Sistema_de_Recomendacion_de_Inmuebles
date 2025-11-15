"""
Adaptador de Preferencias - Reemplaza demonios con lógica bajo demanda
Integra funcionalidad de aprendizaje de preferencias en el flujo LangGraph
"""

from typing import Dict, List, Optional
from collections import defaultdict
from datetime import datetime
from neo4j_connector import Neo4jConnector

class PreferenceAdapter:
    """
    Reemplaza PreferenceLearningDemon con lógica bajo demanda
    Se ejecuta cuando el usuario hace una consulta, no continuamente
    """
    
    def __init__(self):
        self.connector = Neo4jConnector()
    
    def inferir_preferencias_desde_consulta(self, pregunta: str, parametros: Dict) -> Dict:
        """
        Infiere preferencias del usuario desde su consulta
        
        Args:
            pregunta: Consulta en lenguaje natural
            parametros: Parámetros extraídos (barrio, presupuesto, etc.)
        
        Returns:
            dict con preferencias inferidas
        """
        preferencias = {
            'budget_range': None,
            'location_importance': 0.5,
            'amenity_preferences': [],
            'property_type_pref': None
        }
        
        # Inferir rango de presupuesto
        if 'presupuesto' in parametros:
            budget = parametros['presupuesto']
            preferencias['budget_range'] = {
                'min': int(budget * 0.8),
                'max': int(budget * 1.2),
                'ideal': budget
            }
        
        # Inferir importancia de ubicación
        if 'barrio' in parametros:
            preferencias['location_importance'] = 0.9  # Alta si especificó barrio
        
        # Inferir preferencias de amenidades desde palabras clave
        amenity_keywords = {
            'parque': ('parque', 'verde', 'naturaleza'),
            'escuela': ('escuela', 'educación', 'niños', 'colegio'),
            'hospital': ('hospital', 'salud', 'médico'),
            'transporte': ('transporte', 'colectivo', 'subte', 'metro'),
            'supermercado': ('supermercado', 'comercio', 'compras'),
        }
        
        pregunta_lower = pregunta.lower()
        for amenity, keywords in amenity_keywords.items():
            if any(kw in pregunta_lower for kw in keywords):
                preferencias['amenity_preferences'].append({
                    'type': amenity,
                    'priority': 0.8
                })
        
        return preferencias
    
    def aprender_desde_interaccion(self, usuario: str, propiedad_clickeada: str, score: float):
        """
        Registra interacción del usuario para aprendizaje futuro
        Reemplaza la lógica del demonio pero se ejecuta bajo demanda
        
        Args:
            usuario: Nombre del usuario
            propiedad_clickeada: Propiedad que el usuario seleccionó
            score: Score de compatibilidad que tenía
        """
        
        if not self.connector.is_connected():
            return
        
        try:
            with self.connector.get_session() as session:
                # Registrar interacción en Neo4j
                session.run("""
                    MERGE (u:User {name: $usuario})
                    MERGE (p:Property {name: $propiedad})
                    CREATE (u)-[:CLICKED {
                        timestamp: datetime(),
                        score: $score,
                        context: 'langchain_query'
                    }]->(p)
                """, usuario=usuario, propiedad=propiedad_clickeada, score=score)
                
                print(f"✅ Interacción registrada: {usuario} → {propiedad_clickeada}")
        
        except Exception as e:
            print(f"⚠️ No se pudo registrar interacción: {e}")
    
    def obtener_preferencias_historicas(self, usuario: str) -> Dict:
        """
        Obtiene preferencias aprendidas del usuario desde Neo4j
        Reemplaza el análisis continuo del demonio
        
        Returns:
            dict con preferencias históricas del usuario
        """
        
        if not self.connector.is_connected():
            return {}
        
        preferencias = {
            'barrios_favoritos': [],
            'rango_precio_usual': None,
            'tipo_propiedad_favorita': None
        }
        
        try:
            with self.connector.get_session() as session:
                # Barrios más clickeados
                result = session.run("""
                    MATCH (u:User {name: $usuario})-[:CLICKED]->(p:Property)-[:HAS_ADDRESS]->(a:Address)
                    RETURN a.neighborhood AS barrio, count(*) AS clicks
                    ORDER BY clicks DESC
                    LIMIT 3
                """, usuario=usuario)
                
                preferencias['barrios_favoritos'] = [
                    {'barrio': r['barrio'], 'frecuencia': r['clicks']}
                    for r in result
                ]
                
                # Rango de precio usual
                result = session.run("""
                    MATCH (u:User {name: $usuario})-[:CLICKED]->(p:Property)
                    RETURN avg(p.price) AS avg_price,
                           min(p.price) AS min_price,
                           max(p.price) AS max_price
                """, usuario=usuario)
                
                precio = result.single()
                if precio and precio['avg_price']:
                    preferencias['rango_precio_usual'] = {
                        'promedio': int(precio['avg_price']),
                        'min': int(precio['min_price']),
                        'max': int(precio['max_price'])
                    }
        
        except Exception as e:
            print(f"⚠️ No se pudieron cargar preferencias históricas: {e}")
        
        return preferencias
    
    def ajustar_score_con_historial(self, propiedad: Dict, preferencias_historicas: Dict) -> float:
        """
        Ajusta el score difuso considerando historial del usuario
        Reemplaza la optimización continua del demonio
        
        Args:
            propiedad: Datos de la propiedad
            preferencias_historicas: Preferencias aprendidas
        
        Returns:
            float: Ajuste al score (0.0 a 0.2 bonus)
        """
        
        bonus = 0.0
        
        # Bonus si está en barrio favorito
        barrios_fav = [b['barrio'] for b in preferencias_historicas.get('barrios_favoritos', [])]
        if propiedad.get('location') in barrios_fav:
            bonus += 0.1
        
        # Bonus si está en rango de precio usual
        rango = preferencias_historicas.get('rango_precio_usual')
        if rango:
            precio_prop = propiedad.get('price', 0)
            if rango['min'] <= precio_prop <= rango['max']:
                bonus += 0.1
        
        return min(bonus, 0.2)  # Máximo 0.2 de bonus

# EJEMPLO DE USO EN LANGGRAPH
"""
# En langgraph_workflow.py, puedes agregar:

from preference_adapter import PreferenceAdapter

adapter = PreferenceAdapter()

def n_evaluar_difuso_con_historial(state: ConsultaState) -> ConsultaState:
    propiedades = state.get("propiedades", [])
    usuario = state.get("usuario")
    
    # Obtener preferencias históricas
    if usuario:
        pref_historicas = adapter.obtener_preferencias_historicas(usuario)
    else:
        pref_historicas = {}
    
    # Calcular scores con bonus histórico
    for prop in propiedades:
        score_base = calcular_score_propiedad(prop, usuario_virtual)
        bonus = adapter.ajustar_score_con_historial(prop, pref_historicas)
        prop['score_difuso'] = score_base + bonus
    
    return state
"""
