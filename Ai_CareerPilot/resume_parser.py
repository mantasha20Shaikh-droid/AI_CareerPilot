from pathlib import Path
from docx import Document
import fitz
ALLOWED = {'.pdf', '.docx'}
def extract_resume_text(path):
    ext = Path(path).suffix.lower()
    if ext == '.pdf':
        with fitz.open(path) as doc: return '\n'.join(page.get_text() for page in doc).strip()
    if ext == '.docx':
        doc = Document(path)
        return '\n'.join(p.text for p in doc.paragraphs).strip()
    raise ValueError('Only PDF and DOCX resumes are supported.')
