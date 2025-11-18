"""
Test específico: Búsqueda cerca del Parque General San Martín
"""

from ui.gradio_ui import buscar_propiedades_cercanas

def test_parque_san_martin():
    """Test con nombre completo del parque"""
    print("="*60)
    print("TEST: Propiedades cerca del Parque General San Martín")
    print("="*60)
    
    usuario = "TestUser"
    pregunta = "Quiero una propiedad cerca del Parque General San Martín"
    
    print(f"\n📝 Consulta: {pregunta}")
    print(f"👤 Usuario: {usuario}\n")
    
    resultado = buscar_propiedades_cercanas(pregunta, usuario)
    
    if resultado:
        respuesta, info_tecnica = resultado
        print("RESPUESTA:")
        print(respuesta)
        print("\n" + "="*60)
        print("INFO TÉCNICA:")
        print(info_tecnica)
    else:
        print("❌ No se detectó como búsqueda de proximidad")

if __name__ == "__main__":
    print("\n🧪 PRUEBA DE MAPA CON PARQUE GENERAL SAN MARTÍN\n")
    
    try:
        test_parque_san_martin()
        
        print("\n\n" + "="*60)
        print("✅ PRUEBA COMPLETADA")
        print("="*60)
        print("\n💡 Si funcionó:")
        print("   - El mapa se abrió en tu navegador")
        print("   - Deberías ver propiedades marcadas cerca del parque")
        print("   - Archivo: mapa_propiedades_cercanas.html")
        
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
