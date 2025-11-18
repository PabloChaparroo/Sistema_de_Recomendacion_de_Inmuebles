"""
Interfaz Gradio SIMPLIFICADA para Sistema de Recomendación de Inmuebles
Compatible con Python 3.14 (sin queue que causa crashes)
"""

import sys
import os

# Agregar directorio raíz al path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import gradio as gr
from workflow.langgraph_workflow import ejecutar_consulta, LANGCHAIN_DISPONIBLE
from database.neo4j_connector import Neo4jConnector

def procesar_consulta(pregunta: str, usuario_seleccionado: str, mostrar_detalles: bool = True):
    """Procesa consulta - USA LANGCHAIN DIRECTAMENTE con Ollama"""
    
    if not pregunta or pregunta.strip() == "":
        return "⚠️ Por favor ingresa una consulta", ""
    
    print(f"\n{'='*60}")
    print(f"🔍 PROCESANDO: {pregunta}")
    print(f"{'='*60}\n")
    
    try:
        # Usar el flujo completo que guarda preferencias en Neo4j
        print(f"👤 Usuario: {usuario_seleccionado}")
        print("⏳ Procesando consulta con IA y guardando preferencias...")
        
        resultado = ejecutar_consulta(pregunta, usuario=usuario_seleccionado)
        
        respuesta = resultado.get("respuesta", "No hay respuesta disponible")
        explicacion = resultado.get("explicacion", "")
        
        if mostrar_detalles:
            explicacion += f"\n\n👤 **Preferencias guardadas para:** {usuario_seleccionado}"
        
        print(f"✅ Respuesta generada exitosamente\n")
        return respuesta, explicacion
    
    except Exception as e:
        print(f"❌ EXCEPCIÓN: {e}\n")
        import traceback
        traceback.print_exc()
        return f"❌ **Error técnico:**\n\n{str(e)}\n\n💡 **Posibles causas:**\n• Ollama no está corriendo\n• Neo4j no está activo\n• Error de conexión", f"**Tipo de error:** `{type(e).__name__}`"

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
            f"💡 Asegúrate de que Neo4j esté ejecutándose"
        )

# === INTERFAZ GRADIO SIMPLIFICADA ===

with gr.Blocks(theme=gr.themes.Soft(), title="Sistema de Recomendación de Inmuebles") as demo:
    
    # HEADER
    gr.Markdown(
        """
        # 🏠 Sistema Inteligente de Recomendación de Inmuebles
        
        ### Consultas con IA + Lógica Difusa + Neo4j
        
        🎯 **Usuario activo:** Maria González (por defecto)
        """
    )
    
    if LANGCHAIN_DISPONIBLE:
        gr.Markdown("✅ **🤖 IA Generativa ACTIVA** - LangChain + Ollama (Mistral-7B)")
    else:
        gr.Markdown("⚠️ **LangChain en modo limitado**")
    
    # VERIFICACIÓN DE CONEXIÓN
    with gr.Accordion("🔌 Estado de Conexión", open=False):
        btn_verificar = gr.Button("Verificar conexión Neo4j")
        estado_conexion = gr.Markdown()
        btn_verificar.click(fn=verificar_conexion, outputs=estado_conexion)
    
    gr.Markdown("---")
    
    gr.Markdown("## 🔍 Búsqueda de Propiedades")
    
    # SELECTOR DE USUARIO
    usuario = gr.Dropdown(
        label="👤 Selecciona Usuario",
        choices=["Maria", "Juan", "Carlos"],
        value="Maria",
        interactive=True
    )
    
    # INPUT PRINCIPAL
    pregunta = gr.Textbox(
        label="Tu consulta",
        placeholder="Ej: ¿Cuántas propiedades hay en total?",
        lines=2
    )
    
    with gr.Row():
        mostrar_detalles = gr.Checkbox(
            label="Mostrar explicación técnica",
            value=True
        )
        btn_consultar = gr.Button("🔍 Buscar", variant="primary")
    
    # OUTPUTS
    with gr.Row():
        with gr.Column():
            respuesta = gr.Markdown(label="📋 Respuesta")
        
        with gr.Column():
            explicacion = gr.Markdown(label="🔬 Explicación Técnica")
    
    # EJEMPLOS
    gr.Examples(
        examples=[
            ["Maria", "¿Cuántas propiedades hay en total?", True],
            ["Juan", "Busca casas en Ciudad de Mendoza", True],
            ["Carlos", "¿Hay propiedades con más de 3 habitaciones y piscina?", True],
            ["Maria", "Necesito una casa en Godoy Cruz con 2 habitaciones, a un precio menor que 550000, me gusta caminar", True],
            ["Juan", "Propiedades con 3 habitaciones", False],
            ["Carlos", "¿Qué barrios tienen más propiedades?", True],
            ["Maria", "Recomiéndame algo en Godoy Cruz", True],
        ],
        inputs=[usuario, pregunta, mostrar_detalles],
        label="💡 Ejemplos de consultas"
    )
    
    # EVENTOS
    btn_consultar.click(
        fn=procesar_consulta,
        inputs=[pregunta, usuario, mostrar_detalles],
        outputs=[respuesta, explicacion]
    )
    
    pregunta.submit(
        fn=procesar_consulta,
        inputs=[pregunta, usuario, mostrar_detalles],
        outputs=[respuesta, explicacion]
    )
    
    # FOOTER
    gr.Markdown(
        """
        ---
        
        ### 🔧 Tecnologías
        
        - **Neo4j**: Base de datos de grafos
        - **LangChain**: Traducción lenguaje natural → Cypher
        - **Ollama**: LLM local (Mistral-7B)
        - **Lógica Difusa**: Evaluación de compatibilidad
        - **Gradio**: Interfaz web
        
        ---
        
        📖 **Versión simplificada compatible con Python 3.14**
        """
    )

# === LANZAMIENTO ===
if __name__ == "__main__":
    print("\n" + "="*60)
    print("🚀 LANZANDO INTERFAZ GRADIO SIMPLIFICADA")
    print("="*60)
    
    print(verificar_conexion())
    
    print("\n💡 La interfaz se abrirá en: http://localhost:7861")
    print("="*60 + "\n")
    
    # SIN queue() para evitar crashes en Python 3.14
    demo.launch(
        server_name="127.0.0.1",
        server_port=7861,
        share=False,
        inbrowser=True,
        show_error=True
    )
