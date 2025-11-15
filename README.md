# Sistema de Recomendación de Inmuebles con IA

Sistema inteligente de recomendación de propiedades que combina:
- **Neo4j**: Base de datos de grafos
- **Lógica Difusa**: Evaluación de compatibilidad
- **LangChain + HuggingFace**: IA Generativa
- **Gradio**: Interfaz web interactiva
- **Demonios de Aprendizaje**: Sistema que aprende automáticamente de las interacciones

## 📋 Requisitos Previos

- Python 3.10 o superior
- Neo4j Desktop
- Cuenta de HuggingFace (gratuita)

## 🚀 Instalación

### 1. Clonar el Repositorio

```bash
git clone https://github.com/PabloChaparroo/Sistema_de_Recomendacion_de_Inmuebles.git
cd Sistema_de_Recomendacion_de_Inmuebles
```

### 2. Crear Entorno Virtual

```bash
py -m venv venv
.\venv\Scripts\activate
```

### 3. Instalar Dependencias

```bash
pip install -r requirements.txt
```

### 4. Configurar Neo4j Desktop

#### Paso 1: Abrir Neo4j Desktop
1. Abre la aplicación Neo4j Desktop
2. Espera a que cargue completamente

#### Paso 2: Crear un Proyecto
1. En "Projects" (lado izquierdo), haz clic en **"New"** o **"+ New Project"**
2. Nombre del proyecto: **"Sistema_Recomendacion_Inmuebles"**

#### Paso 3: Crear la Base de Datos
1. Dentro del proyecto, haz clic en **"Add"** → **"Local DBMS"**
2. Configuración:
   - **Name:** `housing`
   - **Password:** `password` (o la que prefieras, anótala)
   - **Version:** Última versión estable (5.x)
3. Haz clic en **"Create"**

#### Paso 4: Instalar Plugin APOC
1. Haz clic en la base de datos `housing`
2. Pestaña **"Plugins"** (derecha)
3. Busca **"APOC"** y haz clic en **"Install"**
4. Espera a que termine

#### Paso 5: Iniciar la Base de Datos
1. Haz clic en **"Start"** (▶️)
2. Espera hasta que el estado sea **"Active"** (punto verde)

#### Paso 6: Verificar Conexión
1. Haz clic en **"Open"** → **"Neo4j Browser"**
2. En el prompt, escribe: `:server status`
3. Deberías ver la conexión activa

### 5. Configurar Variables de Entorno

El archivo `.env` ya está configurado con:

```env
# HuggingFace API Token
HUGGINGFACEHUB_API_TOKEN=tu_token_aqui

# Neo4j Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USER=neo4j
NEO4J_PASSWORD=password
NEO4J_DATABASE=housing
```

**Importante:** Si cambiaste la contraseña en Neo4j Desktop, actualiza `NEO4J_PASSWORD` en el archivo `.env`

## 🎮 Uso

### Iniciar el Sistema

```bash
py main.py
```

### Opciones del Menú

1. **Interfaz Web (Gradio)** - Recomendado
   - Abre automáticamente en el navegador
   - Interfaz amigable para consultas
   - Muestra recomendaciones con scores

2. **Consulta Rápida (CLI)**
   - Consultas desde la terminal
   - Respuestas inmediatas

3. **Ver Estadísticas**
   - Estado de la base de datos
   - Preferencias aprendidas
   - Métricas del sistema

4. **Salir**

## 📊 Estructura del Proyecto

```
Sistema_de_Recomendacion_de_Inmuebles/
├── data/                    # Datos CSV de propiedades
├── database/               # Conector Neo4j
│   └── neo4j_connector.py
├── demons/                 # Demonios de aprendizaje automático
│   ├── demons_manager.py
│   ├── preference_learning_demon.py
│   ├── pattern_discovery_demon.py
│   └── ...
├── fuzzy/                  # Lógica difusa para evaluación
│   ├── fuzzy_logic.py
│   └── fuzzy_evaluators.py
├── models/                 # Modelos de frames
│   ├── frame_models.py
│   └── housing_frames.py
├── ui/                     # Interfaz Gradio
│   └── gradio_ui.py
├── workflow/               # LangGraph workflow
│   ├── langgraph_workflow.py
│   └── langchain_integration.py
├── main.py                 # Punto de entrada
├── requirements.txt        # Dependencias
└── .env                    # Variables de entorno
```

## 🧠 Características Principales

### Sistema de Aprendizaje Automático
El sistema incluye **demonios de IA** que aprenden continuamente:

- **PreferenceLearningDemon**: Aprende preferencias de usuarios (cada 60s)
- **AdaptivePricingDemon**: Analiza rangos de precios por barrio (cada 300s)
- **TemporalTrendsDemon**: Detecta tendencias temporales (cada 180s)
- **PatternDiscoveryDemon**: Descubre patrones de búsqueda (cada 240s)
- **RecommendationOptimizer**: Optimiza recomendaciones (cada 120s)

### Lógica Difusa
Evalúa compatibilidad entre usuario y propiedades considerando:
- Presupuesto
- Ubicación
- Tamaño (habitaciones)
- Amenidades cercanas
- Transporte

### IA Generativa (LangChain + HuggingFace)
- Procesa consultas en lenguaje natural
- Genera respuestas contextuales
- Explica las recomendaciones

## 🔧 Solución de Problemas

### Error: No se puede conectar a Neo4j

**Solución:**
1. Verifica que Neo4j Desktop esté ejecutándose
2. Asegúrate de que la base de datos `housing` esté activa (punto verde)
3. Verifica las credenciales en `.env`:
   - URI: `bolt://localhost:7687`
   - Usuario: `neo4j`
   - Contraseña: La que configuraste

### Error: Puerto ocupado (Gradio)

El sistema intentará automáticamente puertos alternativos: 7860, 7861, 7862, 8080, 8888

### Error: Token de HuggingFace inválido

1. Ve a [huggingface.co](https://huggingface.co)
2. Crea una cuenta (gratuita)
3. Ve a Settings → Access Tokens
4. Crea un nuevo token
5. Actualiza `HUGGINGFACEHUB_API_TOKEN` en `.env`

## 📝 Ejemplos de Consultas

- "¿Hay casas en Palermo?"
- "Busca departamentos por menos de 200000"
- "Propiedades con 3 habitaciones"
- "Casas cerca del transporte público"
- "Departamentos céntricos económicos"

## 🛠️ Tecnologías

- **Python 3.14**
- **Neo4j 5.x** - Base de datos de grafos
- **LangChain** - Framework para aplicaciones con LLM
- **HuggingFace** - Modelos de lenguaje
- **Gradio** - Interfaz web
- **Pandas** - Procesamiento de datos

## 👥 Contribuir

1. Fork el proyecto
2. Crea una rama (`git checkout -b feature/mejora`)
3. Commit tus cambios (`git commit -m 'Agrega nueva funcionalidad'`)
4. Push a la rama (`git push origin feature/mejora`)
5. Abre un Pull Request

## 📄 Licencia

Este proyecto es parte de un trabajo académico de la UTN.

## 📧 Contacto

- Repositorio: [github.com/PabloChaparroo/Sistema_de_Recomendacion_de_Inmuebles](https://github.com/PabloChaparroo/Sistema_de_Recomendacion_de_Inmuebles)
- Autor: Pablo Chaparro

---

**Nota:** Este sistema aprende de las interacciones de los usuarios. Cuanto más se use, mejores serán las recomendaciones.
