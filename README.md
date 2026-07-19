# GestSudo AI

> **Asistente Inteligente para Gestión de Proyectos Empresariales**

## Resumen Ejecutivo

**GestSudo AI** es el módulo de Inteligencia Artificial de **GestSudo**, plataforma empresarial desarrollada por **Sudo Agile S.A.**

Este proyecto fue desarrollado para el **Challenge Alura Agente** e implementa una arquitectura **Retrieval-Augmented Generation (RAG)** utilizando **Azure OpenAI**, **LangChain**, **FAISS** y **Streamlit** para responder consultas sobre la documentación oficial de GestSudo.

---

## Arquitectura

```text
Usuario -> Streamlit -> LangChain/RAG -> FAISS <-> Azure OpenAI -> Respuesta
```

## Tecnologías

- Python
- Streamlit
- Azure OpenAI (GPT-5-mini)
- text-embedding-3-small
- LangChain
- FAISS
- GitHub

## Estructura

```text
GestSudo-AI
├── app.py
├── streamlit_app.py
├── requirements.txt
├── docs/
│   ├── DOCUMENTACION_DESARROLLADORES.pdf
│   └── DOCUMENTACION_USUARIO.pdf
├── db/faiss_index
├── src/
└── tools/
```

## Documentación

La carpeta `docs/` contiene la documentación oficial utilizada como base de conocimiento del asistente.

## Instalación

```bash
git clone https://github.com/sudoagile/GestSudo-AI.git
cd GestSudo-AI
python -m venv .venv
pip install -r requirements.txt
python app.py
streamlit run streamlit_app.py
```

## Roadmap

- Integración con GestSudo.
- Despliegue en OCI.
- Gestión documental.

## Autor

Eduardo Ramirez De Lama

© Sudo Agile S.A.