import os
import sys
import json
from pathlib import Path
import os
import sys
from pathlib import Path

# Backend directory
BACKEND_DIR = Path(__file__).resolve().parent

# Main project directory: restart/
PROJECT_ROOT = BACKEND_DIR.parent.parent

# Add module directories to Python path
MODULE_PATHS = [
    PROJECT_ROOT,
    PROJECT_ROOT / "module6",
    PROJECT_ROOT / "module5",
    PROJECT_ROOT / "module4",
    PROJECT_ROOT / "modul2",
    PROJECT_ROOT / "module",
    PROJECT_ROOT / "module7_gpt",
    PROJECT_ROOT / "module7_open_source",
    PROJECT_ROOT / "module8",
    PROJECT_ROOT / "module8_option1",
]

for path in MODULE_PATHS:
    if path.exists() and str(path) not in sys.path:
        sys.path.insert(0, str(path))

print("[EvaLink] Project root:", PROJECT_ROOT)

# ============================================================
# PROJECT ROOT
# ============================================================
import sys
from pathlib import Path

# Backend directory
BACKEND_DIR = Path(__file__).resolve().parent

# Project root: restart/
PROJECT_ROOT = BACKEND_DIR.parent.parent

# Add project root to Python imports
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

print("[EvaLink] Project root:", PROJECT_ROOT)
PROJECT_ROOT = Path(__file__).resolve().parents[1]


# ============================================================
# PYTHON IMPORT PATHS
# ============================================================

# Existing modules use a mixture of package-relative
# and legacy absolute imports.
for p in [
    PROJECT_ROOT,
    PROJECT_ROOT / "modul2",
    PROJECT_ROOT / "module4",
    PROJECT_ROOT / "module5",
]:
    if str(p) not in sys.path:
        sys.path.insert(0, str(p))


# ============================================================
# SUPPORTED EVALUATION MODELS
# ============================================================

SUPPORTED_EVALUATION_MODELS = {
    "llama3.1:8b": {
        "name": "Llama 3.1 8B",
        "provider": "Ollama",
    },
    "gpt-5.6-luna": {
        "name": "GPT-5.6 Luna",
        "provider": "OpenAI",
    },
    "claude-sonnet-4-6": {
        "name": "Claude Sonnet 4.6",
        "provider": "Anthropic",
    },
}


# ============================================================
# FULL EVALUATION PIPELINE
# ============================================================

