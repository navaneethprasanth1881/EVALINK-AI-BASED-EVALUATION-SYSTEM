from .document_loader import DocumentLoader


class PDFTextExtractor:
    def __init__(self):
        self.loader = DocumentLoader()

    def extract(self, pdf_path: str):
        return self.loader.load_pdf_text(pdf_path)
