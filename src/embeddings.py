"""Generacion de embeddings y construccion de indice FAISS."""

from pathlib import Path
from typing import List

import requests
from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.embeddings import Embeddings

from src.config import FAISS_INDEX_PATH, GOOGLE_API_KEY, GEMINI_EMBEDDING_MODEL


class GeminiEmbeddings(Embeddings):
    """Implementacion de embeddings usando la API de Gemini."""

    def __init__(self, api_key: str, model: str, timeout: int = 60):
        self.api_key = api_key
        self.model = model
        self.timeout = timeout

    def _embed_text(self, text: str) -> List[float]:
        if not text:
            text = " "

        endpoint = (
            f"https://generativelanguage.googleapis.com/v1beta/models/"
            f"{self.model.replace('models/', '')}:embedContent?key={self.api_key}"
        )
        payload = {
            "model": self.model,
            "content": {"parts": [{"text": text}]},
        }
        response = requests.post(endpoint, json=payload, timeout=self.timeout)
        response.raise_for_status()
        data = response.json()

        values = data.get("embedding", {}).get("values")
        if not values:
            raise ValueError("La respuesta de Gemini no incluyo valores de embedding.")
        return values

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        return [self._embed_text(text) for text in texts]

    def embed_query(self, text: str) -> List[float]:
        return self._embed_text(text)


def construir_indice_faiss(chunks: List[Document], index_path: Path = FAISS_INDEX_PATH) -> Path:
    """Construye y guarda un indice FAISS local a partir de chunks."""
    if not GOOGLE_API_KEY:
        raise ValueError("Falta GOOGLE_API_KEY en variables de entorno.")

    if not chunks:
        raise ValueError("No hay chunks para indexar.")

    embeddings = GeminiEmbeddings(
        api_key=GOOGLE_API_KEY,
        model=GEMINI_EMBEDDING_MODEL,
    )
    vectorstore = FAISS.from_documents(chunks, embeddings)

    index_path.mkdir(parents=True, exist_ok=True)
    vectorstore.save_local(str(index_path))
    print(f"Indice FAISS guardado en: {index_path}")

    return index_path
