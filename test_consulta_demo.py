"""
TEST PARA EXPOSICIÓN - Consulta específica con mapa
Prueba la consulta completa que se va a demostrar
"""

from workflow.langgraph_workflow import ejecutar_consulta
from geocoding.map_generator import MapGenerator
from database.neo4j_connector import Neo4jConnector
import webbrowser
import os

print("="*80)
print("🎯 TEST CONSULTA PARA EXPOSICIÓN")
print("="*80)

# Consulta exacta para la demo
consulta = "Necesito una casa en Godoy Cruz con 2 habitaciones, a un precio menor que 550000, me gusta caminar"

print(f"\n📝 Consulta: {consulta}\n")

# Ejecutar consulta
resultado = ejecutar_consulta(consulta)

print("\n" + "="*80)
print("📊 RESULTADOS:")
print("="*80)

print(f"\n🔍 Tipo detectado: {resultado.get('tipo')}")
print(f"📋 Parámetros: {resultado.get('parametros')}")
print(f"🏠 Propiedades encontradas: {len(resultado.get('propiedades', []))}")

print(f"\n💬 RESPUESTA:\n{resultado.get('respuesta', 'Sin respuesta')}")

if resultado.get('explicacion'):
    print(f"\n📖 EXPLICACIÓN:\n{resultado.get('explicacion')}")

# Generar mapa si hay propiedades
propiedades = resultado.get('propiedades', [])
if propiedades:
    print("\n" + "="*80)
    print("🗺️ GENERANDO MAPA...")
    print("="*80)
    
    try:
        # Obtener coordenadas de las propiedades
        connector = Neo4jConnector()
        
        # Consultar propiedades con coordenadas
        query = """
        MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
        WHERE toLower(a.city) CONTAINS 'godoy cruz'
        AND p.rooms >= 2
        AND a.latitude IS NOT NULL 
        AND a.longitude IS NOT NULL
        RETURN p.name as nombre, p.price as precio, p.rooms as habitaciones,
               a.latitude as lat, a.longitude as lng,
               a.neighborhood as barrio, a.city as ciudad
        ORDER BY p.price
        LIMIT 10
        """
        
        with connector.get_session() as session:
            result = session.run(query)
            props_con_coords = [dict(r) for r in result]
        
        connector.close()
        
        print(f"   ✅ Encontradas {len(props_con_coords)} propiedades con coordenadas")
        
        if props_con_coords:
            # Generar mapa
            map_gen = MapGenerator()
            archivo_mapa = "mapa_demo_exposicion.html"
            
            # Preparar datos para el mapa
            propiedades_mapa = []
            for p in props_con_coords:
                propiedades_mapa.append({
                    'name': p['nombre'],
                    'price': p['precio'],
                    'rooms': p['habitaciones'],
                    'location': f"{p['barrio']}, {p['ciudad']}",
                    'lat': p['lat'],
                    'lon': p['lng']
                })
            
            # Generar mapa
            poi_coords = (propiedades_mapa[0]['lat'], propiedades_mapa[0]['lon'])
            archivo_mapa = map_gen.create_map(
                propiedades_mapa,
                poi_coords,
                "Godoy Cruz"
            )
            
            print(f"\n   ✅ Mapa generado: {archivo_mapa}")
            
            # Abrir en navegador
            ruta_completa = os.path.abspath(archivo_mapa)
            webbrowser.open('file://' + ruta_completa)
            print(f"   🌐 Abriendo mapa en navegador...")
        else:
            print("   ⚠️ No hay propiedades con coordenadas para mostrar en el mapa")
    
    except Exception as e:
        print(f"   ❌ Error generando mapa: {e}")
        import traceback
        traceback.print_exc()

else:
    print("\n⚠️ No se encontraron propiedades para mostrar en el mapa")

print("\n" + "="*80)
print("✅ TEST COMPLETADO")
print("="*80)
