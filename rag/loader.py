"""Extract text per page, preserving physical PDF page numbers."""
from io import BytesIO

from langchain_core.documents import Document
from pypdf import PdfReader


def load_pdf(data: bytes, filename: str) -> list[Document]:
    reader = PdfReader(BytesIO(data))
    if reader.is_encrypted:
        raise ValueError("Use an unencrypted PDF.")
    documents = []
    for page_number, page in enumerate(reader.pages, start=1):
        text = (page.extract_text() or "").strip()
        if text:
            documents.append(Document(page_content=text, metadata={
                "source": filename, "page": page_number,
            }))
    if not documents:
        raise ValueError("No readable text found. Scanned PDFs need OCR first.")
    return documents
