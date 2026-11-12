import re
from typing import Dict


class MarkingRuleParser:

    def parse(self, description: str, marks: float) -> Dict:
        text = description.strip()

        any_match = re.search(
            r"(?i)\bany\s+(two|three|four|\d+)\b",
            text
        )

        if any_match:
            token = any_match.group(1).lower()
            n = {
                "two": 2,
                "three": 3,
                "four": 4,
            }.get(token)

            if n is None and token.isdigit():
                n = int(token)

            return {
                "description": text,
                "marks": marks,
                "rule_type": "any_n",
                "required_count": n,
            }

        return {
            "description": text,
            "marks": marks,
            "rule_type": "standard",
            "required_count": None,
        }
