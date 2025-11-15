"""
Script para cargar datos de ejemplo en Neo4j
Crea propiedades, usuarios y amenidades para probar el sistema
"""
import os
from dotenv import load_dotenv
from neo4j import GraphDatabase

load_dotenv()

driver = GraphDatabase.driver(
    os.getenv("NEO4J_URI", "bolt://localhost:7687"),
    auth=(os.getenv("NEO4J_USER", "neo4j"), os.getenv("NEO4J_PASSWORD"))
)

# Usar la base de datos configurada
database = os.getenv("NEO4J_DATABASE", "neo4j")

print("=" * 70)
print("📦 CARGANDO DATOS DE EJEMPLO EN NEO4J")
print("=" * 70 + "\n")

with driver.session(database=database) as session:
    # Limpiar base de datos
    print(f"🧹 Limpiando base de datos '{database}'...")
    session.run("MATCH (n) DETACH DELETE n")
    print("✅ Base de datos limpia\n")
    
    # Crear propiedades
    print("🏠 Creando propiedades...")
    propiedades = [
        {"id": "P001", "city": "Mendoza", "price": 120000, "bedrooms": 3, "bathrooms": 2, "area": 120},
        {"id": "P002", "city": "Mendoza", "price": 95000, "bedrooms": 2, "bathrooms": 1, "area": 85},
        {"id": "P003", "city": "Godoy Cruz", "price": 150000, "bedrooms": 4, "bathrooms": 3, "area": 180},
        {"id": "P004", "city": "Guaymallén", "price": 80000, "bedrooms": 2, "bathrooms": 1, "area": 70},
        {"id": "P005", "city": "Mendoza", "price": 200000, "bedrooms": 5, "bathrooms": 4, "area": 250},
        {"id": "P006", "city": "Las Heras", "price": 110000, "bedrooms": 3, "bathrooms": 2, "area": 130},
        {"id": "P007", "city": "Mendoza", "price": 75000, "bedrooms": 1, "bathrooms": 1, "area": 50},
        {"id": "P008", "city": "Godoy Cruz", "price": 135000, "bedrooms": 3, "bathrooms": 2, "area": 140},
    ]
    
    for prop in propiedades:
        session.run("""
            CREATE (p:Property {
                id: $id,
                city: $city,
                price: $price,
                bedrooms: $bedrooms,
                bathrooms: $bathrooms,
                area: $area
            })
        """, **prop)
    print(f"✅ {len(propiedades)} propiedades creadas\n")
    
    # Crear amenidades
    print("🎯 Creando amenidades...")
    amenidades = [
        {"name": "Parque"},
        {"name": "Gimnasio"},
        {"name": "Piscina"},
        {"name": "Seguridad 24hs"},
        {"name": "Cochera"},
        {"name": "Parrilla"},
    ]
    
    for amenity in amenidades:
        session.run("CREATE (a:Amenity {name: $name})", **amenity)
    print(f"✅ {len(amenidades)} amenidades creadas\n")
    
    # Crear usuarios
    print("👤 Creando usuarios...")
    usuarios = [
        {"id": "U001", "name": "Juan Pérez", "age": 35},
        {"id": "U002", "name": "María González", "age": 28},
        {"id": "U003", "name": "Carlos Rodríguez", "age": 42},
    ]
    
    for user in usuarios:
        session.run("CREATE (u:User {id: $id, name: $name, age: $age})", **user)
    print(f"✅ {len(usuarios)} usuarios creados\n")
    
    # Crear relaciones Property -> Amenity
    print("🔗 Creando relaciones HAS_AMENITY...")
    relaciones_amenity = [
        ("P001", "Parque"),
        ("P001", "Gimnasio"),
        ("P001", "Cochera"),
        ("P002", "Seguridad 24hs"),
        ("P003", "Piscina"),
        ("P003", "Gimnasio"),
        ("P003", "Seguridad 24hs"),
        ("P003", "Cochera"),
        ("P004", "Parrilla"),
        ("P005", "Piscina"),
        ("P005", "Gimnasio"),
        ("P005", "Seguridad 24hs"),
        ("P005", "Cochera"),
        ("P005", "Parrilla"),
    ]
    
    for prop_id, amenity_name in relaciones_amenity:
        session.run("""
            MATCH (p:Property {id: $prop_id})
            MATCH (a:Amenity {name: $amenity_name})
            CREATE (p)-[:HAS_AMENITY]->(a)
        """, prop_id=prop_id, amenity_name=amenity_name)
    print(f"✅ {len(relaciones_amenity)} relaciones HAS_AMENITY creadas\n")
    
    # Crear relaciones User -> Property (VISITED)
    print("🔗 Creando relaciones VISITED...")
    visitas = [
        ("U001", "P001"),
        ("U001", "P003"),
        ("U001", "P005"),
        ("U002", "P002"),
        ("U002", "P004"),
        ("U003", "P001"),
        ("U003", "P002"),
        ("U003", "P003"),
    ]
    
    for user_id, prop_id in visitas:
        session.run("""
            MATCH (u:User {id: $user_id})
            MATCH (p:Property {id: $prop_id})
            CREATE (u)-[:VISITED]->(p)
        """, user_id=user_id, prop_id=prop_id)
    print(f"✅ {len(visitas)} relaciones VISITED creadas\n")
    
    # Crear relaciones User -> Amenity (PREFERS_AMENITY)
    print("🔗 Creando relaciones PREFERS_AMENITY...")
    preferencias = [
        ("U001", "Parque"),
        ("U001", "Gimnasio"),
        ("U002", "Piscina"),
        ("U002", "Seguridad 24hs"),
        ("U003", "Cochera"),
        ("U003", "Parrilla"),
    ]
    
    for user_id, amenity_name in preferencias:
        session.run("""
            MATCH (u:User {id: $user_id})
            MATCH (a:Amenity {name: $amenity_name})
            CREATE (u)-[:PREFERS_AMENITY]->(a)
        """, user_id=user_id, amenity_name=amenity_name)
    print(f"✅ {len(preferencias)} relaciones PREFERS_AMENITY creadas\n")

driver.close()

print("=" * 70)
print("✅ DATOS DE EJEMPLO CARGADOS EXITOSAMENTE")
print("=" * 70)
print("\n📊 Resumen:")
print(f"  • {len(propiedades)} propiedades")
print(f"  • {len(amenidades)} amenidades")
print(f"  • {len(usuarios)} usuarios")
print(f"  • {len(relaciones_amenity)} relaciones HAS_AMENITY")
print(f"  • {len(visitas)} relaciones VISITED")
print(f"  • {len(preferencias)} relaciones PREFERS_AMENITY")
print("\n🚀 Ahora puedes ejecutar: python test_ollama.py")
print("=" * 70)
