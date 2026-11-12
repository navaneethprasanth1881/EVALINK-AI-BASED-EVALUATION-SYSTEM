import json
from pathlib import Path
from .config7 import OUTPUT_DIR
from .loader import Module7Loader
from .answer_normalizer import AnswerNormalizer
from .local_llm import OllamaEvaluator
from .validator import EvaluationValidator

class Module7Pipeline:
    def __init__(self, model=None):
        import os
        self.model = model or os.getenv("MODULE7_MODEL", "qwen2.5:14b")
        self.loader = Module7Loader()
        self.normalizer = AnswerNormalizer()
        self.evaluator = OllamaEvaluator(self.model)
        self.validator = EvaluationValidator()
    def run(self, question_schema_path, student_answers_path):
        schema = self.loader.load_question_schema(question_schema_path)
        student_data = self.loader.load_student_answers(student_answers_path)
        student = self.normalizer.normalize(student_data)

        questions = schema.get("questions", []) if isinstance(schema, dict) else schema

        if not isinstance(questions, list):
            raise ValueError("Question schema must contain a questions list.")

        # ---------------------------------------------------------
        # OR groups from the question paper
        # Only ONE question from each group counts.
        # If both are answered, the higher mark is selected.
        # ---------------------------------------------------------
        # Read OR/selection groups from the dynamic Module 6 schema.
        # Fallback to no groups if an older schema has none.
        OR_GROUPS = []
        for group in schema.get("selection_groups", []) or []:
            members = {str(n) for n in group.get("questions", [])}
            if len(members) > 1:
                OR_GROUPS.append(members)

        output = []

        # ---------------------------------------------------------
        # Evaluate every question that the student answered
        # ---------------------------------------------------------
        for q in questions:
            number = str(
                q.get("question_number", q.get("number", ""))
            ).strip()

            if number not in student:
                continue

            result = self.evaluator.evaluate(
                q,
                student[number]["answer_text"]
            )

            result = self.validator.validate(result, q)

            result["source_pages"] = student[number]["source_pages"]
            result["ocr_confidence"] = student[number]["ocr_confidence"]

            output.append(result)

        # ---------------------------------------------------------
        # Determine which questions actually count
        # ---------------------------------------------------------
        selected_questions = []
        skipped_questions = []

        evaluated_by_number = {
            str(result.get("question_number", "")).strip(): result
            for result in output
        }

        # Track questions that belong to OR groups
        questions_in_or_groups = set()

        for group in OR_GROUPS:
            questions_in_or_groups.update(group)

        # ---------------------------------------------------------
        # Add normal questions
        # Part A questions are NOT OR questions
        # ---------------------------------------------------------
        for result in output:
            number = str(
                result.get("question_number", "")
            ).strip()

            if number not in questions_in_or_groups:
                selected_questions.append(result)

        # ---------------------------------------------------------
        # For every OR group:
        # choose the question with the highest awarded marks
        # ---------------------------------------------------------
        for group in OR_GROUPS:

            answered = [
                evaluated_by_number[number]
                for number in group
                if number in evaluated_by_number
            ]

            if not answered:
                continue

            # Highest awarded mark wins
            best = max(
                answered,
                key=lambda x: float(x.get("awarded_marks", 0))
            )

            selected_questions.append(best)

            # Record the questions that were not selected
            for result in answered:
                if result is not best:
                    skipped_questions.append({
                        "question_number": result.get("question_number"),
                        "awarded_marks": result.get("awarded_marks"),
                        "max_marks": result.get("max_marks"),
                        "reason": (
                            "OR alternative not counted because "
                            "another answer in the same OR group "
                            "received higher marks."
                        )
                    })

        # ---------------------------------------------------------
        # Calculate FINAL marks only from selected questions
        # ---------------------------------------------------------
        total_max_marks = sum(
            float(result.get("max_marks", 0))
            for result in selected_questions
        )

        total_awarded_marks = sum(
            float(result.get("awarded_marks", 0))
            for result in selected_questions
        )

        percentage = (
            (total_awarded_marks / total_max_marks) * 100
            if total_max_marks > 0
            else 0
        )

        # ---------------------------------------------------------
        # Sort selected questions numerically
        # ---------------------------------------------------------
        selected_questions.sort(
            key=lambda x: int(
                x.get("question_number", 0)
            )
        )

        skipped_questions.sort(
            key=lambda x: int(
                x.get("question_number", 0)
            )
        )

        # ---------------------------------------------------------
        # Final output
        # ---------------------------------------------------------
        final_result = {
            "model": self.model,

            "total_max_marks": total_max_marks,
            "total_awarded_marks": total_awarded_marks,
            "percentage": round(percentage, 2),

            "questions_evaluated": len(output),

            "questions_counted": len(selected_questions),

            "evaluations": output,

            "counted_questions": [
                result.get("question_number")
                for result in selected_questions
            ],

            "or_questions_not_counted": skipped_questions
        }

        # ---------------------------------------------------------
        # Save output
        # ---------------------------------------------------------
        outdir = Path(OUTPUT_DIR)
        outdir.mkdir(parents=True, exist_ok=True)

        path = outdir / (
            f"evaluation_results_"
            f"{self.model.replace(':', '_').replace('/', '_')}.json"
        )

        path.write_text(
            json.dumps(
                final_result,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        return {
            "model": self.model,
            "questions_evaluated": len(output),
            "questions_counted": len(selected_questions),
            "total_max_marks": total_max_marks,
            "total_awarded_marks": total_awarded_marks,
            "percentage": round(percentage, 2),
            "output": str(path)
        }