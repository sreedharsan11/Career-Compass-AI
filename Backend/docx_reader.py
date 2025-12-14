from docx import Document


def extract_text_from_docx(file_storage):
    """Extract text from uploaded DOCX file_storage (Werkzeug FileStorage)."""
    file_storage.stream.seek(0)
    document = Document(file_storage.stream)
    paragraphs = [p.text for p in document.paragraphs if p.text.strip()]
    return "\n".join(paragraphs)
