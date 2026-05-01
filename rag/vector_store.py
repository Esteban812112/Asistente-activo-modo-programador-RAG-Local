import os
import pickle
import numpy as np
from typing import List, Dict, Tuple
from rag.config import RAGConfig

class VectorStore:
    def __init__(self):
        self.config = RAGConfig()
        self.vectors = []
        self.metadata = []
        self.is_initialized = False
        
    def initialize(self, chunks: List[Dict[str, str]], vectors: List[np.ndarray]):
        self.vectors = vectors
        self.metadata = chunks
        self.is_initialized = True
        self._save()
        
    def search(self, query_vector: np.ndarray, top_k: int = None) -> List[Tuple[Dict[str, str], float]]:
        if not self.is_initialized:
            self._load()
            if not self.is_initialized:
                return []
        
        if top_k is None:
            top_k = self.config.TOP_K_RESULTS
            
        similarities = []
        for idx, vec in enumerate(self.vectors):
            sim = np.dot(query_vector, vec) / (np.linalg.norm(query_vector) * np.linalg.norm(vec))
            if sim >= self.config.SIMILARITY_THRESHOLD:
                similarities.append((idx, sim))
        
        similarities.sort(key=lambda x: x[1], reverse=True)
        
        return [(self.metadata[idx], sim) for idx, sim in similarities[:top_k]]
    
    def _save(self):
        os.makedirs(self.config.VECTOR_DB_DIR, exist_ok=True)
        data = {
            'vectors': [v.tolist() for v in self.vectors],
            'metadata': self.metadata
        }
        with open(os.path.join(self.config.VECTOR_DB_DIR, 'vectors.pkl'), 'wb') as f:
            pickle.dump(data, f)
        print(f"Vector DB guardada en {self.config.VECTOR_DB_DIR}")
    
    def _load(self):
        path = os.path.join(self.config.VECTOR_DB_DIR, 'vectors.pkl')
        if os.path.exists(path):
            with open(path, 'rb') as f:
                data = pickle.load(f)
            self.vectors = [np.array(v) for v in data['vectors']]
            self.metadata = data['metadata']
            self.is_initialized = True
            print(f"Vector DB cargada: {len(self.vectors)} chunks")