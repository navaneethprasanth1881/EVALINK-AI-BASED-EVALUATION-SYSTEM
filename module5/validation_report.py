"""
Module 5 - JSON Validation

Validation Report

Combines structural and content validation results
and saves the final validation report.

IMPORTANT:
This module does NOT modify OCR data.
"""

import json
import os
from datetime import datetime

from config5 import JSONValidationConfig


class ValidationReport:

    # =========================================================
    # Constructor
    # =========================================================

    def __init__(self):

        self.output_folder = (
            JSONValidationConfig.OUTPUT_FOLDER
        )

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    # =========================================================
    # Build Report
    # =========================================================

    def build(
        self,
        structure_result,
        content_result
    ):

        """
        Combine structural and content validation results.
        """

        structure_errors = (
            structure_result.get(
                "errors",
                []
            )
        )

        structure_warnings = (
            structure_result.get(
                "warnings",
                []
            )
        )

        content_errors = (
            content_result.get(
                "errors",
                []
            )
        )

        content_warnings = (
            content_result.get(
                "warnings",
                []
            )
        )

        # -----------------------------------------------------
        # Combine
        # -----------------------------------------------------

        all_errors = (

            structure_errors
            +
            content_errors

        )

        all_warnings = (

            structure_warnings
            +
            content_warnings

        )

        # -----------------------------------------------------
        # Determine Status
        # -----------------------------------------------------

        if all_errors:

            status = (
                JSONValidationConfig.STATUS_INVALID
            )

        elif all_warnings:

            status = (
                JSONValidationConfig.STATUS_WARNING
            )

        else:

            status = (
                JSONValidationConfig.STATUS_VALID
            )

        # -----------------------------------------------------
        # Build Report
        # -----------------------------------------------------

        report = {

            "validation": {

                "status": status,

                "valid":
                    len(all_errors) == 0,

                "timestamp":
                    datetime.now().isoformat(),

                "error_count":
                    len(all_errors),

                "warning_count":
                    len(all_warnings)

            },

            "structure_validation": {

                "valid":
                    structure_result.get(
                        "valid",
                        False
                    ),

                "errors":
                    structure_errors,

                "warnings":
                    structure_warnings

            },

            "content_validation": {

                "valid":
                    content_result.get(
                        "valid",
                        False
                    ),

                "errors":
                    content_errors,

                "warnings":
                    content_warnings

            },

            "errors":
                all_errors,

            "warnings":
                all_warnings

        }

        return report

    # =========================================================
    # Save Report
    # =========================================================

    def save(
        self,
        structure_result,
        content_result
    ):

        """
        Build and save validation report.
        """

        report = self.build(

            structure_result,

            content_result

        )

        output_path = os.path.join(

            self.output_folder,

            JSONValidationConfig.REPORT_FILENAME

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

    # =========================================================
    # Save Validated Copy
    # =========================================================

    def save_validated_copy(
        self,
        data
    ):

        """
        Save an unchanged copy of the OCR JSON.

        IMPORTANT:
        No corrections are made here.
        """

        if not (
            JSONValidationConfig
            .SAVE_VALIDATED_COPY
        ):

            return None

        output_path = os.path.join(

            self.output_folder,

            JSONValidationConfig
            .VALIDATED_FILENAME

        )

        with open(

            output_path,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                data,

                file,

                indent=4,

                ensure_ascii=False

            )

        return output_path

    # =========================================================
    # Print Report
    # =========================================================

    def print_report(
        self,
        report
    ):

        """
        Print a readable validation summary.
        """

        validation = report[
            "validation"
        ]

        print()

        print("=" * 60)

        print("JSON VALIDATION REPORT")

        print("=" * 60)

        print()

        print(
            f"Status: "
            f"{validation['status']}"
        )

        print(
            f"Errors: "
            f"{validation['error_count']}"
        )

        print(
            f"Warnings: "
            f"{validation['warning_count']}"
        )

        # -----------------------------------------------------
        # Errors
        # -----------------------------------------------------

        if report["errors"]:

            print()

            print("ERRORS:")

            for error in report["errors"]:

                print(
                    f"  - {error}"
                )

        # -----------------------------------------------------
        # Warnings
        # -----------------------------------------------------

        if report["warnings"]:

            print()

            print("WARNINGS:")

            for warning in report["warnings"]:

                print(
                    f"  - {warning}"
                )

        print()

        print("=" * 60)