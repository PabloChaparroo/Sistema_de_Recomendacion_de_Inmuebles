# 📸 GUÍA PASO A PASO PARA CAPTURAS DE PANTALLA - INFORME PG6

Esta guía te indica exactamente **qué capturas tomar** y **dónde ubicarlas** en el informe.

---

## 📋 LISTA DE CAPTURAS NECESARIAS

| # | Descripción | Ubicación en informe | Prioridad |
|---|-------------|---------------------|-----------|
| 1 | Ollama funcionando en terminal | Sección 2 | ⭐⭐⭐ OBLIGATORIA |
| 2 | Grafo visualizado en Neo4j Browser | Sección 3 | ⭐⭐⭐ OBLIGATORIA |
| 3 | Esquema del modelo de datos | Sección 3 | ⭐⭐⭐ OBLIGATORIA |
| 4 | Ejecución completa de test_ollama.py | Sección 5 | ⭐⭐⭐ OBLIGATORIA |
| 5 | Código de langchain_integration.py | Sección 4 | ⭐⭐ Recomendada |
| 6 | Verificación de datos en Neo4j | Sección 3 | ⭐⭐ Recomendada |
| 7 | Consultas adicionales personalizadas | Sección 5 | ⭐ Opcional |

---

## 📸 CAPTURA 1: Ollama funcionando (OBLIGATORIA)

### ¿Dónde va en el informe?
**Sección 2: Descripción del Modelo y Pruebas con Ollama**

### Paso a paso:

1. **Abrir PowerShell** en Windows
2. **Ejecutar comando:**
   ```powershell
   ollama run mistral
   ```
3. **Esperar** a que aparezca el prompt `>>>`
4. **Escribir estas preguntas de prueba:**
   ```
   >>> ¿Cómo funcionas?
   (Espera respuesta)
   
   >>> Explica qué es Cypher para Neo4j en una oración
   (Espera respuesta)
   
   >>> /bye
   ```
5. **Tomar captura de pantalla** de toda la ventana PowerShell

### ✅ Qué debe verse en la captura:
- El comando `ollama run mistral` ejecutado
- Las preguntas que escribiste
- Las respuestas de Mistral
- El prompt interactivo `>>>`

### 💡 Tip:
Usa **Windows + Shift + S** para captura de pantalla rápida.

---

## 📸 CAPTURA 2: Grafo en Neo4j Browser (OBLIGATORIA)

### ¿Dónde va en el informe?
**Sección 3: Diagrama del Grafo en Neo4j**

### Paso a paso:

1. **Abrir Neo4j Desktop**
2. **Iniciar tu base de datos** (botón verde "Start")
3. **Clic en "Open"** → Seleccionar **"Neo4j Browser"**
4. Se abre **http://localhost:7474** en tu navegador
5. **En el cuadro de texto superior**, escribir:
   ```cypher
   MATCH (n)
   RETURN n
   LIMIT 25
   ```
6. **Presionar Enter** o clic en el botón ▶️
7. **Esperar** a que aparezca el grafo visualizado
8. **Tomar captura de pantalla** de toda la ventana del navegador

### ✅ Qué debe verse en la captura:
- Los nodos de colores (Property, User, Amenity)
- Las líneas conectando nodos (relaciones)
- La consulta Cypher arriba
- Los resultados abajo

### 💡 Tips:
- **Zoom:** Usa la rueda del mouse para ajustar el tamaño
- **Drag:** Arrastra nodos para organizar visualmente
- **Modo de vista:** Clic en el ícono de gráfico (arriba a la derecha)

---

## 📸 CAPTURA 3: Esquema del modelo (OBLIGATORIA)

### ¿Dónde va en el informe?
**Sección 3: Diagrama del Grafo en Neo4j** (después de CAPTURA 2)

### Paso a paso:

1. **En Neo4j Browser** (mismo lugar que CAPTURA 2)
2. **Limpiar el cuadro de texto** (borrar consulta anterior)
3. **Escribir:**
   ```cypher
   CALL db.schema.visualization()
   ```
4. **Presionar Enter**
5. Aparece el **diagrama del esquema** con:
   - Recuadros para cada tipo de nodo (Property, User, Amenity)
   - Flechas mostrando las relaciones (HAS_AMENITY, VISITED, PREFERS_AMENITY)
6. **Tomar captura de pantalla**

### ✅ Qué debe verse en la captura:
- Los 3 tipos de nodos: Property, User, Amenity
- Las 3 relaciones: HAS_AMENITY, VISITED, PREFERS_AMENITY
- Estructura clara del modelo de datos

### 💡 Tip:
Esta captura es **clave** porque muestra el diseño de tu base de datos de forma profesional.

