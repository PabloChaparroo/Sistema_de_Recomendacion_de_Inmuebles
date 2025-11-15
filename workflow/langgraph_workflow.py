"""
Flujos multi-paso con LangGraph para consultas complejas sobre inmuebles
Orquesta consultas difusas, recomendaciones y explicaciones
"""

from typing import TypedDict, Optional, List, Dict, Any
from models.housing_frames import calcular_score_propiedad, UserFrame
from database.neo4j_connector import Neo4jConnector
import os

# Cargar .env si no está cargado
try:
    from dotenv import load_dotenv
    load_dotenv()
except:
    pass

# Verificar si hay token de HuggingFace configurado
LANGCHAIN_DISPONIBLE = False
qa_chain = None
graph_langchain = None

if os.environ.get('HUGGINGFACEHUB_API_TOKEN'):
    try:
        print("🔄 Inicializando LangChain con HuggingFace...")
        # Importar desde el paquete workflow (ruta relativa tras reorganización)
        from workflow.langchain_integration import create_housing_qa
        qa_chain, graph_langchain = create_housing_qa()
        LANGCHAIN_DISPONIBLE = qa_chain is not None
        if LANGCHAIN_DISPONIBLE:
            print("✅ IA Generativa ACTIVADA (LangChain + HuggingFace)")
        else:
            print("⚠️ LangChain no se pudo inicializar - usando modo directo")
    except Exception as e:
        print(f"⚠️ Error al cargar LangChain: {e}")
        print("⚠️ Usando modo directo a Neo4j")
        LANGCHAIN_DISPONIBLE = False
else:
    print("💡 Token de HuggingFace no encontrado - usando modo directo")

# === ESTADO COMPARTIDO ENTRE NODOS ===
class ConsultaState(TypedDict, total=False):
    """Estado que viaja por el grafo de LangGraph"""
    pregunta: str
    tipo: str  # "simple" | "recomendacion" | "busqueda_filtrada"
    usuario: Optional[str]
    parametros: Optional[Dict]  # Filtros extraídos de la pregunta
    propiedades: Optional[List[Dict]]
    respuesta: Optional[str]
    explicacion: Optional[str]
    cypher_ejecutado: Optional[str]

# === NODOS DEL GRAFO ===

def n_clasificar_pregunta(state: ConsultaState) -> ConsultaState:
    """
    N1: Clasifica el tipo de consulta según palabras clave
    """
    pregunta = (state.get("pregunta") or "").lower()
    
    # Detectar tipo de consulta
    if any(k in pregunta for k in ["recomienda", "mejor", "sugiere", "ideal"]):
        state["tipo"] = "recomendacion"
    elif any(k in pregunta for k in ["busca", "buscar", "barrio", "zona", "presupuesto", "precio", "habitaciones", "casa", "casas", "departamento", "depto", "ciudad", "mendoza", "propiedad", "propiedades"]):
        state["tipo"] = "busqueda_filtrada"
    else:
        state["tipo"] = "simple"
    
    # Extraer parámetros básicos
    parametros = {}
    
    # Detectar barrios/departamentos de Mendoza (están en neighborhood, no en city)
    # Mapeo de palabras clave a nombres exactos en la base de datos
    # IMPORTANTE: Ordenar de más específico a menos específico
    barrios_map = [
        ("ciudad de mendoza", "Ciudad de Mendoza"),
        ("lujan de cuyo", "Luján de Cuyo"),
        ("luján de cuyo", "Luján de Cuyo"),
        ("chacras de coria", "Chacras de Coria"),
        ("godoy cruz", "Godoy Cruz"),
        ("las heras", "Las Heras"),
        ("villa nueva", "Villa Nueva"),
        ("san rafael", "San Rafael"),
        ("quinta sección", "Quinta Sección"),
        ("cuarta sección", "Cuarta Sección"),
        ("sexta sección", "Sexta Sección"),
        ("san jose", "San José"),
        ("san josé", "San José"),
        ("guaymallen", "Guaymallén"),
        ("guaymallén", "Guaymallén"),
        ("dorrego", "Dorrego"),
        ("maipu", "Maipú"),
        ("maipú", "Maipú"),
        ("godoy", "Godoy Cruz"),
        ("luján", "Luján de Cuyo"),
        ("mendoza", "Ciudad de Mendoza"),
        ("ciudad", "Ciudad de Mendoza"),
    ]
    
    for keyword, barrio_real in barrios_map:
        if keyword in pregunta:
            parametros["barrio"] = barrio_real
            break  # Tomar solo el primer match
    
    # Detectar tipo de propiedad (pero no lo usaremos como filtro si no está en la BD)
    tipo_buscado = None
    if "casa" in pregunta or "casas" in pregunta:
        tipo_buscado = "Casa"
    elif "departamento" in pregunta or "depto" in pregunta or "dpto" in pregunta:
        tipo_buscado = "Departamento"
    
    # NOTA: No agregamos tipo a los parámetros porque property_type está vacío en la BD
    # parametros["tipo"] = tipo_buscado  # Comentado hasta que se llene property_type
    
    # Detectar presupuesto (buscar números)
    import re
    numeros = re.findall(r'\d+(?:\.\d+)?', pregunta)
    if numeros:
        # Asumir que el número más grande es el presupuesto
        parametros["presupuesto"] = int(float(max(numeros, key=lambda x: float(x))))
    
    # Detectar habitaciones
    if "habitacion" in pregunta or "dormitorio" in pregunta or "ambiente" in pregunta:
        for num in numeros:
            if int(float(num)) <= 10:  # Razonable para habitaciones
                parametros["min_rooms"] = int(float(num))
                break
    
    state["parametros"] = parametros
    return state

