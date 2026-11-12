from module3.config3 import DocumentConfig

class PageClassifier:
    def classify(self, page_number):
        if page_number == DocumentConfig.COVER_PAGE_NUMBER:
            return DocumentConfig.COVER_PAGE
        if page_number >= DocumentConfig.ANSWER_START_PAGE:
            return DocumentConfig.ANSWER_PAGE
        return DocumentConfig.UNKNOWN_PAGE

    def classify_document(self, document):
        for page in document.pages:
            page_type = self.classify(page.page_number)
            page.page_type = page_type
            page.is_cover = (page_type == DocumentConfig.COVER_PAGE)
        return document