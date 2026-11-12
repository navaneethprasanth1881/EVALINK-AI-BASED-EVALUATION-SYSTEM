class EvaluationValidator:
    def validate(self, result, question):
        if not isinstance(result, dict):
            raise ValueError("Evaluation result must be an object.")

        max_marks = float(question.get("max_marks", result.get("max_marks", 0)) or 0)
        awarded = float(result.get("awarded_marks", result.get("score", 0)) or 0)

        if awarded < 0:
            result["awarded_marks"] = 0

        if awarded > max_marks:
            result["awarded_marks"] = max_marks

        result["max_marks"] = max_marks
        result["awarded_marks"] = float(result.get("awarded_marks", 0))

        criteria = result.get("criteria", []) or []
        for c in criteria:
            cmax = float(c.get("max_marks", 0) or 0)
            cscore = float(c.get("awarded_marks", 0) or 0)
            c["max_marks"] = cmax
            c["awarded_marks"] = max(0.0, min(cscore, cmax))

        return result
