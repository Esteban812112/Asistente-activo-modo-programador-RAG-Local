🚀 Tutor Técnico de Programación con IA (RAG + Ollama)

🧠 Descripción del Proyecto

Este proyecto es un **Tutor Técnico de Programación basado en Inteligencia Artificial**, capaz de responder preguntas sobre desarrollo de software utilizando:

* 📚 **RAG (Retrieval Augmented Generation)** → documentos locales
* 🤖 **Ollama (modelo local)** → IA sin necesidad de API externa
* 💾 **Historial de conversación** → mantiene contexto
* 🌐 **Interfaz web** → interacción sencilla

A diferencia de versiones anteriores, este sistema **NO usa APIs externas (como Gemini)**, lo que permite:

✅ Funcionar **offline**
✅ Evitar límites de uso
✅ Mayor control del sistema

---

## 🎯 Objetivos del Proyecto

* Implementar un **asistente de programación con IA local**
* Integrar **RAG para responder con documentos propios**
* Mantener **historial de conversación en JSON**
* Desarrollar una **interfaz web interactiva**
* Optimizar el uso de recursos (menos consumo de tokens)

---

## 🏗️ Arquitectura del Sistema

El sistema está compuesto por:

### 1️⃣ 🧠 Modelo IA Local (Ollama)

Se utiliza Ollama para ejecutar modelos de lenguaje localmente.

Ejemplo de modelo usado:

* `gemma3:1b`

---

### 2️⃣ 📚 Sistema RAG (Documentos Locales)

El sistema utiliza documentos `.txt` ubicados en la carpeta `documents/`.

Proceso:

1. Se divide el contenido en fragmentos (chunks)
2. Se generan embeddings
3. Se busca el contexto más relevante
4. Se envía al modelo para responder

---

### 3️⃣ 💾 Historial en JSON

Se guarda cada interacción:

```json
[
  {
    "usuario": "¿Qué es un JOIN?",
    "respuesta": "Un JOIN permite combinar tablas..."
  }
]
```

Esto permite mantener contexto y mejorar respuestas.

---

### 4️⃣ ⚙️ Backend en Python

Encargado de:

* Procesar preguntas
* Consultar el RAG
* Llamar al modelo local (Ollama)
* Gestionar caché y rendimiento

---

### 5️⃣ 🌐 Interfaz Web

Permite:

* Escribir preguntas
* Ver respuestas
* Consultar historial

---

## ⚡ Funcionamiento del Sistema

El sistema responde de 3 formas:

### 📚 Con RAG (documentos)

Si encuentra información relevante:

```
📚 Respuesta basada en documentos
```

---

### 🤖 Con IA (sin RAG)

Si no hay contexto:

```
🤖 Respuesta generada por IA
```

---

### ⚠️ Fuera de contexto

Si la pregunta no es de programación:

```
⚠️ Tema fuera del alcance
```


## 📦 Instalación del Proyecto

### 1️⃣ Clonar repositorio

```bash
git clone https://github.com/TU_USUARIO/tutor-rag-ollama.git
cd tutor-rag-ollama
```


### 2️⃣ Crear entorno virtual

```bash
python -m venv env
```

### 3️⃣ Activar entorno

Windows:

```bash
env\Scripts\activate
```

### 4️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```


## 🤖 Instalación de Ollama

1. Descargar desde 👉 Ollama
2. Verificar instalación:

```bash
ollama --version
```
### Descargar modelo:

```bash
ollama run gemma3:1b
```


## ▶️ Ejecución del Proyecto

```bash
python app.py
```

Abrir en navegador:

http://127.0.0.1:5000

## 📁 Estructura del Proyecto

```
tutor-rag-ollama
│
├── app.py
├── tutor.py
├── historial.py
├── rag_pipeline.py
├── requirements.txt
├── historial.json
│
├── documents/
│   ├── Python.txt
│   ├── SQL.txt
│   └── ...
│
├── templates/
│   └── index.html
│
└── env/


