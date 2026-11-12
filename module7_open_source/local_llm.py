import json
import urllib.request
import urllib.error
from .config7 import OLLAMA_URL, MAX_TOKENS

class OllamaEvaluator:
    """Calls a local Ollama model. No paid API is used."""

    def __init__(self, model):
        self.model = model

    def evaluate(self, question, answer_text):
        prompt = f"""
        You are an academic answer evaluator.

        Evaluate the student's answer ONLY against the supplied question schema
        and marking criteria.

        QUESTION SCHEMA:
        {json.dumps(question, ensure_ascii=False, indent=2)}

        STUDENT ANSWER:
        {answer_text}

        Rules:
        - Evaluate every criterion separately.
        - Award no more than the criterion maximum.
        - Award no more than the question maximum.
        - Award partial marks when the answer partially satisfies a criterion.
        - Accept equivalent wording for correct concepts.
        - For any_n rules, count only the best N valid distinct points.
        - Evidence must come directly from the student answer.
        - Never invent evidence.
        - Never award marks for information that is not present in the answer.
        - Missing concepts must only describe absent requirements.
        - The sum of all criterion awarded_marks MUST equal the question awarded_marks.
        - question awarded_marks MUST NOT exceed question max_marks.
        - Explain clearly WHY the student received the awarded marks.
        - The explanation must refer to specific evidence from the student's answer.
        - If marks are deducted, clearly state what was missing, incorrect,
        incomplete, or unclear.

        Return ONLY valid JSON in exactly this structure:

        {{
        "question_number": "...",
        "max_marks": 0,
        "awarded_marks": 0,
        "marking_explanation": "...",
        "criteria": [
            {{
            "criterion_id": "...",
            "criterion_description": "...",
            "max_marks": 0,
            "awarded_marks": 0,
            "status": "full",
            "evidence": "...",
            "reason": "...",
            "missing_concepts": []
            }}
        ],
        "overall_feedback": "..."
        }}

        Allowed status:
        - full
        - partial
        - not_met

        IMPORTANT:
        1. Calculate awarded_marks from the criterion marks.
        2. Do not exceed max_marks.
        3. Explain the final question score in marking_explanation.
        4. Return JSON only.
        """

        payload = {
            "model": self.model,
            "messages": [
                {
                    "role": "system",
                    "content": "You are a strict rubric-based examination evaluator. Output valid JSON only."
                },
                {"role": "user", "content": prompt}
            ],
            "stream": False,
            "format": "json",
            "options": {
                "num_predict": MAX_TOKENS
            }
        }

        body = json.dumps(payload).encode("utf-8")
        request = urllib.request.Request(
            OLLAMA_URL,
            data=body,
            headers={"Content-Type": "application/json"},
            method="POST"
        )

        try:
            with urllib.request.urlopen(request, timeout=300) as response:
                result = json.loads(response.read().decode("utf-8"))
        except urllib.error.URLError as exc:
            raise RuntimeError(
                f"Could not connect to Ollama at {OLLAMA_URL}. "
                "Make sure Ollama is running."
            ) from exc

        content = result.get("message", {}).get("content", "")
        if not content:
            raise ValueError("Local model returned an empty response.")

        try:
            return json.loads(content)
        except json.JSONDecodeError as exc:
            from .json_utils import extract_json
            return extract_json(content)
