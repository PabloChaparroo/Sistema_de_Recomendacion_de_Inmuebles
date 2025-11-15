"""
Interfaz Gradio para Sistema de Recomendación de Inmuebles
Permite consultas en lenguaje natural con IA + Lógica Difusa
"""

import gradio as gr
from workflow.langgraph_workflow import ejecutar_consulta, LANGCHAIN_DISPONIBLE
from database.neo4j_connector import Neo4jConnector

# Variable global para usuario actual
usuario_actual = None

def obtener_usuarios():
    """Obtiene lista de usuarios existentes desde Neo4j"""
    connector = Neo4jConnector()
    try:
        with connector.get_session() as session:
            result = session.run("MATCH (u:User) RETURN u.name AS nombre ORDER BY nombre")
            usuarios = [record['nombre'] for record in result]
        connector.close()
        return usuarios
    except:
        return []

def crear_usuario(nombre: str):
    """Crea un nuevo usuario en Neo4j"""
    global usuario_actual
    
    if not nombre or nombre.strip() == "":
        return "⚠️ Por favor ingresa un nombre", obtener_usuarios(), None
    
    nombre = nombre.strip()
    connector = Neo4jConnector()
    
    try:
        with connector.get_session() as session:
            # Verificar si ya existe
            result = session.run("MATCH (u:User {name: $nombre}) RETURN u", nombre=nombre)
            if result.single():
                return f"⚠️ El usuario '{nombre}' ya existe. Selecciónalo de la lista.", obtener_usuarios(), None
            
            # Crear nuevo usuario con transacción explícita
            def create_user_tx(tx, nombre):
                tx.run("""
                    CREATE (u:User {
                        name: $nombre,
                        created_at: datetime(),
                        edad: 25,
                        occupation: 'Usuario'
                    })
                """, nombre=nombre)
            
            session.execute_write(create_user_tx, nombre)
        
        connector.close()
        usuario_actual = nombre
        return f"✅ Usuario '{nombre}' creado exitosamente!\n\n🎯 Ahora eres: **{nombre}**", obtener_usuarios(), nombre
    
    except Exception as e:
        return f"❌ Error al crear usuario: {e}", obtener_usuarios(), None

def seleccionar_usuario(nombre: str):
    """Selecciona un usuario existente"""
    global usuario_actual
    
    if not nombre:
        return "⚠️ Selecciona un usuario de la lista", None
    
    usuario_actual = nombre
    return f"✅ Sesión iniciada como: **{nombre}**\n\n💡 Todas tus búsquedas se guardarán para aprender tus preferencias", nombre

def registrar_click_propiedad(usuario: str, nombre_propiedad: str):
    """Registra que un usuario hizo click en una propiedad"""
    if not usuario or not nombre_propiedad:
        return "⚠️ Selecciona un usuario y una propiedad"
    
    connector = Neo4jConnector()
    try:
        with connector.get_session() as session:
            def click_tx(tx, usuario, prop_nombre):
                # Extraer solo el nombre de la propiedad (antes del guion si existe)
                prop_base = prop_nombre.split(' - ')[0] if ' - ' in prop_nombre else prop_nombre
                
                tx.run("""
                    MATCH (u:User {name: $usuario})
                    MATCH (p:Property)
                    WHERE p.name CONTAINS $prop_nombre OR p.name = $prop_nombre
                    MERGE (u)-[c:CLICKED]->(p)
                    ON CREATE SET c.timestamp = datetime(), c.count = 1
                    ON MATCH SET c.timestamp = datetime(), c.count = c.count + 1
                    RETURN p.name as nombre_completo
                """, usuario=usuario, prop_nombre=prop_base)
            
            result = session.execute_write(click_tx, usuario, nombre_propiedad)
            connector.close()
            
            return f"✅ Click registrado: {nombre_propiedad}\n\n💡 El sistema aprenderá de tus preferencias en 60 segundos"
    
    except Exception as e:
        connector.close()
        return f"❌ Error: {e}"

