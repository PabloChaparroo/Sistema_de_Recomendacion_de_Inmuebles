"""
Simulador de clicks de usuarios para entrenar el sistema de recomendaciones
Genera datos de interacción para que los demonios de IA aprendan preferencias
"""

from database.neo4j_connector import Neo4jConnector
from datetime import datetime
import random
import time


def simular_click(nombre_usuario, propiedad_nombre):
    """Registra un click de un usuario en una propiedad"""
    connector = Neo4jConnector()
    
    try:
        def _crear_click(tx, usuario, prop_nombre):
            tx.run("""
                MATCH (u:User {name: $usuario})
                MATCH (p:Property {name: $prop_nombre})
                MERGE (u)-[c:CLICKED]->(p)
                ON CREATE SET c.timestamp = datetime(), c.count = 1
                ON MATCH SET c.timestamp = datetime(), c.count = c.count + 1
            """, usuario=usuario, prop_nombre=prop_nombre)
        
        with connector.get_session() as session:
            session.execute_write(_crear_click, nombre_usuario, propiedad_nombre)
            print(f"   ✅ {nombre_usuario} → {propiedad_nombre}")
        
        connector.close()
        return True
    
    except Exception as e:
        print(f"   ❌ Error: {e}")
        connector.close()
        return False


def registrar_busqueda(nombre_usuario, query_text):
    """Registra una búsqueda del usuario"""
    connector = Neo4jConnector()
    
    try:
        def _crear_busqueda(tx, usuario, query):
            tx.run("""
                MATCH (u:User {name: $usuario})
                CREATE (u)-[:SEARCHED {
                    query: $query,
                    timestamp: datetime()
                }]->(:SearchQuery {text: $query})
            """, usuario=usuario, query=query)
        
        with connector.get_session() as session:
            session.execute_write(_crear_busqueda, nombre_usuario, query_text)
        
        connector.close()
    except:
        connector.close()


def simular_sesion_carlos():
    """
    PERFIL: Carlos Lopez
    - Busca casas grandes (3-4 habitaciones)
    - Prefiere Godoy Cruz y Maipú
    - Presupuesto: $5M - $15M
    - Familia con hijos
    """
    print("\n" + "="*70)
    print("👨 SESIÓN: Carlos Lopez (Familia, busca casa grande)")
    print("="*70)
    
    usuario = "Carlos Lopez"
    connector = Neo4jConnector()
    
    # Búsquedas que haría Carlos
    busquedas = [
        "Casas en Godoy Cruz",
        "Propiedades de 3 habitaciones",
        "Casas en Maipú",
        "Busca casas familiares de 4 habitaciones"
    ]
    
    print("\n📝 Registrando búsquedas de Carlos:")
    for busqueda in busquedas:
        registrar_busqueda(usuario, busqueda)
        print(f"   🔍 '{busqueda}'")
        time.sleep(0.2)
    
    # Buscar propiedades que le interesarían a Carlos
    with connector.get_session() as session:
        result = session.run("""
            MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
            WHERE a.neighborhood IN ['Godoy Cruz', 'Maipú']
              AND p.rooms >= 3
              AND p.price >= 3000000 AND p.price <= 15000000
            RETURN p.name AS nombre, p.price AS precio, 
                   p.rooms AS habitaciones, a.neighborhood AS barrio
            ORDER BY p.price
            LIMIT 8
        """)
        
        propiedades = [dict(r) for r in result]
    
    connector.close()
    
    if propiedades:
        print(f"\n🏠 Propiedades encontradas: {len(propiedades)}")
        print("\n👆 Carlos clickea en las que más le interesan:\n")
        
        # Carlos clickea en las 5 primeras (las más baratas dentro de su rango)
        for i, prop in enumerate(propiedades[:5], 1):
            print(f"{i}. ${prop['precio']:,.0f} | {prop['habitaciones']} hab | {prop['barrio']}")
            simular_click(usuario, prop['nombre'])
            time.sleep(0.3)
        
        print(f"\n✅ Carlos hizo {len(propiedades[:5])} clicks")
    else:
        print("\n⚠️  No se encontraron propiedades para Carlos")