---

## 📸 CAPTURA 4: Ejecución de test_ollama.py (OBLIGATORIA)

### ¿Dónde va en el informe?
**Sección 5: Ejemplos de Interacción**

### Paso a paso:

1. **Abrir PowerShell** en la carpeta de tu proyecto
2. **Asegurarte** de que Neo4j está corriendo
3. **Ejecutar:**
   ```powershell
   python test_ollama.py
   ```
4. **Esperar** a que termine (puede tomar 30-60 segundos)
5. **Tomar captura de pantalla** cuando muestre "✅ PRUEBAS COMPLETADAS"

### ✅ Qué debe verse en la captura:

Debe mostrar las **3 pruebas completas**:

**PRUEBA 1:**
```
📊 PRUEBA 1: Contar propiedades totales
✅ Cypher generado:
MATCH (p:Property) RETURN count(p) LIMIT 10;

💬 Respuesta: En total hay 8 propiedades.
```

**PRUEBA 2:**
```
🏙️  PRUEBA 2: Buscar propiedades en Mendoza
✅ Cypher generado:
MATCH (p:Property) WHERE p.city = 'Mendoza' RETURN COUNT(p) LIMIT 10;

💬 Respuesta: Hay 4 propiedades en la ciudad de Mendoza.
```

**PRUEBA 3:**
```
🎯 PRUEBA 3: Listar amenidades disponibles
✅ Cypher generado:
MATCH (a:Amenity) RETURN a.name LIMIT 10

💬 Respuesta: Las amenidades son: Parque, Gimnasio, Piscina, Seguridad 24hs, Cochera, Parrilla.
```

### 💡 Tip:
Si la ventana es muy larga, toma **2 capturas**:
- Una con PRUEBA 1 y 2
- Otra con PRUEBA 3 y el mensaje final

---

## 📸 CAPTURA 5: Código de langchain_integration.py (Recomendada)

### ¿Dónde va en el informe?
**Sección 4: Código de LangChain**

### Paso a paso:

1. **Abrir VS Code**
2. **Navegar** a `workflow/langchain_integration.py`
3. **Scroll** hasta la función `create_housing_qa()` (líneas 15-70)
4. **Tomar captura** del código

### ✅ Qué debe verse en la captura:
```python
def create_housing_qa():
    # 1. Conectar a Neo4j
    graph = Neo4jGraph(...)
    
    # 2. Configurar LLM con Ollama
    llm = OllamaLLM(
        model="mistral",
        temperature=0.1,
        ...
    )
    
    # 3. Template para generar consultas Cypher
    cypher_prompt = PromptTemplate(...)
    
    # 4. Crear cadena de Q&A
    chain = GraphCypherQAChain.from_llm(...)
```

### 💡 Tip alternativa:
Si no quieres captura del código, puedes **copiarlo directamente en el informe** (ya está incluido en INFORME_PG6_COMPLETO.md).

---

## 📸 CAPTURA 6: Verificación de datos (Recomendada)

### ¿Dónde va en el informe?
**Sección 3: Diagrama del Grafo en Neo4j** (como complemento)

### Paso a paso:

1. **En Neo4j Browser**
2. **Ejecutar estas consultas** una por una:

**Consulta 1 - Contar nodos:**
```cypher
MATCH (p:Property) RETURN count(p) as Propiedades
UNION
MATCH (u:User) RETURN count(u) as Usuarios
UNION
MATCH (a:Amenity) RETURN count(a) as Amenidades
```

**Consulta 2 - Ver propiedades de ejemplo:**
```cypher
MATCH (p:Property)
RETURN p.id, p.city, p.price, p.bedrooms
LIMIT 5
```

**Consulta 3 - Ver relaciones:**
```cypher
MATCH (p:Property)-[r:HAS_AMENITY]->(a:Amenity)
RETURN p.id, a.name
LIMIT 10
```

3. **Tomar captura** de cada resultado

### ✅ Qué debe verse:
- Tablas con datos reales
- Comprobación de que los datos se cargaron correctamente

---

## 📸 CAPTURA 7: Consultas adicionales (Opcional)

### ¿Dónde va en el informe?
**Sección 5: Ejemplos de Interacción** (al final)

### Paso a paso:

1. **Abrir Python** en terminal:
   ```powershell
   python
   ```

2. **Ejecutar consultas personalizadas:**
   ```python
   from workflow.langchain_integration import ask_question
   
   # Consulta personalizada 1
   resultado = ask_question("Lista las 3 propiedades más baratas")
   print(resultado['answer'])
   
   # Consulta personalizada 2
   resultado = ask_question("¿Qué propiedades tienen piscina?")
   print(resultado['answer'])
   
   # Consulta personalizada 3
   resultado = ask_question("¿Cuántos usuarios visitaron propiedades en Mendoza?")
   print(resultado['answer'])
   ```

