"""
Module 5 - JSON Validation

End-to-End Test

Input:
    output/module_4/ocr_result.json

Pipeline:
    JSON Loader
        ↓
    Structure Validator
        ↓
    Content Validator
        ↓
    Validation Report
"""

import os

from json_validator import JSONValidator
from config5 import JSONValidationConfig


def main():

    ###########################################################
    # Header
    ###########################################################

    print()

    print("=" * 60)

    print("MODULE 5 - JSON VALIDATION TEST")

    print("=" * 60)

    print()

    ###########################################################
    # Input Path
    ###########################################################

    input_path = os.path.join(

        JSONValidationConfig.INPUT_FOLDER,

        JSONValidationConfig.INPUT_FILENAME

    )

    print(
        f"Input JSON:\n{input_path}"
    )

    print()

    ###########################################################
    # Check Input
    ###########################################################

    if not os.path.exists(input_path):

        print(
            "ERROR: Module 4 OCR JSON was not found."
        )

        print()

        print(
            "Expected:"
        )

        print(
            input_path
        )

        print()

        print(
            "Run Module 4 first."
        )

        return

    ###########################################################
    # Create Validator
    ###########################################################

    validator = JSONValidator()

    ###########################################################
    # Run Validation
    ###########################################################

    try:

        result = validator.validate()

    except Exception as error:

        print()

        print(
            "VALIDATION PIPELINE FAILED"
        )

        print()

        print(
            f"Error: {error}"
        )

        return

    ###########################################################
    # Extract Report
    ###########################################################

    report = result["report"]

    validation = report[
        "validation"
    ]

    ###########################################################
    # Display Status
    ###########################################################

    print()

    print("=" * 60)

    print("FINAL VALIDATION RESULT")

    print("=" * 60)

    print()

    print(
        f"Status       : "
        f"{validation['status']}"
    )

    print(
        f"Valid        : "
        f"{validation['valid']}"
    )

    print(
        f"Error Count  : "
        f"{validation['error_count']}"
    )

    print(
        f"Warning Count: "
        f"{validation['warning_count']}"
    )

    ###########################################################
    # Errors
    ###########################################################

    if report["errors"]:

        print()

        print("-" * 60)

        print("ERRORS")

        print("-" * 60)

        for number, error in enumerate(

            report["errors"],

            start=1

        ):

            print(
                f"{number}. {error}"
            )

    ###########################################################
    # Warnings
    ###########################################################

    if report["warnings"]:

        print()

        print("-" * 60)

        print("WARNINGS")

        print("-" * 60)

        for number, warning in enumerate(

            report["warnings"],

            start=1

        ):

            print(
                f"{number}. {warning}"
            )

    ###########################################################
    # Output Files
    ###########################################################

    print()

    print("-" * 60)

    print("OUTPUT FILES")

    print("-" * 60)

    print()

    print(
        "Validation report:"
    )

    print(
        result["report_path"]
    )

    if result["validated_path"]:

        print()

        print(
            "Validated OCR copy:"
        )

        print(
            result["validated_path"]
        )

    ###########################################################
    # Final Decision
    ###########################################################

    print()

    print("=" * 60)

    if validation["valid"]:

        print(
            "MODULE 5 PASSED"
        )

        print()

        print(
            "OCR JSON is structurally and "
            "logically valid."
        )

        print()

        print(
            "The document can proceed "
            "to Module 6."
        )

    else:

        print(
            "MODULE 5 FAILED"
        )

        print()

        print(
            "OCR JSON contains validation errors."
        )

        print()

        print(
            "The document should NOT proceed "
            "to Module 6 until the issue "
            "is reviewed."
        )

    print()

    print("=" * 60)


if __name__ == "__main__":

    main()