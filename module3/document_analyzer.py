from module3.cover_page_detector import CoverPageDetector
from module3.page_classifier import PageClassifier
from module3.document_validator import DocumentValidator
from module3.analysis_report import AnalysisReport

class DocumentAnalyzer:
    def __init__(self):
        self.cover_detector = CoverPageDetector()
        self.classifier = PageClassifier()
        self.validator = DocumentValidator()
        self.report = AnalysisReport()

    def analyze(self, document):
        document.cover_page = self.cover_detector.get_cover_page(document)
        document = self.classifier.classify_document(document)
        
        document.answer_pages = [
            page.page_number
            for page in document.pages
            if page.page_type == "ANSWER"
        ]
        
        validation = self.validator.validate(document)
        document.is_valid = validation["valid"]
        
        document.analysis_report = self.report.build(document, validation)
        if self.report.report:
            self.report.save()
            
        return document