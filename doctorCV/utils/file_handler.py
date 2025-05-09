# utils/file_handler.py

import pdfplumber
import docx

def extract_text_from_file(file_path):
    """PDF veya DOCX dosyasından metni çıkarır."""
    if file_path.endswith(".pdf"):
        try:
            with pdfplumber.open(file_path) as pdf:
                text = "\n".join([page.extract_text() or "" for page in pdf.pages])
            return text
        except Exception as e:
            print("PDF okuma hatası:", e)
            return ""
    elif file_path.endswith(".docx"):
        try:
            doc = docx.Document(file_path)
            return "\n".join([para.text for para in doc.paragraphs])
        except Exception as e:
            print("DOCX okuma hatası:", e)
            return ""
    else:
        return ""
