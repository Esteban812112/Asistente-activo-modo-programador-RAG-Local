import ollama

from historial import (
    cargar_historial,
    agregar_interaccion,
    guardar_historial
)

from rag_pipeline import RAGPipeline

# ==============================
# INICIALIZAR RAG
# ==============================

print("📚 Cargando sistema RAG...")
rag = RAGPipeline()
print("✅ RAG listo!")

# ==============================
# CONFIG MODELO
# ==============================

MODEL_NAME = "gemma3:1b"

# ==============================
# CACHE
# ==============================

respuestas_cache = {}

cache_hits = 0
cache_misses = 0

# ==============================
# SYSTEM PROMPT
# ==============================

system_instruction = """
Eres CodeDragon, un tutor experto en programación.

OBJETIVO:
Responder preguntas técnicas de programación
de forma clara, útil y resumida.

REGLAS:

1. Usa contexto RAG si existe.
2. Si no existe contexto RAG, usa conocimiento general.
3. NO inventes información falsa.
4. Responde de forma educativa pero breve.
5. Explica solo lo importante.
6. Usa ejemplos pequeños cuando ayuden.
7. Usa Markdown simple.

8. SOLO responde preguntas de:
- programación
- software
- tecnología
- desarrollo
- IA
- bases de datos
- DevOps
- ciberseguridad

9. Si la pregunta NO es técnica:
responde EXACTAMENTE:

"⚠️ Solo puedo responder temas de programación y tecnología."

ESTILO:
- profesional
- amigable
- claro
- técnico pero entendible
"""

# ==============================
# PALABRAS PROGRAMACIÓN
# ==============================

PALABRAS_PROGRAMACION = [

    # Lenguajes
    "python", "java", "javascript",
    "typescript", "c++", "c#",
    "php", "ruby", "go", "rust",
    "kotlin", "swift", "dart",

    # Frameworks
    "django", "flask", "fastapi",
    "spring", "express", "nestjs",
    "laravel", "rails",

    # Frontend
    "react", "vue", "angular",
    "svelte", "nextjs",

    # CSS
    "css", "scss", "sass",
    "tailwind", "bootstrap",

    # Bases de datos
    "sql", "mysql", "postgresql",
    "sqlite", "mongodb", "redis",
    "firebase", "supabase",

    # Programación
    "programacion",
    "codigo",
    "algoritmo",
    "estructura de datos",
    "variable",
    "funcion",
    "metodo",
    "clase",
    "objeto",

    # Algoritmos
    "big o",
    "recursividad",
    "backtracking",
    "programacion dinamica",

    # Web
    "api",
    "rest",
    "graphql",
    "frontend",
    "backend",
    "fullstack",

    # HTML
    "html",
    "div",
    "span",
    "form",
    "input",

    # JavaScript
    "json",
    "async",
    "await",
    "fetch",
    "axios",

    # React
    "hooks",
    "usestate",
    "useeffect",
    "redux",
    "jsx",

    # SQL
    "select",
    "insert",
    "update",
    "delete",
    "join",

    # Git
    "git",
    "github",
    "gitlab",
    "commit",
    "push",
    "pull",

    # DevOps
    "docker",
    "kubernetes",
    "terraform",
    "jenkins",

    # Cloud
    "aws",
    "azure",
    "gcp",

    # IA
    "inteligencia artificial",
    "machine learning",
    "deep learning",
    "llm",
    "rag",
    "ollama",
    "gemma",
    "mistral",
    "gpt",

    # Librerías
    "tensorflow",
    "pytorch",
    "pandas",
    "numpy",

    # Seguridad
    "xss",
    "csrf",
    "sql injection",
    "bcrypt",

    # Herramientas
    "linux",
    "bash",
    "terminal",
    "vscode",
    "npm",
    "pip",

    # Acciones
    "instalar",
    "configurar",
    "compilar",
    "deploy",
    "debug",
    "error",
    "corregir"
]

# ==============================
# VALIDAR TEMA
# ==============================

