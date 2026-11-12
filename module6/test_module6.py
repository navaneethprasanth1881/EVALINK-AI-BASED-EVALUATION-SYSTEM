import argparse
import json
from pathlib import Path

from .pipeline import Module6Pipeline
from .config6 import OUTPUT_DIR


def main():
    parser = argparse.ArgumentParser(
        description="Dynamic Module 6 - Question and Answer Schema Manager"
    )

    parser.add_argument(
        "--question-paper",
        required=True,
        help="Teacher uploaded question paper PDF",
    )

    parser.add_argument(
        "--answer-schema",
        required=True,
        help="Teacher uploaded answer scheme PDF",
    )

    parser.add_argument(
        "--course-code",
        default=None,
    )

    parser.add_argument(
        "--subject",
        default=None,
    )

    parser.add_argument(
        "--maximum-marks",
        type=float,
        default=None,
    )

    parser.add_argument(
        "--duration",
        default=None,
    )

    args = parser.parse_args()

    pipeline = Module6Pipeline(OUTPUT_DIR)

    result = pipeline.run(
        question_paper_path=args.question_paper,
        answer_schema_path=args.answer_schema,
        exam_metadata={
            "course_code": args.course_code,
            "subject": args.subject,
            "maximum_marks": args.maximum_marks,
            "duration": args.duration,
        },
    )

    print("=" * 70)
    print("MODULE 6 - DYNAMIC QUESTION & ANSWER SCHEMA MANAGER")
    print("=" * 70)

    print(f"Questions detected : {result['paper_question_count']}")
    print(f"Selection groups   : {result['selection_group_count']}")

    validation = result["validation"]

    if validation["valid"]:
        print("Validation         : PASS")
    else:
        print("Validation         : FAIL")

    if validation["errors"]:
        print("\nErrors:")
        for error in validation["errors"]:
            print(f"  - {error}")

    if validation["warnings"]:
        print("\nWarnings:")
        for warning in validation["warnings"]:
            print(f"  - {warning}")

    print("\nGenerated:")
    print(Path(OUTPUT_DIR) / "question_schema.json")
    print(Path(OUTPUT_DIR) / "validation_report.json")
    print(Path(OUTPUT_DIR) / "extracted_documents.json")


if __name__ == "__main__":
    main()
