"""
Core Document Object

Represents the complete answer booklet
throughout the processing pipeline.
"""

from dataclasses import dataclass, field
from typing import Optional

from page import Page


@dataclass
class Document:

    # ---------------------------------------------------------
    # Input PDF
    # ---------------------------------------------------------

    pdf_path: str

    total_pages: int = 0

    # ---------------------------------------------------------
    # Pages
    # ---------------------------------------------------------

    pages: list[Page] = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Module 1
    # ---------------------------------------------------------

    quality_report: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Module 2
    # ---------------------------------------------------------

    preprocessed_pdf_path: Optional[str] = None

    preprocessing_report: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Module 3
    # ---------------------------------------------------------

    cover_page: Optional[int] = None

    answer_pages: list[int] = field(
        default_factory=list
    )

    analysis_report: dict = field(
        default_factory=dict
    )

    is_valid: bool = False

    # ---------------------------------------------------------
    # Student information
    # Filled later by Claude OCR
    # ---------------------------------------------------------

    student_details: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Module 4
    # ---------------------------------------------------------

    ocr_json: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Module 6
    # ---------------------------------------------------------

    mapped_questions: list = field(
        default_factory=list
    )

    # ---------------------------------------------------------
    # Module 7
    # ---------------------------------------------------------

    evaluation_results: list = field(
        default_factory=list
    )

    total_marks: float = 0.0

    maximum_marks: float = 0.0

    # ---------------------------------------------------------
    # Add page
    # ---------------------------------------------------------

    def add_page(self, page: Page):

        self.pages.append(page)

        self.total_pages = len(
            self.pages
        )