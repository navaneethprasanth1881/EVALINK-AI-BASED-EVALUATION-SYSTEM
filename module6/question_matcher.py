from difflib import SequenceMatcher
from typing import Dict, List, Optional


class QuestionMatcher:
    """Matches extracted question paper questions with answer-scheme entries."""

    def similarity(self, a: str, b: str) -> float:
        return SequenceMatcher(
            None,
            (a or "").lower(),
            (b or "").lower()
        ).ratio()

    def match(
        self,
        paper_questions: List[Dict],
        scheme: Dict
    ) -> List[Dict]:
        output = []

        scheme_questions = scheme.get("questions", {})

        for q in paper_questions:
            number = str(q["number"])
            entry = scheme_questions.get(number)

            item = dict(q)
            item["scheme_match"] = entry is not None

            if entry:
                item["scheme"] = entry

            output.append(item)

        return output