def simular_sesion_ana():
    """
    PERFIL: Ana Martinez
    - Busca departamentos pequeños (1-2 habitaciones)
    - Prefiere Ciudad de Mendoza (céntrico)
    - Presupuesto: $2M - $6M
    - Joven profesional, sola
    """
    print("\n" + "="*70)
    print("👩 SESIÓN: Ana Martinez (Joven profesional, busca depto pequeño)")
    print("="*70)
    
    usuario = "Ana Martinez"
    connector = Neo4jConnector()
    
    # Búsquedas que haría Ana
    busquedas = [
        "Departamentos en Ciudad de Mendoza",
        "Propiedades de 1 habitación",
        "Busca departamentos céntricos",
        "Propiedades económicas en el centro"
    ]
    
    print("\n📝 Registrando búsquedas de Ana:")
    for busqueda in busquedas:
        registrar_busqueda(usuario, busqueda)
        print(f"   🔍 '{busqueda}'")
        time.sleep(0.2)
    
    # Buscar propiedades que le interesarían a Ana
    with connector.get_session() as session:
        result = session.run("""
            MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
            WHERE a.neighborhood = 'Ciudad de Mendoza'
              AND p.rooms <= 2
              AND p.price >= 1000000 AND p.price <= 6000000
            RETURN p.name AS nombre, p.price AS precio, 
                   p.rooms AS habitaciones, a.neighborhood AS barrio
            ORDER BY p.price
            LIMIT 8
        """)
        
        propiedades = [dict(r) for r in result]
    
    connector.close()
    
    if propiedades:
        print(f"\n🏠 Propiedades encontradas: {len(propiedades)}")
        print("\n👆 Ana clickea en las que más le interesan:\n")
        
        # Ana clickea en las 4 más económicas
        for i, prop in enumerate(propiedades[:4], 1):
            print(f"{i}. ${prop['precio']:,.0f} | {prop['habitaciones']} hab | {prop['barrio']}")
            simular_click(usuario, prop['nombre'])
            time.sleep(0.3)
        
        print(f"\n✅ Ana hizo {len(propiedades[:4])} clicks")
    else:
        print("\n⚠️  No se encontraron propiedades para Ana")


def simular_sesion_maria():
    """
    PERFIL: Maria Garcia
    - Busca casas de lujo (4+ habitaciones)
    - Prefiere Luján de Cuyo, Chacras de Coria
    - Presupuesto: $15M+
    - Familia adinerada
    """
    print("\n" + "="*70)
    print("👩‍💼 SESIÓN: Maria Garcia (Alta gama, busca casa de lujo)")
    print("="*70)
    
    usuario = "Maria Garcia"
    connector = Neo4jConnector()
    
    # Búsquedas que haría María
    busquedas = [
        "Casas en Luján de Cuyo",
        "Propiedades de 4 habitaciones",
        "Casas grandes en Chacras de Coria",
        "Propiedades premium"
    ]
    
    print("\n📝 Registrando búsquedas de María:")
    for busqueda in busquedas:
        registrar_busqueda(usuario, busqueda)
        print(f"   🔍 '{busqueda}'")
        time.sleep(0.2)
    
    # Buscar propiedades que le interesarían a María
    with connector.get_session() as session:
        result = session.run("""
            MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
            WHERE a.neighborhood IN ['Luján de Cuyo', 'Chacras de Coria']
              AND p.rooms >= 4
              AND p.price >= 15000000
            RETURN p.name AS nombre, p.price AS precio, 
                   p.rooms AS habitaciones, a.neighborhood AS barrio
            ORDER BY p.price DESC
            LIMIT 6
        """)
        
        propiedades = [dict(r) for r in result]
    
    connector.close()
    
    if propiedades:
        print(f"\n🏠 Propiedades encontradas: {len(propiedades)}")
        print("\n👆 María clickea en las que más le interesan:\n")
        
        # María clickea en las 3 más caras (busca lo mejor)
        for i, prop in enumerate(propiedades[:3], 1):
            print(f"{i}. ${prop['precio']:,.0f} | {prop['habitaciones']} hab | {prop['barrio']}")
            simular_click(usuario, prop['nombre'])
            time.sleep(0.3)
        
        print(f"\n✅ María hizo {len(propiedades[:3])} clicks")
    else:
        print("\n⚠️  No se encontraron propiedades para María")


