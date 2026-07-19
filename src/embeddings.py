"""Generación de embeddings y construcción de índice FAISS con Azure OpenAI."""

from pathlib import Path
from typing import List

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_openai import AzureOpenAIEmbeddings

from src.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_EMBEDDING_API_VERSION,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    FAISS_INDEX_PATH,
)


def crear_embeddings() -> AzureOpenAIEmbeddings:
    """Crea y devuelve la instancia de embeddings de Azure OpenAI."""
    if not AZURE_OPENAI_API_KEY:
        raise ValueError("Falta AZURE_OPENAI_API_KEY en variables de entorno.")
    if not AZURE_OPENAI_ENDPOINT:
        raise ValueError("Falta AZURE_OPENAI_ENDPOINT en variables de entorno.")

    return AzureOpenAIEmbeddings(
        azure_deployment=AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        azure_endpoint=AZURE_OPENAI_ENDPOINT,
        api_key=AZURE_OPENAI_API_KEY,
        api_version=AZURE_OPENAI_EMBEDDING_API_VERSION,
    )


def construir_indice_faiss(chunks: List[Document], index_path: Path = FAISS_INDEX_PATH) -> Path:
    """Construye y guarda un índice FAISS local a partir de chunks."""
    if not chunks:
        raise ValueError("No hay chunks para indexar.")

    embeddings = crear_embeddings()
    vectorstore = FAISS.from_documents(chunks, embeddings)

    index_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_path))
    print(f"Índice FAISS guardado en: {index_path}")

    return index_path
