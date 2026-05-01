# Tutor Técnico de Programación con IA
# Descripción del Proyecto

Este proyecto consiste en el desarrollo de un **Tutor Técnico de Programación basado en Inteligencia Artificial**, capaz de responder preguntas relacionadas con conceptos de programación y ayudar a los usuarios a comprender diferentes temas del desarrollo de software.

El sistema utiliza **IA generativa** para analizar preguntas y proporcionar explicaciones claras, manteniendo además un **historial de conversación** que permite conservar el contexto de las interacciones.

La aplicación incluye una **interfaz gráfica interactiva**, permitiendo que el usuario pueda comunicarse fácilmente con el tutor técnico.


# Objetivos del Proyecto

* Implementar un **asistente de programación basado en IA**
* Utilizar **roles o instrucciones específicas** para controlar el comportamiento del modelo
* Mantener un **historial de conversación**
* Desarrollar una **interfaz gráfica sencilla para interacción con el usuario**
* Integrar diferentes componentes del sistema en una aplicación funcional

# Arquitectura del Sistema

El sistema está compuesto por los siguientes componentes principales:

1. **Instruction (Role)**
   Define el comportamiento del asistente de inteligencia artificial.

2. **Historial en JSON**
   Guarda las conversaciones entre el usuario y el tutor.

3. **Backend en Python**
   Procesa las preguntas y conecta con la IA.

4. **Interfaz Gráfica**
   Permite interactuar con el tutor técnico.


#  Instruction (Rol del Tutor)

El modelo de inteligencia artificial recibe una **instrucción inicial** que define su comportamiento como un tutor de programación.

Esto permite que el asistente:

* explique conceptos de programación
* responda preguntas técnicas
* mantenga un estilo educativo y claro

### Ejemplo de código del rol



###  Imagen del Instruction Role

<img width="1110" height="693" alt="image" src="https://github.com/user-attachments/assets/2b6c0a4a-4c56-4187-858f-8dfedd704ee0" />


# 📂 Historial de Conversación en JSON

El sistema guarda cada interacción en un archivo **JSON**, permitiendo conservar el contexto de la conversación.

Esto permite que el asistente recuerde preguntas anteriores y genere respuestas más coherentes.

### Ejemplo de estructura del historial

```json
[
  {
    "usuario": "¿Qué es una variable?",
    "respuesta": "Una variable es un espacio en memoria..."
  }
]
```

###  Imagen del historial en código

<img width="1037" height="697" alt="image" src="https://github.com/user-attachments/assets/7c9330f9-8c10-4023-90be-7c149b5094c7" />



# 🖥 Interfaz Gráfica

La aplicación cuenta con una **interfaz gráfica simple** que permite al usuario interactuar con el tutor.

Funciones principales de la interfaz:

* escribir preguntas
* visualizar respuestas del tutor
* mantener el flujo de conversación

### Imagen de la interfaz gráfica

<img width="1210" height="657" alt="image" src="https://github.com/user-attachments/assets/d965a37c-b597-4d38-9413-c64c68b87e99" />


#  Historial en la Interfaz

La interfaz también muestra el **historial completo de conversación**, permitiendo que el usuario pueda revisar preguntas y respuestas anteriores.

### Imagen del historial en la interfaz

<img width="1309" height="629" alt="image" src="https://github.com/user-attachments/assets/ad2ae7a1-0861-4caf-b1f2-36702e8f3829" />


#  Instalación del Proyecto

## 1️⃣ Clonar el repositorio

```bash
git clone https://github.com/Esteban812112/Tutor-t-cnico-de-programaci-n.git
```

---

## 2️⃣ Entrar a la carpeta del proyecto

```bash
cd Tutor-t-cnico-de-programaci-n
```

---

## 3️⃣ Crear entorno virtual

```bash
python -m venv env
```

---

## 4️⃣ Activar entorno virtual

En Windows

```bash
env\Scripts\activate
```

---

## 5️⃣ Instalar dependencias

```bash
pip install -r requirements.txt
```

---

# ▶️Ejecución del Proyecto

Para ejecutar la aplicación:

```bash
python app.py
```

Luego abrir en el navegador:

```
http://127.0.0.1:5000
```



#  Estructura del Proyecto

```
tutor-programacion-ia
│
├── app.py
├── tutor.py
├── historial.py
├── requirements.txt
├── historial.json
│
├── templates
│   └── index.html
│
└── static
```

