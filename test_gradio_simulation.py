"""
Test exacto de lo que hace Gradio
"""

print("TEST: Simulando Gradio UI")
print("="*70)

# Simular la función procesar_consulta de Gradio
from workflow.langchain_integration import ask_question

pregunta = "¿Cuántas propiedades hay en total?"

print(f"🔍 Pregunta: {pregunta}")
print("\n⏳ Procesando con Ollama (puede tardar 30-60 seg)...\n")

resultado = ask_question(pregunta)

if resultado.get("success"):
    respuesta = resultado.get("answer", "No hay respuesta")
    cypher = resultado.get("cypher", "N/A")
    
    print("="*70)
    print("✅ ÉXITO")
    print("="*70)
    print(f"\n📋 RESPUESTA:")
    print(respuesta)
    print(f"\n🔍 CYPHER:")
    print(cypher)
else:
    error = resultado.get("error", "Error desconocido")
    print("="*70)
    print("❌ ERROR")
    print("="*70)
    print(f"Error: {error}")
