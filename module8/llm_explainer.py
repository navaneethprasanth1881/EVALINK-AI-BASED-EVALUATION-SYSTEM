import os
import time
import anthropic
from .config8 import MODEL, MAX_TOKENS

class ExplanationGenerator:
    def __init__(self, model=None):
        self.model = model or MODEL
        key = os.getenv("ANTHROPIC_API_KEY")
        if not key:
            raise RuntimeError("ANTHROPIC_API_KEY environment variable is not set.")
        self.client = anthropic.Anthropic(api_key=key)

    def generate(self, evaluation):
        prompt = f"""
You are an academic feedback generator.

Using ONLY the supplied evaluation result, create a clear explanation
for the student. Do not invent marks, criteria, evidence, or facts.

EVALUATION:
{evaluation}

Return ONLY valid JSON in this exact structure:
{{
  "question_number": "...",
  "score": 0,
  "max_marks": 0,
  "criterion_explanations": [
    {{
      "criterion_id": "...",
      "status": "full",
      "awarded_marks": 0,
      "max_marks": 0,
      "evidence": "...",
      "explanation": "...",
      "missing_concepts": []
    }}
  ],
  "strengths": [],
  "areas_for_improvement": [],
  "overall_feedback": "..."
}}

Allowed status values: full, partial, not_met.
Use double quotes and valid JSON. No markdown fences.
"""
        for attempt in range(3):
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=MAX_TOKENS,
                    messages=[{"role": "user", "content": prompt}],
                )
                raw = "".join(
                    block.text for block in response.content
                    if hasattr(block, "text")
                ).strip()
                from .json_utils import extract_json
                return extract_json(raw)
            except (anthropic.InternalServerError,
                    anthropic.APIConnectionError,
                    anthropic.RateLimitError):
                if attempt == 2:
                    raise
                time.sleep(2 ** attempt)
