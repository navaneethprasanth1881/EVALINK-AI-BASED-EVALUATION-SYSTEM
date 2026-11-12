from pathlib import Path
from typing import Dict, List


class QuestionPaperLoader:
    """
    Loads a teacher-uploaded question paper.

    This loader does NOT contain subject-specific or
    question-number-specific information.
    """

    def __init__(self):
        pass

    def load(self, pdf_path: str) -> Dict:
        return self.load_pdf_text(pdf_path)

    def load_pdf_text(self, pdf_path: str) -> Dict:
        path = Path(pdf_path)

        if not path.exists():
            raise FileNotFoundError(
                f"Question paper not found: {path}"
            )

        try:
            import pypdf
        except ImportError:
            raise ImportError(
                "pypdf is not installed. "
                "Run: pip install pypdf"
            )

        reader = pypdf.PdfReader(str(path))

        pages: List[Dict] = []

        for page_number, page in enumerate(
            reader.pages,
            start=1
        ):
            text = page.extract_text() or ""

            pages.append({
                "page_number": page_number,
                "text": text.strip()
            })

        combined_text = "\n\n".join(
            page["text"]
            for page in pages
            if page["text"]
        )

        return {
            "path": str(path),
            "page_count": len(pages),
            "pages": pages,
            "text": combined_text
        }