def simular_sesion_pepe():
    """
    PERFIL: Pepe (nuevo usuario)
    - Explora sin preferencias claras
    - Clickea en varias zonas diferentes
    - Presupuesto variable
    """
    print("\n" + "="*70)
    print("🧑 SESIÓN: Pepe (Explorando, sin preferencias claras)")
    print("="*70)
    
    usuario = "pepe"
    connector = Neo4jConnector()
    
    # Búsquedas exploratorias
    busquedas = [
        "¿Cuántas propiedades hay?",
        "Busca propiedades en Mendoza",
        "Propiedades económicas",
        "¿Qué barrios hay?"
    ]
    
    print("\n📝 Registrando búsquedas de Pepe:")
    for busqueda in busquedas:
        registrar_busqueda(usuario, busqueda)
        print(f"   🔍 '{busqueda}'")
        time.sleep(0.2)
    
    # Buscar propiedades variadas
    with connector.get_session() as session:
        result = session.run("""
            MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
            WHERE p.price >= 2000000 AND p.price <= 10000000
            RETURN p.name AS nombre, p.price AS precio, 
                   p.rooms AS habitaciones, a.neighborhood AS barrio
            ORDER BY rand()
            LIMIT 6
        """)
        
        propiedades = [dict(r) for r in result]
    
    connector.close()
    
    if propiedades:
        print(f"\n🏠 Propiedades encontradas: {len(propiedades)}")
        print("\n👆 Pepe clickea aleatoriamente:\n")
        
        # Pepe clickea en 3 propiedades aleatorias
        for i, prop in enumerate(random.sample(propiedades, min(3, len(propiedades))), 1):
            print(f"{i}. ${prop['precio']:,.0f} | {prop['habitaciones']} hab | {prop['barrio']}")
            simular_click(usuario, prop['nombre'])
            time.sleep(0.3)
        
        print(f"\n✅ Pepe hizo 3 clicks")
    else:
        print("\n⚠️  No se encontraron propiedades para Pepe")


def verificar_datos_entrenamiento():
    """Muestra estadísticas de los datos de entrenamiento generados"""
    print("\n" + "="*70)
    print("📊 VERIFICACIÓN DE DATOS DE ENTRENAMIENTO")
    print("="*70)
    
    connector = Neo4jConnector()
    
    with connector.get_session() as session:
        # Contar clicks por usuario
        result = session.run("""
            MATCH (u:User)-[c:CLICKED]->(p:Property)
            RETURN u.name AS usuario, count(c) AS clicks
            ORDER BY clicks DESC
        """)
        
        print("\n👆 CLICKS POR USUARIO:\n")
        total_clicks = 0
        for r in result:
            print(f"   • {r['usuario']}: {r['clicks']} clicks")
            total_clicks += r['clicks']
        
        print(f"\n   📌 TOTAL: {total_clicks} clicks registrados")
        
        # Contar búsquedas por usuario
        result2 = session.run("""
            MATCH (u:User)-[s:SEARCHED]->()
            RETURN u.name AS usuario, count(s) AS busquedas
            ORDER BY busquedas DESC
        """)
        
        print("\n🔍 BÚSQUEDAS POR USUARIO:\n")
        total_busquedas = 0
        for r in result2:
            print(f"   • {r['usuario']}: {r['busquedas']} búsquedas")
            total_busquedas += r['busquedas']
        
        print(f"\n   📌 TOTAL: {total_busquedas} búsquedas registradas")
    
    connector.close()
    
    print("\n" + "="*70)
    print("💡 PRÓXIMOS PASOS:")
    print("="*70)
    print("\n1. ⏰ Espera 1-2 minutos para que los demonios procesen")
    print("2. 🎯 Ejecuta: python main.py → Opción 3 (Ver estadísticas)")
    print("3. 🧠 Verás las preferencias aprendidas por cada usuario")
    print("4. 🔍 Haz más consultas desde Gradio como cada usuario")
    print("5. 📈 El sistema mejorará las recomendaciones automáticamente")
    print("\n" + "="*70)


if __name__ == "__main__":
    print("\n" + "="*70)
    print("🎭 SIMULADOR DE INTERACCIONES DE USUARIOS")
    print("   Genera datos de entrenamiento para los demonios de IA")
    print("="*70)
    
    print("\n⚙️  Iniciando simulaciones...\n")
    
    # Ejecutar sesiones de diferentes usuarios
    try:
        simular_sesion_carlos()
        time.sleep(1)
        
        simular_sesion_ana()
        time.sleep(1)
        
        simular_sesion_maria()
        time.sleep(1)
        
        simular_sesion_pepe()
        time.sleep(1)
        
        # Verificar datos generados
        verificar_datos_entrenamiento()
        
        print("\n✅ SIMULACIÓN COMPLETADA CON ÉXITO\n")
        
    except Exception as e:
        print(f"\n❌ Error durante la simulación: {e}")
        print("\n💡 Asegúrate de que:")
        print("   - Neo4j esté corriendo")
        print("   - Los usuarios existan en la BD")
        print("   - Haya propiedades cargadas")
