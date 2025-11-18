"""
Sistema simplificado de geocodificación con extracción de direcciones
"""
import re
import webbrowser
import os

def extraer_direccion_de_descripcion(descripcion, ubicacion="", ciudad=""):
    """
    Extrae direcciones de la descripción o usa ubicacion directamente
    
    Args:
        descripcion: Texto de descripción de la propiedad
        ubicacion: Campo ubicación del CSV (ej: "Garibaldi 100, Ciudad de Mendoza")
        ciudad: Ciudad de la propiedad
        
    Returns:
        Mejor dirección encontrada
    """
    # 1. Si ubicacion tiene info específica, usarla
    if ubicacion and ubicacion not in ["Mendoza", "Capital", "N/A"]:
        # Limpiar caracteres extraños
        direccion = ubicacion.split(',')[0].strip()
        if len(direccion) > 5:  # Direcciones reales tienen más de 5 caracteres
            return f"{direccion}, {ciudad}, Mendoza, Argentina"
    
    # 2. Buscar patrones de dirección en descripción
    if descripcion:
        # Patrones: "calle X", "en calle X", "ubicado en X", etc.
        patrones = [
            r'(?:ubicado|situada?|encuentra)\s+(?:en\s+)?(?:la\s+)?calle\s+([A-Z][A-Za-záéíóúñÑ\s]+(?:\d+)?)',
            r'calle\s+([A-Z][A-Za-záéíóúñÑ]+\s*\d+)',
            r'(?:en|sobre)\s+(?:calle\s+)?([A-Z][A-Za-záéíóúñÑ]+\s+(?:y|esquina)\s+[A-Z][A-Za-záéíóúñÑ]+)',
        ]
        
        for patron in patrones:
            match = re.search(patron, descripcion, re.IGNORECASE)
            if match:
                direccion_extraida = match.group(1).strip()
                return f"{direccion_extraida}, {ciudad}, Mendoza, Argentina"
    
    # 3. Fallback: usar solo ciudad
    return f"{ciudad}, Mendoza, Argentina"


def generar_mapa_con_propiedades(propiedades, poi_name="Punto de Interés"):
    """
    Genera un mapa HTML simple con las propiedades
    Versión simplificada sin geocodificación (usa datos que ya existen)
    """
    # Por ahora retornar path del mapa existente
    mapa_path = os.path.abspath("mapa_propiedades_cercanas.html")
    
    if os.path.exists(mapa_path):
        # Abrir en navegador
        webbrowser.open('file:///' + mapa_path.replace('\\', '/'))
        return mapa_path
    
    return None


if __name__ == "__main__":
    # Test
    desc = "Re/max ofrece en alquiler departamento ubicado en calle Garibaldi 142, pleno centro"
    ubicacion = "Garibaldi 100, Ciudad de Mendoza, Mendoza"
    
    direccion = extraer_direccion_de_descripcion(desc, ubicacion, "Capital")
    print(f"Dirección extraída: {direccion}")
