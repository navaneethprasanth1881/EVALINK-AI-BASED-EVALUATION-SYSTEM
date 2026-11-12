import json
from pathlib import Path
from .config8 import OUTPUT_DIR
from .report_generator import ReportGenerator

class Module8Pipeline:
    """
    API-free Module 8.

    It consumes Module 7's evaluation_results.json and turns the
    existing evidence, marks, reasons and missing concepts into
    an explainable report. No LLM/API call is made.
    """
    def __init__(self):
        self.reporter = ReportGenerator()

    def run(self, evaluation_path):
        path = Path(evaluation_path)

        if not path.exists():
            raise FileNotFoundError(f"Evaluation file not found: {path}")

        data = json.loads(path.read_text(encoding="utf-8"))

        return self.reporter.generate(data, OUTPUT_DIR)
