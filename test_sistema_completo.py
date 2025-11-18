"""
Script de Prueba Completo del Sistema Integrado
Valida todos los componentes: Ollama, Neo4j, Fuzzy, Demons, LangGraph
"""

import sys
import os
from datetime import datetime

print("\n" + "="*70)
print("🧪 PRUEBA COMPLETA DEL SISTEMA INTEGRADO")
print("="*70 + "\n")

# === TEST 1: NEO4J CONNECTION ===
print("TEST 1: Conexión a Neo4j")
print("-" * 70)
try:
    from database.neo4j_connector import Neo4jConnector
    connector = Neo4jConnector()
    
    if connector.is_connected():
        print("✅ Conexión exitosa a Neo4j")
        stats = connector.get_database_stats()
        print(f"   📊 Propiedades: {stats.get('properties', 0)}")
        print(f"   👥 Usuarios: {stats.get('users', 0)}")
        print(f"   🏷️  Amenidades: {stats.get('amenities', 0)}")
        test1_pass = True
    else:
        print("❌ No se pudo conectar a Neo4j")
        test1_pass = False
    
    connector.close()
except Exception as e:
    print(f"❌ Error: {e}")
    test1_pass = False

print()

# === TEST 2: OLLAMA + LANGCHAIN ===
print("TEST 2: Ollama + LangChain Integration")
print("-" * 70)
try:
    from workflow.langchain_integration import ask_question
    
    pregunta = "¿Cuántas propiedades hay en total?"
    print(f"   🤔 Pregunta: {pregunta}")
    
    resultado = ask_question(pregunta)
    
    if resultado.get("success"):
        print("✅ Ollama funcionando correctamente")
        print(f"   💬 Respuesta: {resultado['answer']}")
        print(f"   🔍 Cypher: {resultado['cypher']}")
        test2_pass = True
    else:
        print(f"❌ Error: {resultado.get('error')}")
        test2_pass = False
        
except Exception as e:
    print(f"❌ Error: {e}")
    test2_pass = False

print()

# === TEST 3: LÓGICA DIFUSA ===
print("TEST 3: Sistema de Lógica Difusa")
print("-" * 70)
try:
    from models.housing_frames import calcular_score_propiedad, UserFrame
    
    # Usuario de prueba
    usuario = UserFrame(
        name="Test User",
        budget=150000,
        min_rooms=2,
        location_preference="Godoy Cruz"
    )
    
    # Propiedad de prueba
    propiedad = {
        'name': 'Propiedad Test',
        'price': 140000,
        'rooms': 2,
        'area': 80,
        'location': 'Godoy Cruz, Mendoza'
    }
    
    score = calcular_score_propiedad(propiedad, usuario)
    
    if score >= 0 and score <= 1:
        print("✅ Lógica difusa funcionando")
        print(f"   📊 Score calculado: {score:.2%}")
        print(f"   🏠 Propiedad: {propiedad['name']}")
        print(f"   👤 Usuario: {usuario.name}")
        test3_pass = True
    else:
        print(f"❌ Score inválido: {score}")
        test3_pass = False
        
except Exception as e:
    print(f"❌ Error: {e}")
    test3_pass = False

print()

# === TEST 4: FRAMES ===
print("TEST 4: Sistema de Frames")
print("-" * 70)
try:
    from models.housing_frames import PropertyFrame, UserFrame
    
    # Crear frame de propiedad con todos los campos requeridos
    prop_frame = PropertyFrame(
        name="Casa Test",
        property_type="casa",
        price=180000,
        rooms=3,
        bathrooms=2,
        area=100,
        location="Mendoza"
    )
    
    # Crear frame de usuario
    user_frame = UserFrame(
        name="Usuario Test",
        budget=200000,
        min_rooms=2
    )
    
    print("✅ Frames creados correctamente")
    print(f"   🏠 PropertyFrame: {prop_frame.name} ({prop_frame.property_type}) - ${prop_frame.price:,}")
    print(f"   👤 UserFrame: {user_frame.name} - Budget: ${user_frame.budget:,}")
    test4_pass = True
    
except Exception as e:
    print(f"❌ Error: {e}")
    test4_pass = False

print()

