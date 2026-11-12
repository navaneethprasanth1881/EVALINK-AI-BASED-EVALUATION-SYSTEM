class MarkingRuleEngine:
    """Deterministic safeguards for rubric totals and any-N criteria."""
    def clamp(self, result, question):
        qmax = float(question.get("marks") or 0)
        criteria_by_id = {str(c.get("id")): c for c in question.get("criteria", [])}
        # Sub-question criteria are included too.
        for sq in question.get("sub_questions", []):
            for c in sq.get("criteria", []): criteria_by_id[str(c.get("id"))] = c

        total = 0.0
        for c in result.get("criteria", []):
            mx = float(c.get("max_marks", 0) or 0)
            if c.get("criterion_id") in criteria_by_id:
                mx = float(criteria_by_id[c["criterion_id"]].get("marks", mx) or mx)
            val = max(0.0, min(float(c.get("awarded_marks", 0) or 0), mx))
            c["max_marks"] = mx
            c["awarded_marks"] = val
            total += val
        result["max_marks"] = qmax
        result["awarded_marks"] = min(total, qmax) if qmax else total
        return result
