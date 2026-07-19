from pathlib import Path

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter


def cargar_documentos():
    """
    Carga todos los archivos PDF ubicados en la carpeta docs.
    """
    documentos = []

    carpeta_docs = Path("docs")

    for archivo in carpeta_docs.glob("*.pdf"):
        print(f"Cargando: {archivo.name}")

        loader = PyPDFLoader(str(archivo))
        documentos.extend(loader.load())

    print(f"Total de páginas cargadas: {len(documentos)}")

    return documentos


def dividir_documentos(documentos):
    """
    Divide los documentos en fragmentos (chunks).
    """
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )

    chunks = splitter.split_documents(documentos)

    print(f"Total de chunks: {len(chunks)}")

    return chunks


if __name__ == "__main__":
    documentos = cargar_documentos()
    dividir_documentos(documentos)