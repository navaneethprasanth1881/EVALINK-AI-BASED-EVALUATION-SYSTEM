from json_loader import JSONLoader
from structure_validator import StructureValidator
from content_validator import ContentValidator
from validation_report import ValidationReport

class JSONValidator:
    def __init__(self):
        self.loader = JSONLoader()
        self.structure_validator = StructureValidator()
        self.content_validator = ContentValidator()
        self.report_generator = ValidationReport()

    def validate(self, data=None):
        if data is None:
            data = self.loader.load()

        print("\nRunning structure validation...")
        structure_result = self.structure_validator.validate(data)

        print("Running content validation...")
        content_result = self.content_validator.validate(data)

        report = self.report_generator.build(structure_result, content_result)
        report_path = self.report_generator.save(structure_result, content_result)
        validated_path = self.report_generator.save_validated_copy(data)
        
        self.report_generator.print_report(report)

        return {
            "data": data,
            "structure": structure_result,
            "content": content_result,
            "report": report,
            "report_path": report_path,
            "validated_path": validated_path
        }

    
    
    def validate_document(self, document):
        if not hasattr(document, "ocr_json"):
            raise ValueError("Document does not contain ocr_json.")

        validation_data = {
            "document": {
                "pdf_path": document.pdf_path,
                "total_pages": document.total_pages,
                "cover_page": document.cover_page,
                "answer_pages": document.answer_pages
            },
            "student": document.student_details,
            "pages": document.ocr_json.get("pages", [])
        }

        # TEMPORARY DEBUGGING
        print("\n========== MODULE 5 DEBUG ==========")
        print("JSONValidator file:", __file__)
        print("Input root fields:", list(validation_data.keys()))
        print("Cover page:", validation_data["document"]["cover_page"])
        print("Total pages:", validation_data["document"]["total_pages"])
        print("Number of pages:", len(validation_data["pages"]))

        if validation_data["pages"]:
            print("First page type:", validation_data["pages"][0].get("page_type"))

        print("====================================\n")

        result = self.validate(validation_data)

        document.validation_result = result["report"]
        document.json_valid = result["report"]["validation"]["valid"]

        return document
