# 🗺️ Sistema de Mapas de Proximidad - Guía Rápida

## 🚀 Inicio Rápido

### 1. Primera Vez (Generar Caché)

El sistema necesita pre-calcular coordenadas **UNA SOLA VEZ**:

```bash
# Opción A: Prueba rápida (50 propiedades - 1 minuto)
python generar_coordenadas_cache_rapido.py

# Opción B: Completo (1357 propiedades - 25 minutos)
python generar_coordenadas_cache.py
```

✅ **Importante**: Esto se hace solo una vez. El archivo `data/coordenadas_cache.json` se reutiliza siempre.

### 2. Usar el Sistema

```bash
python main.py
# Selecciona: 1 (Interfaz Gradio)
```

### 3. Hacer Búsquedas de Proximidad

Ejemplos de consultas que funcionan:

```
✅ "Quiero una propiedad cerca del Parque General San Martín"
✅ "Propiedades cercanas a Plaza Independencia"
✅ "Busca inmuebles a 3 km de la Universidad Nacional de Cuyo"
✅ "Algo cerca de Godoy Cruz"
✅ "Propiedades alrededor del Hospital Central"
```

## ⚡ Velocidad

### Antes (Sin Caché)
- ⏱️ **3-5 minutos** por búsqueda
- 🐌 Geocodifica cada propiedad en tiempo real
- 📡 Depende de API externa

### Después (Con Caché)
- ⚡ **< 1 segundo** por búsqueda
- 🚀 Lee coordenadas de archivo local
- 💾 Solo geocodifica el POI (1 llamada API)

## 📊 Ejemplo de Uso

```
Usuario: "Quiero una propiedad cerca del Parque General San Martín"

Sistema:
1. Detecta "cerca del" → Búsqueda de proximidad ✓
2. Extrae POI: "Parque General San Martín"
3. Geocodifica POI: (-32.8917, -68.8737) [0.5 seg]
4. Carga caché: 50 propiedades con coordenadas [0.1 seg]
5. Calcula distancias con Haversine [0.1 seg]
6. Filtra por radio de 5 km → 19 propiedades
7. Genera mapa con Folium [0.3 seg]
8. Abre en navegador automáticamente

Total: < 1 segundo ⚡
```

## 🗂️ Estructura de Archivos

```
data/
  coordenadas_cache.json       ← Caché de coordenadas pre-calculadas
  alquiler_inmuebles.csv        ← Datos originales

geocoding/
  geocoder.py                   ← Geocodificación + Haversine
  map_generator.py              ← Generación de mapas Folium
  
generar_coordenadas_cache.py   ← Script completo (1357 props)
generar_coordenadas_cache_rapido.py ← Script de prueba (50 props)
```

## 🔧 Mantenimiento

### Actualizar Coordenadas

Si agregas nuevas propiedades al CSV:

```bash
python generar_coordenadas_cache.py
```

Esto regenera el caché con todas las propiedades.

### Limpiar Caché

```bash
# Windows PowerShell
Remove-Item data\coordenadas_cache.json

# Luego regenerar
python generar_coordenadas_cache.py
```

## 🎯 POIs Disponibles en Mendoza

El sistema puede encontrar:

- **Parques**: Parque General San Martín, Parque del Bicentenario
- **Plazas**: Plaza Independencia, Plaza España, Plaza Italia
- **Universidades**: Universidad Nacional de Cuyo, UTN Mendoza
- **Hospitales**: Hospital Central, Hospital Lagomaggiore
- **Barrios**: Godoy Cruz, Maipú, Luján de Cuyo, Guaymallén
- **Landmarks**: Terminal de Ómnibus, Estadio Malvinas Argentinas

## 📈 Estadísticas

Con el caché de 50 propiedades (prueba):
- ✅ ~38 propiedades geocodificadas exitosamente (76%)
- ❌ ~12 propiedades con direcciones ambiguas (24%)
- ⚡ Búsquedas: < 1 segundo
- 💾 Tamaño caché: ~5 KB

Con el caché completo (1357 propiedades):
- ✅ ~1000+ propiedades geocodificadas (estimado 70-80%)
- ⚡ Búsquedas: < 1 segundo
- 💾 Tamaño caché: ~150 KB

## 🐛 Solución de Problemas

### "No hay caché de coordenadas disponible"

```bash
python generar_coordenadas_cache_rapido.py
```

### "No se pudo encontrar la ubicación: [POI]"

El nombre del POI debe ser específico:
- ❌ "Parque San Martín"
- ✅ "Parque General San Martín"
- ✅ "Parque General San Martín, Mendoza"

### Búsqueda muy lenta

Verifica que exista `data/coordenadas_cache.json`. Si no existe, el sistema intentará geocodificar en tiempo real (lento).

## 💡 Tips

1. **Primera vez**: Ejecuta `generar_coordenadas_cache_rapido.py` para probar (1 min)
2. **Producción**: Ejecuta `generar_coordenadas_cache.py` una vez (25 min)
3. **Búsquedas**: Usa nombres completos de POIs para mejor precisión
4. **Distancia**: El radio por defecto es 5 km, puedes especificar: "a 3 km de..."