def n_consulta_simple(state: ConsultaState) -> ConsultaState:
    """
    N2: Ejecuta consulta simple usando LangChain (si está disponible) o Neo4j directo
    """
    
    pregunta = state.get("pregunta", "")
    
    # Si LangChain está disponible, usarlo
    if LANGCHAIN_DISPONIBLE and qa_chain:
        try:
            print(f"   🤖 Usando IA Generativa para: {pregunta[:50]}...")
            resultado = qa_chain.invoke({"query": pregunta})
            
            state["respuesta"] = resultado.get('result', 'No se pudo procesar')
            
            if 'intermediate_steps' in resultado and resultado['intermediate_steps']:
                cypher = resultado['intermediate_steps'][0].get('query', '')
                state["cypher_ejecutado"] = cypher
                state["explicacion"] = f"**🤖 Cypher generado por IA:**\n```cypher\n{cypher}\n```\n\n*Modelo: Mistral-7B (HuggingFace)*"
            else:
                state["explicacion"] = "Consulta procesada con IA generativa"
            
            return state
        
        except Exception as e:
            print(f"   ⚠️ Error en IA: {e}, usando fallback...")
            # Continuar con modo directo
    
    # Modo directo (fallback o cuando no hay LangChain)
    pregunta_lower = pregunta.lower()
    connector = Neo4jConnector()
    
    if not connector.is_connected():
        state["respuesta"] = "❌ No se pudo conectar a Neo4j"
        state["explicacion"] = "Verifica que Neo4j esté corriendo"
        return state
    
    try:
        # Detectar qué quiere saber el usuario
        if "cuántas" in pregunta_lower or "cuantas" in pregunta_lower or "total" in pregunta_lower:
            # Contar propiedades
            query = "MATCH (p:Property) RETURN count(p) AS total"
            with connector.get_session() as session:
                result = session.run(query)
                total = result.single()['total']
            
            state["respuesta"] = f"✅ Hay **{total} propiedades** en total en la base de datos."
            state["cypher_ejecutado"] = query
            state["explicacion"] = f"**Cypher ejecutado:**\n```cypher\n{query}\n```"
        
        elif "barrios" in pregunta_lower or "zonas" in pregunta_lower:
            # Listar barrios
            query = """
            MATCH (a:Address)
            RETURN DISTINCT a.neighborhood AS barrio, count(*) AS propiedades
            ORDER BY propiedades DESC
            LIMIT 10
            """
            with connector.get_session() as session:
                result = session.run(query)
                barrios = [f"• **{r['barrio']}**: {r['propiedades']} propiedades" for r in result]
            
            state["respuesta"] = "🏘️ **Barrios disponibles:**\n\n" + "\n".join(barrios)
            state["cypher_ejecutado"] = query
            state["explicacion"] = f"**Cypher ejecutado:**\n```cypher\n{query}\n```"
        
        else:
            # Respuesta genérica
            state["respuesta"] = "💡 Prueba consultas más específicas como:\n• '¿Cuántas propiedades hay?'\n• '¿Qué barrios hay?'\n• 'Busca casas en Palermo'\n• 'Departamentos por menos de 200000'"
            state["explicacion"] = "Consulta no reconocida. Usa filtros específicos."
    
    except Exception as e:
        state["respuesta"] = f"❌ Error: {e}"
        state["explicacion"] = f"Tipo de error: {type(e).__name__}"
    
    finally:
        connector.close()
    
    return state

