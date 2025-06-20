# app/rag/chain.py
from langchain.chains import RetrievalQA
from langchain_google_genai import ChatGoogleGenerativeAI
from app.rag.vectorstore import create_vectorstore
from app.rag.splitter import split_documents
from app.rag.loader import load_documents
import os

def create_chain():
    """Configura el sistema de consulta especializado en anatomía muscular con RAG."""
    try:
        # 1. Carga de recursos académicos
        medical_docs = load_documents()
        
        # 2. Preparación de contenido médico
        anatomy_chunks = split_documents(medical_docs)
        
        # 3. Creación de base de conocimiento vectorial
        muscle_knowledge_base = create_vectorstore(anatomy_chunks)

        # 4. Configuración del modelo médico
        google_api_key = os.getenv("GOOGLE_API_KEY")
        if not google_api_key:
            raise ValueError("Se requiere API Key de Google para el servicio de consultas médicas")
        
        medical_llm = ChatGoogleGenerativeAI(
            model="gemini-2.0-flash",  # Modelo balanceado para terminología médica
            google_api_key=google_api_key,
            temperature=0.2,  # Menor aleatoriedad para respuestas precisas
            max_output_tokens=720  # Suficiente para explicaciones anatómicas
        )

        # 5. Cadena de consulta especializada
        anatomy_qa_chain = RetrievalQA.from_chain_type(
            llm=medical_llm,
            chain_type="stuff",
            retriever=muscle_knowledge_base.as_retriever(
                search_kwargs={"k": 4}  # 4 chunks óptimos para contexto muscular
            ),
            return_source_documents=True
        )

        return anatomy_qa_chain, medical_llm

    except Exception as e:
        print(f"Error al configurar el sistema de consultas médicas: {str(e)}")
        raise