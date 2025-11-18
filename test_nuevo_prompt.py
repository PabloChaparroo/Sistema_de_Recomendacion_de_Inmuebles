"""
Test directo: Verificar Cypher generado con nuevo prompt
"""

from workflow.langchain_integration import create_housing_qa

print("="*60)
print("TEST: Consulta con nuevo prompt")
print("="*60)

# Recrear chain para forzar nuevo prompt
chain, graph = create_housing_qa()

consulta = "Necesito una casa en Godoy Cruz con 2 habitaciones, a un precio menor que 550000"

print(f"\n📝 Consulta: {consulta}\n")

try:
    resultado = chain.invoke({"query": consulta})
    
    print("🔍 CYPHER GENERADO:")
    if 'intermediate_steps' in resultado:
        cypher = resultado['intermediate_steps'][0]['query']
        print(cypher)
    
    print("\n📋 RESPUESTA:")
    print(resultado.get('result', 'Sin respuesta'))
    
except Exception as e:
    print(f"\n❌ ERROR: {e}")
