# 🏠 Sistema Inteligente de Recomendación de Inmuebles con IA

**Proyecto Integrador - Inteligencia Artificial**  
**Universidad Tecnológica Nacional**

---

## 🎯 Descripción General

Sistema avanzado de búsqueda y recomendación de propiedades inmobiliarias que integra múltiples tecnologías de IA:

### Componentes Principales

1. **Procesamiento de Lenguaje Natural (NLP)**
   - Ollama (Mistral 7B) + LangChain
   - Traduce consultas en español a Cypher automáticamente
   - Respuestas contextualizadas y comprensibles

2. **Base de Datos de Grafos**
   - Neo4j para modelar propiedades, usuarios, amenidades y relaciones
   - Consultas Cypher optimizadas
   - Visualización de relaciones complejas

3. **Lógica Difusa (Fuzzy Logic)**
   - Evaluación de compatibilidad (scores 0.0-1.0)
   - Factores: precio (30%), habitaciones (20%), amenidades (50%)
   - Sistema de ranking inteligente

4. **Aprendizaje Automático Adaptativo**
   - 5 demonios IA que aprenden continuamente:
     - **PreferenceLearningDemon**: Aprende preferencias de usuarios (cada 60s)
     - **AdaptivePricingDemon**: Predice tendencias de precios (cada 300s)
     - **TemporalTrendsDemon**: Detecta patrones temporales (cada 180s)
     - **PatternDiscoveryDemon**: Descubre correlaciones (cada 240s)
     - **RecommendationOptimizerDemon**: Optimiza recomendaciones (cada 120s)

5. **Modelos Predictivos**
   - Frames de propiedades y usuarios
   - Sistema de inferencia basado en características
   - Predicción de compatibilidad

---

## 🛠️ Arquitectura del Sistema

```
Usuario (Lenguaje Natural)
    ↓
LangChain + Ollama (Mistral 7B)
    ↓
Generación de Cypher
    ↓
Neo4j (Grafo de Propiedades)
    ↓
Lógica Difusa (Scoring)
    ↓
Demonios IA (Aprendizaje)
    ↓
Respuesta Personalizada
```

---

## 🚀 Tecnologías Utilizadas

### LLM y NLP
- **Ollama**: Ejecución local de Mistral 7B (4GB)
- **LangChain**: Framework de orquestación
- **langchain-ollama**: Integración específica

### Base de Datos
- **Neo4j 6.0+**: Base de datos de grafos
- **Cypher**: Lenguaje de consulta

### Inteligencia Artificial
- **Lógica Difusa**: Evaluación de compatibilidad
- **Demonios Adaptativos**: Aprendizaje continuo
- **Frames**: Representación del conocimiento

### Interfaz
- **Gradio**: Interfaz web interactiva
- **Python 3.10+**: Backend del sistema
- **CLI**: Línea de comandos

---

## 📋 Requisitos Previos

### Software
1. **Python 3.10+**: https://www.python.org/downloads/
2. **Neo4j Desktop**: https://neo4j.com/download/
3. **Ollama**: https://ollama.com/download

### Hardware Mínimo
- **RAM**: 12 GB (16 GB recomendado)
- **Disco**: 10 GB libres
- **CPU**: 4 cores mínimo

---

## 🔧 Instalación Completa

### 1. Clonar repositorio
```bash
git clone https://github.com/PabloChaparroo/Sistema_de_Recomendacion_de_Inmuebles.git
cd Sistema_de_Recomendacion_de_Inmuebles
```

### 2. Configurar entorno virtual
```bash
python -m venv venv
.\venv\Scripts\Activate.ps1  # Windows PowerShell
# o
source venv/bin/activate  # Linux/Mac
```

### 3. Instalar dependencias
```bash
pip install -r requirements.txt
```

### 4. Configurar Neo4j
1. Abrir Neo4j Desktop
2. Crear base de datos llamada **"housing"**
3. Iniciar la base de datos
4. Credenciales predeterminadas: `neo4j` / `password`

### 5. Configurar variables de entorno
Crear archivo `.env` en la raíz:
```env
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=housing
```

### 6. Instalar y configurar Ollama
```bash
# Descargar Ollama desde https://ollama.com/download

# Iniciar servidor
ollama serve

# En otra terminal, descargar Mistral
ollama pull mistral
```

### 7. Cargar datos de ejemplo
```bash
python load_sample_data.py
```

---

## 📊 Preparación de la Base de Datos

### Verificar conexión
```bash
python check_neo4j.py
```

### Datos incluidos
- **8 propiedades** en Mendoza (Godoy Cruz, Guaymallén, Las Heras)
- **6 amenidades** (Parque, Gimnasio, Piscina, Seguridad, Cochera, Parrilla)
- **3 usuarios** de ejemplo
- Relaciones: HAS_AMENITY, VISITED, PREFERS_AMENITY

---

## 🎮 Uso del Sistema

### Opción 1: Interfaz Principal (Recomendada)
```bash
python main.py
```

Menú interactivo con:
- Interfaz web Gradio
- Consultas CLI rápidas
- Estadísticas del sistema
- Demonios IA activos automáticamente

### Opción 2: Solo Ollama + Neo4j (Testing)
```bash
python test_ollama.py
```

Ejecuta 3 pruebas predefinidas:
1. Contar propiedades totales
2. Filtrar por ciudad
3. Listar amenidades

### Opción 3: Python Interactivo
```python
from workflow.langchain_integration import ask_question

resultado = ask_question("¿Cuántas propiedades hay en Mendoza?")
print(resultado['answer'])
print(resultado['cypher'])
```

