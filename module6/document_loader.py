from pathlib import Path
from typing import Dict, List


class DocumentLoader:
    """Load teacher PDFs using native text extraction with OCR fallback."""

    def __init__(self, enable_ocr=True):
        self.enable_ocr = enable_ocr

    def load_pdf_text(self, pdf_path: str, document_type: str = "document") -> Dict:
        path = Path(pdf_path)
        if not path.exists():
            raise FileNotFoundError(f"PDF not found: {path}")

        try:
            import pypdf
        except ImportError as exc:
            raise ImportError("Install pypdf with: pip install pypdf") from exc

        reader = pypdf.PdfReader(str(path))
        pages: List[Dict] = []
        extracted_chars = 0

        for index, page in enumerate(reader.pages, start=1):
            text = (page.extract_text() or "").strip()
            extracted_chars += len(text)
            pages.append({"page_number": index, "text": text})

        native_text = "\n\n".join(p["text"] for p in pages if p["text"])
        # A scanned PDF commonly produces empty/near-empty text on most pages.
        scanned = extracted_chars < max(40, len(pages) * 20)

        if scanned and self.enable_ocr:
            from .teacher_ocr import TeacherDocumentOCR
            return TeacherDocumentOCR().extract(str(path), document_type)

        return {
            "path": str(path),
            "page_count": len(pages),
            "source": "pdf_text",
            "pages": pages,
            "text": native_text,
        }
