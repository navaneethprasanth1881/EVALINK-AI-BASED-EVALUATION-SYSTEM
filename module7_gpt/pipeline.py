import json
from pathlib import Path

from .config7 import OUTPUT_DIR
from .loader import Module7Loader
from .answer_normalizer import AnswerNormalizer
from .openai_evaluator import OpenAIEvaluator
from .validator import EvaluationValidator


class Module7Pipeline:

    def __init__(self, model=None):
        self.loader = Module7Loader()
        self.normalizer = AnswerNormalizer()
        self.evaluator = OpenAIEvaluator(model)
        self.validator = EvaluationValidator()

    def run(self, question_schema_path, student_answers_path):
        print("### NEW MODULE 7 PIPELINE EXECUTING ###", flush=True)
        # ---------------------------------------------------------
        # Load question schema and student answers
        # ---------------------------------------------------------
        schema = self.loader.load_json(question_schema_path)

        student_data = self.loader.load_json(student_answers_path)
        student = self.normalizer.normalize(student_data)
        print("[DEBUG] Normalized answer numbers:", list(student.keys()))
        questions = (
            schema.get("questions", [])
            if isinstance(schema, dict)
            else schema
        )
        print("\n========== MODULE 7 SCHEMA DEBUG ==========", flush=True)

        for q in questions:
            print(
                "[DEBUG] Parent:",
                q.get("question_number", q.get("number")),
                "| Subquestions:",
                [
                    sq.get("id")
                    for sq in q.get("sub_questions", [])
                ],
                flush=True
            )

        print("============================================\n", flush=True)
        if not isinstance(questions, list):
            raise ValueError(
                "Question schema must contain a questions list."
            )

        # ---------------------------------------------------------
        # Evaluate every question answered by the student
        # ---------------------------------------------------------
                # ---------------------------------------------------------
        # Evaluate answered questions, including nested sub-questions
        # ---------------------------------------------------------
        evaluations = []

        for q in questions:

            number = str(
                q.get("question_number", q.get("number", ""))
            ).strip()

            sub_questions = q.get("sub_questions", [])

            # -----------------------------------------------------
            # Handle questions containing sub-questions (Q7, etc.)
            # -----------------------------------------------------
            if sub_questions:

                sub_evaluations = []

                for sub_q in sub_questions:

                    sub_number = str(
                        sub_q.get("id", "")
                    ).strip()

                    # Skip only this sub-question if unanswered
                    print(
                        f"[DEBUG] Checking sub-question: {sub_number}",
                        f"| Available answers: {list(student.keys())}",
                        flush=True
                    )

                    if sub_number not in student:
                        print(f"[DEBUG] No answer found for: {sub_number}", flush=True)
                        continue

                    print(f"[DEBUG] EVALUATING SUB-QUESTION: {sub_number}", flush=True)

                    # Prepare a standalone question for evaluation
                    evaluation_question = {
                        **sub_q,
                        "number": sub_number,
                        "question_number": sub_number
                    }

                    result = self.evaluator.evaluate(
                        evaluation_question,
                        student[sub_number]["answer_text"]
                    )
                    print(f"[DEBUG] EVALUATOR COMPLETED: {sub_number}", flush=True)
                    result = self.validator.validate(
                        result,
                        evaluation_question
                    )

                    result["question_number"] = sub_number

                    result["source_pages"] = student[
                        sub_number
                    ]["source_pages"]

                    result["ocr_confidence"] = student[
                        sub_number
                    ]["ocr_confidence"]

                    sub_evaluations.append(result)

                # If none of the sub-questions was answered,
                # do not add this parent question.
                if not sub_evaluations:
                    continue

                # Parent maximum includes ALL its sub-questions,
                # including unanswered ones.
                parent_max = sum(
                    float(sq.get("marks", 0))
                    for sq in sub_questions
                )

                parent_awarded = sum(
                    float(r.get("awarded_marks", 0))
                    for r in sub_evaluations
                )

                evaluations.append({
                    "question_number": number,
                    "max_marks": parent_max,
                    "awarded_marks": parent_awarded,
                    "criteria": [
                        criterion
                        for r in sub_evaluations
                        for criterion in r.get("criteria", [])
                    ],
                    "sub_question_evaluations": sub_evaluations,
                    "overall_feedback": " ".join(
                        r.get("overall_feedback", "")
                        for r in sub_evaluations
                    ),
                    "source_pages": sorted(set(
                        page
                        for r in sub_evaluations
                        for page in r.get("source_pages", [])
                    )),
                    "ocr_confidence": sum(
                        float(r.get("ocr_confidence", 0))
                        for r in sub_evaluations
                    ) / len(sub_evaluations)
                })

                continue

            # -----------------------------------------------------
            # Handle normal questions (Q2, Q3, Q4, etc.)
            # -----------------------------------------------------
            if number not in student:
                continue

            result = self.evaluator.evaluate(
                q,
                student[number]["answer_text"]
            )

            result = self.validator.validate(
                result,
                q
            )

            result["question_number"] = number
            result["source_pages"] = student[number]["source_pages"]
            result["ocr_confidence"] = student[number]["ocr_confidence"]

            evaluations.append(result)

        # ---------------------------------------------------------
        # Create lookup by question number
        # ---------------------------------------------------------
        evaluated_by_number = {
            str(r.get("question_number", "")).strip(): r
            for r in evaluations
        }

        # ---------------------------------------------------------
        # OR groups from the question paper
        #
        # Q9  OR Q10
        # Q11 OR Q12
        # Q13 OR Q14
        # Q15 OR Q16
        #
        # Only ONE question from each pair counts.
        # If both are answered, highest awarded mark counts.
        # ---------------------------------------------------------
        or_groups = [
            {"7", "8"},
            {"9", "10"},
            {"11", "12"}
        ]
        '''or_groups = [
            {"9", "10"},
            {"11", "12"},
            {"13", "14"},
            {"15", "16"}
        ]'''

        or_questions = set()

        for group in or_groups:
            or_questions.update(group)

        # ---------------------------------------------------------
        # Questions that actually count toward final marks
        # ---------------------------------------------------------
        counted_questions = []

        # Part A and any other non-OR questions
        for result in evaluations:

            number = str(
                result.get("question_number", "")
            ).strip()

            if number not in or_questions:
                counted_questions.append(result)

        # ---------------------------------------------------------
        # Select the highest-scoring answer from each OR pair
        # ---------------------------------------------------------
        or_not_counted = []

        for group in or_groups:

            answered = [
                evaluated_by_number[number]
                for number in group
                if number in evaluated_by_number
            ]

            # Student answered neither question
            if not answered:
                continue

            # Student answered only one
            if len(answered) == 1:

                counted_questions.append(answered[0])

                continue

            # Student answered BOTH
            # Select the one with highest awarded marks
            best = max(
                answered,
                key=lambda r: float(
                    r.get("awarded_marks", 0)
                )
            )

            counted_questions.append(best)

            # Store the other answer as not counted
            for result in answered:

                if result is not best:

                    or_not_counted.append({
                        "question_number": result.get(
                            "question_number"
                        ),
                        "max_marks": result.get(
                            "max_marks", 0
                        ),
                        "awarded_marks": result.get(
                            "awarded_marks", 0
                        ),
                        "reason": (
                            "Both questions in the OR group "
                            "were answered. This question was "
                            "not counted because the other "
                            "answer received higher marks."
                        )
                    })

        # ---------------------------------------------------------
        # Sort questions numerically
        # ---------------------------------------------------------
        counted_questions.sort(
            key=lambda r: int(
                r.get("question_number", 0)
            )
        )

        or_not_counted.sort(
            key=lambda r: int(
                r.get("question_number", 0)
            )
        )

        # ---------------------------------------------------------
        # Calculate FINAL marks
        # ---------------------------------------------------------
        # The examination has a fixed maximum of 60 marks.
        total_max_marks = 60.0

        total_awarded_marks = sum(
            float(
                r.get("awarded_marks", 0)
            )
            for r in counted_questions
        )

        # ---------------------------------------------------------
        # Make sure the question paper remains 60 marks
        # ---------------------------------------------------------
        if total_max_marks > 60:

            raise ValueError(
                f"Calculated maximum marks is "
                f"{total_max_marks}, but the examination "
                f"is only 60 marks."
            )

        # ---------------------------------------------------------
        # Calculate percentage
        # ---------------------------------------------------------
        percentage = (
            (total_awarded_marks / total_max_marks) * 100
            if total_max_marks > 0
            else 0
        )

        # ---------------------------------------------------------
        # Final result
        # ---------------------------------------------------------
        final_result = {

            "model": self.evaluator.model,

            "total_max_marks": total_max_marks,

            "total_awarded_marks": total_awarded_marks,

            "percentage": round(
                percentage,
                2
            ),

            "questions_evaluated": len(
                evaluations
            ),

            "questions_counted": len(
                counted_questions
            ),

            # Every evaluated question
            "evaluations": evaluations,

            # Questions actually used for final score
            "counted_questions": [
                r.get("question_number")
                for r in counted_questions
            ],

            # OR answers that were evaluated but not counted
            "or_questions_not_counted": or_not_counted
        }

        # ---------------------------------------------------------
        # Save output
        # ---------------------------------------------------------
        output_dir = Path(OUTPUT_DIR)

        output_dir.mkdir(
            parents=True,
            exist_ok=True
        )

        safe_model = (
            self.evaluator.model or "openai"
        ).replace(":", "_").replace("/", "_")

        path = (
            output_dir
            / f"evaluation_results_{safe_model}.json"
        )

        path.write_text(
            json.dumps(
                final_result,
                indent=2,
                ensure_ascii=False
            ),
            encoding="utf-8"
        )

        # ---------------------------------------------------------
        # Return summary
        # ---------------------------------------------------------
        return {

            "model": self.evaluator.model,

            "questions_evaluated": len(
                evaluations
            ),

            "questions_counted": len(
                counted_questions
            ),

            "total_max_marks": total_max_marks,

            "total_awarded_marks": total_awarded_marks,

            "percentage": round(
                percentage,
                2
            ),

            "output": str(path)
        }