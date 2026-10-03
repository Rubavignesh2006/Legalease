from docx import Document
from fpdf import FPDF


def format_docx(text: str) -> bytes:
    doc = Document()

    for line in text.splitlines():
        if line.strip():
            doc.add_paragraph(line)

    output_path = "legal_document.docx"
    doc.save(output_path)

    with open(output_path, "rb") as file:
        return file.read()


def format_pdf(text: str) -> bytes:
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=11)

    for line in text.splitlines():
        if line.strip():
            pdf.multi_cell(0, 8, line)

    return bytes(pdf.output())