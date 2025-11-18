"""
Test: consulta de habitaciones en Gradio
"""

from ui.gradio_ui import procesar_consulta

consultas_test = [
    'Propiedades con 3 habitaciones',
    'Propiedades con 2 dormitorios',
    '¿Cuántas propiedades hay?'
]

for consulta in consultas_test:
    print("\n" + "="*60)
    print(f"TEST: {consulta}")
    print("="*60)
    
    respuesta, explicacion = procesar_consulta(consulta, 'TestUser', mostrar_detalles=True)
    
    print("\n📋 RESPUESTA:")
    print(respuesta[:400])
    
    if explicacion:
        print("\n🔬 EXPLICACIÓN:")
        print(explicacion[:500])
