import re
from typing import Dict, List


class QuestionExtractor:
    """Generic question-number and question-text extractor.

    This intentionally does not hardcode a subject or question count.
    It is a first-pass parser; the answer scheme is used later to enrich
    each question with marking criteria.
    """

    QUESTION_RE = re.compile(
        r"(?m)^(?:Q(?:uestion)?\s*)?(\d{1,3})\s*[\.)\-:]\s*(.+)$",
        re.IGNORECASE,
    )

    SUBQUESTION_RE = re.compile(
        r"(?m)^\s*(?:\(?([a-z])\)|([a-z])\.)\s*(.+)$",
        re.IGNORECASE,
    )

    MARK_RE = re.compile(r"(\d+(?:\.\d+)?)\s*Marks?", re.IGNORECASE)

    def extract(self, text: str) -> List[Dict]:
        lines = [line.strip() for line in text.splitlines() if line.strip()]
        questions = []

        current = None

        for line in lines:
            match = self.QUESTION_RE.match(line)
            if match:
                if current:
                    questions.append(current)

                number, body = match.groups()
                current = {
                    "number": number,
                    "text": body.strip(),
                    "marks": self._find_marks(body),
                    "sub_questions": [],
                }
                continue

            if current:
                sub = self.SUBQUESTION_RE.match(line)
                if sub:
                    letter = sub.group(1) or sub.group(2)
                    body = sub.group(3).strip()
                    current["sub_questions"].append({
                        "id": f"{current['number']}{letter.lower()}",
                        "text": body,
                        "marks": self._find_marks(body),
                    })
                else:
                    current["text"] += " " + line

        if current:
            questions.append(current)

        return questions

    @staticmethod
    def _find_marks(text: str):
        match = re.search(r"\((\d+(?:\.\d+)?)\s*Marks?\)", text, re.I)
        if match:
            return float(match.group(1))
        match = re.search(r"\[(\d+(?:\.\d+)?)\s*Marks?\]", text, re.I)
        if match:
            return float(match.group(1))
        return None