def procesar_consulta(pregunta: str, usuario: str, mostrar_detalles: bool = True):
    """
    Procesa consulta del usuario y retorna respuesta + explicación
    
    Args:
        pregunta: Pregunta en lenguaje natural
        usuario: Nombre del usuario actual
        mostrar_detalles: Si mostrar explicación técnica
    
    Returns:
        tuple: (respuesta, explicacion)
    """
    
    if not usuario or usuario.strip() == "":
        return "⚠️ Primero selecciona o crea un usuario arriba ⬆️", ""
    
    if not pregunta or pregunta.strip() == "":
        return "⚠️ Por favor ingresa una consulta", ""
    
    try:
        # Ejecutar flujo LangGraph con usuario
        resultado = ejecutar_consulta(pregunta, usuario=usuario)
        
        # Registrar la búsqueda en Neo4j (para que los demonios aprendan)
        connector = Neo4jConnector()
        try:
            with connector.get_session() as session:
                def register_search_tx(tx, usuario, pregunta):
                    tx.run("""
                        MATCH (u:User {name: $usuario})
                        CREATE (u)-[:SEARCHED {
                            query: $pregunta,
                            timestamp: datetime()
                        }]->(:SearchQuery {text: $pregunta})
                    """, usuario=usuario, pregunta=pregunta)
                
                session.execute_write(register_search_tx, usuario, pregunta)
        except:
            pass
        finally:
            connector.close()
        
        respuesta = resultado.get("respuesta", "❌ No se pudo procesar la consulta")
        explicacion = resultado.get("explicacion", "") if mostrar_detalles else ""
        
        # Agregar info del usuario a la explicación
        if explicacion and mostrar_detalles:
            explicacion = f"👤 **Usuario activo:** {usuario}\n\n" + explicacion
        
        return respuesta, explicacion
    
    except Exception as e:
        return f"❌ Error: {e}", f"Tipo de error: {type(e).__name__}"

def verificar_conexion():
    """Verifica estado de conexión a Neo4j"""
    connector = Neo4jConnector()
    
    if connector.is_connected():
        stats = connector.get_database_stats()
        connector.close()
        
        return (
            f"✅ **Conectado a Neo4j**\n\n"
            f"📊 **Estadísticas:**\n"
            f"• Propiedades: {stats.get('properties', 0)}\n"
            f"• Usuarios: {stats.get('users', 0)}\n"
            f"• Amenidades: {stats.get('amenities', 0)}\n"
            f"• Relaciones: {stats.get('relationships', 0)}\n"
        )
    else:
        return (
            f"❌ **No conectado a Neo4j**\n\n"
            f"💡 Asegúrate de que Neo4j esté ejecutándose en:\n"
            f"• URI: bolt://localhost:7687\n"
            f"• Usuario: neo4j\n"
            f"• Base de datos: housing\n"
        )

# === INTERFAZ GRADIO ===

