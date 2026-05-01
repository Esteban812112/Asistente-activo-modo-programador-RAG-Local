from typing import List, Dict
from rag.config import RAGConfig


class DocumentChunker:

    def __init__(self):

        self.config = RAGConfig()

    # ==========================================
    # LIMPIAR TEXTO
    # ==========================================

    def clean_text(self, text: str) -> str:

        # Eliminar espacios extras
        text = text.replace("\t", " ")

        # Normalizar saltos
        text = text.replace("\r", "\n")

        # Eliminar múltiples líneas vacías
        while "\n\n\n" in text:
            text = text.replace("\n\n\n", "\n\n")

        return text.strip()

    # ==========================================
    # DIVIDIR DOCUMENTO EN CHUNKS
    # ==========================================

    def chunk_document(
        self,
        document: Dict[str, str]
    ) -> List[Dict[str, str]]:

        content = self.clean_text(
            document["content"]
        )

        metadata = document["metadata"]

        chunks = []

        # ======================================
        # DIVIDIR POR PÁRRAFOS
        # ======================================

        paragraphs = content.split("\n\n")

        current_chunk = ""

        chunk_id = 0

        # ======================================
        # CREAR CHUNKS
        # ======================================

        for para in paragraphs:

            para = para.strip()

            if not para:
                continue

            # ==============================
            # SI EL CHUNK YA ES GRANDE
            # ==============================

            if (
                len(current_chunk) + len(para)
                > self.config.CHUNK_SIZE
                and current_chunk
            ):

                chunks.append({

                    "content": current_chunk.strip(),

                    "metadata": {

                        **metadata,

                        "chunk_id": chunk_id,

                        "chunk_size": len(current_chunk)
                    }
                })

                chunk_id += 1

                # ==================================
                # OVERLAP MÁS INTELIGENTE
                # ==================================

                overlap_text = current_chunk[
                    -self.config.CHUNK_OVERLAP:
                ]

                current_chunk = overlap_text + "\n\n"

            # ==============================
            # AGREGAR PÁRRAFO
            # ==============================

            current_chunk += para + "\n\n"

        # ======================================
        # GUARDAR ÚLTIMO CHUNK
        # ======================================

        if current_chunk.strip():

            chunks.append({

                "content": current_chunk.strip(),

                "metadata": {

                    **metadata,

                    "chunk_id": chunk_id,

                    "chunk_size": len(current_chunk)
                }
            })

        # ======================================
        # DEBUG
        # ======================================

        print(
            f"📄 Documento: {metadata.get('source', 'desconocido')}"
        )

        print(
            f"🧩 Chunks generados: {len(chunks)}"
        )

        return chunks

    # ==========================================
    # PROCESAR TODOS LOS DOCUMENTOS
    # ==========================================

    def process_all_documents(
        self,
        documents: List[Dict[str, str]]
    ) -> List[Dict[str, str]]:

        all_chunks = []

        print("\n📚 Procesando documentos...\n")

        for doc in documents:

            doc_chunks = self.chunk_document(doc)

            all_chunks.extend(doc_chunks)

        print(
            f"\n✅ Total de chunks generados: {len(all_chunks)}\n"
        )

        return all_chunks