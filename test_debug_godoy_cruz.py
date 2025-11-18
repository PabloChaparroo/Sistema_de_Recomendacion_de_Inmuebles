"""
Script para debuggear qué hay realmente en Godoy Cruz
"""
from database.neo4j_connector import Neo4jConnector

connector = Neo4jConnector()

if not connector.is_connected():
    print("❌ No se pudo conectar a Neo4j")
    exit(1)

print("=" * 80)
print("1. ¿Cuántas propiedades hay en total?")
print("=" * 80)

with connector.get_session() as session:
    result = session.run("MATCH (p:Property) RETURN count(p) as total")
    total = result.single()['total']
    print(f"Total propiedades: {total}\n")

print("=" * 80)
print("2. ¿Qué valores hay en a.city?")
print("=" * 80)

with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        RETURN DISTINCT a.city, count(p) as cantidad
        ORDER BY cantidad DESC
        LIMIT 20
    """)
    for record in result:
        print(f"  • {record['a.city']}: {record['cantidad']} propiedades")

print("\n" + "=" * 80)
print("3. Propiedades en Godoy Cruz (cualquier variante)")
print("=" * 80)

with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        WHERE toLower(a.city) CONTAINS "godoy"
        RETURN p.name, p.price, p.rooms, a.city, a.neighborhood
        ORDER BY p.price
        LIMIT 10
    """)
    records = list(result)
    print(f"Total encontradas: {len(records)}\n")
    for r in records:
        print(f"  • {r['p.name']}")
        print(f"    Precio: ${r['p.price']:,}")
        print(f"    Habitaciones: {r['p.rooms']}")
        print(f"    Ciudad: {r['a.city']}")
        print(f"    Barrio: {r['a.neighborhood']}")
        print()

print("=" * 80)
print("4. Propiedades en Godoy Cruz con 2+ habitaciones")
print("=" * 80)

with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        WHERE toLower(a.city) CONTAINS "godoy" AND p.rooms >= 2
        RETURN p.name, p.price, p.rooms, a.city
        ORDER BY p.price
        LIMIT 10
    """)
    records = list(result)
    print(f"Total encontradas: {len(records)}\n")
    for r in records:
        print(f"  • {r['p.name']} - ${r['p.price']:,} - {r['p.rooms']} hab - {r['a.city']}")

print("\n" + "=" * 80)
print("5. Propiedades en Godoy Cruz con 2+ hab y precio < 550000")
print("=" * 80)

with connector.get_session() as session:
    result = session.run("""
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        WHERE toLower(a.city) CONTAINS "godoy" 
          AND p.rooms >= 2 
          AND p.price < 550000
        RETURN p.name, p.price, p.rooms, a.city
        ORDER BY p.price
        LIMIT 10
    """)
    records = list(result)
    print(f"Total encontradas con TODOS los filtros: {len(records)}\n")
    
    if len(records) == 0:
        print("❌ NO HAY propiedades que cumplan TODOS los criterios")
        print("\nProbando sin el filtro de precio:")
        result2 = session.run("""
            MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
            WHERE toLower(a.city) CONTAINS "godoy" AND p.rooms >= 2
            RETURN p.price
            ORDER BY p.price
            LIMIT 1
        """)
        record = result2.single()
        if record:
            print(f"   → La propiedad MÁS BARATA en Godoy Cruz con 2+ hab cuesta: ${record['p.price']:,}")
            print(f"   → Esto es {'MAYOR' if record['p.price'] >= 550000 else 'MENOR'} que $550,000")
    else:
        for r in records:
            print(f"  ✅ {r['p.name']} - ${r['p.price']:,} - {r['p.rooms']} hab")

connector.close()