def run_full_evaluation(
    answer_pdf,
    question_pdf,
    rubric_pdf,
    model="llama3.1:8b",
):
    """
    Run the complete EvaLink answer evaluation pipeline.

    PIPELINE
    --------

    Module 1
        Image Quality Analysis

    Module 2
        Image Preprocessing

    Module 3
        Document Management

    Module 4
        Claude OCR ONLY

    Module 5
        OCR JSON Validation

    Module 6
        Dynamic Question + Rubric Schema

    Module 7
        Evaluation Model
            - Llama 3.1 8B
            - GPT-5.6 Luna
            - Claude Sonnet 4.6

    Module 8
        API-free Explainability

    IMPORTANT
    ---------

    Claude is used in Module 4 for OCR.

    Claude can ALSO be selected independently in Module 7
    as an evaluation model.

    Qwen is NOT supported.
    """

    # ========================================================
    # RESOLVE INPUT PATHS
    # ========================================================

    answer_pdf = Path(answer_pdf).resolve()
    question_pdf = Path(question_pdf).resolve()
    rubric_pdf = Path(rubric_pdf).resolve()

    # ========================================================
    # VALIDATE INPUT FILES
    # ========================================================

    if not answer_pdf.exists():
        raise FileNotFoundError(
            f"Answer PDF not found: {answer_pdf}"
        )

    if not question_pdf.exists():
        raise FileNotFoundError(
            f"Question paper not found: {question_pdf}"
        )

    if not rubric_pdf.exists():
        raise FileNotFoundError(
            f"Rubric / answer scheme not found: {rubric_pdf}"
        )

    # ========================================================
    # VALIDATE EVALUATION MODEL
    # ========================================================

    if model not in SUPPORTED_EVALUATION_MODELS:

        supported = "\n".join(
            f"  - {key} "
            f"({value['name']} / {value['provider']})"
            for key, value
            in SUPPORTED_EVALUATION_MODELS.items()
        )

        raise ValueError(
            f"Unsupported evaluation model: {model}\n\n"
            f"Supported evaluation models:\n"
            f"{supported}"
        )

    model_info = SUPPORTED_EVALUATION_MODELS[model]

    print("\n")
    print("=" * 70)
    print("EvaLink - FULL ANSWER EVALUATION PIPELINE")
    print("=" * 70)

    print(
        f"Evaluation Model : {model_info['name']}"
    )

    print(
        f"Provider         : {model_info['provider']}"
    )

    print("=" * 70)

    # ========================================================
    # MODULE 1
    # IMAGE QUALITY ANALYSIS
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 1 - IMAGE QUALITY ANALYSIS")
    print("=" * 70)

    from module1.quality_analyzer import QualityAnalyzer

    quality_analyzer = QualityAnalyzer()

    document = quality_analyzer.analyze(
        str(answer_pdf)
    )

    print(
        "[EvaLink] Module 1 completed successfully."
    )

    # ========================================================
    # MODULE 2
    # IMAGE PREPROCESSING
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 2 - IMAGE PREPROCESSING")
    print("=" * 70)

    from modul2.preprocessor import Preprocessor

    preprocessor = Preprocessor()

    document = preprocessor.process(
        document
    )

    print(
        "[EvaLink] Module 2 completed successfully."
    )

    # ========================================================
    # MODULE 3
    # DOCUMENT MANAGEMENT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 3 - DOCUMENT MANAGEMENT")
    print("=" * 70)

    from module3.document_analyzer import DocumentAnalyzer

    document_analyzer = DocumentAnalyzer()

    document = document_analyzer.analyze(
        document
    )

    # --------------------------------------------------------
    # DOCUMENT VALIDATION
    # --------------------------------------------------------

    if not document.is_valid:

        errors = document.analysis_report.get(
            "errors",
            []
        )

        if errors:

            error_message = "; ".join(
                str(error)
                for error in errors
            )

        else:

            error_message = (
                "Unknown document validation error."
            )

        raise RuntimeError(
            "Document validation failed: "
            + error_message
        )

    print(
        "[EvaLink] Module 3 completed successfully."
    )

    # ========================================================
    # MODULE 4
    # CLAUDE OCR
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 4 - CLAUDE OCR")
    print("=" * 70)

    print(
        "[EvaLink] Claude is being used for OCR."
    )

    from ocr_processor import OCRProcessor
    from ocr_report import OCRReport

    ocr_processor = OCRProcessor()

    document = ocr_processor.process(
        document
    )

    # Save OCR output/report
    OCRReport().save(
        document
    )

    print(
        "[EvaLink] Module 4 completed successfully."
    )

    # ========================================================
    # MODULE 5
    # OCR JSON VALIDATION
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 5 - OCR JSON VALIDATION")
    print("=" * 70)

    from json_validator import JSONValidator

    validator = JSONValidator()

    validation = validator.validate_document(
        document
    )

    # --------------------------------------------------------
    # VALIDATION CHECK
    # --------------------------------------------------------

    if not document.json_valid:

        raise RuntimeError(
            "OCR JSON validation failed."
        )

    print(
        "[EvaLink] Module 5 completed successfully."
    )

    # ========================================================
    # LOCATE OCR OUTPUT
    # ========================================================

    # Backend output directory
    OUTPUT_DIR = BACKEND_DIR / "output"

    # Module 4 OCR output
    ocr_path = (
        OUTPUT_DIR / "module_4" / "ocr_result.json"
    )

    # Module 5 validated output
    validated_path = (
        OUTPUT_DIR / "module_5" / "validated_ocr.json"
    )

    # --------------------------------------------------------
    # USE VALIDATED OCR WHEN AVAILABLE
    # --------------------------------------------------------

    if validated_path.exists():

        student_answers = validated_path

        print(
            "[EvaLink] Using validated OCR:"
        )

        print(
            f"          {validated_path}"
        )

    elif ocr_path.exists():

        student_answers = ocr_path

        print(
            "[EvaLink] Validated OCR not found."
        )

        print(
            "[EvaLink] Falling back to OCR result:"
        )

        print(
            f"          {ocr_path}"
        )

    else:

        raise FileNotFoundError(
            "OCR output was not found.\n\n"
            f"Expected:\n"
            f"  {validated_path}\n"
            f"or:\n"
            f"  {ocr_path}"
        )

    # ========================================================
    # MODULE 6
    # DYNAMIC QUESTION/RUBRIC SCHEMA
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 6 - DYNAMIC QUESTION/RUBRIC SCHEMA")
    print("=" * 70)

    from module6.pipeline import Module6Pipeline
    from module6.config6 import OUTPUT_DIR as M6_OUTPUT

    m6 = Module6Pipeline(
        M6_OUTPUT
    )

    m6_result = m6.run(
        str(question_pdf),
        str(rubric_pdf)
    )

    # --------------------------------------------------------
    # MODULE 6 VALIDATION
    # --------------------------------------------------------

    if not m6_result["validation"]["valid"]:

        errors = (
            m6_result["validation"].get(
                "errors",
                []
            )
        )

        if errors:

            error_message = "; ".join(
                str(error)
                for error in errors
            )

        else:

            error_message = (
                "Unknown question/rubric schema error."
            )

        raise RuntimeError(
            "Question/rubric schema validation failed: "
            + error_message
        )

    # --------------------------------------------------------
    # SCHEMA PATH
    # --------------------------------------------------------

    schema_path = (
        Path(M6_OUTPUT)
        / "question_schema.json"
    )

    if not schema_path.exists():

        raise FileNotFoundError(
            "Module 6 did not create "
            "question_schema.json:\n"
            f"{schema_path}"
        )

    print(
        "[EvaLink] Question schema created:"
    )

    print(
        f"          {schema_path}"
    )

    print(
        "[EvaLink] Module 6 completed successfully."
    )

    # ========================================================
    # MODULE 7
    # ANSWER EVALUATION
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 7 - LLM ANSWER EVALUATION")
    print("=" * 70)

    print(
        f"[EvaLink] Selected model: "
        f"{model_info['name']}"
    )

    print(
        f"[EvaLink] Provider: "
        f"{model_info['provider']}"
    )

    # --------------------------------------------------------
    # Llama 3.1 8B
    # --------------------------------------------------------

    if model == "llama3.1:8b":

        print(
            "[EvaLink] Starting Llama evaluation "
            "through Ollama..."
        )

        from module7_open_source.pipeline import (
            Module7Pipeline as LocalPipeline
        )

        evaluator = LocalPipeline(
            model=model
        )

    # --------------------------------------------------------
    # GPT-5.6 Luna
    # --------------------------------------------------------

    elif model == "gpt-5.6-luna":

        print(
            "[EvaLink] Starting GPT evaluation "
            "through OpenAI..."
        )

        from module7_gpt.pipeline import (
            Module7Pipeline as GPTPipeline
        )
        import module7_gpt.pipeline

        print(
            "[DEBUG] ACTUAL MODULE 7 FILE:",
            module7_gpt.pipeline.__file__,
            flush=True
        )
        evaluator = GPTPipeline(
            model=model
        )

    # --------------------------------------------------------
    # Claude Sonnet 4.6
    # --------------------------------------------------------

    elif model == "claude-sonnet-4-6":

        print(
            "[EvaLink] Starting Claude evaluation "
            "through Anthropic..."
        )

        from module7_claude.pipeline import (
            Module7Pipeline as ClaudePipeline
        )

        evaluator = ClaudePipeline(
            model=model
        )

    # --------------------------------------------------------
    # SHOULD NEVER HAPPEN
    # --------------------------------------------------------

    else:

        raise ValueError(
            f"Unsupported evaluation model: {model}"
        )

    # ========================================================
    # RUN MODULE 7
    # ========================================================

    m7_result = evaluator.run(
        str(schema_path),
        str(student_answers)
    )

    # ========================================================
    # GET EVALUATION OUTPUT
    # ========================================================

    if not m7_result:

        raise RuntimeError(
            "Module 7 returned an empty result."
        )

    if "output" not in m7_result:

        raise RuntimeError(
            "Module 7 result does not contain "
            "'output'."
        )

    eval_path = Path(
        m7_result["output"]
    )

    # ========================================================
    # CHECK EVALUATION FILE
    # ========================================================

    if not eval_path.exists():

        raise FileNotFoundError(
            "Module 7 evaluation output was not created:\n"
            f"{eval_path}"
        )

    print(
        "[EvaLink] Evaluation output created:"
    )

    print(
        f"          {eval_path}"
    )

    print(
        "[EvaLink] Module 7 completed successfully."
    )

    # ========================================================
    # MODULE 8
    # API-FREE EXPLAINABILITY
    # ========================================================

    print("\n")
    print("=" * 70)
    print("MODULE 8 - EXPLAINABILITY")
    print("=" * 70)

    try:

        from module8_option1.pipeline import (
            Module8Pipeline
        )

        m8 = Module8Pipeline()

        m8_result = m8.run(
            str(eval_path)
        )

        print(
            "[EvaLink] Module 8 completed successfully."
        )

    except Exception as e:

        # Module 8 is supplementary.
        # Evaluation should still be available
        # if explainability fails.

        print(
            "[EvaLink] Module 8 warning:"
        )

        print(
            f"          {e}"
        )

        m8_result = {
            "status": "failed",
            "error": str(e),
        }

    # ========================================================
    # LOAD MODULE 7 EVALUATION JSON
    # ========================================================

    try:

        data = json.loads(
            eval_path.read_text(
                encoding="utf-8"
            )
        )

    except json.JSONDecodeError as e:

        raise RuntimeError(
            "Module 7 produced invalid JSON:\n"
            f"{e}"
        )

    # ========================================================
    # STUDENT INFORMATION
    # ========================================================

    student = data.get(
        "student",
        {}
    )

    # --------------------------------------------------------
    # Module 7 may not contain complete student metadata.
    # Therefore recover it from Module 4 OCR.
    # --------------------------------------------------------

    try:

        if ocr_path.exists():

            ocr_data = json.loads(
                ocr_path.read_text(
                    encoding="utf-8"
                )
            )

            if ocr_data.get("student"):

                student = (
                    ocr_data["student"]
                )

    except Exception as e:

        print(
            "[EvaLink] Warning while reading "
            "student metadata:"
        )

        print(
            f"          {e}"
        )

    # ========================================================
    # BUILD FINAL RESULT
    # ========================================================

    result = {
        # ----------------------------------------------------
        # Student
        # ----------------------------------------------------

        "student": student,

        # ----------------------------------------------------
        # Evaluation
        # ----------------------------------------------------

        "evaluation": data,

        # ----------------------------------------------------
        # Selected model
        # ----------------------------------------------------

        "model": model,

        "model_name": model_info[
            "name"
        ],

        "provider": model_info[
            "provider"
        ],

        # ----------------------------------------------------
        # File paths
        # ----------------------------------------------------

        "evaluation_path": str(
            eval_path
        ),

        "explainability": m8_result,

        "schema_path": str(
            schema_path
        ),

        "ocr_path": str(
            ocr_path
        ),

        # ----------------------------------------------------
        # Module 5 validation
        # ----------------------------------------------------

        "validation": document.validation_result,
    }

    # ========================================================
    # FINAL CONSOLE OUTPUT
    # ========================================================

    print("\n")
    print("=" * 70)
    print("EvaLink - EVALUATION COMPLETED")
    print("=" * 70)

    print(
        f"Student       : "
        f"{student.get('name', 'Unknown')}"
    )

    print(
        f"Evaluation    : "
        f"{model_info['name']}"
    )

    print(
        f"Provider      : "
        f"{model_info['provider']}"
    )

    print(
        f"Evaluation JSON:"
    )

    print(
        f"  {eval_path}"
    )

    print(
        f"Schema:"
    )

    print(
        f"  {schema_path}"
    )

    print("=" * 70)

    return result