import re
from typing import Dict, List


class SchemaExtractor:
    """Extracts question-level and criterion-level information from an answer scheme."""

    Q_HEADER_RE = re.compile(
        r"(?mi)^\s*(?:Q(?:uestion)?\s*)?(\d{1,3})\s*(?:\(([^)]+)\))?\s*(?:[:.-])?\s*(.*)$"
    )
    CRITERION_MARK_RE = re.compile(
        r"^(?:[•\-\*]\s*)?(.*?)(?:\s*[→:]\s*|\s+)(\d+(?:\.\d+)?)\s*(?:marks?|m)\s*$",
        re.IGNORECASE,
    )
    ANY_N_RE = re.compile(
        r"any\s+(two|three|four|\d+)\b", re.IGNORECASE
    )

    def extract(self, text: str) -> Dict[str, List[Dict]]:
        result = {"questions": {}}
        lines = [line.strip() for line in text.splitlines() if line.strip()]

        current_q = None
        current_sub = None

        for line in lines:
            qmatch = self.Q_HEADER_RE.match(line)
            if qmatch:
                number, sub, title = qmatch.groups()

                # Avoid treating obvious section/module lines as questions.
                if int(number) <= 999:
                    current_q = number
                    current_sub = sub.lower() if sub else None
                    result["questions"].setdefault(
                        current_q,
                        {"criteria": [], "sub_questions": {}}
                    )
                    if title:
                        result["questions"][current_q]["title"] = title
                    if current_sub:
                        result["questions"][current_q]["sub_questions"].setdefault(
                            current_sub, {"criteria": [], "title": title}
                        )
                    continue

            cmatch = self.CRITERION_MARK_RE.match(line)
            if not cmatch:
                continue

            description, marks = cmatch.groups()
            criterion = {
                "description": description.strip(" -•*"),
                "marks": float(marks),
                "rule_type": "standard",
                "required_count": None,
            }

            any_match = self.ANY_N_RE.search(criterion["description"])
            if any_match:
                token = any_match.group(1).lower()
                n = {"two": 2, "three": 3, "four": 4}.get(
                    token,
                    int(token) if token.isdigit() else None
                )
                criterion["rule_type"] = "any_n"
                criterion["required_count"] = n

            if current_q is not None:
                if current_sub:
                    result["questions"][current_q]["sub_questions"][
                        current_sub
                    ]["criteria"].append(criterion)
                else:
                    result["questions"][current_q]["criteria"].append(criterion)

        return result