with gr.Blocks(theme=gr.themes.Soft(), title="Sistema de Recomendación de Inmuebles") as demo:
    
    # Variable de estado para usuario actual
    usuario_state = gr.State(value=None)
    
    # HEADER
    gr.Markdown(
        """
        # 🏠 Sistema Inteligente de Recomendación de Inmuebles
        
        ### Consultas Personalizadas con IA que Aprende de Ti
        """
    )
    
    # === SECCIÓN DE USUARIO ===
    gr.Markdown("## 👤 Gestión de Usuario")
    gr.Markdown("*El sistema aprenderá tus preferencias personales basándose en tus búsquedas*")
    
    with gr.Row():
        with gr.Column(scale=1):
            gr.Markdown("### 🆕 Crear Nuevo Usuario")
            nombre_nuevo = gr.Textbox(
                label="Nombre",
                placeholder="Ej: Juan Pérez",
                scale=2
            )
            btn_crear = gr.Button("➕ Crear Usuario", variant="primary")
            
        with gr.Column(scale=1):
            gr.Markdown("### 📋 Seleccionar Usuario Existente")
            usuario_dropdown = gr.Dropdown(
                label="Usuarios disponibles",
                choices=obtener_usuarios(),
                interactive=True,
                scale=2
            )
            btn_seleccionar = gr.Button("✅ Seleccionar", variant="secondary")
    
    # Mensaje de estado del usuario
    estado_usuario = gr.Markdown("⚠️ **No hay usuario seleccionado.** Crea uno o selecciona uno existente.")
    
    gr.Markdown("---")
    
    # Mostrar estado de LangChain
    if LANGCHAIN_DISPONIBLE:
        gr.Markdown("✅ **🤖 IA Generativa ACTIVA** - LangChain + HuggingFace (Mistral-7B)")
        gr.Markdown("💡 Puedes hacer cualquier pregunta en lenguaje natural")
    else:
        gr.Markdown(
            """
            ⚠️ **LangChain en modo limitado**
            
            Para habilitar IA generativa:
            1. Obtén token gratis: https://huggingface.co/settings/tokens
            2. Crea archivo `.env` con: `HUGGINGFACEHUB_API_TOKEN=tu_token`
            3. Reinicia el sistema con `python main.py`
            """
        )
    
    # VERIFICACIÓN DE CONEXIÓN
    with gr.Accordion("🔌 Estado de Conexión", open=False):
        btn_verificar = gr.Button("Verificar conexión Neo4j")
        estado_conexion = gr.Markdown()
        
        btn_verificar.click(fn=verificar_conexion, outputs=estado_conexion)
    
    gr.Markdown("---")
    
    gr.Markdown("## 🔍 Búsqueda de Propiedades")
    
    # INPUT PRINCIPAL
    with gr.Row():
        pregunta = gr.Textbox(
            label="Tu consulta",
            placeholder="Ej: Busca departamentos de 2 ambientes por menos de $180,000",
            lines=3,
            scale=4
        )
    
    with gr.Row():
        mostrar_detalles = gr.Checkbox(
            label="Mostrar explicación técnica (Cypher, scores difusos, etc.)",
            value=True
        )
        btn_consultar = gr.Button("🔍 Buscar", variant="primary", scale=1)
    
    # OUTPUTS
    with gr.Row():
        with gr.Column(scale=1):
            respuesta = gr.Markdown(label="📋 Respuesta")
        
        with gr.Column(scale=1):
            explicacion = gr.Markdown(label="🔬 Explicación Técnica")
    
    # EJEMPLOS
    gr.Examples(
        examples=[
            ["¿Cuántas propiedades hay en total?", True],
            ["Busca casas en Ciudad de Mendoza", True],
            ["¿Hay departamentos por menos de 600000?", True],
            ["Propiedades con 3 habitaciones", False],
            ["¿Qué barrios tienen más propiedades?", True],
            ["Recomiéndame algo en Godoy Cruz", True],
        ],
        inputs=[pregunta, mostrar_detalles],
        label="💡 Ejemplos de consultas"
    )
    
    gr.Markdown("---")
    
    # === SECCIÓN DE CLICKS MANUALES ===
    gr.Markdown("## 👆 Registrar Interés en Propiedades")
    gr.Markdown("*Marca las propiedades que te interesan para que el sistema aprenda tus preferencias*")
    
    with gr.Row():
        nombre_propiedad_click = gr.Textbox(
            label="Nombre de la propiedad",
            placeholder="Ej: Propiedad #611 - Villa Nueva",
            info="Copia el nombre completo de una propiedad de los resultados arriba"
        )
        btn_registrar_click = gr.Button("⭐ Me interesa esta propiedad", variant="primary")
    
    resultado_click = gr.Markdown()
    
    # === EVENTOS ===
    
    # Crear usuario
    btn_crear.click(
        fn=crear_usuario,
        inputs=[nombre_nuevo],
        outputs=[estado_usuario, usuario_dropdown, usuario_state]
    )
    
    # Seleccionar usuario
    btn_seleccionar.click(
        fn=seleccionar_usuario,
        inputs=[usuario_dropdown],
        outputs=[estado_usuario, usuario_state]
    )
    
    # Consultar (usando el usuario actual)
    btn_consultar.click(
        fn=procesar_consulta,
        inputs=[pregunta, usuario_state, mostrar_detalles],
        outputs=[respuesta, explicacion]
    )
    
    pregunta.submit(  # También al presionar Enter
        fn=procesar_consulta,
        inputs=[pregunta, usuario_state, mostrar_detalles],
        outputs=[respuesta, explicacion]
    )
    
    # Registrar click en propiedad
    btn_registrar_click.click(
        fn=registrar_click_propiedad,
        inputs=[usuario_state, nombre_propiedad_click],
        outputs=[resultado_click]
    )
    
    # FOOTER
    gr.Markdown(
        """
        ---
        
        ### 🔧 Tecnologías
        
        - **Neo4j**: Base de datos de grafos para relaciones complejas
        - **LangChain**: Traducción lenguaje natural → Cypher
        - **HuggingFace**: Modelos de IA open-source (Mistral-7B)
        - **Lógica Difusa**: Evaluación de compatibilidad con scores 0.0-1.0
        - **Gradio**: Interfaz web interactiva
        
        ---
        
        📖 **Arquitectura basada en la guía de Sistema de Consultas Complejas**
        """
    )

# === LANZAMIENTO ===
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 LANZANDO INTERFAZ GRADIO")
    print("="*60)
    
    # Verificar conexión primero
    print(verificar_conexion())
    
    print("\n💡 La interfaz se abrirá en tu navegador automáticamente")
    print("💡 Si no se abre, ve a: http://localhost:7860")
    print("\n📌 Para compartir públicamente, usa: share=True en launch()")
    print("="*60 + "\n")
    
    demo.queue()  # Habilitar cola para mejor rendimiento
    demo.launch(
        server_name="127.0.0.1",  # Solo localhost (más seguro)
        server_port=7860,
        share=False,
        inbrowser=True,
        show_error=True
    )