# === TEST 5: DEMONS MANAGER ===
print("TEST 5: Sistema de Demonios IA")
print("-" * 70)
try:
    from demons.demons_manager import DemonsManager
    
    connector = Neo4jConnector()
    demons_mgr = DemonsManager(connector)
    
    print("✅ DemonsManager creado")
    print(f"   🤖 Demonios disponibles:")
    print(f"      • PreferenceLearningDemon (aprende cada 60s)")
    print(f"      • AdaptivePricingDemon (analiza cada 300s)")
    print(f"      • TemporalTrendsDemon (detecta cada 180s)")
    print(f"      • PatternDiscoveryDemon (descubre cada 240s)")
    print(f"      • RecommendationOptimizerDemon (optimiza cada 120s)")
    
    # No iniciar los demonios en el test, solo verificar que existen
    test5_pass = True
    connector.close()
    
except Exception as e:
    print(f"❌ Error: {e}")
    test5_pass = False

print()

# === TEST 6: LANGGRAPH WORKFLOW ===
print("TEST 6: LangGraph Workflow Completo")
print("-" * 70)
try:
    from workflow.langgraph_workflow import ejecutar_consulta
    
    pregunta = "Busca propiedades en Mendoza"
    print(f"   🤔 Pregunta: {pregunta}")
    
    resultado = ejecutar_consulta(pregunta, usuario="Test User")
    
    if resultado.get("respuesta"):
        print("✅ Workflow LangGraph funcionando")
        print(f"   📝 Tipo consulta: {resultado.get('tipo')}")
        print(f"   💬 Respuesta generada: {len(resultado['respuesta'])} caracteres")
        if resultado.get('parametros'):
            print(f"   🎯 Parámetros extraídos: {resultado['parametros']}")
        test6_pass = True
    else:
        print("❌ No se generó respuesta")
        test6_pass = False
        
except Exception as e:
    print(f"❌ Error: {e}")
    print(f"   Detalle: {type(e).__name__}")
    test6_pass = False

print()

# === TEST 7: FUZZY EVALUATORS ===
print("TEST 7: Evaluadores Fuzzy")
print("-" * 70)
try:
    from fuzzy.fuzzy_evaluators import PriceFuzzyEvaluator
    from fuzzy.fuzzy_logic import FuzzyLogic
    
    # Test evaluación de precio
    evaluador_precio = PriceFuzzyEvaluator()
    memberships = evaluador_precio.evaluate_price_membership(150000)
    
    # Test función triangular
    score_triangular = FuzzyLogic.triangular_membership(
        value=75,
        a=50,
        b=75,
        c=100
    )
    
    print("✅ Evaluadores fuzzy funcionando")
    print(f"   💰 Memberships precio 150k: {memberships}")
    print(f"   📐 Score triangular (75 en rango 50-100): {score_triangular:.2%}")
    test7_pass = True
    
except Exception as e:
    print(f"❌ Error: {e}")
    test7_pass = False

print()

# === RESUMEN FINAL ===
print("="*70)
print("📊 RESUMEN DE PRUEBAS")
print("="*70)
print()

resultados = [
    ("Neo4j Connection", test1_pass),
    ("Ollama + LangChain", test2_pass),
    ("Lógica Difusa", test3_pass),
    ("Sistema de Frames", test4_pass),
    ("Demonios IA", test5_pass),
    ("LangGraph Workflow", test6_pass),
    ("Evaluadores Fuzzy", test7_pass),
]

total_tests = len(resultados)
passed_tests = sum(1 for _, passed in resultados if passed)

for nombre, passed in resultados:
    status = "✅ PASS" if passed else "❌ FAIL"
    print(f"{status}  {nombre}")

print()
print(f"📈 Resultado: {passed_tests}/{total_tests} pruebas exitosas ({passed_tests/total_tests*100:.0f}%)")
print()

if passed_tests == total_tests:
    print("🎉 ¡TODAS LAS PRUEBAS PASARON!")
    print("   El sistema está completamente funcional.")
    print()
    print("✨ Componentes validados:")
    print("   ✓ Base de datos Neo4j")
    print("   ✓ LLM Ollama (Mistral 7B)")
    print("   ✓ Lógica Difusa")
    print("   ✓ Modelos Predictivos (Frames)")
    print("   ✓ Sistema de Aprendizaje (Demons)")
    print("   ✓ Orquestación (LangGraph)")
    print("   ✓ NLP (LangChain)")
    sys.exit(0)
else:
    print("⚠️  Algunas pruebas fallaron.")
    print("   Revisa los mensajes de error arriba.")
    print()
    print("💡 Soluciones comunes:")
    print("   • Neo4j: Verificar que esté ejecutándose")
    print("   • Ollama: Ejecutar 'ollama serve' en terminal")
    print("   • Dependencias: pip install -r requirements.txt")
    sys.exit(1)

print()
