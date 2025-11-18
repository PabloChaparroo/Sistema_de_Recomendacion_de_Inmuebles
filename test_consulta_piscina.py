"""
Test específico para la consulta de piscina
"""
from workflow.langchain_integration import create_housing_qa

print("\n" + "="*70)
print("🏊 TEST: Consulta de propiedades con piscina")
print("="*70 + "\n")

qa_chain, graph = create_housing_qa()

pregunta = "¿Hay propiedades con más de 3 habitaciones y piscina?"
print(f"❓ PREGUNTA: {pregunta}\n")

resultado = qa_chain.invoke({"query": pregunta})

print("\n📝 CYPHER GENERADO:")
if 'intermediate_steps' in resultado and len(resultado['intermediate_steps']) > 0:
    cypher = resultado['intermediate_steps'][0].get('query', 'No disponible')
    print(f"   {cypher}")

print("\n💬 RESPUESTA:")
print(f"   {resultado['result']}")

print("\n" + "="*70)
print("✅ TEST COMPLETADO")
print("="*70)
