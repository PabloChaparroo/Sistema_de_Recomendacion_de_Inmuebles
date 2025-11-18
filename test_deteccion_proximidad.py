"""
Test: Verificar que consultas normales NO se detecten como proximidad
"""

from ui.gradio_ui import buscar_propiedades_cercanas

def test_consultas_normales():
    """Verifica que consultas normales no se detecten como proximidad"""
    
    consultas_normales = [
        "Propiedades con 2 habitaciones",
        "¿Cuántas propiedades hay?",
        "Busca casas en Godoy Cruz",
        "Departamentos por menos de 500000",
        "Propiedades con piscina",
        "Casas con 3 dormitorios"
    ]
    
    print("="*60)
    print("TEST: Consultas normales NO deben detectarse como proximidad")
    print("="*60)
    
    for consulta in consultas_normales:
        resultado = buscar_propiedades_cercanas(consulta, "TestUser")
        
        if resultado:
            print(f"\n❌ FALSO POSITIVO: '{consulta}'")
            print(f"   Se detectó como búsqueda de proximidad")
        else:
            print(f"\n✅ OK: '{consulta}'")
            print(f"   No se detectó como proximidad (correcto)")

def test_consultas_proximidad():
    """Verifica que búsquedas de proximidad SÍ se detecten"""
    
    consultas_proximidad = [
        "Propiedades cerca del Parque General San Martín",
        "Cercanas a Plaza Independencia",
        "A 3 km de la Universidad",
        "Alrededor de Godoy Cruz",
        "En proximidad del Hospital Central"
    ]
    
    print("\n\n" + "="*60)
    print("TEST: Búsquedas de proximidad SÍ deben detectarse")
    print("="*60)
    
    for consulta in consultas_proximidad:
        resultado = buscar_propiedades_cercanas(consulta, "TestUser")
        
        if resultado:
            print(f"\n✅ OK: '{consulta}'")
            print(f"   Se detectó como proximidad (correcto)")
        else:
            print(f"\n❌ FALSO NEGATIVO: '{consulta}'")
            print(f"   NO se detectó como proximidad")

if __name__ == "__main__":
    print("\n🧪 PRUEBA DE DETECCIÓN DE BÚSQUEDAS\n")
    
    test_consultas_normales()
    test_consultas_proximidad()
    
    print("\n\n" + "="*60)
    print("✅ PRUEBAS COMPLETADAS")
    print("="*60)
