"""
Test de integración del sistema de mapas con Gradio
Verifica que todo funcione antes de lanzar la interfaz completa
"""

from ui.gradio_ui import buscar_propiedades_cercanas, procesar_consulta

def test_proximidad_directa():
    """Test directo de la función de búsqueda de proximidad"""
    print("="*60)
    print("TEST 1: Búsqueda directa de proximidad")
    print("="*60)
    
    usuario = "TestUser"
    pregunta = "Quiero una propiedad cerca del Parque San Martín"
    
    print(f"\n📝 Consulta: {pregunta}")
    print(f"👤 Usuario: {usuario}\n")
    
    resultado = buscar_propiedades_cercanas(pregunta, usuario)
    
    if resultado:
        respuesta, info_tecnica = resultado
        print("✅ Búsqueda de proximidad detectada\n")
        print("RESPUESTA:")
        print(respuesta)
        print("\n" + "="*60)
        print("INFO TÉCNICA:")
        print(info_tecnica)
    else:
        print("❌ No se detectó como búsqueda de proximidad")

def test_procesar_consulta_con_mapa():
    """Test del flujo completo a través de procesar_consulta()"""
    print("\n\n" + "="*60)
    print("TEST 2: Flujo completo con procesar_consulta()")
    print("="*60)
    
    usuario = "TestUser"
    pregunta = "Propiedades cercanas a Plaza Independencia"
    
    print(f"\n📝 Consulta: {pregunta}")
    print(f"👤 Usuario: {usuario}\n")
    
    respuesta, explicacion = procesar_consulta(pregunta, usuario, mostrar_detalles=True)
    
    print("RESPUESTA:")
    print(respuesta)
    print("\n" + "="*60)
    print("EXPLICACIÓN:")
    print(explicacion)

def test_consulta_normal():
    """Test de que las consultas normales siguen funcionando"""
    print("\n\n" + "="*60)
    print("TEST 3: Consulta normal (sin mapa)")
    print("="*60)
    
    usuario = "TestUser"
    pregunta = "¿Cuántas propiedades hay en total?"
    
    print(f"\n📝 Consulta: {pregunta}")
    print(f"👤 Usuario: {usuario}\n")
    
    respuesta, explicacion = procesar_consulta(pregunta, usuario, mostrar_detalles=False)
    
    print("RESPUESTA:")
    print(respuesta)
    
    if explicacion:
        print("\nEXPLICACIÓN:")
        print(explicacion)

if __name__ == "__main__":
    print("\n🧪 PRUEBAS DE INTEGRACIÓN - SISTEMA DE MAPAS\n")
    
    try:
        # Test 1: Búsqueda directa
        test_proximidad_directa()
        
        # Test 2: Flujo completo
        test_procesar_consulta_con_mapa()
        
        # Test 3: Consulta normal
        test_consulta_normal()
        
        print("\n\n" + "="*60)
        print("✅ TODAS LAS PRUEBAS COMPLETADAS")
        print("="*60)
        print("\n💡 Si los mapas se generaron correctamente:")
        print("   - Se abrieron automáticamente en tu navegador")
        print("   - Archivo guardado: mapa_propiedades_cercanas.html")
        print("\n🚀 Ahora puedes ejecutar: python main.py")
        
    except Exception as e:
        print(f"\n\n❌ ERROR EN LAS PRUEBAS: {e}")
        import traceback
        traceback.print_exc()