3. **Tomar captura** de las respuestas

### ✅ Qué debe verse:
- Preguntas diferentes a las del test_ollama.py
- Respuestas coherentes y correctas
- Demuestra versatilidad del sistema

---

## 🎨 FORMATO DE LAS CAPTURAS

### Recomendaciones generales:

1. **Resolución:** Mínimo 1280x720px
2. **Formato:** PNG o JPG (PNG preferible)
3. **Texto legible:** Asegúrate que se pueda leer todo
4. **Sin información sensible:** Oculta datos personales si es necesario

### Herramientas recomendadas:

**Windows:**
- **Windows + Shift + S:** Captura rápida de área
- **Snipping Tool:** Más opciones de edición
- **ShareX:** Herramienta avanzada (gratis)

**Edición:**
- **Paint:** Para agregar flechas o texto
- **PowerPoint:** Insertar varias capturas en un slide
- **Canva:** Para diseño más profesional

---

## 📝 CÓMO INSERTAR EN EL INFORME

### Si usas Word:

1. **Insertar → Imágenes → Este dispositivo**
2. **Seleccionar captura**
3. **Ajustar tamaño** (ancho completo de página)
4. **Agregar pie de foto:**
   - Clic derecho → "Insertar título"
   - Ejemplo: "Figura 1: Ollama ejecutando modelo Mistral"

### Si usas Markdown (como este archivo):

```markdown
![Descripción de la imagen](ruta/a/captura.png)
*Figura 1: Ollama ejecutando modelo Mistral*
```

### Si usas LaTeX:

```latex
\begin{figure}[h]
    \centering
    \includegraphics[width=0.8\textwidth]{captura1.png}
    \caption{Ollama ejecutando modelo Mistral}
    \label{fig:ollama}
\end{figure}
```

---

## ✅ CHECKLIST FINAL

Antes de entregar, verifica que tienes:

- [ ] **CAPTURA 1:** Ollama funcionando ⭐⭐⭐
- [ ] **CAPTURA 2:** Grafo visualizado ⭐⭐⭐
- [ ] **CAPTURA 3:** Esquema del modelo ⭐⭐⭐
- [ ] **CAPTURA 4:** test_ollama.py ejecutado ⭐⭐⭐
- [ ] **CAPTURA 5:** Código de LangChain ⭐⭐
- [ ] **CAPTURA 6:** Verificación de datos ⭐⭐
- [ ] **CAPTURA 7:** Consultas adicionales ⭐

**Mínimo para aprobar:** CAPTURAS 1, 2, 3, 4 (las obligatorias)

---

## 🚀 ORDEN RECOMENDADO PARA TOMAR LAS CAPTURAS

### Sesión 1 (15 minutos):
1. Iniciar Neo4j Desktop
2. Tomar CAPTURA 2 (grafo)
3. Tomar CAPTURA 3 (esquema)
4. Tomar CAPTURA 6 (verificación) - opcional

### Sesión 2 (10 minutos):
1. Abrir PowerShell
2. Ejecutar `ollama run mistral`
3. Tomar CAPTURA 1

### Sesión 3 (5 minutos):
1. Ejecutar `python test_ollama.py`
2. Tomar CAPTURA 4

### Sesión 4 (10 minutos - opcional):
1. Abrir VS Code
2. Tomar CAPTURA 5 (código)
3. Ejecutar consultas personalizadas
4. Tomar CAPTURA 7

---

## 💡 TIPS FINALES

### Para que se vea profesional:

1. **Limpia tu escritorio** antes de capturar
2. **Cierra pestañas innecesarias** del navegador
3. **Usa modo claro** en VS Code (mejor para imprimir)
4. **Agranda la fuente** si es necesario (Ctrl + Scroll)
5. **Centra las ventanas** en la pantalla

### Si algo sale mal:

- **Ollama no responde:** Reinicia con `ollama serve` en otra terminal
- **Neo4j vacío:** Re-ejecuta `python load_sample_data.py`
- **Errores en test:** Verifica que Neo4j y Ollama estén corriendo
- **Capturas borrosas:** Aumenta la resolución de pantalla

---

## 📧 SOPORTE

Si tienes problemas con alguna captura:
1. Revisa esta guía paso por paso
2. Verifica que todos los servicios estén corriendo
3. Consulta el archivo `INFORME_PG6_COMPLETO.md` para contexto

---

**¡Éxito con tu informe! 🎓**
