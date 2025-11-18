"""
Sistema de Recomendacion de Inmuebles con IA
Neo4j + Logica Difusa + LangChain + HuggingFace + Gradio
"""

import sys
import os

# Cargar variables de entorno desde .env (para token de HuggingFace)
try:
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Archivo .env cargado correctamente")
except ImportError:
    print("⚠️ Instalando python-dotenv...")
    os.system("pip install python-dotenv")
    from dotenv import load_dotenv
    load_dotenv()
    print("✅ Archivo .env cargado correctamente")

# Agregar directorio actual al path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Funcion principal del sistema"""
    print("\n" + "="*70)
    print(" SISTEMA INTELIGENTE DE RECOMENDACION DE INMUEBLES")
    print("   Neo4j + Logica Difusa + LangChain + Ollama (LLM Local)")
    print("   CON APRENDIZAJE AUTOMATICO ACTIVADO")
    print("="*70 + "\n")
    
    # Verificar conexion Neo4j
    from database.neo4j_connector import Neo4jConnector
    
    print(" Verificando conexion a Neo4j...")
    connector = Neo4jConnector()
    
    if not connector.is_connected():
        print(" No se puede conectar a Neo4j")
        print("\n SOLUCION:")
        print("   1. Asegurate de que Neo4j Desktop este ejecutandose")
        print("   2. Verifica que la base 'housing' este activa")
        print("   3. URI: bolt://localhost:7687")
        print("   4. Usuario: neo4j | Contrasena: password\n")
        return 1
    
    stats = connector.get_database_stats()
    
    print(f" Conectado exitosamente a Neo4j")
    print(f"    {stats.get('properties', 0)} propiedades | "
          f"{stats.get('users', 0)} usuarios | "
          f"{stats.get('amenities', 0)} amenidades")
    print(f"\n 🌐 Neo4j Browser: http://localhost:7474")
    print(f" 📊 Base de datos: housing\n")
    
    # Verificar si hay datos
    if stats.get('properties', 0) == 0:
        print(" La base de datos esta vacia")
        if input("¿Cargar datos de ejemplo? (s/n): ").lower() in ['s', 'si', 'y', 'yes']:
            try:
                from populate_real_data import populate_database
                print("\n Cargando datos de ejemplo...")
                populate_database()
                print(" Datos cargados correctamente\n")
            except ImportError:
                print(" Nota: populate_real_data.py no encontrado. Carga datos manualmente.\n")
    
    # INICIAR DEMONIOS AUTOMATICAMENTE
    print(" Iniciando sistema de aprendizaje automatico...")
    from demons.demons_manager import DemonsManager
    
    global demons_manager
    demons_manager = DemonsManager(connector)
    demons_manager.start_all_demons()
    
    print(" Demonios IA activos - El sistema aprendera automaticamente")
    print("   - PreferenceLearning: Aprende preferencias cada 60s")
    print("   - AdaptivePricing: Analiza precios cada 300s")
    print("   - TemporalTrends: Detecta tendencias cada 180s")
    print("   - PatternDiscovery: Descubre patrones cada 240s")
    print("   - RecommendationOptimizer: Optimiza cada 120s\n")
    
    # Mostrar menu
    mostrar_menu()
    
    # Detener demonios al salir
    print("\n Deteniendo sistema de aprendizaje...")
    demons_manager.stop_all_demons()
    connector.close()
    
    return 0


def mostrar_menu():
    """Menu principal simplificado con aprendizaje automatico"""
    while True:
        print("\n" + "="*70)
        print(" MENU PRINCIPAL - Aprendizaje IA Activo")
        print("="*70)
        print()
        print("  1. Interfaz Web (Gradio) - RECOMENDADO")
        print("  2. Consulta rapida (CLI)")
        print("  3. Ver estadisticas del sistema")
        print("  4. Salir")
        print()
        
        try:
            opcion = input("Elige opcion (1-4): ").strip()
            
            if opcion == "1":
                lanzar_gradio()
            elif opcion == "2":
                consulta_cli()
            elif opcion == "3":
                ver_estadisticas()
            elif opcion == "4":
                print("\n Hasta luego!\n")
                break
            else:
                print(" Opcion no valida")
        
        except KeyboardInterrupt:
            print("\n\n Sistema terminado\n")
            break
        except Exception as e:
            print(f"\n Error: {e}\n")


