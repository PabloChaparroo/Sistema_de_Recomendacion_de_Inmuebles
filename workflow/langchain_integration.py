"""
Integración de LangChain con Neo4j para consultas en lenguaje natural
Usa Ollama (LLM local) en lugar de APIs externas
"""

import os
from dotenv import load_dotenv
from langchain_community.graphs import Neo4jGraph
from langchain_community.chains.graph_qa.cypher import GraphCypherQAChain
from langchain_core.prompts import PromptTemplate
from langchain_ollama import OllamaLLM

load_dotenv()


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
    
    # 2. Configurar LLM con Ollama (LOCAL - sin API keys)
    print("🤖 Configurando Ollama...")
    llm = OllamaLLM(
        model="mistral",
        temperature=0.1,
        base_url="http://localhost:11434"
    )
    
    # 3. Template para generar consultas Cypher
    cypher_prompt = PromptTemplate(
        input_variables=["schema", "question"],
        template="""Eres un experto en Neo4j y Cypher para un sistema inmobiliario.

Esquema de la base de datos:
{schema}

Pregunta del usuario: {question}

Genera SOLO la consulta Cypher necesaria para responder la pregunta.
Reglas:
- Usa nodos: Property (propiedades), User (usuarios), Amenity (amenidades)
- Relaciones: HAS_AMENITY, PREFERS_AMENITY, VISITED
- Propiedades importantes: city, price, bedrooms, bathrooms, area
- NO agregues explicaciones, solo Cypher
- Usa LIMIT 10 para evitar respuestas largas

Consulta Cypher:"""
    )
    
    # 4. Crear cadena de Q&A con Neo4j
    print("⛓️  Creando cadena de preguntas...")
    chain = GraphCypherQAChain.from_llm(
        llm=llm,
        graph=graph,
        verbose=True,
        return_intermediate_steps=True,
        cypher_prompt=cypher_prompt,
        allow_dangerous_requests=True  # Necesario para Neo4j
    )
    
    print("✅ Sistema de Q&A listo\n")
    return chain, graph


def ask_question(question: str):
    """
    Hace una pregunta al sistema
    
    Args:
        question (str): Pregunta en lenguaje natural
        
    Returns:
        dict: Respuesta con resultado y pasos intermedios
    """
    chain, _ = create_housing_qa()
    
    try:
        result = chain.invoke({"query": question})
        return {
            "success": True,
            "question": question,
            "answer": result.get("result", "No se encontró respuesta"),
            "cypher": result.get("intermediate_steps", [{}])[0].get("query", "") if result.get("intermediate_steps") else ""
        }
    except Exception as e:
        return {
            "success": False,
            "question": question,
            "error": str(e)
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
