"""
Cargar coordenadas del cache JSON a Neo4j
"""
import json
from database.neo4j_connector import Neo4jConnector

print("📂 Cargando coordenadas desde cache...")
with open("data/coordenadas_cache.json", "r", encoding="utf-8") as f:
    cache = json.load(f)

print(f"✅ {len(cache)} coordenadas en cache\n")

connector = Neo4jConnector()

print("🔄 Actualizando Neo4j...")
updated = 0

with connector.get_session() as session:
    for direccion, coords in cache.items():
        # Actualizar todas las Address que contengan partes de esta dirección
        ciudad_partes = direccion.split(",")
        if len(ciudad_partes) >= 2:
            ciudad = ciudad_partes[-2].strip().lower()
            
            result = session.run("""
                MATCH (a:Address)
                WHERE toLower(a.city) = $ciudad
                SET a.latitude = $lat, a.longitude = $lng
                RETURN count(a) as count
            """, ciudad=ciudad, lat=coords["lat"], lng=coords["lng"])
            
            count = result.single()["count"]
            if count > 0:
                updated += count
                print(f"   ✓ {ciudad}: {count} propiedades actualizadas")

connector.close()

print(f"\n✅ Total actualizado: {updated} direcciones")
