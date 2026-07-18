from pathlib import Path

from langchain_community.document_loaders import TextLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def cargar_documentos():
    carpeta_docs = Path("docs")

    documentos = []

    for archivo in carpeta_docs.glob("*.txt"):
        loader = TextLoader(str(archivo), encoding="utf-8")
        documentos.extend(loader.load())

    return documentos


def dividir_documentos(documentos):
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    return splitter.split_documents(documentos)


if __name__ == "__main__":
    documentos = cargar_documentos()
    chunks = dividir_documentos(documentos)

    print(f"Documentos cargados: {len(documentos)}")
    print(f"Chunks generados: {len(chunks)}\n")

    print("=" * 60)
    print(chunks[0].page_content)