### Opción 4: Interfaz Web (Gradio)
```bash
python -c "from ui.gradio_ui import demo; demo.launch()"
```

---

## 📂 Estructura del Proyecto

```
Sistema_de_Recomendacion_de_Inmuebles/
│
├── data/
│   └── alquiler_inmuebles.csv         # Dataset original
│
├── database/
│   └── neo4j_connector.py             # Conexión a Neo4j
│
├── demons/                            # Aprendizaje automático
│   ├── demons_manager.py              # Gestor de demonios
│   ├── preference_learning_demon.py   # Aprende preferencias
│   ├── recommendation_optimizer_demon.py
│   ├── temporal_trends_demon.py
│   ├── pattern_discovery_demon.py
│   └── compact_demons.py
│
├── fuzzy/                             # Lógica difusa
│   ├── fuzzy_logic.py                 # Motor de lógica difusa
│   ├── fuzzy_evaluators.py           # Evaluadores de propiedades
│   └── transport_evaluation.py
│
├── models/                            # Representación del conocimiento
│   ├── frame_models.py               # Frames base
│   └── housing_frames.py             # Frames de propiedades
│
├── workflow/                          # Flujo principal
│   ├── langchain_integration.py      # Ollama + Neo4j
│   └── langgraph_workflow.py         # Orquestación completa
│
├── ui/
│   └── gradio_ui.py                  # Interfaz web
│
├── main.py                           # Punto de entrada principal
├── test_ollama.py                    # Script de pruebas
├── load_sample_data.py               # Carga de datos
├── check_neo4j.py                    # Verificación de BD
├── requirements.txt                  # Dependencias
├── .env                              # Configuración (crear)
└── README.md                         # Este archivo
```

---

## 💬 Ejemplos de Consultas

### Consultas Simples
```
¿Cuántas propiedades hay en total?
¿Cuántas propiedades hay en Mendoza?
Lista las amenidades disponibles
```

### Búsquedas Filtradas
```
Busca casas en Godoy Cruz
Departamentos por menos de $150,000
Propiedades con 3 habitaciones
Propiedades con piscina y gimnasio
```

### Consultas de Recomendación
```
Recomiéndame una propiedad en Guaymallén
¿Cuál es la mejor opción con mi presupuesto de $180,000?
Sugiere propiedades para una familia de 4 personas
```

---

## 🔍 Cómo Funciona

### 1. Entrada del Usuario
Usuario ingresa pregunta en español por CLI, Gradio o código Python.

### 2. Procesamiento con Ollama
```python
# LangChain envía pregunta + esquema Neo4j a Ollama
llm = OllamaLLM(model="mistral", temperature=0.1)
chain = GraphCypherQAChain.from_llm(llm=llm, graph=graph)
```

### 3. Generación de Cypher
Ollama genera consulta Cypher automáticamente:
```cypher
MATCH (p:Property {city: 'Mendoza'})
RETURN count(p) as total
```

### 4. Ejecución en Neo4j
Neo4j ejecuta el Cypher y retorna resultados estructurados.

### 5. Evaluación con Lógica Difusa
```python
score = calcular_score_propiedad(propiedad, usuario)
# Score basado en: precio, habitaciones, amenidades
```

### 6. Aprendizaje Continuo
Los 5 demonios IA analizan:
- Clicks del usuario
- Búsquedas realizadas
- Propiedades visitadas
- Patrones temporales
- Correlaciones entre amenidades

### 7. Respuesta Personalizada
Sistema retorna:
- Respuesta en lenguaje natural
- Lista de propiedades rankeadas
- Scores de compatibilidad
- Explicación técnica (opcional)

---

## 📸 Guía de Capturas

Ver archivo **GUIA_CAPTURAS.md** para instrucciones detalladas de screenshots requeridos para el informe.

---

## 🐛 Troubleshooting

### Error: "Cannot connect to Ollama"
```bash
# Solución: Iniciar servidor Ollama
ollama serve
```

### Error: "Model not found"
```bash
# Solución: Descargar modelo Mistral
ollama pull mistral
```

### Error: "Connection refused to Neo4j"
1. Abrir Neo4j Desktop
2. Verificar que base "housing" esté activa
3. Comprobar puerto 7687 en `.env`

### Consulta lenta la primera vez
- **Normal**: Primera consulta a Ollama carga modelo en RAM (15-30s)
- Consultas subsecuentes: 2-4 segundos

### Lógica difusa no aplica scores
- Verificar que `models/housing_frames.py` esté presente
- Comprobar que propiedades tengan atributos necesarios

---

## 📚 Documentación Adicional

- **INFORME_PG6_COMPLETO.md**: Informe académico detallado
- **GUIA_CAPTURAS.md**: Instrucciones para screenshots
- **requirements.txt**: Lista completa de dependencias

---

## 👥 Autores

**Grupo N - UTN FRM**
- [Agregar nombres de integrantes]

---

## 📄 Licencia

Proyecto académico - Universidad Tecnológica Nacional

---

## 🔗 Referencias

- Ollama: https://ollama.com/
- Neo4j: https://neo4j.com/
- LangChain: https://python.langchain.com/
- Mistral 7B: https://mistral.ai/

---

## 🆘 Soporte

Para problemas o consultas:
1. Revisar esta documentación
2. Consultar GUIA_CAPTURAS.md
3. Verificar logs en la terminal
4. Comprobar estado de Neo4j y Ollama

---

**Última actualización**: Noviembre 2025
