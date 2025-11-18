"""
Carga propiedades reales desde alquiler_inmuebles.csv a Neo4j
"""
import pandas as pd
from database.neo4j_connector import Neo4jConnector
import os

def cargar_propiedades_desde_csv():
    """Carga todas las propiedades del CSV real a Neo4j"""
    
    csv_path = "data/alquiler_inmuebles.csv"
    
    if not os.path.exists(csv_path):
        print(f"❌ No se encontró el archivo: {csv_path}")
        return
    
    print("\n" + "="*60)
    print("📊 CARGANDO PROPIEDADES DESDE CSV A NEO4J")
    print("="*60 + "\n")
    
    # Leer CSV
    print(f"📂 Leyendo {csv_path}...")
    df = pd.read_csv(csv_path)
    print(f"✅ CSV cargado: {len(df)} propiedades encontradas\n")
    
    # Mostrar columnas disponibles
    print("📋 Columnas en el CSV:")
    for col in df.columns:
        print(f"   • {col}")
    print()
    
    # Conectar a Neo4j
    connector = Neo4jConnector()
    
    if not connector.is_connected():
        print("❌ No se pudo conectar a Neo4j")
        return
    
    print("🔗 Conectado a Neo4j\n")
    
    # Limpiar datos existentes
    print("🗑️  Limpiando base de datos...")
    with connector.get_session() as session:
        session.run("MATCH (n) DETACH DELETE n")
    print("✅ Base de datos limpiada\n")
    
    # Crear propiedades desde CSV
    print("🏠 Creando propiedades...")
    created_count = 0
    error_count = 0
    
    with connector.get_session() as session:
        for idx, row in df.iterrows():
            try:
                # Extraer datos del CSV
                ciudad = row.get('ciudad', '').strip() if pd.notna(row.get('ciudad')) else 'mendoza'
                direccion = row.get('direccion', '').strip() if pd.notna(row.get('direccion')) else 'Sin dirección'
                precio = int(row.get('alquiler', 0)) if pd.notna(row.get('alquiler')) else 0
                ambientes = int(row.get('ambientes', 2)) if pd.notna(row.get('ambientes')) else 2
                dormitorios = int(row.get('dormitorios', 1)) if pd.notna(row.get('dormitorios')) else 1
                banos = int(row.get('banos', 1)) if pd.notna(row.get('banos')) else 1
                m2_total = int(row.get('m2_total', 50)) if pd.notna(row.get('m2_total')) else 50
                
                # Crear Property Y Address con relación
                session.run("""
                    CREATE (p:Property {
                        id: $id,
                        name: $name,
                        price: $price,
                        rooms: $rooms,
                        bedrooms: $bedrooms,
                        bathrooms: $bathrooms,
                        area: $area
                    })
                    CREATE (a:Address {
                        street: $street,
                        city: $city,
                        neighborhood: $neighborhood
                    })
                    CREATE (p)-[:HAS_ADDRESS]->(a)
                """, 
                    id=f"P{idx+1:04d}",
                    name=f'Propiedad #{idx+1} - {ciudad.title()}',
                    price=precio,
                    rooms=ambientes,
                    bedrooms=dormitorios,
                    bathrooms=banos,
                    area=m2_total,
                    street=direccion,
                    city=ciudad,
                    neighborhood=ciudad  # Por ahora usar ciudad también como neighborhood
                )
                created_count += 1
                
                if (created_count % 100 == 0):
                    print(f"   ✓ {created_count} propiedades creadas...")
                    
            except Exception as e:
                error_count += 1
                if error_count <= 5:  # Solo mostrar primeros 5 errores
                    print(f"   ⚠️  Error en fila {idx}: {e}")
    
    print(f"\n✅ {created_count} propiedades creadas exitosamente")
    if error_count > 0:
        print(f"⚠️  {error_count} propiedades con errores (omitidas)")
    
    # Crear amenidades básicas
    print("\n🎯 Creando amenidades...")
    amenidades = [
        {"name": "parque", "display_name": "Parque"},
        {"name": "gimnasio", "display_name": "Gimnasio"},
        {"name": "piscina", "display_name": "Piscina"},
        {"name": "seguridad", "display_name": "Seguridad 24hs"},
        {"name": "cochera", "display_name": "Cochera"},
        {"name": "parrilla", "display_name": "Parrilla"},
    ]
    
    with connector.get_session() as session:
        for amenity in amenidades:
            session.run("CREATE (a:Amenity {name: $name, display_name: $display_name})", **amenity)
    
    print(f"✅ {len(amenidades)} amenidades creadas\n")
    
    # Asignar amenidades aleatorias a algunas propiedades
    print("🔗 Asignando amenidades a propiedades...")
    with connector.get_session() as session:
        # Piscina a propiedades más caras
        session.run("""
            MATCH (p:Property), (a:Amenity {name: 'piscina'})
            WHERE p.price > 150000
            WITH p, a LIMIT 50
            CREATE (p)-[:HAS_AMENITY]->(a)
        """)
        
        # Cochera a propiedades medianas
        session.run("""
            MATCH (p:Property), (a:Amenity {name: 'cochera'})
            WHERE p.price > 80000 AND p.rooms >= 2
            WITH p, a LIMIT 200
            CREATE (p)-[:HAS_AMENITY]->(a)
        """)
        
        # Seguridad a propiedades de todos los precios
        session.run("""
            MATCH (p:Property), (a:Amenity {name: 'seguridad'})
            WITH p, a LIMIT 300
            CREATE (p)-[:HAS_AMENITY]->(a)
        """)
    
    print("✅ Amenidades asignadas\n")
    
    # Crear usuarios de ejemplo
    print("👤 Creando usuarios...")
    usuarios = [
        {"id": "U001", "name": "Juan Pérez", "age": 35},
        {"id": "U002", "name": "María González", "age": 28},
        {"id": "U003", "name": "Carlos Rodríguez", "age": 42},
    ]
    
    with connector.get_session() as session:
        for user in usuarios:
            session.run("CREATE (u:User {id: $id, name: $name, age: $age})", **user)
    
    print(f"✅ {len(usuarios)} usuarios creados\n")
    
    # Crear medios de transporte
    print("🚗 Creando medios de transporte...")
    transportes = [
        {"name": "Walking", "speed_kmh": 5, "cost_per_km": 0},
        {"name": "Bus", "speed_kmh": 25, "cost_per_km": 30},
        {"name": "Bicycle", "speed_kmh": 15, "cost_per_km": 0},
        {"name": "Car", "speed_kmh": 50, "cost_per_km": 150},
    ]
    
    with connector.get_session() as session:
        for transport in transportes:
            session.run("CREATE (t:Transport {name: $name, speed_kmh: $speed_kmh, cost_per_km: $cost_per_km})", **transport)
    
    print(f"✅ {len(transportes)} medios de transporte creados\n")
    
    # Estadísticas finales
    stats = connector.get_database_stats()
    connector.close()
    
    print("="*60)
    print("✅ CARGA COMPLETADA")
    print("="*60)
    print(f"📊 Estadísticas finales:")
    print(f"   • Propiedades: {stats.get('properties', 0)}")
    print(f"   • Usuarios: {stats.get('users', 0)}")
    print(f"   • Amenidades: {stats.get('amenities', 0)}")
    print(f"   • Transportes: {stats.get('transports', 0)}")
    print(f"   • Relaciones: {stats.get('relationships', 0)}")
    print("="*60 + "\n")


if __name__ == "__main__":
    cargar_propiedades_desde_csv()
