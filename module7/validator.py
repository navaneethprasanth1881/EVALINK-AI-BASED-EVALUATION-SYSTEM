class EvaluationValidator:
    def validate(self, evaluation):
        errors=[]; warnings=[]
        for e in evaluation.get("evaluations", []):
            if not e.get("question_number"):
                errors.append("Evaluation missing question_number.")
            if float(e.get("awarded_marks",0)) < 0:
                errors.append(f"{e.get('question_number')}: negative awarded marks.")
            if float(e.get("awarded_marks",0)) > float(e.get("max_marks",0)) + 1e-9:
                errors.append(f"{e.get('question_number')}: awarded marks exceed maximum.")
            for c in e.get("criteria", []):
                if not c.get("criterion_id"): warnings.append(f"{e.get('question_number')}: criterion without ID.")
        return {"valid": not errors, "error_count":len(errors), "warning_count":len(warnings), "errors":errors, "warnings":warnings}
