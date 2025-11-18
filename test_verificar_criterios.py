"""
Verificar si existen propiedades con los criterios solicitados
"""

from database.neo4j_connector import Neo4jConnector

c = Neo4jConnector()

# Query exacta generada por Ollama
query = """
MATCH (p:Property)
WHERE toLower(p.location) CONTAINS "godoy cruz" AND p.rooms = 2 AND p.price < 550000
RETURN p.name, p.price, p.rooms, p.location LIMIT 10
"""

print("="*60)
print("VERIFICACIÓN: ¿Existen propiedades con estos criterios?")
print("="*60)
print(f"\nQuery:\n{query}\n")

with c.get_session() as session:
    result = session.run(query)
    rows = [dict(r) for r in result]

print(f"✅ Resultados encontrados: {len(rows)}\n")

if rows:
    for i, row in enumerate(rows[:5], 1):
        print(f"{i}. {row}")
else:
    print("❌ No se encontraron resultados")
    print("\n💡 Probando consultas individuales:")
    
    with c.get_session() as session:
        # Test 1: ¿Hay propiedades en Godoy Cruz?
        r1 = session.run('MATCH (p:Property) WHERE toLower(p.location) CONTAINS "godoy cruz" RETURN count(p) AS total')
        total1 = r1.single()['total']
        print(f"   - En Godoy Cruz: {total1} propiedades")
        
        # Test 2: ¿Hay propiedades con 2 rooms?
        r2 = session.run('MATCH (p:Property) WHERE p.rooms = 2 RETURN count(p) AS total')
        total2 = r2.single()['total']
        print(f"   - Con 2 habitaciones: {total2} propiedades")
        
        # Test 3: ¿Hay propiedades < 550000?
        r3 = session.run('MATCH (p:Property) WHERE p.price < 550000 RETURN count(p) AS total')
        total3 = r3.single()['total']
        print(f"   - Precio < 550000: {total3} propiedades")

c.close()