def n_buscar_propiedades(state: ConsultaState) -> ConsultaState:
    """
    N3: Busca propiedades según filtros extraídos
    """
    parametros = state.get("parametros", {})
    
    # Usar Neo4jConnector directamente (sin necesidad de LangChain)
    connector = Neo4jConnector()
    
    if not connector.is_connected():
        state["propiedades"] = []
        return state
    
    # Construir query dinámicamente según parámetros
    condiciones = []
    params = {}
    
    if "tipo" in parametros:
        condiciones.append("p.property_type = $tipo")
        params["tipo"] = parametros["tipo"]
    
    if "barrio" in parametros:
        condiciones.append("toLower(a.neighborhood) CONTAINS toLower($barrio)")
        params["barrio"] = parametros["barrio"]
    
    if "presupuesto" in parametros:
        condiciones.append("p.price <= $presupuesto")
        params["presupuesto"] = parametros["presupuesto"]
    
    if "min_rooms" in parametros:
        condiciones.append("p.rooms >= $min_rooms")
        params["min_rooms"] = parametros["min_rooms"]
    
    # Construir WHERE clause
    where_clause = " AND ".join(condiciones) if condiciones else "1=1"
    
    query = f"""
    MATCH (p:Property)-[:HAS_ADDRESS]->(a:Address)
    WHERE {where_clause}
    RETURN p.name AS propiedad, 
           p.property_type AS tipo,
           p.price AS precio, 
           p.rooms AS habitaciones,
           p.area AS area, 
           a.neighborhood AS barrio,
           a.city AS ciudad
    ORDER BY p.price
    LIMIT 20
    """
    
    with connector.get_session() as session:
        result = session.run(query, **params)
        resultados = [dict(record) for record in result]
    
    state["cypher_ejecutado"] = query.replace("$tipo", f"'{params.get('tipo', '')}'").replace("$ciudad", f"'{params.get('ciudad', '')}'").replace("$barrio", f"'{params.get('barrio', '')}'").replace("$presupuesto", str(params.get('presupuesto', '')))
    
    connector.close()
    
    # Convertir a formato estándar
    propiedades = []
    for r in resultados:
        propiedades.append({
            'name': r.get('propiedad', 'Sin nombre'),
            'type': r.get('tipo', 'N/A'),
            'price': r.get('precio', 0),
            'rooms': r.get('habitaciones', 0),
            'area': r.get('area', 0),
            'location': f"{r.get('barrio', 'Desconocido')}, {r.get('ciudad', 'Mendoza')}",
        })
    
    state["propiedades"] = propiedades
    return state

def n_evaluar_difuso(state: ConsultaState) -> ConsultaState:
    """
    N4: Aplica lógica difusa para rankear propiedades
    """
    propiedades = state.get("propiedades", [])
    parametros = state.get("parametros", {})
    
    if not propiedades:
        return state
    
    # Crear UserFrame con parámetros de búsqueda
    usuario_virtual = UserFrame(
        name="Usuario búsqueda",
        budget=parametros.get("presupuesto"),
        min_rooms=parametros.get("min_rooms", 1),
        location_preference=parametros.get("barrio")
    )
    
    # Calcular scores difusos
    for prop in propiedades:
        prop['score_difuso'] = calcular_score_propiedad(prop, usuario_virtual)
    
    # Ordenar por score
    propiedades.sort(key=lambda x: x.get('score_difuso', 0), reverse=True)
    
    state["propiedades"] = propiedades
    return state

