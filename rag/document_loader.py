import os
from typing import List, Dict
from rag.config import RAGConfig

class DocumentLoader:
    def __init__(self):
        self.config = RAGConfig()
        
    def load_documents(self) -> List[Dict[str, str]]:
        documents = []
        if not os.path.exists(self.config.DOCUMENTS_DIR):
            os.makedirs(self.config.DOCUMENTS_DIR)
            self._create_sample_documents()
            
        for filename in os.listdir(self.config.DOCUMENTS_DIR):
            filepath = os.path.join(self.config.DOCUMENTS_DIR, filename)
            if filename.endswith('.txt'):
                with open(filepath, 'r', encoding='utf-8') as f:
                    content = f.read()
                documents.append({
                    'content': content,
                    'metadata': {'source': filename, 'type': 'text'}
                })
        return documents
    
    def _create_sample_documents(self):
        sample = {
            "variables_python.txt": """
# Variables en Python
Una variable es un contenedor para almacenar datos.
Ejemplo:
nombre = "Juan"
edad = 25
altura = 1.75
Python infiere el tipo automáticamente.
""",
            "condicionales.txt": """
# Estructuras condicionales
if condición:
    # código si es verdadero
else:
    # código si es falso
    
Ejemplo:
if edad >= 18:
    print("Mayor de edad")
else:
    print("Menor de edad")
""",
            "bucles.txt": """
# Bucles en programación
for elemento in lista:
    print(elemento)
    
while condicion:
    # se repite mientras sea verdad
    contador += 1
"""
        }
        for name, content in sample.items():
            with open(os.path.join(self.config.DOCUMENTS_DIR, name), 'w', encoding='utf-8') as f:
                f.write(content)