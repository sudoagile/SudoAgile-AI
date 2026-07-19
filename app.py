from src.embeddings import construir_indice_faiss
from src.loader import cargar_documentos, dividir_documentos


def main():
    documentos = cargar_documentos()
    chunks = dividir_documentos(documentos)
    construir_indice_faiss(chunks)
    print("Pipeline completado: PDF -> chunks -> embeddings Azure OpenAI -> FAISS.")


if __name__ == "__main__":
    main()
