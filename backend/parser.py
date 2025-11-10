import io
import pdfminer.high_level as pdf
import docx
import re

def _read_pdf(file_stream):
    # pdfminer expects a file path or a binary stream
    try:
        file_stream.seek(0)
        return pdf.extract_text(file_stream)
    except Exception:
        return ""

def _read_docx(file_stream):
    try:
        file_stream.seek(0)
        doc = docx.Document(file_stream)
        return "\n".join([p.text for p in doc.paragraphs])
    except Exception:
        return ""

def parse_resume(file_storage):
    filename = file_storage.filename.lower()
    file_stream = file_storage.stream
    text = ""
    if filename.endswith('.pdf'):
        text = _read_pdf(file_stream)
    elif filename.endswith('.docx') or filename.endswith('.doc'):
        text = _read_docx(file_stream)
    else:
        # fallback - try reading raw bytes as text
        try:
            file_stream.seek(0)
            text = file_stream.read().decode('utf-8', errors='ignore')
        except Exception:
            text = ""
    # simple cleanup
    text = re.sub(r'\s+', ' ', text).strip()
    return text