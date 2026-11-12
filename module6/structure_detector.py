import re
from typing import Dict, List


class StructureDetector:
    """Detects sections, OR relationships and generic selection language."""

    OR_RE = re.compile(
        r"(?i)\bOR\b"
    )

    def detect_selection_groups(
        self,
        question_text: str,
        question_numbers: List[str],
    ) -> List[Dict]:
        groups = []

        # Explicit pair form: "9 OR 10", "Q9 OR Q10"
        for a, b in re.findall(
            r"(?i)\bQ?\s*(\d+)\s+OR\s+Q?\s*(\d+)\b",
            question_text
        ):
            groups.append({
                "questions": [a, b],
                "selection_type": "OR",
                "selection_rule": "highest_score",
            })

        # If OCR/text has standalone OR separators, pairing is ambiguous.
        # Do not guess; the caller should review/approve these groups.
        if not groups and len(question_numbers) >= 2:
            pass

        return groups

    def detect_any_n_instruction(self, text: str):
        match = re.search(
            r"(?i)answer\s+any\s+(\d+)",
            text
        )
        if match:
            return {
                "type": "ANY_N",
                "n": int(match.group(1))
            }
        return None
