"""
Script para pre-calcular coordenadas de todas las propiedades
Se ejecuta UNA SOLA VEZ y guarda resultados en JSON
"""

import pandas as pd
import json
import time
from geocoding.geocoder import Geocoder

def generar_cache_coordenadas():
    """Geocodifica todas las propiedades y guarda en cache JSON"""
    
    print("="*60)
    print("🗺️  GENERANDO CACHÉ DE COORDENADAS")
    print("="*60)
    
    # Cargar CSV
    print("\n📂 Cargando propiedades desde CSV...")
    df = pd.read_csv('data/alquiler_inmuebles.csv')
    print(f"✅ {len(df)} propiedades encontradas")
    
    geocoder = Geocoder()
    cache_coordenadas = {}
    
    exitosos = 0
    fallidos = 0
    
    print("\n🔄 Geocodificando propiedades...")
    print("⏱️  Esto tomará varios minutos (1 request/segundo para respetar límites API)")
    print("-"*60)
    
    for idx, row in df.iterrows():
        # Obtener mejor dirección disponible
        ubicacion = row.get('ubicacion') or row.get('direccion') or row.get('ciudad', 'Mendoza')
        
        # Mostrar progreso cada 10 propiedades
        if idx % 10 == 0:
            print(f"Progreso: {idx}/{len(df)} ({(idx/len(df)*100):.1f}%) - ✅ {exitosos} | ❌ {fallidos}")
        
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
            exitosos += 1
        else:
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
    print("🎉 PROCESO COMPLETADO")
    print("="*60)
    print("\n💡 Ahora las búsquedas de proximidad serán INSTANTÁNEAS")
    print("   - No más esperas de 3-5 minutos")
    print("   - Los mapas se generarán en menos de 1 segundo")
    
    return cache_coordenadas

if __name__ == "__main__":
    print("\n⚠️  ADVERTENCIA: Este script tomará 20-30 minutos")
    print("   (respetamos el límite de 1 request/segundo de Nominatim)")
    print("\n💡 Puedes interrumpir con Ctrl+C en cualquier momento")
    print("   y volver a ejecutar - el caché de geocoder evita re-consultas")
    
    respuesta = input("\n¿Continuar? (s/n): ")
    
    if respuesta.lower() == 's':
        try:
            generar_cache_coordenadas()
        except KeyboardInterrupt:
            print("\n\n⚠️  Proceso interrumpido por el usuario")
            print("💡 Puedes volver a ejecutar para continuar donde quedó")
        except Exception as e:
            print(f"\n\n❌ ERROR: {e}")
            import traceback
            traceback.print_exc()
    else:
        print("\n❌ Proceso cancelado")
