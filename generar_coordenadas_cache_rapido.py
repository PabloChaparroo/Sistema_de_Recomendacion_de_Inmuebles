"""
Versión RÁPIDA para pruebas - Solo geocodifica 50 propiedades
"""

import pandas as pd
import json
import time
from geocoding.geocoder import Geocoder

def generar_cache_rapido(num_propiedades=50):
    """Geocodifica solo las primeras N propiedades para pruebas rápidas"""
    
    print("="*60)
    print(f"🗺️  GENERANDO CACHÉ DE PRUEBA ({num_propiedades} propiedades)")
    print("="*60)
    
    # Cargar CSV
    print("\n📂 Cargando propiedades desde CSV...")
    df = pd.read_csv('data/alquiler_inmuebles.csv')
    df = df.head(num_propiedades)  # Solo primeras N
    print(f"✅ {len(df)} propiedades seleccionadas")
    
    geocoder = Geocoder()
    cache_coordenadas = {}
    
    exitosos = 0
    fallidos = 0
    
    print("\n🔄 Geocodificando propiedades...")
    print(f"⏱️  Tiempo estimado: {num_propiedades * 1.1 / 60:.1f} minutos")
    print("-"*60)
    
    for idx, row in df.iterrows():
        # Obtener mejor dirección disponible
        ubicacion = row.get('ubicacion') or row.get('direccion') or row.get('ciudad', 'Mendoza')
        
        print(f"[{idx+1}/{num_propiedades}] {ubicacion[:60]}...", end=" ")
        
        # Intentar geocodificar
        coords = geocoder.geocode_poi(ubicacion)
        
        if coords:
            cache_coordenadas[str(idx)] = {
                'ubicacion': ubicacion,
                'lat': coords[0],
                'lon': coords[1],
                'precio': float(row.get('alquiler', 0)) if pd.notna(row.get('alquiler')) else 0,
                'habitaciones': int(row.get('dormitorios', 0)) if pd.notna(row.get('dormitorios')) else 0,
                'ambientes': int(row.get('ambientes', 1)) if pd.notna(row.get('ambientes')) else 1,
                'tipo': 'Departamento' if row.get('ambientes', 1) < 4 else 'Casa'
            }
            print("✅")
            exitosos += 1
        else:
            print("❌")
            fallidos += 1
        
        # Respetar rate limit (1 req/seg)
        time.sleep(1.1)
    
    print("-"*60)
    print(f"\n✅ Geocodificación completada!")
    print(f"   - Exitosos: {exitosos}/{len(df)} ({(exitosos/len(df)*100):.1f}%)")
    print(f"   - Fallidos: {fallidos}/{len(df)} ({(fallidos/len(df)*100):.1f}%)")
    
    # Guardar en JSON
    cache_file = 'data/coordenadas_cache.json'
    print(f"\n💾 Guardando caché en: {cache_file}")
    
    with open(cache_file, 'w', encoding='utf-8') as f:
        json.dump(cache_coordenadas, f, indent=2, ensure_ascii=False)
    
    print(f"✅ Caché guardado exitosamente!")
    print(f"   - Archivo: {cache_file}")
    print(f"   - Tamaño: {len(cache_coordenadas)} propiedades geocodificadas")
    
    print("\n" + "="*60)
    print("🎉 CACHÉ DE PRUEBA COMPLETADO")
    print("="*60)
    print("\n💡 Ahora puedes probar búsquedas rápidas con:")
    print("   python test_parque_san_martin.py")
    print("\n⚡ Más adelante ejecuta el script completo:")
    print("   python generar_coordenadas_cache.py")
    
    return cache_coordenadas

if __name__ == "__main__":
    print("\n🚀 CACHÉ DE PRUEBA - RÁPIDO (50 propiedades)")
    print("   Tiempo estimado: ~1 minuto\n")
    
    try:
        generar_cache_rapido(50)
    except KeyboardInterrupt:
        print("\n\n⚠️  Proceso interrumpido por el usuario")
    except Exception as e:
        print(f"\n\n❌ ERROR: {e}")
        import traceback
        traceback.print_exc()
