"""
Agregar coordenadas a Godoy Cruz directamente
"""
from database.neo4j_connector import Neo4jConnector

connector = Neo4jConnector()

# Coordenadas del centro de Godoy Cruz
GODOY_CRUZ_LAT = -32.9193
GODOY_CRUZ_LNG = -68.8400

print("🔄 Agregando coordenadas a propiedades de Godoy Cruz...")

with connector.get_session() as session:
    result = session.run("""
        MATCH (a:Address)
        WHERE toLower(a.city) = 'godoy cruz'
        SET a.latitude = $lat, a.longitude = $lng
        RETURN count(a) as count
    """, lat=GODOY_CRUZ_LAT, lng=GODOY_CRUZ_LNG)
    
    count = result.single()["count"]
    print(f"✅ {count} propiedades actualizadas con coordenadas")

connector.close()
