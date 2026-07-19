"""Chatbot RAG para GestSudo."""

from __future__ import annotations

from pathlib import Path
from typing import TypedDict

from langchain_community.vectorstores import FAISS
from langchain_core.documents import Document
from langchain_core.output_parsers import StrOutputParser
from langchain_core.prompts import ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

from src.config import (
    AZURE_OPENAI_API_KEY,
    AZURE_OPENAI_CHAT_API_VERSION,
    AZURE_OPENAI_CHAT_DEPLOYMENT,
    AZURE_OPENAI_ENDPOINT,
    AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
    FAISS_INDEX_PATH,
)
from src.embeddings import crear_embeddings
from src.prompts import SYSTEM_PROMPT, construir_prompt


class FuenteDocumento(TypedDict):
    """Fuente recuperada por el retriever."""

    documento: str
    pagina: int | None
    fragmento: str


class RespuestaChatbot(TypedDict):
    """Estructura de salida del chatbot."""

    respuesta: str
    fuentes: list[FuenteDocumento]


class SudoAgileChatbot:
    """Asistente RAG que consulta el índice FAISS con Azure OpenAI."""

    def __init__(
        self,
        index_path: Path = FAISS_INDEX_PATH,
        api_key: str | None = AZURE_OPENAI_API_KEY,
        chat_deployment: str = AZURE_OPENAI_CHAT_DEPLOYMENT,
        embedding_deployment: str = AZURE_OPENAI_EMBEDDING_DEPLOYMENT,
        k: int = 4,
    ) -> None:
        if not api_key:
            raise ValueError("Falta AZURE_OPENAI_API_KEY en variables de entorno.")
        if not AZURE_OPENAI_ENDPOINT:
            raise ValueError("Falta AZURE_OPENAI_ENDPOINT en variables de entorno.")

        self.index_path = index_path
        self.chat_deployment = chat_deployment
        self.embedding_deployment = embedding_deployment
        self.k = k
        self.embeddings = crear_embeddings()
        self.vectorstore = self._cargar_vectorstore()
        self.retriever = self.vectorstore.as_retriever(search_kwargs={"k": k})
        self.llm = AzureChatOpenAI(
            azure_deployment=chat_deployment,
            azure_endpoint=AZURE_OPENAI_ENDPOINT,
            api_key=api_key,
            api_version=AZURE_OPENAI_CHAT_API_VERSION,
        )
        self._cadena_respuesta = (
            ChatPromptTemplate.from_messages(
                [
                    ("system", SYSTEM_PROMPT),
                    ("human", "{entrada_usuario}"),
                ]
            )
            | self.llm
            | StrOutputParser()
        )

    def _cargar_vectorstore(self) -> FAISS:
        """Carga el índice FAISS local desde disco."""
        indice_faiss = self.index_path / "index.faiss"
        indice_metadatos = self.index_path / "index.pkl"

        if not indice_faiss.exists() or not indice_metadatos.exists():
            raise FileNotFoundError(
                f"No se encontró el índice FAISS en {self.index_path}. "
                "Ejecuta app.py para generarlo."
            )

        return FAISS.load_local(
            str(self.index_path),
            self.embeddings,
            allow_dangerous_deserialization=True,
        )

    def _formatear_contexto(self, documentos: list[Document]) -> str:
        """Convierte los documentos recuperados en un contexto legible."""
        bloques: list[str] = []

        for indice, documento in enumerate(documentos, start=1):
            metadata = documento.metadata or {}
            fuente = metadata.get("source", "Documento desconocido")
            pagina = metadata.get("page")
            pagina_texto = f", página {pagina + 1}" if isinstance(pagina, int) else ""

            bloques.append(
                f"[{indice}] Fuente: {fuente}{pagina_texto}\n"
                f"{documento.page_content.strip()}"
            )

        return "\n\n".join(bloques)

    def _formatear_fuentes(self, documentos: list[Document]) -> list[FuenteDocumento]:
        """Extrae las fuentes usadas en la respuesta."""
        fuentes: list[FuenteDocumento] = []
        vistos: set[tuple[str, int | None]] = set()

        for documento in documentos:
            metadata = documento.metadata or {}
            fuente = metadata.get("source", "Documento desconocido")
            pagina = metadata.get("page")
            clave = (fuente, pagina if isinstance(pagina, int) else None)

            if clave in vistos:
                continue

            vistos.add(clave)
            fuentes.append(
                FuenteDocumento(
                    documento=fuente,
                    pagina=pagina + 1 if isinstance(pagina, int) else None,
                    fragmento=documento.page_content.strip()[:300],
                )
            )

        return fuentes

    def obtener_estado(self) -> dict[str, object]:
        """Devuelve información útil para el panel de estado."""
        fuentes_unicas: set[str] = set()

        docstore = getattr(self.vectorstore.docstore, "_dict", {})
        chunks_indexados = len(docstore)

        for documento in docstore.values():
            metadata = getattr(documento, "metadata", {}) or {}
            fuente = metadata.get("source")
            if fuente:
                fuentes_unicas.add(str(fuente))

        return {
            "modelo_chat": self.chat_deployment,
            "modelo_embeddings": self.embedding_deployment,
            "documentos_indexados": len(fuentes_unicas),
            "chunks_indexados": chunks_indexados,
            "faiss_disponible": True,
            "ruta_indice": str(self.index_path),
        }

    def preguntar(self, pregunta: str) -> RespuestaChatbot:
        """Consulta el retriever y devuelve respuesta + fuentes."""
        if not pregunta.strip():
            raise ValueError("La pregunta no puede estar vacía.")

        documentos = self.retriever.invoke(pregunta)
        contexto = self._formatear_contexto(documentos)
        entrada_usuario = construir_prompt(pregunta, documentos)

        if not contexto:
            raise ValueError("No se recuperó contexto relevante para la consulta.")

        try:
            respuesta = self._cadena_respuesta.invoke(
                {"entrada_usuario": entrada_usuario}
            )

        except Exception as error:
            import traceback

            print("\n" + "=" * 80)
            print("ERROR COMPLETO DE AZURE OPENAI")
            print("=" * 80)
            traceback.print_exc()
            print("=" * 80 + "\n")

            raise RuntimeError(
                f"Error real de Azure OpenAI:\n{type(error).__name__}: {error}"
            ) from error

        return {
            "respuesta": respuesta,
            "fuentes": self._formatear_fuentes(documentos),
        }