def lanzar_gradio():
    """Lanza interfaz web Gradio"""
    print("\n Lanzando interfaz web Gradio...")
    print(" Se abrira automaticamente en tu navegador")
    
    try:
        from ui.gradio_ui import demo
        
        # Intentar múltiples puertos
        puertos = [7860, 7861, 7862, 8080, 8888]
        
        for puerto in puertos:
            try:
                print(f"\n Intentando puerto {puerto}...")
                print(f" Si no se abre, ve a: http://localhost:{puerto}")
                print("\n  Presiona Ctrl+C para detener el servidor\n")
                
                demo.launch(
                    server_name="127.0.0.1",  # Solo localhost
                    server_port=puerto,
                    share=False,
                    debug=False,
                    inbrowser=True,
                    show_error=True,
                    quiet=False
                )
                break  # Si funciona, salir del loop
                
            except OSError as e:
                if "Address already in use" in str(e) or "port" in str(e).lower():
                    print(f" Puerto {puerto} ocupado, intentando siguiente...")
                    continue
                else:
                    raise
        
    except ImportError as e:
        print(f" Error: {e}")
        print("\n Instala Gradio: pip install gradio")
    except KeyboardInterrupt:
        print("\n\n Servidor Gradio detenido")
    except Exception as e:
        print(f" Error lanzando Gradio: {e}")


def consulta_cli():
    """Consulta rapida desde CLI"""
    print("\n CONSULTA RAPIDA")
    print("-" * 70)
    print("Ejemplos:")
    print("  • ¿Hay casas en Palermo?")
    print("  • Busca departamentos por menos de 200000")
    print("  • Propiedades con 3 habitaciones")
    print("-" * 70)
    
    pregunta = input("\n  Tu consulta: ").strip()
    
    if not pregunta:
        print(" Consulta vacia")
        return
    
    try:
        from workflow.langgraph_workflow import ejecutar_consulta
        
        print("\n Procesando...\n")
        resultado = ejecutar_consulta(pregunta)
        
        print(" RESPUESTA:")
        print("-" * 70)
        print(resultado.get("respuesta", "Sin respuesta"))
        
        if input("\n¿Ver detalles tecnicos? (s/n): ").lower() in ['s', 'si']:
            print("\n EXPLICACION:")
            print("-" * 70)
            print(resultado.get("explicacion", "Sin explicacion"))
        
    except ImportError as e:
        print(f" Error: {e}")
        print(" Instala dependencias: pip install langchain langchain-community")
    except Exception as e:
        print(f" Error: {e}")


def ver_estadisticas():
    """Muestra estadisticas del sistema y estado de aprendizaje"""
    print("\n ESTADISTICAS DEL SISTEMA")
    print("-" * 70)
    
    try:
        from database.neo4j_connector import Neo4jConnector
        
        connector = Neo4jConnector()
        if not connector.is_connected():
            print(" No conectado a Neo4j")
            return
        
        stats = connector.get_database_stats()
        
        print(f"\n Propiedades: {stats.get('properties', 0)}")
        print(f" Usuarios: {stats.get('users', 0)}")
        print(f" Amenidades: {stats.get('amenities', 0)}")
        print(f" Relaciones: {stats.get('relationships', 0)}")
        
        # Consultar detalles adicionales
        with connector.get_session() as session:
            # Precios
            result = session.run("""
                MATCH (p:Property)
                RETURN min(p.price) AS min_price, 
                       max(p.price) AS max_price,
                       avg(p.price) AS avg_price
            """)
            precios = result.single()
            
            if precios:
                print(f"\n Rango de precios:")
                print(f"   Minimo: ${precios['min_price']:,}")
                print(f"   Promedio: ${int(precios['avg_price']):,}")
                print(f"   Maximo: ${precios['max_price']:,}")
            
            # Barrios
            result = session.run("""
                MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
                RETURN a.neighborhood AS barrio, count(p) AS cantidad
                ORDER BY cantidad DESC
                LIMIT 5
            """)
            
            barrios = list(result)
            if barrios:
                print(f"\n Barrios con mas propiedades:")
                for b in barrios:
                    print(f"   • {b['barrio']}: {b['cantidad']}")
            
            # MOSTRAR ESTADO DE APRENDIZAJE
            print(f"\n SISTEMA DE APRENDIZAJE:")
            print("-" * 70)
            
            # Preferencias aprendidas
            result = session.run("""
                MATCH (u:User)-[p:PREFERS]->(f)
                RETURN count(*) as total_prefs
            """)
            prefs = result.single()
            if prefs:
                print(f" Preferencias aprendidas: {prefs['total_prefs']}")
            
            # Clicks registrados
            result = session.run("""
                MATCH ()-[c:CLICKED]->()
                RETURN count(c) as total_clicks
            """)
            clicks = result.single()
            if clicks:
                print(f" Clicks registrados: {clicks['total_clicks']}")
            
            # Patrones descubiertos
            result = session.run("""
                MATCH ()-[r:CO_VIEWED]->()
                RETURN count(r) as total_patterns
            """)
            patterns = result.single()
            if patterns:
                print(f" Patrones descubiertos: {patterns['total_patterns']}")
            
            print("\n Estado: Demonios IA activos - Aprendiendo continuamente")
        
        connector.close()
        
    except Exception as e:
        print(f" Error: {e}")


if __name__ == "__main__":
    sys.exit(main())
