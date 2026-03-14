"""
Document Parser Service
Extracts text from PDF, DOCX, and scanned documents (OCR).
"""

import io
import re
from typing import Optional


def extract_text_from_pdf(file_bytes: bytes) -> str:
    """Extract text from a PDF file using pdfplumber."""
    try:
        import pdfplumber
        text_parts = []
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                page_text = page.extract_text()
                if page_text:
                    text_parts.append(page_text)
        return "\n\n".join(text_parts)
    except Exception as e:
        raise ValueError(f"Failed to parse PDF: {str(e)}")


def extract_text_from_docx(file_bytes: bytes) -> str:
    """Extract text from a DOCX file using python-docx."""
    try:
        from docx import Document
        doc = Document(io.BytesIO(file_bytes))
        text_parts = []
        for paragraph in doc.paragraphs:
            if paragraph.text.strip():
                text_parts.append(paragraph.text.strip())
        return "\n\n".join(text_parts)
    except Exception as e:
        raise ValueError(f"Failed to parse DOCX: {str(e)}")


def extract_text_from_image(file_bytes: bytes) -> str:
    """Extract text from a scanned image using Tesseract OCR."""
    try:
        import pytesseract
        from PIL import Image
        image = Image.open(io.BytesIO(file_bytes))
        text = pytesseract.image_to_string(image)
        return text.strip()
    except Exception as e:
        raise ValueError(f"Failed OCR extraction: {str(e)}")


def extract_text(file_bytes: bytes, filename: str) -> str:
    """
    Main entry point: detect file type and extract text accordingly.
    Supports .pdf, .docx, .doc, .png, .jpg, .jpeg, .tiff, .bmp
    """
    ext = filename.lower().rsplit(".", 1)[-1] if "." in filename else ""

    if ext == "pdf":
        text = extract_text_from_pdf(file_bytes)
        # If PDF extraction yields very little text, try OCR
        if len(text.strip()) < 50:
            try:
                text = extract_text_from_image(file_bytes)
            except Exception:
                pass
        return text
    elif ext in ("docx", "doc"):
        return extract_text_from_docx(file_bytes)
    elif ext in ("png", "jpg", "jpeg", "tiff", "bmp"):
        return extract_text_from_image(file_bytes)
    elif ext == "txt":
        return file_bytes.decode("utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file format: .{ext}")


def clean_text(text: str) -> str:
    """Clean and normalize extracted text."""
    # Remove excessive whitespace
    text = re.sub(r'\n{3,}', '\n\n', text)
    # Remove page numbers
    text = re.sub(r'\n\s*Page\s+\d+\s*(of\s+\d+)?\s*\n', '\n', text, flags=re.IGNORECASE)
    # Normalize quotes
    text = text.replace('\u201c', '"').replace('\u201d', '"')
    text = text.replace('\u2018', "'").replace('\u2019', "'")
    # Remove excessive spaces
    text = re.sub(r'[ \t]+', ' ', text)
    return text.strip()
