import os

class RAGConfig:
    CHUNK_SIZE = 500
    CHUNK_OVERLAP = 50
    TOP_K_RESULTS = 3
    EMBEDDING_MODEL = "all-MiniLM-L6-v2"
    SIMILARITY_THRESHOLD = 0.5
    DOCUMENTS_DIR = "documents"
    VECTOR_DB_DIR = "vector_db"
    
    SYSTEM_PROMPT = """Eres un Tutor Experto en Programación.

INSTRUCCIÓN IMPORTANTE: Responde basándote en el siguiente contexto recuperado de documentos:

{context}

Pregunta: {question}

Reglas:
- Si el contexto tiene la información, úsala y cita la fuente
- Si no hay información relevante, usa tu conocimiento general
- Sé claro y da ejemplos de código cuando sea útil
- Si usaste el contexto, indica 📚 [Fuente: nombre]
"""