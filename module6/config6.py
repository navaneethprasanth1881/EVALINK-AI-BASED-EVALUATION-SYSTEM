from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent
OUTPUT_DIR = BASE_DIR / "output" / "module_6"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

QUESTION_PAPER_PATH = BASE_DIR / "input" / "question_paper.pdf"
ANSWER_SCHEMA_PATH = BASE_DIR / "input" / "answer_schema.pdf"

QUESTION_SCHEMA_OUTPUT = OUTPUT_DIR / "question_schema.json"
VALIDATION_OUTPUT = OUTPUT_DIR / "validation_report.json"
EXTRACTED_TEXT_OUTPUT = OUTPUT_DIR / "extracted_documents.json"

MAX_PDF_PAGES = 100
