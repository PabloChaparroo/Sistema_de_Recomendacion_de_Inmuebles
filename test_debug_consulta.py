"""
Debug de consultas - Verificar por qué no encuentra propiedades
"""

from database.neo4j_connector import Neo4jConnector

connector = Neo4jConnector()

print("=" * 70)
print("VERIFICACIÓN DE DATOS EN NEO4J")
print("=" * 70)

# 1. Verificar cuántas propiedades hay
with connector.get_session() as session:
    result = session.run("MATCH (p:Property) RETURN count(p) as total")
    total = result.single()["total"]
    print(f"\n✅ Total de propiedades: {total}")
    
    # 2. Ver algunas propiedades
    result = session.run("MATCH (p:Property) RETURN p LIMIT 5")
    print(f"\n📋 Primeras 5 propiedades:")
    for record in result:
        prop = record["p"]
        print(f"   • {prop.get('name', 'Sin nombre')} - Rooms: {prop.get('rooms', 'N/A')} - Price: ${prop.get('price', 'N/A')}")
    
    # 3. Ver schema de Property
    result = session.run("MATCH (p:Property) RETURN keys(p) LIMIT 1")
    keys = result.single()
    if keys:
        print(f"\n🔑 Propiedades disponibles en Property:")
        print(f"   {keys['keys(p)']}")
    
    # 4. Ver amenidades
    result = session.run("MATCH (a:Amenity) RETURN a.name as name")
    amenities = [record["name"] for record in result]
    print(f"\n🏊 Amenidades en la base: {amenities}")
    
    # 5. Test consulta simple
    print(f"\n🔍 TEST: Consulta directa en Cypher")
    result = session.run("MATCH (p:Property) RETURN count(p) as total")
    print(f"   MATCH (p:Property) RETURN count(p) -> {result.single()['total']}")
    
    # 6. Test con rooms
    result = session.run("MATCH (p:Property) WHERE p.rooms > 3 RETURN count(p) as total")
    print(f"   Con rooms > 3 -> {result.single()['total']}")

connector.close()

print("\n" + "=" * 70)
print("AHORA PROBANDO CON LANGCHAIN")
print("=" * 70)

from workflow.langchain_integration import ask_question

# Test 1: Consulta simple
print("\n🔍 TEST 1: ¿Cuántas propiedades hay en total?")
resultado = ask_question("¿Cuántas propiedades hay en total?")
print(f"   Success: {resultado.get('success')}")
print(f"   Answer: {resultado.get('answer', 'N/A')}")
print(f"   Cypher: {resultado.get('cypher', 'N/A')}")
if not resultado.get('success'):
    print(f"   Error: {resultado.get('error')}")
