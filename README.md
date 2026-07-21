# 🤖 Sistema Multi-Agente de Atencion al Cliente con RAG y Monitoreo (Langfuse)

Un sistema inteligente de atención al cliente basado en una arquitectura Multi-Agente orquestada mediante **LangChain** y **OpenAI**, con capacidad de RAG (*Retrieval-Augmented Generation*) sobre bases de datos vectoriales (**ChromaDB**) y auditoría continua de métricas con **Langfuse**.

---

## 📌 Descripción del Proyecto

Este sistema clasifica, enruta y resuelve tickets de usuarios dirigiéndolos automáticamente a agentes especializados por dominio:

- **Orquestador (Router):** Analiza la intención de la consulta y la clasifica en un departamento específico.
- **Clarification Agent:** Atiende saludos o consultas ambiguas solicitando más información.
- **HR Agent / Tech Agent / Finance Agent:** Agentes especializados respaldados por un pipeline RAG con acceso a bases de conocimiento específicas (Recursos Humanos, Soporte Técnico y Finanzas).
- **Evaluator Agent:** Un auditor automatizado que evalúa críticamente cada respuesta en tres dimensiones (*Relevancia*, *Completitud*, *Precisión*) enviando los puntajes en tiempo real a **Langfuse**.

---

## ⚙️ Requisitos Previos e Instalación

### 1. Clonar el repositorio
```bash
git clone https://github.com/TobiTobiT0bi/Integrador_03_Henry.git
cd Integrador_03_Henry
```

### 2. Crear entorno virtual e instalar dependencias

Se recomienda el uso de uv o venv:

Usando uv (Recomendado):
```bash
uv sync
```
Usando venv tradicional:
```bash
python -m venv .venv

# En Linux/macOS:
source .venv/bin/activate

# En Windows (PowerShell):
.venv\Scripts\Activate.ps1

# Instalar dependencias
pip install -r requirements.txt
```
## 🔑 Configuración de Variables de Entorno

Crea un archivo .env en la raíz del proyecto basándote en el siguiente modelo:
```bash

# Clave API de OpenAI
OPENAI_API_KEY="sk-proj-..."

# Configuración del Modelo
MODEL_NAME="gpt-4o-mini"

# Configuración de Langfuse (Monitoreo y Observabilidad)
LANGFUSE_PUBLIC_KEY="pk-lf-..."
LANGFUSE_SECRET_KEY="sk-lf-..."
LANGFUSE_HOST="[https://cloud.langfuse.com](https://cloud.langfuse.com)"
```
    ⚠️ Nota: Asegúrate de no subir tu archivo .env al control de versiones.
## 🛠️ Uso del Makefile (Configuración Rápida)

El proyecto incluye un `Makefile` para automatizar todo el proceso de instalación, configuración del entorno y ejecución de tareas comunes con comandos simples.

### Comandos Disponibles

| Comando | Descripción |
| :--- | :--- |
| `make setup` | **Configuración inicial completa:** crea el entorno virtual, instala todas las dependencias con `uv` y verifica el archivo `.env`. |
| `make run` | Inicia la **consola interactiva** del sistema multi-agente. |
| `make test` | Ejecuta las pruebas automáticas sobre el **Golden Dataset** (`test_queries.json`). |
| `make index` | Fuerza la **re-indexación** de la base de datos vectorial ChromaDB (útil si agregas nuevos documentos en `data/`). |
| `make clean` | Elimina la base de datos local `chroma_db/`, archivos temporales y la caché de Python (`__pycache__`). |

---

### 🚀 Flujo de Trabajo Recomendado

Si estás iniciando el proyecto desde cero, ejecuta simplemente:

1. **Configuración inicial en un solo paso:**
```bash
   make setup
```
## 🔥 Cómo Ejecutar el Proyecto
### Opción A: Desde la Consola Interactiva (CLI)

Para interactuar en tiempo real con el sistema desde la consola:
```bash
make run
```

O directamente con Python:
```bash
uv run python -m src.multi_agent_system
```

Para correr las pruebas automáticas sobre el Golden Dataset:

```bash
uv run python -m src.multi_agent_system --test
```

### Opción B: Desde el Notebook Jupyter (notebooks/pipeline.ipynb)

Si ejecutas la solución desde el entorno Jupyter Notebook, sigue estrictamente este orden de ejecución de celdas:
### 🧩 Orden de Ejecución:

- **Carga de Entorno y Configuración (Celda 1)**: Carga de variables de entorno y validación de claves API (OPENAI_API_KEY, LANGFUSE_*).

