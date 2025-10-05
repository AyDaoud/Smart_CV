from fastapi import UploadFile
from docx import Document
from pdfminer.high_level import extract_text as extract_pdf_text
import io

async def extract_text(file: UploadFile) -> str:
    """Extracts text from a .pdf or .docx file."""
    content = await file.read()
    file_stream = io.BytesIO(content)

    if file.content_type == "application/pdf":
        try:
            return extract_pdf_text(file_stream)
        except Exception as e:
            print(f"Error parsing PDF: {e}")
            return ""
    elif file.content_type == "application/vnd.openxmlformats-officedocument.wordprocessingml.document":
        try:
            document = Document(file_stream)
            return "\n".join([para.text for para in document.paragraphs if para.text])
        except Exception as e:
            print(f"Error parsing DOCX: {e}")
            return ""
    else:
        return ""