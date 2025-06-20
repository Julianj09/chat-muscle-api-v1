# app/rag/splitter.py
from langchain.text_splitter import RecursiveCharacterTextSplitter
from typing import List
from langchain.schema import Document

def split_documents(documents: List[Document]) -> List[Document]:
    """Divide contenido médico en chunks para procesamiento con IA."""
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=500,  # Ideal para retener conceptos anatómicos completos
        chunk_overlap=100,  # Mantiene contexto entre músculos relacionados
        length_function=len,
        add_start_index=True  # Útil para referenciar ubicaciones en textos médicos
    )
    chunks = splitter.split_documents(documents)
    print(f"[MuscleAI Splitter] {len(chunks)} segmentos de conocimiento médico generados.")
    return chunks