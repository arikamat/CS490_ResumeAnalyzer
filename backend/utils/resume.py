from PyPDF2 import PdfReader
import re
from docx import Document


def extract_text_from_pdf(file):
    """
    Extracts and cleans text from pdf file
    Args:
       file (stream or path): Path to pdf or file stream of pdf

    Returns:
        str: Post processed text extracted from pdf
    """
    reader = PdfReader(file)
    text = ""
    for page in reader.pages:
        text += page.extract_text()
    text = text.replace("\n\n", "<PARAGRAPH_BREAK>")
    text = text.replace("\n", " ")
    text = text.replace("<PARAGRAPH_BREAK>", "\n\n")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def extract_text_from_docx(file):
    """
    Extracts and cleans text from docx file
    Args:
       file (stream or path): Path to docx or file stream of docx

    Returns:
        str: Post processed text extracted from docx
    """
    doc = Document(file)
    text = []
    for i in doc.paragraphs:
        text.append(i.text)
    final_str = "\n".join(text).strip()
    return final_str
