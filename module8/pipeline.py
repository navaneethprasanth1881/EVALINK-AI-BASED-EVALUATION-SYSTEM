import json
from pathlib import Path
from .config8 import OUTPUT_DIR
from .llm_explainer import ExplanationGenerator
from .report_generator import ReportGenerator

class Module8Pipeline:
    def __init__(self, model=None):
        self.explainer = ExplanationGenerator(model=model)
        self.reporter = ReportGenerator()

    def run(self, evaluation_path):
        data = json.loads(Path(evaluation_path).read_text(encoding="utf-8"))

        if isinstance(data, dict):
            evaluations = data.get("evaluations") or data.get("results") or data.get("questions")
            student = data.get("student", {})
        else:
            evaluations, student = data, {}

        if not isinstance(evaluations, list):
            raise ValueError("Evaluation JSON must contain a list under evaluations/results/questions.")

        explanations = []
        for evaluation in evaluations:
            explanations.append(self.explainer.generate(evaluation))

        output = Path(OUTPUT_DIR)
        output.mkdir(parents=True, exist_ok=True)

        json_path = output / "explainability_results.json"
        json_path.write_text(
            json.dumps({"student": student, "evaluations": explanations}, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        html_path = output / "evaluation_report.html"
        self.reporter.generate_html(explanations, html_path, student)

        return {
            "explainability_json": str(json_path),
            "html_report": str(html_path),
            "questions": len(explanations),
        }
