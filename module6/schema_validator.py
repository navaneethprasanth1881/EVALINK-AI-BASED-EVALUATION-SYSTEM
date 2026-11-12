from typing import Dict, List


class SchemaValidator:

    def validate(self, schema: Dict) -> Dict:
        errors: List[str] = []
        warnings: List[str] = []

        exam = schema.get("exam", {})
        questions = schema.get("questions", [])
        groups = schema.get("selection_groups", [])

        if not questions:
            errors.append("No questions were extracted.")

        numbers = [q.get("number") for q in questions]
        duplicates = {
            n for n in numbers if numbers.count(n) > 1
        }
        if duplicates:
            errors.append(
                f"Duplicate question numbers: {sorted(duplicates)}"
            )

        for q in questions:
            qid = q.get("id", q.get("number"))
            marks = q.get("marks", 0)

            if marks is None:
                warnings.append(f"{qid}: marks not detected.")

            criteria_total = sum(
                float(c.get("marks", 0))
                for c in q.get("criteria", [])
            )

            sub_total = sum(
                sum(float(c.get("marks", 0))
                    for c in sq.get("criteria", []))
                for sq in q.get("sub_questions", [])
            )

            expected = criteria_total + sub_total

            if marks and expected and abs(float(marks) - expected) > 0.001:
                warnings.append(
                    f"{qid}: question marks={marks}, "
                    f"criterion total={expected}. "
                    "Review schema; this may be intentional."
                )

        for group in groups:
            if len(group.get("questions", [])) < 2:
                errors.append(
                    f"{group.get('id')}: selection group has fewer than 2 questions."
                )

            if group.get("selection_rule") == "highest_score":
                if group.get("maximum_counted_marks") is None:
                    warnings.append(
                        f"{group.get('id')}: maximum_counted_marks not detected."
                    )

        return {
            "valid": not errors,
            "error_count": len(errors),
            "warning_count": len(warnings),
            "errors": errors,
            "warnings": warnings,
        }
