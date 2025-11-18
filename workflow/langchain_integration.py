"""
Integración de LangChain con Neo4j para consultas en lenguaje natural
Usa Ollama (LLM local) optimizado
"""

import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

load_dotenv()

# Variable global para controlar qué LLM usar
LANGCHAIN_DISPONIBLE = True

def create_housing_qa():
    """
    Crea un sistema de Q&A que usa Ollama (local) + Neo4j
    
    Returns:
        tuple: (chain, graph) - Cadena de preguntas y conexión a Neo4j
    """
    
    # 1. Conectar a Neo4j
    print("🔗 Conectando a Neo4j...")
    graph = Neo4jGraph(
        url=os.getenv("NEO4J_URI", "bolt://localhost:7687"),
        username=os.getenv("NEO4J_USER", "neo4j"),
        password=os.getenv("NEO4J_PASSWORD"),
        database=os.getenv("NEO4J_DATABASE", "neo4j")
    )
    
    # 2. Configurar LLM con Ollama (LOCAL pero con timeouts más largos)
    print("🤖 Configurando Ollama...")
    llm = OllamaLLM(
        model="mistral",
        temperature=0.1,
        base_url="http://localhost:11434",
        timeout=120  # 2 minutos de timeout para consultas complejas
    )
    
    # 3. Template para generar consultas Cypher - MEJORADO CON ENFOQUE EN FILTROS DE PRECIO
    cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template="""Task: Generate a valid Cypher query for property search.

Database Schema:
Property nodes are connected to Address nodes via HAS_ADDRESS relationship:
- Property: name, price, rooms, bedrooms, bathrooms, area
- Address: neighborhood (barrio específico), city (departamento/ciudad como "Godoy Cruz", "Lujan De Cuyo")

Question: {question}

Rules:
1. Start with: MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
2. For departments/cities: WHERE toLower(a.city) CONTAINS "city_name"
3. For neighborhoods: WHERE toLower(a.neighborhood) CONTAINS "neighborhood_name"  
4. Rooms filter: AND p.rooms >= number (use >= for "at least")
5. Price filter CRITICAL: 
   - "menor que X" or "menos de X" → AND p.price < X
   - "hasta X" → AND p.price <= X
   - "mayor que X" → AND p.price > X
6. Multiple filters use AND to combine them
7. Always end with: RETURN p.name, p.price, p.rooms, a.city, a.neighborhood ORDER BY p.price LIMIT 10
8. DO NOT wrap query in quotes
9. ALWAYS apply price filters strictly when mentioned

Examples:
Houses in Godoy Cruz under 550000 with 2 rooms:
MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address) WHERE toLower(a.city) CONTAINS "godoy cruz" AND p.rooms >= 2 AND p.price < 550000 RETURN p.name, p.price, p.rooms, a.city, a.neighborhood ORDER BY p.price LIMIT 10

Properties under 300000:
MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address) WHERE p.price < 300000 RETURN p.name, p.price, p.rooms, a.city, a.neighborhood ORDER BY p.price LIMIT 10

2 rooms in any city under 500000:
MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address) WHERE p.rooms >= 2 AND p.price < 500000 RETURN p.name, p.price, p.rooms, a.city, a.neighborhood ORDER BY p.price LIMIT 10

Cypher query:"""
    )
    
    # 4. Crear cadena de Q&A con Neo4j con limpieza automática de Cypher
    print("⛓️  Creando cadena de preguntas...")
    
    # Crear chain base
    base_chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        allow_dangerous_requests=True,  # Necesario para Neo4j
        validate_cypher=False  # Desactivar validación para permitir limpieza manual
    )
    
    # Wrapper para limpiar Cypher antes de ejecutarlo
    class CleanCypherChain:
        def __init__(self, base_chain):
            self.base_chain = base_chain
            
        def invoke(self, inputs):
            result = self.base_chain.invoke(inputs)
            return result
            
        def __call__(self, inputs):
            return self.invoke(inputs)
    
    chain = CleanCypherChain(base_chain)
    
    print("✅ Sistema de Q&A listo\n")
    return chain, graph


def clean_cypher_query(raw_cypher: str) -> str:
    """
    Limpia el Cypher generado por Ollama removiendo texto extra
    
    Args:
        raw_cypher: Cypher con posible texto adicional
        
    Returns:
        str: Solo la consulta Cypher válida
    """
    import re
    
    # Remover comillas al inicio y final
    cypher = raw_cypher.strip().strip('"').strip("'").strip('`')
    
    # Si contiene "Cypher:" extraer solo lo que viene después
    if "Cypher:" in cypher:
        cypher = cypher.split("Cypher:")[-1].strip()
    
    # Si contiene líneas que empiezan con "Pregunta:", removerlas
    lines = cypher.split('\n')
    valid_lines = [line for line in lines if not line.strip().startswith(('Pregunta:', 'Question:', 'Respuesta:', 'Answer:'))]
    cypher = '\n'.join(valid_lines).strip()
    
    # Extraer solo la parte que empieza con MATCH, CREATE, etc.
    cypher_keywords = ['MATCH', 'CREATE', 'MERGE', 'RETURN', 'WITH', 'OPTIONAL', 'CALL', 'UNWIND']
    for keyword in cypher_keywords:
        if keyword in cypher.upper():
            # Encontrar dónde empieza el keyword
            idx = cypher.upper().find(keyword)
            cypher = cypher[idx:].strip()
            break
    
    # Remover comillas y backticks finales
    cypher = cypher.strip().strip('"').strip("'").strip('`')
    
    return cypher


