import os
from rag import DocumentLoader, DocumentChunker, LocalVectorizer, VectorStore, RAGRetriever, RAGConfig

class RAGPipeline:
    def __init__(self):
        self.config = RAGConfig()
        self.document_loader = DocumentLoader()
        self.chunker = DocumentChunker()
        self.vectorizer = LocalVectorizer()
        self.vector_store = VectorStore()
        self.retriever = None
        self._initialize()
        
    def _initialize(self):
        print("Inicializando RAG Pipeline...")
        vector_db_path = self.config.VECTOR_DB_DIR
        
        if os.path.exists(vector_db_path) and os.listdir(vector_db_path):
            print("Cargando vector DB existente...")
            self.vector_store._load()
        else:
            print("Creando nueva vector DB...")
            docs = self.document_loader.load_documents()
            print(f"  - {len(docs)} documentos cargados")
            
            chunks = self.chunker.process_all_documents(docs)
            print(f"  - {len(chunks)} chunks creados")
            
            vectors = self.vectorizer.vectorize_batch(chunks)
            print(f"  - {len(vectors)} vectores generados")
            
            self.vector_store.initialize(chunks, vectors)
            
        self.retriever = RAGRetriever()
        print("RAG Pipeline listo!")
        
    def query(self, question: str) -> dict:
        context, sources = self.retriever.retrieve_context(question)
        return {
            'context': context,
            'sources': sources,
            'has_context': len(sources) > 0
        }
    
    def get_stats(self) -> dict:
        return {
            'chunks': len(self.vector_store.vectors) if self.vector_store.is_initialized else 0,
            'documents_dir': self.config.DOCUMENTS_DIR,
            'model': self.config.EMBEDDING_MODEL
        }