def es_tema_programacion(texto):

    # ==========================
    # VALIDAR VACÍO
    # ==========================

    if not texto:
        return False

    texto = texto.lower().strip()

    # ==========================
    # MUY CORTO
    # ==========================

    if len(texto) < 3:
        return False

    # ==========================
    # NORMALIZAR
    # ==========================

    caracteres = [

        ",", ".", "-", "_",
        "(", ")", "[", "]",
        "{", "}", ":", ";",
        "!", "?", "/", "\\",
        "'", '"', "\n", "\t",
        "*", "+", "="
    ]

    for c in caracteres:
        texto = texto.replace(c, " ")

    texto = " ".join(texto.split())

    # ==========================
    # PALABRAS NO TECH
    # ==========================

    PALABRAS_NO_TECH = {

        "hola",
        "hi",
        "hey",
        "hello",

        "jaja",
        "jeje",
        "xd",

        "pizza",
        "hamburguesa",

        "gato",
        "perro",

        "futbol",
        "baloncesto",
        "musica",
        "pelicula",

        "novia",
        "novio",
        "sexo",
        "porno",

        "clima",
        "lluvia",
        "receta",
        "cocina"
    }

    # ==========================
    # FRASES NO TECH
    # ==========================

    FRASES_NO_TECH = [

        "como estas",
        "quien eres",
        "como te llamas",
        "mejor jugador",
        "mejor equipo",
        "partido de futbol",
        "donde ver futbol",
        "receta de cocina",
        "como esta el clima",
        "quien gano el partido"
    ]

    # ==========================
    # BLOQUEAR FRASES
    # ==========================

    for frase in FRASES_NO_TECH:

        if frase in texto:
            return False

    # ==========================
    # TOKENIZAR
    # ==========================

    palabras = texto.split()

    # ==========================
    # CONTADORES
    # ==========================

    score_programacion = 0
    score_no_tech = 0

    # ==========================
    # CONTAR NO TECH
    # ==========================

    for palabra in palabras:

        if palabra in PALABRAS_NO_TECH:
            score_no_tech += 1

    # ==========================
    # PALABRAS EXTRA TECH
    # ==========================

    PALABRAS_EXTRA = [

        "programador",
        "programacion",
        "developer",
        "desarrollador",
        "desarrollo",
        "codigo",
        "software",
        "tecnologia",
        "informatica",
        "computacion",
        "app",
        "aplicacion",
        "pagina web",
        "sitio web",
        "web",
        "backend",
        "frontend",
        "fullstack",
        "base de datos",
        "inteligencia artificial",
        "machine learning",
        "ia",
        "algoritmo",
        "bug",
        "debug",
        "error",
        "servidor",
        "api",
        "docker",
        "linux",
        "github",
        "git"
    ]

    # ==========================
    # UNIR LISTAS
    # ==========================

    TODOS_LOS_TERMINOS = (
        PALABRAS_PROGRAMACION +
        PALABRAS_EXTRA
    )

    # ==========================
    # BUSCAR FRASES TECH
    # ==========================

    for termino in TODOS_LOS_TERMINOS:

        termino = termino.lower()

        # frase exacta
        if termino == texto:
            score_programacion += 5
            continue

        # frase contenida
        if termino in texto:
            score_programacion += 3

    # ==========================
    # BUSCAR POR PALABRAS
    # ==========================

    for palabra_usuario in palabras:

        if len(palabra_usuario) < 3:
            continue

        for termino in TODOS_LOS_TERMINOS:

            termino = termino.lower()

            # exacta
            if palabra_usuario == termino:
                score_programacion += 2
                continue

            # parcial inteligente
            if (

                len(palabra_usuario) >= 5
                and palabra_usuario in termino

            ):
                score_programacion += 1

            elif (

                len(termino) >= 5
                and termino in palabra_usuario

            ):
                score_programacion += 1

    # ==========================
    # DETECTAR PREGUNTAS TECH
    # ==========================

    preguntas_tech = [

        "como hacer",
        "como crear",
        "como instalar",
        "como configurar",
        "como programar",
        "como desarrollar",
        "como usar",
        "como funciona",
        "que es",
        "error en",
        "problema con"
    ]

    for patron in preguntas_tech:

        if patron in texto:

            for termino in TODOS_LOS_TERMINOS:

                if termino in texto:
                    score_programacion += 2
                    break

    # ==========================
    # BALANCE FINAL
    # ==========================

    if score_no_tech > score_programacion:
        return False

    # ==========================
    # VALIDACIÓN FINAL
    # ==========================

    if score_programacion >= 2:
        return True

    return False
# ==============================
# FUNCIÓN PRINCIPAL
# ==============================

