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
        {"id": "P001", "name": "Casa en Centro", "city": "Mendoza", "location": "Mendoza", "price": 120000, "rooms": 3, "bedrooms": 3, "bathrooms": 2, "area": 120},
        {"id": "P002", "name": "Departamento Económico", "city": "Mendoza", "location": "Mendoza", "price": 95000, "rooms": 2, "bedrooms": 2, "bathrooms": 1, "area": 85},
        {"id": "P003", "name": "Casa Familiar con Piscina", "city": "Godoy Cruz", "location": "Godoy Cruz", "price": 150000, "rooms": 4, "bedrooms": 4, "bathrooms": 3, "area": 180},
        {"id": "P004", "name": "Depto Compacto", "city": "Guaymallén", "location": "Guaymallén", "price": 80000, "rooms": 2, "bedrooms": 2, "bathrooms": 1, "area": 70},
        {"id": "P005", "name": "Casa Lujosa con Piscina", "city": "Mendoza", "location": "Mendoza", "price": 200000, "rooms": 5, "bedrooms": 5, "bathrooms": 4, "area": 250},
        {"id": "P006", "name": "Casa Espaciosa", "city": "Las Heras", "location": "Las Heras", "price": 110000, "rooms": 3, "bedrooms": 3, "bathrooms": 2, "area": 130},
        {"id": "P007", "name": "Monoambiente Centro", "city": "Mendoza", "location": "Mendoza", "price": 75000, "rooms": 1, "bedrooms": 1, "bathrooms": 1, "area": 50},
        {"id": "P008", "name": "Casa Moderna con Piscina", "city": "Godoy Cruz", "location": "Godoy Cruz", "price": 135000, "rooms": 3, "bedrooms": 3, "bathrooms": 2, "area": 140},
    ]
    
    for prop in propiedades:
        session.run("""
            CREATE (p:Property {
                id: $id,
                name: $name,
                city: $city,
                location: $location,
                price: $price,
                rooms: $rooms,
                bedrooms: $bedrooms,
                bathrooms: $bathrooms,
                area: $area
            })
        """, **prop)
    print(f"✅ {len(propiedades)} propiedades creadas\n")
    
    # Crear amenidades (en minúsculas para mejor compatibilidad con consultas)
    print("🎯 Creando amenidades...")
    amenidades = [
        {"name": "parque", "display_name": "Parque"},
        {"name": "gimnasio", "display_name": "Gimnasio"},
        {"name": "piscina", "display_name": "Piscina"},
        {"name": "seguridad", "display_name": "Seguridad 24hs"},
        {"name": "cochera", "display_name": "Cochera"},
        {"name": "parrilla", "display_name": "Parrilla"},
    ]
    
    for amenity in amenidades:
        session.run("CREATE (a:Amenity {name: $name, display_name: $display_name})", **amenity)
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
        ("P001", "parque"),
        ("P001", "gimnasio"),
        ("P001", "cochera"),
        ("P002", "seguridad"),
        ("P003", "piscina"),       # Casa Familiar con Piscina - 4 habitaciones
        ("P003", "gimnasio"),
        ("P003", "seguridad"),
        ("P003", "cochera"),
        ("P004", "parrilla"),
        ("P005", "piscina"),       # Casa Lujosa con Piscina - 5 habitaciones
        ("P005", "gimnasio"),
        ("P005", "seguridad"),
        ("P005", "cochera"),
        ("P005", "parrilla"),
        ("P008", "piscina"),       # Casa Moderna con Piscina - 3 habitaciones (pero NO cumple > 3)
        ("P008", "parque"),
        ("P008", "cochera"),
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
        ("U001", "parque"),
        ("U001", "gimnasio"),
        ("U002", "piscina"),
        ("U002", "seguridad"),
        ("U003", "cochera"),
        ("U003", "parrilla"),
    ]
    
    for user_id, amenity_name in preferencias:
        session.run("""
            MATCH (u:User {id: $user_id})
            MATCH (a:Amenity {name: $amenity_name})
            CREATE (u)-[:PREFERS_AMENITY]->(a)
        """, user_id=user_id, amenity_name=amenity_name)
    print(f"✅ {len(preferencias)} relaciones PREFERS_AMENITY creadas\n")
    
    # Crear nodos de Transport
    print("🚗 Creando nodos de transporte...")
    transportes = [
        {"name": "Walking", "type": "walking", "speed_kmh": 5, "cost_per_km": 0},
        {"name": "Bus", "type": "bus", "speed_kmh": 30, "cost_per_km": 0.5},
        {"name": "Bicycle", "type": "bicycle", "speed_kmh": 15, "cost_per_km": 0},
        {"name": "Car", "type": "car", "speed_kmh": 50, "cost_per_km": 2.0},
    ]
    
    for transport in transportes:
        session.run("""
            CREATE (t:Transport {
                name: $name,
                type: $type,
                speed_kmh: $speed_kmh,
                cost_per_km: $cost_per_km
            })
        """, **transport)
    print(f"✅ {len(transportes)} tipos de transporte creados\n")
    
    # Crear relaciones User -> Transport (USES)
    print("🔗 Creando relaciones USES (usuario usa transporte)...")
    uso_transporte = [
        ("U001", "Walking", 0.8),   # Usuario 1 usa mucho caminar
        ("U001", "Bus", 0.6),        # También usa bus
        ("U002", "Bicycle", 0.9),    # Usuario 2 prefiere bicicleta
        ("U002", "Bus", 0.3),        # Usa poco el bus
        ("U003", "Car", 1.0),        # Usuario 3 usa principalmente auto
        ("U003", "Walking", 0.4),    # Camina ocasionalmente
    ]
    
    for user_id, transport_name, preference in uso_transporte:
        session.run("""
            MATCH (u:User {id: $user_id})
            MATCH (t:Transport {name: $transport_name})
            CREATE (u)-[:USES {preference: $preference}]->(t)
        """, user_id=user_id, transport_name=transport_name, preference=preference)
    print(f"✅ {len(uso_transporte)} relaciones USES creadas\n")

driver.close()

print("=" * 70)
print("✅ DATOS DE EJEMPLO CARGADOS EXITOSAMENTE")
print("=" * 70)
print("\n📊 Resumen:")
print(f"  • {len(propiedades)} propiedades")
print(f"  • {len(amenidades)} amenidades")
print(f"  • {len(usuarios)} usuarios")
print(f"  • {len(transportes)} tipos de transporte")
print(f"  • {len(relaciones_amenity)} relaciones HAS_AMENITY")
print(f"  • {len(visitas)} relaciones VISITED")
print(f"  • {len(preferencias)} relaciones PREFERS_AMENITY")
print(f"  • {len(uso_transporte)} relaciones USES")
print("\n🚀 Ahora puedes ejecutar: python test_ollama.py")
print("=" * 70)
