"""
Module 4 - Claude OCR

End-to-End Test

Pipeline:

Module 1
    ↓
Module 2
    ↓
Module 3
    ↓
Module 4
    ↓
OCR JSON
"""
import sys
from pathlib import Path


PROJECT_ROOT = Path(__file__).resolve().parent.parent

sys.path.insert(0, str(PROJECT_ROOT))
sys.path.insert(0, str(PROJECT_ROOT / "modul2"))
sys.path.insert(0, str(PROJECT_ROOT / "module3"))

import os

from module1.quality_analyzer import (
    QualityAnalyzer
)

from modul2.preprocessor import (
    Preprocessor
)

from module3.document_analyzer import (
    DocumentAnalyzer
)

from ocr_processor import OCRProcessor

from ocr_report import OCRReport


def main():

    ###########################################################
    # Input PDF
    ###########################################################

    pdf_path = "module1/ilovepdf_merged.pdf"

    ###########################################################
    # Check PDF
    ###########################################################

    if not os.path.exists(pdf_path):

        raise FileNotFoundError(

            f"PDF not found: {pdf_path}"

        )

    ###########################################################
    # Check API Key
    ###########################################################

    if not os.getenv("ANTHROPIC_API_KEY"):

        raise RuntimeError(

            "ANTHROPIC_API_KEY is not set.\n\n"

            "PowerShell:\n"

            '$env:ANTHROPIC_API_KEY="your_api_key_here"'

        )

    ###########################################################
    # Module 1
    ###########################################################

    print()
    print("=" * 60)
    print("MODULE 1 - INPUT QUALITY")
    print("=" * 60)

    quality_analyzer = QualityAnalyzer()

    document = quality_analyzer.analyze(
        pdf_path
    )

    print("Module 1 completed.")

    ###########################################################
    # Module 2
    ###########################################################

    print()
    print("=" * 60)
    print("MODULE 2 - PREPROCESSING")
    print("=" * 60)

    preprocessor = Preprocessor()

    document = preprocessor.process(
        document
    )

    print("Module 2 completed.")

    print(
        "Preprocessed PDF:"
    )

    print(
        document.preprocessed_pdf_path
    )

    ###########################################################
    # Module 3
    ###########################################################

    print()
    print("=" * 60)
    print("MODULE 3 - DOCUMENT MANAGEMENT")
    print("=" * 60)

    document_analyzer = DocumentAnalyzer()

    document = document_analyzer.analyze(
        document
    )

    print("Module 3 completed.")

    print(
        f"Cover page: "
        f"{document.cover_page}"
    )

    print(
        f"Answer pages: "
        f"{document.answer_pages}"
    )

    ###########################################################
    # Stop if document is invalid
    ###########################################################

    if not document.is_valid:

        print()

        print(
            "Document validation failed."
        )

        print()

        for error in (
            document.analysis_report["errors"]
        ):

            print(
                f"- {error}"
            )

        return

    ###########################################################
    # Module 4
    ###########################################################

    print()
    print("=" * 60)
    print("MODULE 4 - CLAUDE OCR")
    print("=" * 60)

    print()

    print(
        "WARNING: The following step "
        "will make Claude API calls."
    )

    print(
        "OCR will be performed on the "
        "configured pages."
    )

    print()

    confirmation = input(
        "Continue with Claude OCR? [y/N]: "
    )

    if confirmation.lower() != "y":

        print()
        print(
            "OCR test cancelled."
        )

        return

    ###########################################################
    # OCR Processor
    ###########################################################

    processor = OCRProcessor()

    document = processor.process(
        document
    )

    ###########################################################
    # OCR Report
    ###########################################################

    report = OCRReport()

    output_paths = report.save(
        document
    )

    ###########################################################
    # Print Summary
    ###########################################################

    report.print_summary(
        document
    )

    ###########################################################
    # Final Result
    ###########################################################

    print()

    print("=" * 60)

    print("MODULE 4 COMPLETED")

    print("=" * 60)

    print()

    print(
        "OCR JSON:"
    )

    print(
        output_paths.get(
            "ocr_json"
        )
    )

    if "raw_responses" in output_paths:

        print()

        print(
            "Raw Claude responses:"
        )

        print(
            output_paths[
                "raw_responses"
            ]
        )

    print()

    print(
        "Student information:"
    )

    print(
        document.student_details
    )

    print()

    print(
        "OCR pages:"
    )

    for page in document.ocr_json.get(
        "pages",
        []
    ):

        print()

        print(
            f"Page "
            f"{page['page_number']}"
        )

        if "answers" in page:

            for answer in page["answers"]:

                print(
                    f"  Answer "
                    f"{answer['answer_number']}"
                )

                print(
                    f"  Source page: "
                    f"{answer['source_page']}"
                )

                print(
                    f"  Continues: "
                    f"{answer['continues_to_next_page']}"
                )

                print(
                    f"  Text: "
                    f"{answer['answer_text'][:200]}"
                )

        elif "student" in page:

            print(
                "  Cover/student "
                "information processed."
            )

    print()

    print("=" * 60)

    print(
        "Module 4 test finished."
    )

    print("=" * 60)


if __name__ == "__main__":

    main()