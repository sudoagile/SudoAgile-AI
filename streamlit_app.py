"""Interfaz web de GestSudo con Streamlit."""

from __future__ import annotations

import streamlit as st

from src.chatbot import SudoAgileChatbot


st.set_page_config(
    page_title="GestSudo",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)


def _inicializar_chatbot() -> SudoAgileChatbot | None:
    """Inicializa el chatbot y captura errores de arranque."""
    try:
        return SudoAgileChatbot()
    except Exception as error:  # noqa: BLE001
        st.sidebar.error(f"No fue posible cargar el sistema: {error}")
        return None


def _render_sidebar(chatbot: SudoAgileChatbot | None) -> None:
    """Muestra el estado del sistema en la barra lateral."""
    st.sidebar.title("Estado del sistema")

    if chatbot is None:
        st.sidebar.warning("El índice no está disponible.")
        return

    estado = chatbot.obtener_estado()

    st.sidebar.success("Sistema operativo")
    st.sidebar.markdown(f"**Modelo Azure OpenAI:** {estado['modelo_chat']}")
    st.sidebar.markdown(f"**Embeddings:** {estado['modelo_embeddings']}")
    st.sidebar.markdown(f"**Documentos indexados:** {estado['documentos_indexados']}")
    st.sidebar.markdown(f"**Cantidad de chunks:** {estado['chunks_indexados']}")
    st.sidebar.markdown(
        f"**Estado FAISS:** {'Disponible' if estado['faiss_disponible'] else 'No disponible'}"
    )
    st.sidebar.caption(f"Ruta índice: {estado['ruta_indice']}")


def main() -> None:
    """Punto de entrada de la interfaz."""
    chatbot = _inicializar_chatbot()
    _render_sidebar(chatbot)

    st.title("GestSudo")
    st.subheader("Asistente Inteligente para Gestión de Proyectos Empresariales")
    st.caption("Interfaz corporativa para consultas RAG sobre documentos internos.")

    if "historial" not in st.session_state:
        st.session_state.historial = []

    for mensaje in st.session_state.historial:
        with st.chat_message(mensaje["rol"]):
            st.markdown(mensaje["contenido"])

    pregunta = st.text_area(
        "Haz tu consulta",
        placeholder="Escribe tu pregunta sobre documentos, procesos o proyectos...",
        height=120,
    )

    if st.button("Preguntar", type="primary", use_container_width=True):
        if chatbot is None:
            st.error("El chatbot no está disponible. Revisa el índice FAISS y la API key.")
            return

        if not pregunta.strip():
            st.warning("Escribe una pregunta antes de continuar.")
            return

        st.session_state.historial.append({"rol": "user", "contenido": pregunta})

        with st.chat_message("user"):
            st.markdown(pregunta)

        with st.chat_message("assistant"):
            with st.spinner("Consultando Azure OpenAI y recuperando contexto..."):
                try:
                    resultado = chatbot.preguntar(pregunta)
                except Exception as error:  # noqa: BLE001
                    st.error(f"No se pudo generar la respuesta: {error}")
                    return

            st.markdown(resultado["respuesta"])
            st.markdown("**Fuentes utilizadas**")

            if resultado["fuentes"]:
                for fuente in resultado["fuentes"]:
                    pagina = fuente["pagina"] if fuente["pagina"] is not None else "N/D"
                    st.write(f"- {fuente['documento']} | página {pagina}")
            else:
                st.write("No se recuperaron fuentes.")

        st.session_state.historial.append(
            {
                "rol": "assistant",
                "contenido": resultado["respuesta"],
            }
        )


if __name__ == "__main__":
    main()
