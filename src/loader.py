from pathlib import Path

from langchain_community.document_loaders import TextLoader


def cargar_documentos():
    """
    Carga todos los archivos .txt ubicados en la carpeta docs.
    """

    carpeta_docs = Path("docs")

    documentos = []

    for archivo in carpeta_docs.glob("*.txt"):
        loader = TextLoader(str(archivo), encoding="utf-8")
        documentos.extend(loader.load())

    return documentos


if __name__ == "__main__":
    docs = cargar_documentos()

    print(f"Se cargaron {len(docs)} documentos.\n")

    for doc in docs:
        print("=" * 60)
        print(doc.metadata["source"])
        print(doc.page_content[:500])