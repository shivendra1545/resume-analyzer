from pathlib import Path
from pdfminer.high_level import extract_text as pdf_extract_text
from pdfminer.layout import LAParams
from docx import Document
from pypdf import PdfReader


def extract_from_pdf(filepath):
    laparams = LAParams(
        char_margin=2.0,
        word_margin=0.1,
        line_margin=0.5,
        boxes_flow=0.5
    )

    text = pdf_extract_text(filepath, laparams=laparams)

    reader = PdfReader(filepath)
    links = []

    for page in reader.pages:
        annotations = page.get("/Annots") or []

        for annotation in annotations:
            obj = annotation.get_object()
            action = obj.get("/A")

            if action and action.get("/URI"):
                links.append(action.get("/URI"))

    if links:
        text += "\n" + "\n".join(links)

    return text

def extract_from_docx(filepath):
    document = Document(filepath)
    return "\n".join(
        paragraph.text
        for paragraph in document.paragraphs
        if paragraph.text.strip()
    )


def extract_text_from_file(filepath):
    extension = Path(filepath).suffix.lower()

    if extension == ".pdf":
        return extract_from_pdf(filepath)

    if extension == ".docx":
        return extract_from_docx(filepath)

    raise ValueError("Unsupported file type. Use PDF or DOCX.")