- **Inicialización de la BD Vectorial Chroma (Celda 2)**: Procesa los documentos de la carpeta data/ (hr/, tech/, finance/) y genera los vectores o carga los índices existentes en memoria.

- **Instanciación de Agentes y Orquestador (Celda 3)**: Carga los modelos, conecta los retrievers a los agentes y configura el EvaluatorAgent.

- **Ejecución de Pruebas / Golden Dataset (Celda 4)**: Corre el set de consultas de prueba pasando por el orquestador, agentes RAG y la evaluación.

- **Cierre y Sincronización (Celda 5)**: Llama a langfuse.flush() para garantizar el envío de todas las trazas y métricas al panel de Langfuse.

## 💡 Ejemplos de Uso
### Ejemplo 1: Consulta Técnica (RAG Tech)
```
👤 Tú: ¿Cómo realizo el cambio de mi contraseña corporativa?

📥 [Entrada de Ticket]: '¿Cómo realizo el cambio de mi contraseña corporativa?'
🔀 [Orquestador]: Enrutado a -> Tech
💬 [Respuesta del Agente]: Para cambiar tu contraseña corporativa debes ingresar al portal... [Instrucciones detalladas del documento RAG].

🧐 [Evaluador]: Evaluando calidad de la respuesta...
📊 [Resultados de Auditoría]:
   - Relevancia: 0.90
   - Completitud: 0.85
   - Precisión: 0.95
   - Crítica: La respuesta es precisa y proviene de la base de conocimiento, pero omitió adjuntar el enlace directo al portal de credenciales (-0.15 completitud).
```

### Ejemplo 2: Saludo / Consulta Ambigua (Clarification)
```

👤 Tú: Hola, necesito ayuda.

🔀 [Orquestador]: Enrutado a -> Clarification
💬 [Respuesta del Agente]: ¡Hola! ¿En qué área puedo ayudarte? (Recursos Humanos, Soporte Técnico o Finanzas).
```

### ⚙️ Notas de Configuración

- **ChromaDB Local**: La base de datos persistente se genera por defecto en la carpeta chroma_db/. Si modificas los archivos markdown/pdf en data/, debes eliminar esta carpeta para forzar la re-indexación.

- **Modelo LLM por Defecto**: Se utiliza gpt-4o-mini para optimizar costos y tiempos de respuesta. Puede modificarse en el archivo src/config.py o vía la variable MODEL_NAME en .env.

- **Compatibilidad con Langfuse**: Este proyecto utiliza la especificación de Langfuse v4+ (from langfuse.langchain import CallbackHandler).

### 🚨 Limitaciones Conocidas

- **Dependencia de Contexto RAG**: Si la información no está explícitamente detallada en los documentos de la carpeta data/, el agente informará que no posee los datos necesarios en lugar de inventar (evitando alucinaciones).

- **Evaluaciones Rigurosas**: El agente evaluador está configurado con un perfil estrictamente crítico, por lo que respuestas cortas o generalistas rara vez obtendrán puntuaciones perfectas (1.0).

- **Persistencia de Conversación**: La versión actual procesa cada ticket de manera independiente (stateless). No mantiene historial multilaboral entre preguntas consecutivas del mismo usuario.

---

## 🧠 Decisiones de Arquitectura y Criterio de Ingeniería

Para la construcción de este sistema se evaluaron diversas alternativas tecnológicas. A continuación se detallan las decisiones tomadas y las razones de por qué se eligieron sobre otras opciones del ecosistema:

### 1. Selección de Componentes de LangChain & LLM
* **Modelo Centralizado (`gpt-4o-mini`):** Se eligió frente a `gpt-4o` o modelos locales (como Llama 3 8B) debido a su excelente relación costo-latencia y su capacidad nativa para seguir instrucciones complejas en español. Optimiza los tiempos de respuesta del RAG manteniendo un rendimiento casi idéntico en tareas de extracción.
* **Structured Outputs con Pydantic:** Para el `EvaluatorAgent` y el `Orchestrator`, se utilizó la API de salidas estructuradas de LangChain respaldada por esquemas de Pydantic. Esto garantiza un parseo sintácticamente seguro (evita fallos de JSON malformados) y obliga al modelo a generar una razonamiento previo (`reasoning`) antes de asignar un puntaje.

