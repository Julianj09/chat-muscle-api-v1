# app/rag/vectorstore.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from typing import List
from langchain.schema import Document

def create_vectorstore(docs: List[Document]) -> FAISS:
    """Crea un índice FAISS de conocimiento anatómico usando embeddings médicos especializados."""
    if not docs:
        raise ValueError("No se encontraron recursos académicos para crear la base de conocimiento.")

    try:
        print("[MuscleAI VectorStore] Generando embeddings médicos con HuggingFace...")
        embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
        vectorstore = FAISS.from_documents(docs, embeddings)
        print("[MuscleAI VectorStore] Base de conocimiento muscular creada exitosamente.")
        return vectorstore
    except IndexError:
        raise RuntimeError("Error: Los recursos médicos no contienen contenido procesable.")
    except Exception as e:
        raise RuntimeError(f"Error al construir la base de conocimiento anatómico: {str(e)}")