"""
Test rápido de HuggingFace API - Verificar velocidad
"""

import os
import time
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

# Verificar token
token = os.getenv("HUGGINGFACEHUB_API_TOKEN")
print(f"🔑 Token HuggingFace: {token[:20]}..." if token else "❌ No token found")

# Test de velocidad
from workflow.langchain_integration import create_housing_qa

print("\n⏱️  Iniciando test de velocidad con HuggingFace API...")
print("=" * 70)

try:
    # Crear chain
    inicio = time.time()
    chain, graph = create_housing_qa()
    tiempo_creacion = time.time() - inicio
    print(f"✅ Chain creado en {tiempo_creacion:.2f} segundos\n")
    
    # Test de consulta
    pregunta = "¿Cuántas propiedades hay en total?"
    print(f"❓ Pregunta: {pregunta}")
    print("🔄 Procesando con HuggingFace API...\n")
    
    inicio = time.time()
    resultado = chain.invoke({"query": pregunta})
    tiempo_total = time.time() - inicio
    
    print("=" * 70)
    print(f"⏱️  Tiempo total: {tiempo_total:.2f} segundos")
    print(f"✅ Respuesta: {resultado.get('result', 'Sin respuesta')}")
    print("=" * 70)
    
    if tiempo_total < 10:
        print("\n🎉 ÉXITO: HuggingFace es MUCHO más rápido que Ollama (60s)")
    elif tiempo_total < 30:
        print("\n✅ BUENO: Más rápido que Ollama pero se puede mejorar")
    else:
        print("\n⚠️  LENTO: Verificar configuración de HuggingFace")
    
    # Mostrar Cypher generado
    if "intermediate_steps" in resultado:
        print(f"\n🔍 Cypher generado:")
        for step in resultado["intermediate_steps"]:
            if "query" in step:
                print(f"   {step['query']}")

except Exception as e:
    print(f"\n❌ ERROR: {e}")
    import traceback
    traceback.print_exc()
