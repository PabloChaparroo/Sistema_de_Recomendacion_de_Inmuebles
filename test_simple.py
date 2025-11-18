from workflow.langchain_integration import ask_question
import time

print("\n" + "="*60)
print("🧪 TEST SIMPLE DE CONSULTA")
print("="*60 + "\n")

pregunta = "¿Cuántas propiedades hay en total?"
print(f"❓ Pregunta: {pregunta}\n")

start = time.time()
resultado = ask_question(pregunta)
duracion = time.time() - start

print(f"\n⏱️  Tiempo: {duracion:.1f} segundos")
print(f"✅ Éxito: {resultado.get('success')}")
print(f"\n📋 Respuesta:")
print(f"   {resultado.get('answer', 'Sin respuesta')}\n")
print(f"🔍 Cypher generado:")
print(f"   {resultado.get('cypher', 'N/A')}\n")

if resultado.get('success'):
    print("✅ ¡LA CONSULTA FUNCIONÓ!")
else:
    print("❌ ERROR:", resultado.get('error'))

print("\n" + "="*60)
