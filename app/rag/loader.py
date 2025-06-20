# app/rag/loader.py
from langchain_community.document_loaders import TextLoader, PyPDFLoader
from langchain.schema import Document
from typing import List
import os
import glob

def load_documents(path: str = "app/rag/data") -> List[Document]:
    """Carga documentos médicos (.txt) y PDF (.pdf) sobre anatomía muscular."""
    try:
        print(f"[MuscleAI Loader] Buscando recursos académicos en: {os.path.abspath(path)}")
        documents: List[Document] = []

        # Cargar archivos .txt (guías musculares)
        txt_files = glob.glob(os.path.join(path, "**/*.txt"), recursive=True)
        for file_path in txt_files:
            loader = TextLoader(file_path, autodetect_encoding=True)
            documents.extend(loader.load())

        # Cargar archivos .pdf (libros de fisioterapia)
        pdf_files = glob.glob(os.path.join(path, "**/*.pdf"), recursive=True)
        for file_path in pdf_files:
            loader = PyPDFLoader(file_path)
            documents.extend(loader.load())

        print(f"[MuscleAI Loader] Recursos académicos cargados: {len(documents)}")

        if not documents:
            print("[MuscleAI Loader] ⚠️ No se encontraron documentos de anatomía muscular.")

        return documents

    except Exception as e:
        raise RuntimeError(f"[MuscleAI Loader] Error cargando recursos médicos: {str(e)}")