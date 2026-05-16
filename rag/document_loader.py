# rag/document_loader.py
import os
import re
from typing import List, Dict
from rag.config import RAGConfig

# Nuevas importaciones
try:
    from pypdf import PdfReader
    PDF_AVAILABLE = True
except ImportError:
    PDF_AVAILABLE = False
    print("⚠️ pypdf no instalado. Los PDF no se podrán leer. Instala: pip install pypdf")

try:
    from docx import Document
    DOCX_AVAILABLE = True
except ImportError:
    DOCX_AVAILABLE = False
    print("⚠️ python-docx no instalado. Los DOCX no se podrán leer. Instala: pip install python-docx")

try:
    import markdown
    from bs4 import BeautifulSoup
    MD_AVAILABLE = True
except ImportError:
    MD_AVAILABLE = False
    print("⚠️ markdown no instalado. Los MD se leerán como texto plano.")

try:
    import pandas as pd
    CSV_AVAILABLE = True
except ImportError:
    CSV_AVAILABLE = False
    print("⚠️ pandas no instalado. Los CSV no se podrán leer. Instala: pip install pandas")

class DocumentLoader:
    """Carga documentos desde diferentes formatos (txt, pdf, docx, md, csv)"""
    
    def __init__(self):
        self.config = RAGConfig()
        self.documents_dir = self.config.DOCUMENTS_DIR
        
    def load_documents(self) -> List[Dict[str, str]]:
        """Carga todos los documentos del directorio configurado"""
        documents = []
        
        if not os.path.exists(self.documents_dir):
            os.makedirs(self.documents_dir)
            self._create_sample_documents()
            
        for filename in os.listdir(self.documents_dir):
            filepath = os.path.join(self.documents_dir, filename)
            
            # TXT y MD (texto plano)
            if filename.endswith('.txt'):
                documents.extend(self._load_txt(filepath, filename))
            
            # Markdown
            elif filename.endswith('.md'):
                documents.extend(self._load_md(filepath, filename))
            
            # PDF
            elif filename.endswith('.pdf') and PDF_AVAILABLE:
                documents.extend(self._load_pdf(filepath, filename))
            elif filename.endswith('.pdf') and not PDF_AVAILABLE:
                print(f"⚠️ No se pudo cargar {filename}: pip install pypdf")
            
            # Word
            elif filename.endswith('.docx') and DOCX_AVAILABLE:
                documents.extend(self._load_docx(filepath, filename))
            elif filename.endswith('.docx') and not DOCX_AVAILABLE:
                print(f"⚠️ No se pudo cargar {filename}: pip install python-docx")
            
            # CSV
            elif filename.endswith('.csv') and CSV_AVAILABLE:
                documents.extend(self._load_csv(filepath, filename))
            
            # JSON
            elif filename.endswith('.json'):
                documents.extend(self._load_json(filepath, filename))
            
            # HTML
            elif filename.endswith('.html') or filename.endswith('.htm'):
                documents.extend(self._load_html(filepath, filename))
            
            # Otros formatos como texto
            elif filename.endswith('.py') or filename.endswith('.js') or filename.endswith('.java'):
                documents.extend(self._load_code(filepath, filename))
                
        return documents
    
    def _load_txt(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos de texto plano"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
        except UnicodeDecodeError:
            # Intentar con latin-1 si falla UTF-8
            with open(filepath, 'r', encoding='latin-1') as f:
                content = f.read()
                
        return [{
            'content': content,
            'metadata': {
                'source': filename,
                'type': 'text'
            }
        }]
    
    def _load_md(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos Markdown"""
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            
        # Limpiar markdown (opcional)
        if MD_AVAILABLE:
            html = markdown.markdown(content)
            soup = BeautifulSoup(html, 'html.parser')
            text = soup.get_text()
        else:
            text = content
            
        return [{
            'content': text,
            'metadata': {
                'source': filename,
                'type': 'markdown'
            }
        }]
    
    def _load_pdf(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos PDF"""
        try:
            reader = PdfReader(filepath)
            content = ""
            for page in reader.pages:
                page_text = page.extract_text()
                if page_text:
                    content += page_text + "\n"
                
            return [{
                'content': content,
                'metadata': {
                    'source': filename,
                    'type': 'pdf',
                    'pages': len(reader.pages)
                }
            }]
        except Exception as e:
            print(f"❌ Error cargando PDF {filename}: {e}")
            return []
    
    def _load_docx(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos Word (DOCX)"""
        try:
            doc = Document(filepath)
            content = "\n".join([paragraph.text for paragraph in doc.paragraphs])
            
            return [{
                'content': content,
                'metadata': {
                    'source': filename,
                    'type': 'docx'
                }
            }]
        except Exception as e:
            print(f"❌ Error cargando DOCX {filename}: {e}")
            return []
    
    def _load_csv(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos CSV"""
        try:
            df = pd.read_csv(filepath)
            content = df.to_string()
            
            return [{
                'content': content,
                'metadata': {
                    'source': filename,
                    'type': 'csv',
                    'rows': len(df)
                }
            }]
        except Exception as e:
            print(f"❌ Error cargando CSV {filename}: {e}")
            return []
    
    def _load_json(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos JSON"""
        import json
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            content = json.dumps(data, indent=2, ensure_ascii=False)
            
            return [{
                'content': content,
                'metadata': {
                    'source': filename,
                    'type': 'json'
                }
            }]
        except Exception as e:
            print(f"❌ Error cargando JSON {filename}: {e}")
            return []
    
    def _load_html(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos HTML"""
        try:
            from bs4 import BeautifulSoup
            with open(filepath, 'r', encoding='utf-8') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')
            content = soup.get_text()
            
            return [{
                'content': content,
                'metadata': {
                    'source': filename,
                    'type': 'html'
                }
            }]
        except Exception as e:
            print(f"❌ Error cargando HTML {filename}: {e}")
            return []
    
    def _load_code(self, filepath: str, filename: str) -> List[Dict[str, str]]:
        """Carga archivos de código fuente (py, js, java, etc.)"""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            extension = filename.split('.')[-1]
            return [{
                'content': content,
                'metadata': {
                    'source': filename,
                    'type': 'code',
                    'language': extension
                }
            }]
        except Exception as e:
            print(f"❌ Error cargando código {filename}: {e}")
            return []
    
    def _create_sample_documents(self):
        """Crea documentos de ejemplo sobre programación"""
        sample_docs = {
            "programacion_basica.txt": """
# Fundamentos de Programación

## Variables
Una variable es un espacio en la memoria de la computadora donde se almacena un valor.

## Condicionales
Permiten ejecutar diferentes bloques de código según condiciones.

## Bucles
for: itera sobre una secuencia
while: repite mientras una condición sea verdadera
""",
            "sql_basico.txt": """
# SQL Básico

SELECT - Obtiene datos de una tabla
INSERT - Agrega nuevos registros
UPDATE - Modifica registros existentes
DELETE - Elimina registros
"""
        }
        
        os.makedirs(self.documents_dir, exist_ok=True)
        for filename, content in sample_docs.items():
            filepath = os.path.join(self.documents_dir, filename)
            if not os.path.exists(filepath):
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)