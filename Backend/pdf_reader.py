import io
import pdfplumber


def extract_text_from_pdf(file_storage):
    """Extract text from uploaded PDF file_storage (Werkzeug FileStorage)."""
    file_storage.stream.seek(0)
    data = file_storage.read()
    file_storage.stream.seek(0)

    text = []
    with pdfplumber.open(io.BytesIO(data)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text() or ""
            text.append(page_text)
    return "\n".join(text)
