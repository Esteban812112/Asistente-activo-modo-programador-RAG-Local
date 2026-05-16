# test_similitud.py
# Pruebas de similitud coseno con lenguaje coloquial

from rag_pipeline import RAGPipeline
import json

rag = RAGPipeline()

# Lista de preguntas de prueba (coloquiales vs técnicas)
preguntas_prueba = [
    {
        "coloquial": "¿cómo pierdo la materia?",
        "tecnica": "cancelación por bajo rendimiento académico"
    },
    {
        "coloquial": "¿me pueden echar de la universidad?",
        "tecnica": "pérdida de cupo académico"
    },
    {
        "coloquial": "¿qué pasa si no entrego trabajos?",
        "tecnica": "normas de evaluación y asignaturas reprobadas"
    },
    {
        "coloquial": "¿cómo me puedo retirar de una clase?",
        "tecnica": "procedimiento de cancelación de asignatura"
    }
]

print("="*60)
print("PRUEBAS DE SIMILITUD COSENO - LENGUAJE COLOQUIAL")
print("="*60)

resultados = []

for prueba in preguntas_prueba:
    print(f"\n📝 Pregunta coloquial: {prueba['coloquial']}")
    
    # Consultar RAG
    resultado = rag.query(prueba['coloquial'])
    
    if resultado['has_context']:
        similitud = resultado['sources'][0][1]
        fuente = resultado['sources'][0][0]['metadata'].get('source', 'desconocido')
        print(f"   ✅ Similitud: {similitud:.2%}")
        print(f"   📚 Fuente: {fuente}")
        print(f"   ✅ Relacionado con: {prueba['tecnica']}")
    else:
        print(f"   ❌ No se encontró contexto")
        print(f"   ⚠️ Necesita agregar documento con '{prueba['tecnica']}'")

print("\n" + "="*60)