### 2. Base de Datos Vectorial: ChromaDB vs. FAISS
* **Elección:** **ChromaDB** (Persistencia Local por Colecciones).
* **¿Por qué ChromaDB y no FAISS?:**
  - **Persistencia Nativa y Simplicidad:** FAISS (de Meta) es una librería de indexación puramente en memoria enfocada en rendimiento extremo a gran escala, pero requiere gestión manual de serialización en disco y metadatos. ChromaDB ofrece persistencia integrada fuera de la caja (*out-of-the-box*) y gestión simplificada de colecciones por archivos en disco (`chroma_db/`).
  - **Filtrado por Metadatos y Separación de Dominios:** ChromaDB permite aislar físicamente los datos por colecciones independientes (`HR`, `TECH`, `FINANCE`) de forma muy transparente, evitando que las consultas a un área interfieran o consuman memoria de otras.

### 3. Modelo de Embeddings: OpenAI Embeddings vs. Text Transformers (Sentence-Transformers)
* **Elección:** **OpenAI `text-embedding-3-small`**.
* **¿Por qué OpenAI Embeddings y no modelos locales/HuggingFace?:**
  - **Dimensión y Rendimiento en Español:** Los modelos locales ligeros de HuggingFace (como `all-MiniLM-L6-v2`) suelen estar fuertemente sesgados hacia el idioma inglés y requieren mayor potencia computacional local (CPU/GPU) durante el proceso de indexación.
  - **Mismo Espacio de Vectorización y Normalización:** Al usar `text-embedding-3-small`, se aprovechan dimensiones optimizadas para semántica multilenguaje (incluyendo español técnico/corporativo) con una latencia de red despreciable y un costo prácticamente nulo para el volumen del proyecto, delegando la carga de cómputo fuera del servidor local.

### 4. Estrategia de Routing y Dominio de Agentes
* **Dynamic Prompt-Based Router vs. Clasificador Vectorial:** En lugar de un clasificador por similitud semántica (que suele fallar con frases cortas o ambiguas), se optó por un Router basado en LLM con un prompt optimizado. Esto permite detectar la intención real del usuario, manejar saludos informales y redirigirlos al `ClarificationAgent`.
* **Aislamiento por Agentes Especialistas:** Se descartó un RAG monolítico (una sola base de datos con todos los manuales). Tener agentes e índices vectoriales independientes reduce el espacio de búsqueda del retriever, eliminando el "ruido de contexto" (interferencias entre políticas de RRHH y manuales de IT) y aumentando la precisión del RAG.

### 5. Estrategia de Observabilidad (Langfuse v4)
* **Tracing Pasivo mediante Callbacks:** Se eligió la integración nativa por `CallbackHandler` en las cadenas de LangChain en lugar de código decorador manual. Esto captura de forma no intrusiva toda la jerarquía de llamadas (Router -> Retriever -> LLM -> Evaluador) sin contaminar la lógica de negocio.

### 6. Estrategia de Búsqueda Vectorial: k-NN (Exacto) vs. ANN (Aproximado)

En los sistemas de recuperación de información basados en embeddings, existen dos enfoques principales para encontrar los vectores más similares a la consulta del usuario:

* **k-NN (k-Nearest Neighbors - Búsqueda Exacta):** Calcula la distancia vectorial (por ejemplo, distancia Coseno o Euclidiana) comparando el vector de la consulta contra **absolutamente todos** los vectores almacenados en el índice ($O(N)$). Garantiza encontrar siempre los $k$ vecinos matemáticamente más cercanos, pero no escala bien con millones de vectores.
* **ANN (Approximate Nearest Neighbors - Búsqueda Aproximada):** Utiliza estructuras de datos avanzadas (como grafos **HNSW** — *Hierarchical Navigable Small World* — o árboles KD) para explorar solo subconjuntos del espacio vectorial ($O(\log N)$). Ofrece un rendimiento extremadamente rápido a gran escala, sacrificando una fracción mínima de precisión (recall).

#### 💡 Elección en el Proyecto y Criterio de Ingeniería:

* **Elección en producción:** En este proyecto utilizamos **ANN (HNSW)**, que es el algoritmo por defecto que implementa **ChromaDB** en su motor interno (*hnswlib*).
* **¿Por qué ANN (HNSW) sobre k-NN puro?:**
  1. **Sub-segundo y Escalabilidad RAG:** En un sistema de atención al cliente corporativo, el volumen de manuales, normativas y FAQs crece constantemente. HNSW permite mantener tiempos de respuesta en el rango de milisegundos incluso si la base documental escala a decenas de miles de chunks.
  2. **Balance Precisión/Latencia:** Para tareas de RAG en texto en español, el margen de error probabilístico de ANN es prácticamente despreciable frente al beneficio en velocidad, garantizando que el `Retriever` entregue los chunks de contexto relevantes al agente en tiempo real.