def n_redactar_respuesta(state: ConsultaState) -> ConsultaState:
    """
    N5: Genera respuesta final con explicación
    """
    propiedades = state.get("propiedades", [])[:10]  # Top 10 (aumentado de 5)
    parametros = state.get("parametros", {})
    
    if not propiedades:
        state["respuesta"] = "❌ No se encontraron propiedades con esos criterios."
        state["explicacion"] = "Intenta ampliar los filtros de búsqueda."
        return state
    
    # Construir respuesta
    respuesta = [f"🏠 **PROPIEDADES ENCONTRADAS:** ({len(propiedades)} resultados)\n"]
    
    for i, prop in enumerate(propiedades, 1):
        score = prop.get('score_difuso', 0)
        tipo = prop.get('type', None)
        
        # Formatear nombre con tipo solo si existe
        if tipo and tipo != 'None':
            nombre_completo = f"{prop['name']} ({tipo})"
        else:
            nombre_completo = f"{prop['name']}"
        
        respuesta.append(f"{i}. **{nombre_completo}**")
        respuesta.append(f"   💰 ${prop['price']:,}")
        respuesta.append(f"   📏 {prop['area']}m² | 🛏️ {prop['rooms']} hab")
        respuesta.append(f"   📍 {prop['location']}")
        if score > 0 and score < 1.0:  # Solo mostrar score si es significativo
            respuesta.append(f"   ⭐ Compatibilidad: {score:.0%}")
        respuesta.append("")
    
    # Construir explicación
    explicacion = ["📊 **CRITERIOS DE BÚSQUEDA:**"]
    
    if parametros.get("tipo"):
        explicacion.append(f"• Tipo: {parametros['tipo']}")
    if parametros.get("barrio"):
        explicacion.append(f"• Zona/Barrio: {parametros['barrio']}")
    if parametros.get("presupuesto"):
        explicacion.append(f"• Presupuesto máx: ${parametros['presupuesto']:,}")
    if parametros.get("min_rooms"):
        explicacion.append(f"• Habitaciones mín: {parametros['min_rooms']}")
    
    explicacion.append(f"\n🔍 **Cypher ejecutado:**")
    explicacion.append(f"```\n{state.get('cypher_ejecutado', 'N/A')}\n```")
    
    explicacion.append(f"\n🧮 **Sistema de Puntuación Difusa:**")
    explicacion.append("La compatibilidad se calcula usando lógica difusa:")
    explicacion.append("• 🏷️ Precio (30%): Qué tan cerca del presupuesto ideal")
    explicacion.append("• 🛏️ Habitaciones (20%): Coincidencia con tus necesidades")
    explicacion.append("• 🎯 Amenidades (50%): Servicios y comodidades")
    explicacion.append("\n💡 **Score 100%** = Coincidencia perfecta con tus preferencias")
    explicacion.append("💡 **Score < 100%** = Buena opción pero con algunas diferencias")
    
    state["respuesta"] = "\n".join(respuesta)
    state["explicacion"] = "\n".join(explicacion)
    
    return state

# === REGISTRO DE NODOS ===
NODOS = {
    "clasificar": n_clasificar_pregunta,
    "simple": n_consulta_simple,
    "buscar": n_buscar_propiedades,
    "evaluar": n_evaluar_difuso,
    "redactar": n_redactar_respuesta,
}

def ejecutar_consulta(pregunta: str, usuario: Optional[str] = None) -> ConsultaState:
    """
    Orquesta el flujo completo de consulta
    
    Args:
        pregunta: Pregunta del usuario en lenguaje natural
        usuario: Nombre de usuario (opcional)
    
    Returns:
        ConsultaState con respuesta y explicación
    """
    
    # Inicializar estado
    state = {
        "pregunta": pregunta,
        "usuario": usuario
    }
    
    # Ejecutar nodos secuencialmente
    state = NODOS["clasificar"](state)
    
    if state["tipo"] == "simple":
        state = NODOS["simple"](state)
    
    else:  # "busqueda_filtrada" o "recomendacion"
        state = NODOS["buscar"](state)
        state = NODOS["evaluar"](state)
        state = NODOS["redactar"](state)
    
    return state

# === EJEMPLO DE USO ===
if __name__ == "__main__":
    print("🏠 TEST DE LANGGRAPH WORKFLOW\n")
    
    # Probar diferentes consultas
    consultas_test = [
        "¿Hay casas en Palermo con 3 habitaciones?",
        "Busca departamentos por menos de 200000",
        "¿Cuántas propiedades hay?",
    ]
    
    for pregunta in consultas_test:
        print(f"\n{'='*60}")
        print(f"❓ Pregunta: {pregunta}")
        print('='*60)
        
        resultado = ejecutar_consulta(pregunta)
        
        print(f"\n📋 Tipo detectado: {resultado.get('tipo')}")
        print(f"\n{resultado.get('respuesta', 'Sin respuesta')}")
        
        if resultado.get('explicacion'):
            print(f"\n🔬 Explicación:")
            print(resultado['explicacion'])
