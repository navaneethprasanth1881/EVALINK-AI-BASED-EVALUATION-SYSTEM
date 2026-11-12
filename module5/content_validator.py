from config5 import JSONValidationConfig

class ContentValidator:
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

    def validate_page_numbers(self, data):
        document = data.get("document", {})
        total_pages = document.get("total_pages")
        pages = data.get("pages", [])
        
        if not isinstance(total_pages, int):
            return
            
        seen_pages = set()
        for index, page in enumerate(pages):
            page_number = page.get("page_number")
            if not isinstance(page_number, int):
                continue
                
            if JSONValidationConfig.CHECK_PAGE_NUMBER_RANGE:
                if page_number < 1 or page_number > total_pages:
                    self.add_error(f"pages[{index}].page_number {page_number} is outside the valid range 1-{total_pages}.")
                    
            if JSONValidationConfig.CHECK_DUPLICATE_PAGE_NUMBERS:
                if page_number in seen_pages:
                    self.add_error(f"Duplicate page number: {page_number}.")
                seen_pages.add(page_number)

    def validate_page_sequence(self, data):
        document = data.get("document", {})
        total_pages = document.get("total_pages")
        pages = data.get("pages", [])
        
        if not isinstance(total_pages, int):
            return
            
        page_numbers = [page.get("page_number") for page in pages if isinstance(page.get("page_number"), int)]
        expected = list(range(1, total_pages + 1))
        
        # FIXED: Added the missing != operator
        if page_numbers != expected:
            self.add_error("Page sequence does not match the expected document sequence.")

    def validate_cover_page(self, data):
        document = data.get("document", {})
        cover_page = document.get("cover_page")
        total_pages = document.get("total_pages")
        
        if cover_page is None:
            self.add_error("Cover page is missing.")
            return
            
        if not isinstance(cover_page, int):
            return
            
        if cover_page < 1 or (isinstance(total_pages, int) and cover_page > total_pages):
            self.add_error(f"Cover page {cover_page} is outside the document.")

    def validate_answer_pages(self, data):
        document = data.get("document", {})
        answer_pages = document.get("answer_pages", [])
        total_pages = document.get("total_pages")
        
        if not isinstance(answer_pages, list):
            return
            
        seen = set()
        for page_number in answer_pages:
            if page_number in seen:
                self.add_error(f"Duplicate answer page: {page_number}.")
            seen.add(page_number)
            
            if not isinstance(page_number, int):
                continue
                
            if JSONValidationConfig.CHECK_SOURCE_PAGE_RANGE:
                if page_number < 1 or (isinstance(total_pages, int) and page_number > total_pages):
                    self.add_error(f"Answer page {page_number} is outside the document range.")

    def validate_page_types(self, data):
        pages = data.get("pages", [])
        for page in pages:
            page_number = page.get("page_number")
            page_type = page.get("page_type")
            
            if page_type == "COVER":
                # FIXED: Changed "1 1" to "!= 1"
                if page_number != 1:
                    self.add_warning(f"Page {page_number} is marked COVER but is not page 1.")
            elif page_type == "ANSWER":
                # FIXED: Changed "=" to "=="
                if page_number == 1:
                    self.add_warning("Page 1 is marked ANSWER instead of COVER.")

    def validate_answer_text(self, data):
        pages = data.get("pages", [])
        for page in pages:
            page_number = page.get("page_number")
            answers = page.get("answers", [])
            
            if not isinstance(answers, list):
                continue
                
            for index, answer in enumerate(answers):
                answer_text = answer.get("answer_text")
                if not isinstance(answer_text, str):
                    continue
                    
                if not answer_text and not JSONValidationConfig.ALLOW_EMPTY_ANSWER_TEXT:
                    self.add_error(f"Page {page_number}, answer {index + 1}: answer_text is empty.")
                elif not answer_text.strip() and not JSONValidationConfig.ALLOW_WHITESPACE_ONLY_TEXT:
                    self.add_error(f"Page {page_number}, answer {index + 1}: answer_text contains only whitespace.")

    def validate_source_pages(self, data):
        document = data.get("document", {})
        total_pages = document.get("total_pages")
        pages = data.get("pages", [])
        
        for page in pages:
            current_page = page.get("page_number")
            answers = page.get("answers", [])
            
            if not isinstance(answers, list):
                continue
                
            for index, answer in enumerate(answers):
                source_page = answer.get("source_page")
                if not isinstance(source_page, int):
                    continue
                    
                if JSONValidationConfig.CHECK_SOURCE_PAGE_RANGE:
                    if source_page < 1 or (isinstance(total_pages, int) and source_page > total_pages):
                        self.add_error(f"Page {current_page}, answer {index + 1}: source_page {source_page} is outside the document.")
                        
                if JSONValidationConfig.CHECK_ANSWER_PAGE_REFERENCE:
                    if source_page != current_page:
                        self.add_warning(f"Page {current_page}, answer {index + 1}: source_page is {source_page}.")

    def validate_continuation(self, data):
        pages = data.get("pages", [])
        for page in pages:
            page_number = page.get("page_number")
            answers = page.get("answers", [])
            
            if not isinstance(answers, list):
                continue
                
            for index, answer in enumerate(answers):
                continues = answer.get("continues_to_next_page")
                if not isinstance(continues, bool):
                    continue
                    
                document = data.get("document", {})
                total_pages = document.get("total_pages", 0)
                
                if continues and isinstance(total_pages, int) and page_number == total_pages:
                    self.add_error(f"Page {page_number}, answer {index + 1}: answer is marked as continuing after the final page.")

    def validate(self, data):
        self.reset()
        self.validate_page_numbers(data)
        self.validate_page_sequence(data)
        self.validate_cover_page(data)
        self.validate_answer_pages(data)
        self.validate_page_types(data)
        self.validate_answer_text(data)
        self.validate_source_pages(data)
        self.validate_continuation(data)
        
        return {
            "valid": len(self.errors) == 0,
            "errors": list(self.errors),
            "warnings": list(self.warnings)
        }