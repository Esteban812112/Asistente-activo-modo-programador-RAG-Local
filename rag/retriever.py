from typing import List, Dict, Tuple
from rag.vectorizer import LocalVectorizer
from rag.vector_store import VectorStore
from rag.config import RAGConfig

class RAGRetriever:
    def __init__(self):
        self.config = RAGConfig()
        self.vectorizer = LocalVectorizer()
        self.vector_store = VectorStore()
        
    def retrieve_context(self, question: str) -> Tuple[str, List[Tuple[Dict[str, str], float]]]:
        q_vector = self.vectorizer.vectorize_chunk({'content': question})
        relevant = self.vector_store.search(q_vector)
        
        if not relevant:
            return "No se encontró información relevante en los documentos.", []
        
        context_parts = []
        for idx, (chunk, sim) in enumerate(relevant, 1):
            source = chunk['metadata'].get('source', 'desconocido')
            context_parts.append(f"[{idx}] Fuente: {source} (relevancia: {sim:.2f})\n{chunk['content']}\n")
        
        return "\n".join(context_parts), relevant