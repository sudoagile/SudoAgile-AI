"""
Inserta una página de propiedad corporativa al inicio de cada PDF en docs/.

Información insertada:
    - Empresa:  Sudo Agile S. A.
    - Fundador: Eduardo Ramirez De Lama
    - Software: GestSudo

Uso:
    py -3 tools/agregar_portada.py

Después de ejecutarlo, reconstruye el índice FAISS:
    py -3 app.py
"""

from pathlib import Path

import fitz  # PyMuPDF


# ── Configuración ────────────────────────────────────────────────────────────

EMPRESA = "Sudo Agile S. A."
FUNDADOR = "Eduardo Ramirez De Lama"
SOFTWARE = "GestSudo"
CARPETA_DOCS = Path("docs")

# ── Colores ──────────────────────────────────────────────────────────────────

COLOR_TITULO = (0.10, 0.20, 0.45)   # Azul corporativo oscuro
COLOR_CUERPO = (0.15, 0.15, 0.15)   # Gris casi negro
COLOR_LINEA  = (0.10, 0.20, 0.45)   # Igual al título
COLOR_FONDO  = (0.97, 0.97, 0.99)   # Blanco roto suave


# ── Funciones ────────────────────────────────────────────────────────────────

def ya_tiene_portada(ruta_pdf: Path) -> bool:
    """Devuelve True si el PDF ya tiene la página de propiedad insertada."""
    doc = fitz.open(str(ruta_pdf))
    texto_primera = doc[0].get_text()
    doc.close()
    return EMPRESA in texto_primera


def insertar_portada(ruta_pdf: Path) -> None:
    """Inserta la página de propiedad al inicio del PDF indicado."""
    doc = fitz.open(str(ruta_pdf))

    # Insertar página nueva en blanco al inicio (índice 0), tamaño A4
    doc.insert_page(0, width=595, height=842)
    pagina = doc[0]

    # Fondo de color suave
    pagina.draw_rect(
        fitz.Rect(0, 0, 595, 842),
        color=None,
        fill=COLOR_FONDO,
    )

    # Línea de acento superior
    pagina.draw_line(
        fitz.Point(40, 120),
        fitz.Point(555, 120),
        color=COLOR_LINEA,
        width=2,
    )

    # Línea de acento inferior
    pagina.draw_line(
        fitz.Point(40, 722),
        fitz.Point(555, 722),
        color=COLOR_LINEA,
        width=1,
    )

    # Nombre del software (título principal)
    pagina.insert_text(
        fitz.Point(40, 90),
        SOFTWARE,
        fontsize=26,
        color=COLOR_TITULO,
        fontname="helv",
    )

    # Nombre del documento (subtítulo)
    nombre_doc = ruta_pdf.stem.replace("_", " ").title()
    pagina.insert_text(
        fitz.Point(40, 145),
        nombre_doc,
        fontsize=14,
        color=COLOR_CUERPO,
        fontname="helv",
    )

    # Bloque de propiedad
    pagina.insert_text(
        fitz.Point(40, 210),
        f"Empresa:   {EMPRESA}",
        fontsize=12,
        color=COLOR_CUERPO,
        fontname="helv",
    )
    pagina.insert_text(
        fitz.Point(40, 235),
        f"Fundador:  {FUNDADOR}",
        fontsize=12,
        color=COLOR_CUERPO,
        fontname="helv",
    )
    pagina.insert_text(
        fitz.Point(40, 260),
        f"Software:  {SOFTWARE}",
        fontsize=12,
        color=COLOR_CUERPO,
        fontname="helv",
    )

    # Texto legal
    lineas_legales = [
        "Este documento forma parte de la documentacion oficial del sistema",
        f"{SOFTWARE}, desarrollado y mantenido por {EMPRESA}.",
        "",
        "Queda prohibida su reproduccion, distribucion o uso no autorizado",
        f"sin el consentimiento expreso de {EMPRESA}.",
    ]
    y = 340
    for linea in lineas_legales:
        pagina.insert_text(
            fitz.Point(40, y),
            linea,
            fontsize=10,
            color=COLOR_CUERPO,
            fontname="helv",
        )
        y += 18

    # Pie de página
    pagina.insert_text(
        fitz.Point(40, 760),
        f"(c) {EMPRESA} - Todos los derechos reservados",
        fontsize=9,
        color=COLOR_LINEA,
        fontname="helv",
    )

    # Guardar en archivo temporal y reemplazar el original
    ruta_temp = ruta_pdf.with_suffix(".tmp.pdf")
    doc.save(str(ruta_temp))
    doc.close()
    ruta_temp.replace(ruta_pdf)
    print(f"OK Portada agregada: {ruta_pdf.name}")


def main() -> None:
    pdfs = list(CARPETA_DOCS.glob("*.pdf"))

    if not pdfs:
        print(f"No se encontraron PDFs en '{CARPETA_DOCS}'.")
        return

    print(f"PDFs encontrados: {len(pdfs)}\n")

    for ruta in pdfs:
        if ya_tiene_portada(ruta):
            print(f"OMITIDO Ya tiene portada: {ruta.name}")
        else:
            insertar_portada(ruta)

    print(
        "\nListo. Reconstruye el indice FAISS ejecutando:\n"
        "    py -3 app.py"
    )


if __name__ == "__main__":
    main()
