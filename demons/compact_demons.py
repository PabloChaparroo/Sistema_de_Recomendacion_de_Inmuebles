"""
Demonios Adaptativos - Sistema de Recomendación de Inmuebles
Versiones simplificadas compatibles con Neo4j + LangChain

Incluye:
1. AdaptivePricingDemon - Analiza rangos de precios
2. TemporalTrendsDemon - Detecta tendencias temporales
3. PatternDiscoveryDemon - Descubre patrones de búsqueda
4. RecommendationOptimizerDemon - Optimiza recomendaciones
"""

from typing import Dict, List
from datetime import datetime, timedelta
from database.neo4j_connector import Neo4jConnector
from collections import defaultdict


class AdaptivePricingDemon:
    """Analiza rangos de precios reales por barrio"""
    
    def __init__(self, connector: Neo4jConnector = None):
        self.connector = connector or Neo4jConnector()
        self.execution_count = 0
        self.precio_por_barrio = {}
    
    def execute(self):
        self.execution_count += 1
        print(f"💰 DEMONIO PRECIOS ADAPTATIVOS (#{self.execution_count})")
        
        if not self.connector.is_connected():
            return
        
        try:
            with self.connector.get_session() as session:
                result = session.run("""
                    MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
                    RETURN a.neighborhood AS barrio,
                           min(p.price) AS min_precio,
                           max(p.price) AS max_precio,
                           avg(p.price) AS avg_precio,
                           count(p) AS cantidad
                    ORDER BY cantidad DESC
                    LIMIT 10
                """)
                
                for r in result:
                    print(f"   📊 {r['barrio']}: ${r['avg_precio']:,.0f} avg")
        except Exception as e:
            print(f"   ⚠️ Error: {e}")


class TemporalTrendsDemon:
    """Detecta tendencias temporales en clics y búsquedas"""
    
    def __init__(self, connector: Neo4jConnector = None):
        self.connector = connector or Neo4jConnector()
        self.execution_count = 0
    
    def execute(self):
        self.execution_count += 1
        print(f"📈 DEMONIO TENDENCIAS TEMPORALES (#{self.execution_count})")
        
        if not self.connector.is_connected():
            return
        
        try:
            with self.connector.get_session() as session:
                # Barrios más clickeados últimamente
                result = session.run("""
                    MATCH (u:User)-[c:CLICKED]->(p:Property)-[:HAS_ADDRESS]->(a:Address)
                    WHERE c.timestamp >= datetime() - duration('P7D')
                    RETURN a.neighborhood AS barrio, count(*) AS clicks
                    ORDER BY clicks DESC
                    LIMIT 5
                """)
                
                trends = list(result)
                if trends:
                    print(f"   🔥 Barrios trending (última semana):")
                    for t in trends:
                        print(f"      • {t['barrio']}: {t['clicks']} clics")
                # Silencioso si no hay datos
        except Exception as e:
            pass  # Silencioso en errores


class PatternDiscoveryDemon:
    """Descubre patrones en búsquedas y clics"""
    
    def __init__(self, connector: Neo4jConnector = None):
        self.connector = connector or Neo4jConnector()
        self.execution_count = 0
    
    def execute(self):
        self.execution_count += 1
        print(f"🔍 DEMONIO DESCUBRIMIENTO DE PATRONES (#{self.execution_count})")
        
        if not self.connector.is_connected():
            return
        
        try:
            with self.connector.get_session() as session:
                # Patrón: Usuarios que clickearon X también clickearon Y
                result = session.run("""
                    MATCH (u:User)-[:CLICKED]->(p1:Property)
                    MATCH (u)-[:CLICKED]->(p2:Property)
                    WHERE id(p1) < id(p2)
                    WITH p1.name AS prop1, p2.name AS prop2, count(u) AS usuarios_comunes
                    WHERE usuarios_comunes >= 2
                    RETURN prop1, prop2, usuarios_comunes
                    ORDER BY usuarios_comunes DESC
                    LIMIT 3
                """)
                
                patterns = list(result)
                if patterns:
                    print(f"   🧩 Patrones detectados:")
                    for p in patterns:
                        print(f"      • {p['prop1']} + {p['prop2']}: "
                              f"{p['usuarios_comunes']} usuarios")
                # Silencioso si no hay datos
        except Exception as e:
            pass  # Silencioso en errores


class RecommendationOptimizerDemon:
    """Optimiza scores de recomendación basado en feedback"""
    
    def __init__(self, connector: Neo4jConnector = None):
        self.connector = connector or Neo4jConnector()
        self.execution_count = 0
    
    def execute(self):
        self.execution_count += 1
        print(f"⚡ DEMONIO OPTIMIZADOR DE RECOMENDACIONES (#{self.execution_count})")
        
        if not self.connector.is_connected():
            return
        
        try:
            with self.connector.get_session() as session:
                # Analizar qué propiedades tienen mejores tasas de clic
                result = session.run("""
                    MATCH (p:Property)
                    OPTIONAL MATCH (u:User)-[c:CLICKED]->(p)
                    WITH p, count(c) AS total_clicks
                    WHERE total_clicks > 0
                    RETURN p.name AS propiedad, 
                           p.price AS precio,
                           total_clicks
                    ORDER BY total_clicks DESC
                    LIMIT 5
                """)
                
                populares = list(result)
                if populares:
                    print(f"   ⭐ Propiedades más populares:")
                    for pop in populares:
                        print(f"      • {pop['propiedad']}: {pop['total_clicks']} clics")
                # Silencioso si no hay datos
        except Exception as e:
            pass  # Silencioso en errores


# Mantener compatibilidad con imports antiguos
# Los nombres simplificados apuntan a las clases compactas arriba

