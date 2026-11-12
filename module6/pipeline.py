from pathlib import Path

from .document_loader import DocumentLoader
from .question_extractor import QuestionExtractor
from .schema_extractor import SchemaExtractor
from .selection_group_detector import SelectionGroupDetector
from .normalizer import SchemaNormalizer
from .schema_validator import SchemaValidator
from .output_manager import OutputManager
from .llm_structure import TeacherStructureLLM


class Module6Pipeline:

    def __init__(self, output_dir):
        self.output = OutputManager(output_dir)
        self.loader = DocumentLoader()
        self.question_extractor = QuestionExtractor()
        self.schema_extractor = SchemaExtractor()
        self.group_detector = SelectionGroupDetector()
        self.normalizer = SchemaNormalizer()
        self.validator = SchemaValidator()
        self.llm_structure = TeacherStructureLLM()

    def run(
        self,
        question_paper_path,
        answer_schema_path,
        exam_metadata=None,
    ):
        paper = self.loader.load_pdf_text(question_paper_path)
        scheme = self.loader.load_pdf_text(answer_schema_path)

        paper_questions = self.question_extractor.extract(paper["text"])
        scheme_data = self.schema_extractor.extract(scheme["text"])

        # OCR output can lose line layout. If the deterministic parser finds
        # nothing (or no criteria), use a configurable LLM structure pass.
        if not paper_questions:
            paper_questions = self.llm_structure.parse_question_paper(paper["text"])
        if not scheme_data.get("questions"):
            scheme_data = self.llm_structure.parse_answer_scheme(scheme["text"])

        groups = self.group_detector.detect_from_text(
            paper["text"]
        )

        schema = self.normalizer.build(
            paper_questions,
            scheme_data,
            detected_groups=groups,
            exam_metadata=exam_metadata,
        )

        schema_dict = schema.to_dict()
        validation = self.validator.validate(schema_dict)

        self.output.save_json(
            {
                "question_paper": paper,
                "answer_schema": scheme,
            },
            "extracted_documents.json",
        )

        self.output.save_json(
            schema_dict,
            "question_schema.json",
        )

        self.output.save_json(
            validation,
            "validation_report.json",
        )

        return {
            "schema": schema_dict,
            "validation": validation,
            "paper_question_count": len(paper_questions),
            "selection_group_count": len(groups),
        }
