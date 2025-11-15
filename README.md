# Sistema de Recomendación de Inmuebles con Ollama + Neo4j

**Proyecto Integrador - Unidad 4 - Inteligencia Artificial**  
**Universidad Tecnológica Nacional**

---

## 🎯 Descripción

Asistente inteligente que utiliza **Ollama (Mistral 7B)** para interpretar consultas en lenguaje natural sobre propiedades inmobiliarias almacenadas en **Neo4j**, generando automáticamente consultas Cypher y presentando respuestas comprensibles.

---

## 🚀 Tecnologías Utilizadas

- **Ollama**: Ejecución local del modelo Mistral 7B
- **Neo4j**: Base de datos de grafos para información inmobiliaria
- **LangChain**: Orquestación entre Ollama y Neo4j
- **Python 3.10+**: Lenguaje de implementación
- **Gradio** (opcional): Interfaz web para demostraciones

---

## 📋 Requisitos Previos

### Software necesario:
1. **Python 3.10 o superior**
2. **Neo4j Desktop** (https://neo4j.com/download/)
3. **Ollama** (https://ollama.com/download)

### Requisitos de hardware:
- **RAM**: 12 GB mínimo (16 GB recomendado)
- **Disco**: 10 GB libres
- **CPU**: 4 cores mínimo

---

## 🔧 Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/PabloChaparroo/Sistema_de_Recomendacion_de_Inmuebles.git
cd Sistema_de_Recomendacion_de_Inmuebles
```

### 2. Crear entorno virtual
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar variables de entorno
Edita el archivo `.env` con tus credenciales de Neo4j:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=tu_password
NEO4J_DATABASE=housing
```

### 5. Instalar Ollama y descargar modelo
```bash
# Descargar Ollama desde: https://ollama.com/download
# Luego ejecutar:
ollama pull mistral
```

---

## 📊 Preparación de la Base de Datos

### 1. Iniciar Neo4j Desktop
- Crear una base de datos llamada `housing`
- Iniciarla (botón verde "Start")

### 2. Cargar datos de ejemplo
```bash
python load_sample_data.py
```

Esto cargará:
- 8 propiedades
- 6 amenidades
- 3 usuarios
- Relaciones entre ellos

### 3. Verificar la carga
```bash
python check_neo4j.py
```

---

## 🎮 Uso del Sistema

### Opción 1: Pruebas automáticas (recomendado para informe)
```bash
python test_ollama.py
```

Ejecuta 3 consultas de prueba:
1. ¿Cuántas propiedades hay en total?
2. ¿Cuántas propiedades hay en Mendoza?
3. Lista las amenidades disponibles

### Opción 2: Interfaz web con Gradio
```bash
python ui/gradio_ui.py
```

Abre tu navegador en: http://localhost:7860

### Opción 3: Python interactivo
```bash
python
>>> from workflow.langchain_integration import ask_question
>>> resultado = ask_question("¿Hay propiedades con piscina?")
>>> print(resultado['answer'])
```

---

## 📁 Estructura del Proyecto

```
Sistema_de_Recomendacion_de_Inmuebles/
├── workflow/
│   └── langchain_integration.py    # Integración Ollama + Neo4j
├── database/
│   └── neo4j_connector.py          # Conector a Neo4j
├── ui/
│   └── gradio_ui.py                # Interfaz web (opcional)
├── data/
│   └── alquiler_inmuebles.csv      # Dataset original
├── test_ollama.py                  # Script de pruebas
├── load_sample_data.py             # Carga de datos de ejemplo
├── check_neo4j.py                  # Verificación de BD
├── requirements.txt                # Dependencias Python
├── .env                            # Variables de entorno
├── GUIA_CAPTURAS.md                # Guía para capturas del informe
└── README.md                       # Este archivo
```

---

## 🧪 Ejemplos de Consultas

El sistema puede responder preguntas como:

- "¿Cuántas propiedades hay en total?"
- "Lista las propiedades en Mendoza"
- "¿Qué amenidades están disponibles?"
- "¿Hay propiedades con gimnasio?"
- "Muestra las 5 propiedades más baratas"
- "¿Cuántos usuarios hay registrados?"

---

## 🔍 Cómo Funciona

```
Usuario → Pregunta en español
    ↓
LangChain → Envía contexto a Ollama
    ↓
Ollama (Mistral) → Genera consulta Cypher
    ↓
Neo4j → Ejecuta la consulta
    ↓
Ollama → Traduce resultado a español
    ↓
Usuario ← Recibe respuesta clara
```

---

## 📸 Capturas para el Informe

Consulta [`GUIA_CAPTURAS.md`](GUIA_CAPTURAS.md ) para instrucciones detalladas sobre qué capturas tomar y dónde ubicarlas en el informe PG6.

---

## 🐛 Solución de Problemas

### Error: "Could not connect to Neo4j"
**Solución:** Verifica que Neo4j Desktop esté iniciado y que las credenciales en `.env` sean correctas.

### Error: "Connection refused localhost:11434"
**Solución:** Ollama no está corriendo. Ejecuta:
```bash
ollama serve
```

### Error: "Model not found"
**Solución:** Descarga el modelo:
```bash
ollama pull mistral
```

### Respuestas lentas (>10 segundos)
**Solución:** Primera consulta siempre es lenta (carga del modelo). Las siguientes serán más rápidas.

---

## 📝 Documentación Adicional

- **Informe completo:** Ver `INFORME_PG6_COMPLETO.md`
- **Guía de capturas:** Ver [`GUIA_CAPTURAS.md`](GUIA_CAPTURAS.md )

---

## 👥 Autores

**Grupo N** - Proyecto Integrador 2025  
Universidad Tecnológica Nacional - Facultad Regional Mendoza

---

## 📄 Licencia

Este proyecto fue desarrollado con fines académicos para la materia Inteligencia Artificial.

---

## 🔗 Referencias

- [Documentación de Ollama](https://ollama.com/docs)
- [LangChain Docs](https://python.langchain.com/docs/get_started/introduction)
- [Neo4j Cypher Manual](https://neo4j.com/docs/cypher-manual/current/)
- [Mistral AI](https://mistral.ai/)

---

**¿Necesitas ayuda?** Revisa [`GUIA_CAPTURAS.md`](GUIA_CAPTURAS.md ) o ejecuta `python check_neo4j.py` para diagnosticar problemas.
