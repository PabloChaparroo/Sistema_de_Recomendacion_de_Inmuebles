"""
Script de prueba para verificar Ollama + Neo4j
Ejecuta 3 consultas de prueba para validar el sistema
"""

from workflow.langchain_integration import ask_question

print("=" * 70)
print("🧪 PRUEBA DEL SISTEMA: Ollama + Neo4j + LangChain")
print("=" * 70)
print("\n⚠️  Asegúrate de tener:")
print("  1. Neo4j corriendo (Neo4j Desktop)")
print("  2. Ollama ejecutándose (ollama serve)")
print("  3. Modelo mistral descargado (ollama pull mistral)")
print("\n" + "=" * 70 + "\n")

# Prueba 1: Contar propiedades totales
print("📊 PRUEBA 1: Contar propiedades totales")
print("-" * 70)
resultado = ask_question("¿Cuántas propiedades hay en total?")
if resultado["success"]:
    print(f"✅ Cypher generado:\n   {resultado['cypher']}")
    print(f"\n💬 Respuesta: {resultado['answer']}")
else:
    print(f"❌ Error: {resultado['error']}")

print("\n" + "=" * 70 + "\n")

# Prueba 2: Propiedades por ciudad
print("🏙️  PRUEBA 2: Buscar propiedades en Mendoza")
print("-" * 70)
resultado = ask_question("¿Cuántas propiedades hay en la ciudad de Mendoza?")
if resultado["success"]:
    print(f"✅ Cypher generado:\n   {resultado['cypher']}")
    print(f"\n💬 Respuesta: {resultado['answer']}")
else:
    print(f"❌ Error: {resultado['error']}")

print("\n" + "=" * 70 + "\n")

# Prueba 3: Listar amenidades
print("🎯 PRUEBA 3: Listar amenidades disponibles")
print("-" * 70)
resultado = ask_question("Lista todas las amenidades que existen en la base de datos")
if resultado["success"]:
    print(f"✅ Cypher generado:\n   {resultado['cypher']}")
    print(f"\n💬 Respuesta: {resultado['answer']}")
else:
    print(f"❌ Error: {resultado['error']}")

print("\n" + "=" * 70)
print("✅ PRUEBAS COMPLETADAS")
print("=" * 70)
print("\n📝 Notas para el informe PG6:")
print("  - Captura estas consultas y respuestas")
print("  - Documenta el Cypher generado por Ollama")
print("  - Muestra el flujo: Pregunta → Ollama → Cypher → Neo4j → Respuesta")
print("=" * 70 + "\n")
