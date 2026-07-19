# SudoAgile-AI

Pipeline de indexacion vectorial con Gemini + FAISS:

```text
PDF -> PyPDFLoader -> Chunks -> Embeddings Gemini -> FAISS -> db/faiss_index
```

## Requisitos

1. Variable de entorno `GEMINI_API_KEY`.
2. Dependencias instaladas desde `requirements.txt`.

Opcional:

- `GEMINI_EMBEDDING_MODEL` (default: `gemini-embedding-001`).

## Ejecucion

```bash
py -3 app.py
```

Al finalizar, el indice se guarda en `db/faiss_index`.
