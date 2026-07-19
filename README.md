# GestSudo AI

> **Asistente Inteligente Empresarial basado en Retrieval-Augmented
> Generation (RAG)**

![Python](https://img.shields.io/badge/Python-3.12-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-Web-red)
![LangChain](https://img.shields.io/badge/LangChain-RAG-green)
![FAISS](https://img.shields.io/badge/FAISS-Vector_Search-orange)
![Azure OpenAI](https://img.shields.io/badge/Azure-OpenAI-0078D4) ![AWS
EC2](https://img.shields.io/badge/AWS-EC2-FF9900)

------------------------------------------------------------------------

# 1. Descripción del proyecto

**GestSudo AI** es el módulo de Inteligencia Artificial de la plataforma
empresarial **GestSudo**, desarrollado para responder consultas sobre
documentación técnica y funcional mediante lenguaje natural.

La solución implementa una arquitectura **Retrieval-Augmented Generation
(RAG)** que combina **Azure OpenAI**, **LangChain**, **FAISS**,
**PyPDFLoader** y **Streamlit** para ofrecer respuestas contextualizadas
a partir de la documentación oficial del sistema.

Este proyecto fue desarrollado como entrega final del **Challenge de
Inteligencia Artificial de Alura Latam**.

------------------------------------------------------------------------

# 2. Arquitectura de la solución

``` text
                         Usuario
                            │
                            ▼
                 Interfaz Web (Streamlit)
                            │
                            ▼
                Orquestador LangChain (RAG)
                            │
         ┌──────────────────┴──────────────────┐
         │                                     │
         ▼                                     ▼
 Índice Vectorial FAISS             Azure OpenAI
                             GPT-5 Mini + Embeddings
         └──────────────────┬──────────────────┘
                            ▼
                 Respuesta Contextualizada
```

------------------------------------------------------------------------

# 3. Tecnologías utilizadas

  Componente             Tecnología
  ---------------------- -------------------------
  Lenguaje               Python 3
  Interfaz Web           Streamlit
  Modelo de IA           Azure OpenAI GPT-5 Mini
  Embeddings             text-embedding-3-small
  Framework              LangChain
  Base Vectorial         FAISS
  Carga de documentos    PyPDFLoader
  Infraestructura        Amazon EC2
  Control de versiones   Git y GitHub

------------------------------------------------------------------------

# 4. Estructura del proyecto

``` text
SudoAgile-AI/
│
├── app.py                    # Generación del índice FAISS
├── streamlit_app.py          # Aplicación web
├── requirements.txt
├── .env
├── docs/
│   ├── DOCUMENTACION_DESARROLLADORES.pdf
│   └── DOCUMENTACION_USUARIO.pdf
├── db/
│   └── faiss_index/
├── src/
│   ├── chatbot.py
│   ├── config.py
│   ├── embeddings.py
│   ├── loader.py
│   └── prompts.py
└── tools/
```

------------------------------------------------------------------------

# 5. Flujo de procesamiento RAG

1.  Carga de la documentación en formato PDF.
2.  División del contenido en fragmentos (chunks).
3.  Generación de embeddings mediante Azure OpenAI.
4.  Creación del índice vectorial con FAISS.
5.  Recepción de la consulta del usuario.
6.  Búsqueda semántica de los fragmentos más relevantes.
7.  Construcción del contexto para el modelo.
8.  Generación de la respuesta utilizando GPT-5 Mini.

------------------------------------------------------------------------

# 6. Instalación

``` bash
git clone https://github.com/sudoagile/SudoAgile-AI.git

cd SudoAgile-AI

python -m venv .venv

pip install -r requirements.txt
```

------------------------------------------------------------------------

# 7. Variables de entorno

``` env
AZURE_OPENAI_ENDPOINT=
AZURE_OPENAI_API_KEY=
AZURE_OPENAI_CHAT_DEPLOYMENT=
AZURE_OPENAI_EMBEDDING_DEPLOYMENT=
AZURE_OPENAI_CHAT_API_VERSION=
AZURE_OPENAI_EMBEDDING_API_VERSION=
```

------------------------------------------------------------------------

# 8. Construcción del índice vectorial

``` bash
python app.py
```

------------------------------------------------------------------------

# 9. Ejecución de la aplicación

``` bash
streamlit run streamlit_app.py
```

------------------------------------------------------------------------

# 10. Despliegue

## Azure OpenAI

Servicios utilizados:

-   GPT-5 Mini
-   text-embedding-3-small
-   Azure AI Foundry
-   Grupo de Recursos de Azure

**Capturas sugeridas:**

-   Grupo de Recursos.
-   Implementaciones de modelos.
-   Azure AI Foundry.

## Amazon EC2

La aplicación fue desplegada sobre una instancia Ubuntu con:

-   Python
-   Streamlit
-   LangChain
-   FAISS
-   Git

Flujo de despliegue:

``` text
GitHub
   │
git pull
   │
Entorno Virtual Python
   │
Streamlit
   │
Puerto 8501
```

URL pública:

``` text
http://100.58.178.56:8501
```

------------------------------------------------------------------------

# 11. Funcionalidades

-   Consulta de documentación mediante lenguaje natural.
-   Búsqueda semántica utilizando FAISS.
-   Generación de respuestas contextualizadas.
-   Integración con Azure OpenAI.
-   Base de conocimiento en documentos PDF.
-   Interfaz web con Streamlit.
-   Despliegue en AWS EC2.

------------------------------------------------------------------------

# 12. Mejoras futuras

-   Dominio personalizado.
-   HTTPS mediante Let's Encrypt.
-   Proxy inverso con Nginx.
-   Contenedores Docker.
-   Pipeline CI/CD.
-   Autenticación de usuarios.
-   Historial de conversaciones.

------------------------------------------------------------------------

# 13. Autor

**Eduardo Ramírez De Lama**

Proyecto desarrollado para el **Challenge Final de Inteligencia
Artificial - Alura Latam**.

© Sudo Agile S.A.
