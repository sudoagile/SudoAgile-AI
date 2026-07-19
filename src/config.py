"""Configuración de la aplicación."""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
GEMINI_EMBEDDING_MODEL = os.getenv(
    "GEMINI_EMBEDDING_MODEL",
    "gemini-embedding-001"
)

FAISS_INDEX_PATH = Path("db") / "faiss_index"