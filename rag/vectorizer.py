from sentence_transformers import SentenceTransformer
import numpy as np
from typing import List, Dict
from rag.config import RAGConfig

class LocalVectorizer:
    def __init__(self):
        self.config = RAGConfig()
        print(f"Cargando modelo {self.config.EMBEDDING_MODEL}...")
        self.model = SentenceTransformer(self.config.EMBEDDING_MODEL)
        print("Modelo listo")
        
    def vectorize_chunk(self, chunk: Dict[str, str]) -> np.ndarray:
        return self.model.encode(chunk['content'])
    
    def vectorize_batch(self, chunks: List[Dict[str, str]]) -> List[np.ndarray]:
        texts = [chunk['content'] for chunk in chunks]
        return self.model.encode(texts)