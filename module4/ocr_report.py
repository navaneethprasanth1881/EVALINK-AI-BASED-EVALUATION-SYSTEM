"""
Module 4 - Claude OCR

OCR Report

Saves the OCR results produced by Claude.

This module does NOT:
    - modify OCR text
    - correct answers
    - evaluate answers
    - merge answers
    - validate the final JSON
"""

import json
import os

from config4 import ClaudeOCRConfig


class OCRReport:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.output_folder = (
            ClaudeOCRConfig.OUTPUT_FOLDER
        )

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    ###########################################################
    # Build Report
    ###########################################################

    def build(self, document):

        """
        Build the complete OCR report from the Document.

        The OCR content is copied exactly as it exists
        inside document.ocr_json.
        """

        report = {

            "document": {

                "pdf_path":
                    document.pdf_path,

                "total_pages":
                    document.total_pages,

                "cover_page":
                    document.cover_page,

                "answer_pages":
                    document.answer_pages

            },

            "student":
                document.student_details,

            "pages":
                document.ocr_json.get(
                    "pages",
                    []
                )

        }

        return report

    ###########################################################
    # Save OCR JSON
    ###########################################################

    def save_ocr_json(self, document):

        """
        Save structured OCR result.
        """

        report = self.build(document)

        output_path = os.path.join(

            self.output_folder,

            ClaudeOCRConfig.OCR_JSON_FILENAME

        )

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                report,

                file,

                indent=4,

                ensure_ascii=False

            )

        return output_path

    ###########################################################
    # Save Raw Responses
    ###########################################################

    def save_raw_responses(
        self,
        raw_responses
    ):

        """
        Save raw Claude responses.

        This is useful for debugging and research.

        Raw responses should not be used directly
        for evaluation.
        """

        if not ClaudeOCRConfig.SAVE_RAW_RESPONSE:

            return None

        output_path = os.path.join(

            self.output_folder,

            ClaudeOCRConfig.OCR_RAW_FILENAME

        )

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                raw_responses,

                file,

                indent=4,

                ensure_ascii=False,

                default=str

            )

        return output_path

    ###########################################################
    # Save Complete Report
    ###########################################################

    def save(
        self,
        document,
        raw_responses=None
    ):

        """
        Save OCR outputs.

        Returns
        -------
        dict
            Paths of generated files.
        """

        result = {}

        #######################################################
        # Structured OCR JSON
        #######################################################

        if ClaudeOCRConfig.SAVE_OCR_JSON:

            result["ocr_json"] = (
                self.save_ocr_json(
                    document
                )
            )

        #######################################################
        # Raw Claude Responses
        #######################################################

        if raw_responses is not None:

            raw_path = (
                self.save_raw_responses(
                    raw_responses
                )
            )

            if raw_path is not None:

                result["raw_responses"] = (
                    raw_path
                )

        return result

    ###########################################################
    # Print Summary
    ###########################################################

    def print_summary(self, document):

        """
        Print a small OCR summary.
        """

        print()

        print("=" * 60)

        print("CLAUDE OCR REPORT")

        print("=" * 60)

        print()

        print(
            f"Total Pages : "
            f"{document.total_pages}"
        )

        print(
            f"Cover Page  : "
            f"{document.cover_page}"
        )

        print(
            f"Answer Pages: "
            f"{document.answer_pages}"
        )

        print()

        for page in document.ocr_json.get(
            "pages",
            []
        ):

            page_number = page.get(
                "page_number"
            )

            page_type = page.get(
                "page_type"
            )

            print(
                f"Page {page_number}"
                f" -> "
                f"{page_type}"
            )

            if "answers" in page:

                print(
                    f"   Answers found: "
                    f"{len(page['answers'])}"
                )

        print()

        print("=" * 60)