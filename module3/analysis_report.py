import json
import os
from module3.config3 import DocumentConfig

class AnalysisReport:
    def __init__(self):
        self.report = {}
        os.makedirs(DocumentConfig.OUTPUT_FOLDER, exist_ok=True)

    def build(self, document, validation):
        self.report = {
            "total_pages": document.total_pages,
            "cover_page": document.cover_page,
            "answer_pages": document.answer_pages,
            "page_types": [
                {
                    "page_number": page.page_number,
                    "type": page.page_type,
                    "is_cover": page.is_cover
                }
                for page in document.pages
            ],
            "valid": validation["valid"],
            "errors": validation["errors"]
        }
        return self.report

    def save(self):
        output_path = os.path.join(DocumentConfig.OUTPUT_FOLDER, "document_analysis.json")
        with open(output_path, "w", encoding="utf-8") as file:
            json.dump(self.report, file, indent=4)
        return output_path