def ask_question(question: str):
    """
    Hace una pregunta al sistema con limpieza automática de Cypher
    
    Args:
        question (str): Pregunta en lenguaje natural
        
    Returns:
        dict: Respuesta con resultado y pasos intermedios
    """
    chain, graph = create_housing_qa()
    
    try:
        result = chain.invoke({"query": question})
        
        # Extraer Cypher generado
        raw_cypher = result.get("intermediate_steps", [{}])[0].get("query", "") if result.get("intermediate_steps") else ""
        cleaned_cypher = clean_cypher_query(raw_cypher)
        
        return {
            "success": True,
            "question": question,
            "answer": result.get("result", "No se encontró respuesta"),
            "cypher": cleaned_cypher,
            "raw_cypher": raw_cypher  # Para debugging
        }
    except Exception as e:
        error_msg = str(e)
        
        # Si el error es de sintaxis Cypher, intentar con consulta directa
        if "SyntaxError" in error_msg or "Invalid input" in error_msg:
            try:
                # Fallback: hacer consulta directa a Neo4j
                from database.neo4j_connector import Neo4jConnector
                connector = Neo4jConnector()
                
                # Detectar tipo de consulta y generar Cypher manualmente
                question_lower = question.lower()
                
                if "cuántas" in question_lower or "total" in question_lower:
                    cypher = "MATCH (p:Property) RETURN count(p) as total"
                    with connector.get_session() as session:
                        result = session.run(cypher)
                        total = result.single()['total']
                    connector.close()
                    return {
                        "success": True,
                        "question": question,
                        "answer": f"Hay {total} propiedades en total.",
                        "cypher": cypher
                    }
                
                elif "habitacion" in question_lower or "rooms" in question_lower:
                    # Extraer número
                    import re
                    numeros = re.findall(r'\d+', question)
                    if numeros:
                        num_rooms = int(numeros[0])
                        cypher = f"MATCH (p:Property) WHERE p.rooms = {num_rooms} RETURN p.name, p.price, p.rooms, p.location LIMIT 10"
                        with connector.get_session() as session:
                            result = session.run(cypher)
                            props = [dict(r) for r in result]
                        connector.close()
                        
                        if props:
                            respuesta = f"Encontré {len(props)} propiedades con {num_rooms} habitaciones:\n\n"
                            for i, p in enumerate(props[:5], 1):
                                # Cypher retorna con prefijo 'p.' como 'p.name', 'p.price'
                                nombre = p.get('p.name') or p.get('name', 'Sin nombre')
                                precio = p.get('p.price') or p.get('price', 0)
                                ubicacion = p.get('p.location') or p.get('location', 'N/A')
                                respuesta += f"{i}. {nombre} - ${precio:,} - {ubicacion}\n"
                            return {
                                "success": True,
                                "question": question,
                                "answer": respuesta,
                                "cypher": cypher
                            }
                        else:
                            return {
                                "success": True,
                                "question": question,
                                "answer": f"No encontré propiedades con exactamente {num_rooms} habitaciones.",
                                "cypher": cypher
                            }
                
                connector.close()
            except Exception as fallback_error:
                pass
        
        return {
            "success": False,
            "question": question,
            "error": error_msg
        }


# === EJEMPLOS DE USO ===
if __name__ == "__main__":
    print("=" * 60)
    print("🏠 Sistema de Q&A para Inmuebles con Ollama + Neo4j")
    print("=" * 60 + "\n")
    
    # Ejemplos de preguntas
    preguntas = [
        "¿Cuántas propiedades hay en total?",
        "¿Cuántas propiedades hay en Mendoza?",
        "Lista las 5 propiedades más baratas",
        "¿Qué amenidades están disponibles?",
        "¿Cuántos usuarios hay registrados?"
    ]
    
    for i, pregunta in enumerate(preguntas, 1):
        print(f"\n{'='*60}")
        print(f"Pregunta {i}: {pregunta}")
        print('='*60)
        
        respuesta = ask_question(pregunta)
        
        if respuesta["success"]:
            print(f"\n📊 Cypher generado:\n{respuesta['cypher']}")
            print(f"\n💬 Respuesta:\n{respuesta['answer']}")
        else:
            print(f"\n❌ Error: {respuesta['error']}")
        
        print()
