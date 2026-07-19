"""Configuración de la aplicación."""

from pathlib import Path
import os

from dotenv import load_dotenv

load_dotenv()

# Endpoint de Azure OpenAI
AZURE_OPENAI_ENDPOINT = os.getenv("AZURE_OPENAI_ENDPOINT")

# API Key de Azure OpenAI
AZURE_OPENAI_API_KEY = os.getenv("AZURE_OPENAI_API_KEY")

# Deployment de chat (GPT)
AZURE_OPENAI_CHAT_DEPLOYMENT = os.getenv("AZURE_OPENAI_CHAT_DEPLOYMENT", "gpt-5-mini")

# Deployment de embeddings
AZURE_OPENAI_EMBEDDING_DEPLOYMENT = os.getenv(
    "AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-small"
)

# Versión de la API para chat
AZURE_OPENAI_CHAT_API_VERSION = os.getenv(
    "AZURE_OPENAI_CHAT_API_VERSION", "2025-04-01-preview"
)

# Versión de la API para embeddings
AZURE_OPENAI_EMBEDDING_API_VERSION = os.getenv(
    "AZURE_OPENAI_EMBEDDING_API_VERSION", "2023-05-15"
)

# Ruta donde se almacena el índice FAISS
FAISS_INDEX_PATH = Path("db") / "faiss_index"