from config5 import JSONValidationConfig

class StructureValidator:
    def __init__(self):
        self.errors = []
        self.warnings = []

    def reset(self):
        self.errors = []
        self.warnings = []

    def add_error(self, message):
        self.errors.append(message)

    def add_warning(self, message):
        self.warnings.append(message)

    def validate_root(self, data):
        if not isinstance(data, dict):
            self.add_error("Root JSON value must be an object.")
            return False
            
        required_fields = ["document", "student", "pages"]
        for field in required_fields:
            if field not in data:
                self.add_error(f"Missing required root field: {field}")
        return True

    def validate_document(self, data):
        if "document" not in data:
            return
            
        document = data["document"]
        if not isinstance(document, dict):
            self.add_error("document must be an object.")
            return
            
        required_fields = ["pdf_path", "total_pages", "cover_page", "answer_pages"]
        for field in required_fields:
            if field not in document:
                self.add_error(f"document: missing field {field}")
                
        if "pdf_path" in document:
            if not isinstance(document["pdf_path"], str):
                self.add_error("document.pdf_path must be a string.")
                
        if "total_pages" in document:
            if not isinstance(document["total_pages"], int):
                self.add_error("document.total_pages must be an integer.")
                
        if "cover_page" in document:
            value = document["cover_page"]
            if not isinstance(value, (int, type(None))):
                self.add_error("document.cover_page must be an integer or null.")
                
        if "answer_pages" in document:
            answer_pages = document["answer_pages"]
            if not isinstance(answer_pages, list):
                self.add_error("document.answer_pages must be a list.")
            else:
                for index, page_number in enumerate(answer_pages):
                    if not isinstance(page_number, int):
                        self.add_error(f"document.answer_pages[{index}] must be an integer.")

    def validate_student(self, data):
        if "student" not in data:
            return
            
        student = data["student"]
        if not isinstance(student, dict):
            self.add_error("student must be an object.")
            return
            
        for field in JSONValidationConfig.STUDENT_FIELDS:
            if field not in student:
                self.add_error(f"student: missing field {field}")
                continue
            value = student[field]
            if not isinstance(value, (str, type(None))):
                self.add_error(f"student.{field} must be a string or null.")

    def validate_pages(self, data):
        if "pages" not in data:
            return
            
        pages = data["pages"]
        if not isinstance(pages, list):
            self.add_error("pages must be a list.")
            return
            
        for index, page in enumerate(pages):
            self.validate_page(page, index)

    def validate_page(self, page, index):
        prefix = f"pages[{index}]"
        if not isinstance(page, dict):
            self.add_error(f"{prefix} must be an object.")
            return
            
        if "page_number" not in page:
            self.add_error(f"{prefix}: missing 'page_number'.")
        if "page_type" not in page:
            self.add_error(f"{prefix}: missing 'page_type'.")
            
        if "page_number" in page:
            if not isinstance(page["page_number"], int):
                self.add_error(f"{prefix}.page_number must be an integer.")
                
        if "page_type" in page:
            page_type = page["page_type"]
            if not isinstance(page_type, str):
                self.add_error(f"{prefix}.page_type must be a string.")
            elif page_type not in JSONValidationConfig.ALLOWED_PAGE_TYPES:
                self.add_error(f"{prefix}.page_type has invalid value: {page_type}.")
                
        if page.get("page_type") == "COVER":
            self.validate_cover_page(page, prefix)
        if page.get("page_type") == "ANSWER":
            self.validate_answer_page(page, prefix)

    def validate_cover_page(self, page, prefix):
        if "student" not in page:
            self.add_warning(f"{prefix}: cover page does not contain a 'student' object.")
            return
            
        student = page["student"]
        if not isinstance(student, dict):
            self.add_error(f"{prefix}.student must be an object.")

    def validate_answer_page(self, page, prefix):
        if "answers" not in page:
            self.add_error(f"{prefix}: answer page is missing answers.")
            return
            
        answers = page["answers"]
        if not isinstance(answers, list):
            self.add_error(f"{prefix}.answers must be a list.")
            return
            
        for index, answer in enumerate(answers):
            self.validate_answer(answer, f"{prefix}.answers[{index}]")

    def validate_answer(self, answer, prefix):
        if not isinstance(answer, dict):
            self.add_error(f"{prefix} must be an object.")
            return
            
        required_fields = ["answer_number", "answer_text", "continues_to_next_page", "source_page"]
        for field in required_fields:
            if field not in answer:
                self.add_error(f"{prefix}: missing {field}.")
                
        if "answer_number" in answer:
            value = answer["answer_number"]
            if not isinstance(value, tuple(JSONValidationConfig.ALLOWED_ANSWER_NUMBER_TYPES)):
                self.add_error(f"{prefix}.answer_number must be an integer, string, or null.")
                
        if "answer_text" in answer:
            value = answer["answer_text"]
            if not isinstance(value, str):
                self.add_error(f"{prefix}.answer_text must be a string.")
                
        if "continues_to_next_page" in answer:
            value = answer["continues_to_next_page"]
            if not isinstance(value, bool):
                self.add_error(f"{prefix}.continues_to_next_page must be boolean.")
                
        if "source_page" in answer:
            value = answer["source_page"]
            if not isinstance(value, int):
                self.add_error(f"{prefix}.source_page must be an integer.")

    def validate(self, data):
        self.reset()
        valid_root = self.validate_root(data)
        if not valid_root:
            return self.get_result()
            
        self.validate_document(data)
        self.validate_student(data)
        self.validate_pages(data)
        
        return self.get_result()

    def get_result(self):
        return {
            "valid": len(self.errors) == 0,
            "errors": list(self.errors),
            "warnings": list(self.warnings)
        }