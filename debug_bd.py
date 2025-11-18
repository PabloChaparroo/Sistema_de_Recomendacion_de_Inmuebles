"""
Verificar qué hay en la BD de Godoy Cruz
"""
from database.neo4j_connector import Neo4jConnector

connector = Neo4jConnector()

print("\n1. ¿Qué departamentos/ciudades hay?")
with connector.get_session() as session:
    result = session.run("""
        MATCH (a:Address)
        RETURN DISTINCT a.city, count(*) as cantidad
        ORDER BY cantidad DESC
        LIMIT 20
    """)
    for r in result:
        print(f"   • {r['a.city']}: {r['cantidad']} propiedades")

print("\n2. ¿Hay algo con 'Godoy' en city?")
with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        WHERE toLower(a.city) CONTAINS 'godoy'
        RETURN count(p) as total
    """)
    total = result.single()['total']
    print(f"   Total: {total}")

print("\n3. ¿Hay algo con 'Godoy' en neighborhood?")
with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        WHERE toLower(a.neighborhood) CONTAINS 'godoy'
        RETURN count(p) as total, collect(a.city)[0..3] as ejemplos_city
    """)
    r = result.single()
    print(f"   Total: {r['total']}")
    print(f"   Ejemplos city: {r['ejemplos_city']}")

print("\n4. Primeras 5 propiedades con cualquier ubicación:")
with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        RETURN p.name, p.price, p.rooms, a.city, a.neighborhood
        LIMIT 5
    """)
    for r in result:
        print(f"   • {r['p.name']} - {r['a.city']} / {r['a.neighborhood']}")

connector.close()
