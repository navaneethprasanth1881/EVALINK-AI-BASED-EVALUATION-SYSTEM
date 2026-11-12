from module3.config3 import DocumentConfig

class DocumentValidator:
    def validate_page_count(self, document):
        if document.total_pages < DocumentConfig.MIN_TOTAL_PAGES:
            return False, f"Document must contain at least {DocumentConfig.MIN_TOTAL_PAGES} pages."
        return True, None

    def validate_page_sequence(self, document):
        expected = list(range(1, document.total_pages + 1))
        actual = [page.page_number for page in document.pages]
        
        # Fixed: Changed "actual 1 expected" to "actual != expected"
        if actual != expected:
            return False, f"Page sequence is invalid. Expected {expected}, found {actual}."
        return True, None

    def validate_cover_page(self, document):
        # Fixed: Changed "=" to "!="
        if document.cover_page != DocumentConfig.COVER_PAGE_NUMBER:
            return False, "Cover page was not identified correctly."
        return True, None

    def validate_answer_pages(self, document):
        if len(document.answer_pages) == 0:
            return False, "No answer pages were identified."
        return True, None

    def validate(self, document):
        errors = []
        
        valid, error = self.validate_page_count(document)
        if not valid: 
            errors.append(error)
            
        valid, error = self.validate_page_sequence(document)
        if not valid: 
            errors.append(error)
            
        valid, error = self.validate_cover_page(document)
        if not valid: 
            errors.append(error)
            
        valid, error = self.validate_answer_pages(document)
        if not valid: 
            errors.append(error)

        return {
            "valid": len(errors) == 0,
            "errors": errors
        }