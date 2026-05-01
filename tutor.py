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
# CONFIG MODELO LOCAL
# ==============================

MODEL_NAME = "gemma3:1b"

# ==============================
# CACHÉ
# ==============================

respuestas_cache = {}

cache_hits = 0
cache_misses = 0

# ==============================
# SYSTEM PROMPT
# ==============================

system_instruction = """
Eres un Tutor experto en Programación.

OBJETIVO:
- Explicar conceptos de programación.
- Responder de forma clara y educativa.
- Utilizar el contexto RAG como fuente principal.

REGLAS:
- NO inventes información.
- Si existe contexto RAG, úsalo.
- Responde corto y claro.
- Usa ejemplos simples.
- Si la pregunta no tiene relación con programación,
  indícalo educadamente.
"""

# ==============================
# PALABRAS CLAVE
# ==============================

PALABRAS_PROGRAMACION = [

    "python",
    "sql",
    "java",
    "javascript",
    "html",
    "css",
    "programacion",
    "algoritmo",
    "codigo",
    "funcion",
    "variable",
    "base de datos",
    "join",
    "api",
    "backend",
    "frontend",
    "flask",
    "react",
    "lista",
    "diccionario",
    "loop",
    "for",
    "while",
    "if",
    "else",
    "poo",
    "objeto",
    "clase",
    "excepcion",
    "error",
    "debug",

    # NUEVAS
    "practica",
    "practicas",
    "modulo",
    "modulos",
    "paquete",
    "archivo",
    "rendimiento",
    "software",
    "desarrollo",
    "sistema",
    "datos",
    "contraseña",
    "recursividad",
    "recursivo",
    "lambda",
    "decorador",
    "generador",
    "yield"
]

# ==============================
# VALIDAR TEMA
# ==============================

def es_tema_programacion(texto):

    texto = texto.lower()

    coincidencias = sum(
        1 for palabra in PALABRAS_PROGRAMACION
        if palabra in texto
    )

    return coincidencias >= 1

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
    # CACHÉ
    # ==========================

    if pregunta_normalizada in respuestas_cache:

        cache_hits += 1

        print(f"💾 Caché usado | Hits: {cache_hits}")

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

    tiene_contexto = rag_result[
        "has_context"
    ]

    # ==========================
    # VALIDAR SIMILITUD
    # ==========================

    similaridad_minima = 0.30

    hay_similitud = False

    if tiene_contexto:

        try:

            score = rag_result[
                "sources"
            ][0][1]

            print(
                f"📊 Similaridad encontrada: {score}"
            )

            if score >= similaridad_minima:

                hay_similitud = True

        except Exception as e:

            print(
                "⚠️ Error validando similitud:",
                e
            )

    # ==========================
    # VALIDAR TEMA
    # ==========================

    tema_programacion = (
        es_tema_programacion(
            pregunta
        )
    )

    # ==========================
    # BLOQUEAR SI NO ES RELEVANTE
    # ==========================

    if not hay_similitud and not tema_programacion:

        respuesta_texto = f"""
⚠️ No se encontró información relacionada
en la base de conocimiento RAG.

Este asistente está especializado en:

✅ Programación
✅ Python
✅ SQL
✅ Bases de datos
✅ Algoritmos
✅ Desarrollo de software

Pregunta recibida:
"{pregunta}"

Por favor realiza una pregunta relacionada
con programación o los documentos cargados.
"""

        return respuesta_texto

    # ==========================
    # HISTORIAL
    # ==========================

    historial = cargar_historial()

    # ==========================
    # PROMPT
    # ==========================

    mensaje = ""

    # ==========================
    # CONTEXTO RAG
    # ==========================

    if hay_similitud:

        contexto = rag_result[
            "context"
        ][:900]

        mensaje += f"""
CONTEXTO RAG:

{contexto}

"""

    # ==========================
    # HISTORIAL RECIENTE
    # ==========================

    for h in historial[-1:]:

        pregunta_hist = h[
            "usuario"
        ][:80]

        respuesta_hist = h[
            "respuesta"
        ][:120]

        mensaje += f"""
E: {pregunta_hist}
T: {respuesta_hist}
"""

    # ==========================
    # PREGUNTA ACTUAL
    # ==========================

    mensaje += f"""

Pregunta:
{pregunta[:200]}

Respuesta:
"""

    # ==========================
    # PROMPT FINAL
    # ==========================

    prompt_final = f"""
{system_instruction}

{mensaje}
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

                "temperature": 0.2,

                "num_predict": 250,

                "top_p": 0.8,

                "top_k": 20
            }
        )

        respuesta_texto = response[
            "message"
        ][
            "content"
        ]

        # ======================
        # 🆕 AVISO SI NO SE USÓ RAG
        # ======================

        if not hay_similitud:

            aviso = """

⚠️ Nota:
Esta respuesta fue generada por el modelo de IA
y NO se encontró información relevante en la base de datos (RAG).

Puede no estar basada en los documentos cargados.
"""

            respuesta_texto = respuesta_texto + aviso

        # ======================
        # LIMITAR RESPUESTA
        # ======================

        if len(respuesta_texto) > 1200:

            respuesta_texto = (
                respuesta_texto[:1200]
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

        # ======================
        # FALLBACK RAG
        # ======================

        if hay_similitud:

            contexto_local = rag_result[
                "context"
            ][:700]

            respuesta_texto = f"""
⚠️ Ollama no disponible.

📚 Información encontrada
en documentos locales:

{contexto_local}

-----------------------------------

Pregunta:
{pregunta}

✅ El sistema RAG recuperó información correctamente.
"""

        else:

            respuesta_texto = """
⚠️ Error al generar respuesta.

Verifica que:

✅ Ollama esté abierto
✅ El modelo gemma3:1b esté instalado
✅ El servicio Ollama esté ejecutándose
"""

    # ==========================
    # GUARDAR EN CACHÉ
    # ==========================

    respuestas_cache[
        pregunta_normalizada
    ] = respuesta_texto

    # Limitar tamaño caché

    if len(respuestas_cache) > 50:

        primera = list(
            respuestas_cache.keys()
        )[0]

        del respuestas_cache[primera]

    # ==========================
    # GUARDAR HISTORIAL
    # ==========================

    agregar_interaccion(

        pregunta[:300],

        respuesta_texto[:1000]
    )

    # ==========================
    # GUARDAR FUENTES
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
# ESTADÍSTICAS
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