def responder(pregunta):

    global cache_hits
    global cache_misses

    # ==========================
    # NORMALIZAR
    # ==========================

    pregunta_normalizada = (
        pregunta.lower().strip()
    )

    # ==========================
    # CACHE
    # ==========================

    if pregunta_normalizada in respuestas_cache:

        cache_hits += 1

        print(
            f"💾 Caché usado | Hits: {cache_hits}"
        )

        return respuestas_cache[
            pregunta_normalizada
        ]

    cache_misses += 1

    print(
        f"🤖 Consultando Ollama | Misses: {cache_misses}"
    )

     # ==========================
    # CONSULTAR RAG
    # ==========================

    rag_result = rag.query(pregunta)

    tiene_contexto = (
        rag_result.get(
            "has_context",
            False
        )
    )

    # ==========================
    # VALIDAR SIMILITUD
    # ==========================

    # ⚠️ 0.18 era muy bajo
    # activaba RAG casi siempre

    similaridad_minima = 0.45

    hay_similitud = False

    score = 0.0

    fuente_nombre = ""

    preview_texto = ""

    # ==========================
    # OBTENER SOURCES
    # ==========================

    sources = rag_result.get(
        "sources",
        []
    )

    # ==========================
    # VALIDAR CONTEXTO
    # ==========================

    if tiene_contexto and sources:

        try:

            # ======================
            # PRIMER RESULTADO
            # ======================

            primer_resultado = sources[0]

            documento = primer_resultado[0]

            score = float(
                primer_resultado[1]
            )

            # ======================
            # METADATA
            # ======================

            metadata = documento.get(
                "metadata",
                {}
            )

            fuente_nombre = metadata.get(
                "source",
                "desconocido"
            )

            # ======================
            # CONTENIDO
            # ======================

            contenido = documento.get(
                "content",
                ""
            )

            preview_texto = contenido[:150]

            # ======================
            # DEBUG
            # ======================

            print("\n====================")
            print("📚 RESULTADO RAG")
            print("====================")

            print(
                f"📊 Similaridad: "
                f"{score:.2%}"
            )

            print(
                f"📄 Archivo: "
                f"{fuente_nombre}"
            )

            print(
                f"📖 Preview: "
                f"{preview_texto[:80]}..."
            )

            # ======================
            # VALIDAR UMBRAL
            # ======================

            if score >= similaridad_minima:

                hay_similitud = True

                print(
                    f"✅ RAG ACTIVADO "
                    f"(>= {similaridad_minima:.0%})"
                )

            else:

                print(
                    f"❌ RAG IGNORADO "
                    f"(< {similaridad_minima:.0%})"
                )

                # Limpiar basura

                score = 0.0

                fuente_nombre = ""

                preview_texto = ""

        except Exception as e:

            print(
                f"⚠️ Error validando "
                f"similitud: {e}"
            )

            hay_similitud = False

            score = 0.0

            fuente_nombre = ""

            preview_texto = ""

    else:

        print(
            "📭 No se encontró "
            "contexto relevante"
        )

    # ==========================
    # PORCENTAJE RAG
    # ==========================

    porcentaje_rag = (

        round(score * 100, 2)

        if hay_similitud

        else 0

    )

    # ==========================
    # INFO DE FUENTE
    # ==========================

    info_fuente = {

        "nombre": fuente_nombre,

        "similitud": porcentaje_rag,

        "preview": preview_texto,

        "usado": hay_similitud
    }

    # ==========================
    # VALIDAR TEMA
    # ==========================

    tema_programacion = (
        es_tema_programacion(
            pregunta
        )
    )

    # ==========================
    # BLOQUEAR NO TECH
    # ==========================

    if (

        not hay_similitud

        and

        not tema_programacion

    ):

        return (
            "⚠️ Solo puedo responder "
            "temas de programación "
            "y tecnología."
        )

    # ==========================
    # HISTORIAL
    # ==========================

    historial = cargar_historial()

    # ==========================
    # CONSTRUIR MENSAJE
    # ==========================

    mensaje = ""

    # ==========================
    # CONTEXTO RAG
    # ==========================

    if hay_similitud:

        contexto = rag_result.get(
            "context",
            ""
        )[:1500]

        mensaje += f"""
# CONTEXTO RAG

{contexto}

# INFORMACIÓN RAG

✅ Contexto encontrado

📄 Archivo fuente:
{fuente_nombre}

📊 Similitud:
{porcentaje_rag}%

# INSTRUCCIONES IMPORTANTES

- Responde usando principalmente
  el contexto RAG.

- Si el contexto no tiene suficiente
  información, dilo claramente.

- NO inventes información.

- Usa respuestas claras y resumidas.
"""

    else:

        mensaje += """
# CONTEXTO

No se encontró contexto relevante
en los documentos.

Puedes responder usando
conocimiento general.

IMPORTANTE:
- Aclara que la respuesta NO viene
  de documentos RAG.
"""

    # ==========================
    # HISTORIAL RECIENTE
    # ==========================

    for h in historial[-2:]:

        pregunta_hist = h[
            "usuario"
        ][:120]

        respuesta_hist = h[
            "respuesta"
        ][:200]

        mensaje += f"""

Pregunta previa:
{pregunta_hist}

Respuesta previa:
{respuesta_hist}
"""

    # ==========================
    # PREGUNTA ACTUAL
    # ==========================

    mensaje += f"""

# PREGUNTA

{pregunta[:300]}

# INSTRUCCIONES

- Responde claro y resumido.
- Explica solo lo importante.
- Usa ejemplos pequeños.
- Usa Markdown.
- No hagas respuestas demasiado largas.

# RESPUESTA
"""

    # ==========================
    # MEJORAS SEGÚN PREGUNTA
    # ==========================

    pregunta_lower = pregunta.lower()

    if "join" in pregunta_lower:

        mensaje += """

IMPORTANTE:
- Explica diferencia con INNER JOIN
- Incluye ejemplo SQL corto
"""

    if "python" in pregunta_lower:

        mensaje += """

IMPORTANTE:
Incluye un ejemplo corto en Python.
"""

    if "algoritmo" in pregunta_lower:

        mensaje += """

IMPORTANTE:
Explica el algoritmo paso a paso.
"""

    # ==========================
    # GENERAR RESPUESTA
    # ==========================

    try:

        response = ollama.chat(

            model=MODEL_NAME,

            messages=[

                {
                    "role": "system",
                    "content": system_instruction
                },

                {
                    "role": "user",
                    "content": mensaje
                }
            ],

            options={

                "temperature": 0.5,
                "num_predict": 350,
                "top_p": 0.9,
                "top_k": 40,
                "repeat_penalty": 1.1
            }
        )

        # ======================
        # RESPUESTA MODELO
        # ======================

        respuesta_texto = response[
            "message"
        ][
            "content"
        ]

        # ======================
        # INFO RAG
        # ======================

        if hay_similitud:

            respuesta_texto += f"""

---

# 📚 Información RAG

✅ Se utilizó información
de la base documental.

📄 Documento utilizado:
{fuente_nombre}

📊 Similitud:
{porcentaje_rag}%

📖 Fragmento recuperado:
{preview_texto[:120]}...
"""

        else:

            respuesta_texto += """

---

# 📚 Información RAG

⚠️ No se encontró contexto relevante
en la base documental.

La respuesta fue generada usando
conocimiento general del modelo.

📄 Documento utilizado:
Ninguno
"""

        # ======================
        # LIMITAR RESPUESTA
        # ======================

        if len(respuesta_texto) > 2200:

            respuesta_texto = (
                respuesta_texto[:2200]
                + "\n\n[Respuesta truncada]"
            )

        
    # ==========================
    # ERROR OLLAMA
    # ==========================

    except Exception as e:

        error_msg = str(e)

        print(
            "❌ Error Ollama:",
            error_msg
        )

        if hay_similitud:

            contexto_local = rag_result[
                "context"
            ][:1000]

            respuesta_texto = f"""
# ⚠️ Ollama no disponible

El sistema RAG encontró información relevante.

# 📚 Contexto recuperado

{contexto_local}

# ❓ Pregunta

{pregunta}
"""

        else:

            respuesta_texto = """
⚠️ Error al generar respuesta.

Verifica que:

✅ Ollama esté abierto
✅ El modelo esté instalado
✅ El servicio esté ejecutándose
"""

    # ==========================
    # GUARDAR CACHE
    # ==========================

    respuestas_cache[
        pregunta_normalizada
    ] = respuesta_texto

    # Limitar caché

    if len(respuestas_cache) > 50:

        primera = list(
            respuestas_cache.keys()
        )[0]

        del respuestas_cache[
            primera
        ]

    # ==========================
    # GUARDAR HISTORIAL
    # ==========================

    agregar_interaccion(

        pregunta[:300],

        respuesta_texto[:1200]
    )

    # ==========================
    # GUARDAR FUENTES RAG
    # ==========================

    if hay_similitud:

        historial_actual = (
            cargar_historial()
        )

        if historial_actual:

            historial_actual[-1][
                "rag_sources"
            ] = [

                {
                    "source": s[0][
                        "metadata"
                    ].get(
                        "source",
                        "desconocido"
                    ),

                    "similarity": round(
                        s[1],
                        3
                    )
                }

                for s in rag_result[
                    "sources"
                ][:3]
            ]

            guardar_historial(
                historial_actual
            )

    # ==========================
    # RETORNAR
    # ==========================

    return respuesta_texto

# ==============================
# ESTADÍSTICAS CACHE
# ==============================

def get_cache_stats():

    total = (
        cache_hits +
        cache_misses
    )

    return {

        "cache_size": len(
            respuestas_cache
        ),

        "hits": cache_hits,

        "misses": cache_misses,

        "hit_rate": round(
            (cache_hits / total) * 100,
            2
        ) if total > 0 else 0
    }