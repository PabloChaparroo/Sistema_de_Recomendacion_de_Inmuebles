"""
Script para verificar qué datos existen en Neo4j
"""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD"))
)

database = os.getenv("NEO4J_DATABASE", "neo4j")

print("=" * 70)
print(f"🔍 VERIFICANDO BASE DE DATOS NEO4J - '{database}'")
print("=" * 70 + "\n")

with driver.session(database=database) as session:
    # Ver todos los labels (tipos de nodos)
    print("📊 Labels (tipos de nodos) en la base de datos:")
    print("-" * 70)
    result = session.run("CALL db.labels()")
    labels = [record[0] for record in result]
    if labels:
        for label in labels:
            print(f"  ✓ {label}")
    else:
        print("  ❌ No hay labels (base de datos vacía)")
    
    print("\n" + "=" * 70 + "\n")
    
    # Ver todas las relaciones
    print("🔗 Tipos de relaciones en la base de datos:")
    print("-" * 70)
    result = session.run("CALL db.relationshipTypes()")
    rels = [record[0] for record in result]
    if rels:
        for rel in rels:
            print(f"  ✓ {rel}")
    else:
        print("  ❌ No hay relaciones")
    
    print("\n" + "=" * 70 + "\n")
    
    # Contar nodos totales
    print("🔢 Cantidad de nodos por tipo:")
    print("-" * 70)
    for label in labels:
        result = session.run(f"MATCH (n:{label}) RETURN count(n) as count")
        count = result.single()["count"]
        print(f"  {label}: {count} nodos")
    
    print("\n" + "=" * 70 + "\n")
    
    # Ver propiedades de un nodo de ejemplo
    if labels:
        print(f"📝 Propiedades de ejemplo del primer nodo {labels[0]}:")
        print("-" * 70)
        result = session.run(f"MATCH (n:{labels[0]}) RETURN n LIMIT 1")
        record = result.single()
        if record:
            node = record["n"]
            for key, value in node.items():
                print(f"  {key}: {value}")
        else:
            print("  ❌ No se encontraron nodos")

driver.close()

print("\n" + "=" * 70)
print("✅ Verificación completa")
print("=" * 70)
