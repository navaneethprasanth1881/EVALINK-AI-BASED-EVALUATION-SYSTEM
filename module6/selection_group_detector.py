import re
from typing import Dict, List


class SelectionGroupDetector:

    def detect_from_text(self, text: str) -> List[Dict]:
        groups = []

        # Detect explicit "Qx OR Qy" patterns.
        for a, b in re.findall(
            r"(?i)\bQ?\s*(\d+)\s+OR\s+Q?\s*(\d+)\b",
            text
        ):
            group_id = f"SG_{a}_{b}"
            if not any(g["id"] == group_id for g in groups):
                groups.append({
                    "id": group_id,
                    "selection_type": "OR",
                    "questions": [a, b],
                    "selection_rule": "highest_score",
                    "maximum_counted_marks": None,
                })

        return groups
