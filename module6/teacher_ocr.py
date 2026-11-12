import base64
import os
from pathlib import Path
from typing import Dict, List


class TeacherDocumentOCR:
    """Vision OCR for scanned teacher question papers and answer schemes.

    Uses the same Anthropic/Claude ecosystem as the project's OCR module, but
    uses teacher-document prompts instead of the student-answer transcription
    prompt. The model is configurable through MODULE6_MODEL.
    """

    def __init__(self, model=None, dpi=180):
        self.model = model or os.getenv("MODULE6_MODEL", "claude-sonnet-4-6")
        self.dpi = dpi

    def _client(self):
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError(
                "Scanned PDF detected but ANTHROPIC_API_KEY is not set. "
                "Set the key to enable Module 6 teacher-document OCR."
            )
        try:
            import anthropic
        except ImportError as exc:
            raise ImportError(
                "Install Anthropic SDK with: pip install anthropic"
            ) from exc
        return anthropic.Anthropic(api_key=key)

    @staticmethod
    def _render_pages(pdf_path: str, dpi: int):
        try:
            import pymupdf  # PyMuPDF
        except ImportError as exc:
            raise ImportError(
                "Install PyMuPDF with: pip install pymupdf"
            ) from exc

        doc = pymupdf.open(pdf_path)
        scale = dpi / 72.0
        matrix = pymupdf.Matrix(scale, scale)
        for index, page in enumerate(doc, start=1):
            pix = page.get_pixmap(matrix=matrix, alpha=False)
            yield index, pix.tobytes("png")
        doc.close()

    def extract(self, pdf_path: str, document_type: str) -> Dict:
        client = self._client()
        pages: List[Dict] = []

        if document_type == "question_paper":
            instruction = (
                "Transcribe this teacher question-paper page exactly enough for "
                "downstream parsing. Preserve question numbers, subquestion labels, "
                "OR/choice instructions, marks, section/module headings, tables and "
                "important punctuation. Do not answer or evaluate any question."
            )
        else:
            instruction = (
                "Transcribe this teacher answer scheme/valuation scheme page. Preserve "
                "question numbers, subquestion labels, every marking criterion, the "
                "mark value for each criterion, phrases such as 'any two/three', "
                "partial-mark rules, and OR/choice instructions. Do not invent missing "
                "criteria or marks."
            )

        for page_number, png_bytes in self._render_pages(pdf_path, self.dpi):
            image_b64 = base64.b64encode(png_bytes).decode("ascii")
            message = client.messages.create(
                model=self.model,
                max_tokens=6000,
                messages=[
                    {
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": "image/png",
                                    "data": image_b64,
                                },
                            },
                            {"type": "text", "text": instruction},
                        ],
                    }
                ],
            )
            text = "\n".join(
                block.text for block in message.content
                if getattr(block, "type", None) == "text"
            ).strip()
            pages.append({"page_number": page_number, "text": text})

        return {
            "path": str(Path(pdf_path)),
            "page_count": len(pages),
            "source": "claude_vision_ocr",
            "model": self.model,
            "pages": pages,
            "text": "\n\n".join(p["text"] for p in pages if p["text"]),
        }
