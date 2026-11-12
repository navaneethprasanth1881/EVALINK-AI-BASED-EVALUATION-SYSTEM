import json
import os
import re
from typing import Dict, List


class TeacherStructureLLM:
    """Optional second-stage LLM parser for OCR text that regex cannot reliably parse."""

    def __init__(self, model=None):
        self.model = model or os.getenv("MODULE6_MODEL", "claude-sonnet-4-6")

    def _client(self):
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            return None
        try:
            import anthropic
        except ImportError:
            return None
        return anthropic.Anthropic(api_key=key)

    @staticmethod
    def _json(text: str):
        text = text.strip()
        fenced = re.search(r"```(?:json)?\s*(.*?)\s*```", text, re.S | re.I)
        if fenced:
            text = fenced.group(1)
        start = min([x for x in [text.find("{"), text.find("[")] if x >= 0], default=-1)
        if start < 0:
            raise ValueError("No JSON found in model response")
        candidate = text[start:]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            # Try progressively shorter endings for common trailing commentary.
            for end in range(candidate.rfind("}"), 0, -1):
                try:
                    return json.loads(candidate[:end + 1])
                except Exception:
                    continue
            raise

    def parse_question_paper(self, text: str) -> List[Dict]:
        client = self._client()
        if not client:
            return []
        prompt = f"""Extract all questions from this teacher question paper.
Do not invent questions. Return ONLY JSON array. Each item:
{{"number":"9","text":"...","marks":9,"section":"Part B","sub_questions":[{{"id":"9a","text":"...","marks":5}}]}}
Use null for unknown marks. Preserve OR/choice wording inside text.\n\n{text}"""
        response = client.messages.create(model=self.model, max_tokens=12000,
            messages=[{"role":"user", "content": prompt}])
        raw = "\n".join(getattr(b, "text", "") for b in response.content)
        data = self._json(raw)
        return data if isinstance(data, list) else data.get("questions", [])

    def parse_answer_scheme(self, text: str) -> Dict:
        client = self._client()
        if not client:
            return {"questions": {}}
        prompt = f"""Extract the complete marking/valuation scheme below. Return ONLY JSON.
Shape: {{"questions": {{"9": {{"criteria":[{{"description":"...","marks":5,"rule_type":"standard","required_count":null}}], "sub_questions": {{"a": {{"criteria":[...]}}}}}}}}}}
Capture every criterion and its marks. For 'any N' rules use rule_type 'any_n' and required_count N.
Do not invent or combine criteria.\n\n{text}"""
        response = client.messages.create(model=self.model, max_tokens=14000, temperature=0,
            messages=[{"role":"user", "content": prompt}])
        raw = "\n".join(getattr(b, "text", "") for b in response.content)
        data = self._json(raw)
        return data if isinstance(data, dict) else {"questions": {}}
