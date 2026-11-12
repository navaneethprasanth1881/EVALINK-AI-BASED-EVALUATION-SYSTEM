import os
import time

import anthropic

from .config7 import MODEL, MAX_TOKENS
from .json_utils import extract_json


class RubricEvaluator:

    def __init__(self, model=None):
        self.model = model or MODEL

        api_key = os.getenv("ANTHROPIC_API_KEY")

        if not api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY environment variable is not set."
            )

        self.client = anthropic.Anthropic(api_key=api_key)

    def evaluate(self, question, answer_text):

        prompt = self._prompt(question, answer_text)

        response = None
        last_api_error = None

        # Retry temporary Anthropic failures.
        for attempt in range(3):

            try:

                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=MAX_TOKENS,
                    messages=[
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                )

                break

            except (
                anthropic.InternalServerError,
                anthropic.APIConnectionError,
                anthropic.RateLimitError,
            ) as exc:

                last_api_error = exc

                if attempt == 2:

                    raise RuntimeError(
                        "Claude API failed after 3 attempts. "
                        "Wait briefly and run Module 7 again. "
                        f"Last error: {exc}"
                    ) from exc

                time.sleep(2 ** attempt)

        if response is None:

            raise RuntimeError(
                f"Claude API request failed: {last_api_error}"
            )

        # ---------------------------------------------------------
        # Extract text from Claude response
        # ---------------------------------------------------------

        raw_parts = []

        for block in response.content:

            if hasattr(block, "text"):

                raw_parts.append(block.text)

        raw = "".join(raw_parts).strip()

        if not raw:

            raise ValueError(
                "Claude returned an empty evaluation response."
            )

        # ---------------------------------------------------------
        # Parse JSON
        # ---------------------------------------------------------

        try:

            result = extract_json(raw)

        except Exception as exc:

            question_number = "?"

            if isinstance(question, dict):

                question_number = question.get(
                    "question_number",
                    question.get("number", "?")
                )

            # Save the raw response so debugging is easier.
            debug_dir = os.path.join(
                os.getcwd(),
                "output",
                "module_7"
            )

            os.makedirs(debug_dir, exist_ok=True)

            debug_file = os.path.join(
                debug_dir,
                f"failed_response_q{question_number}.txt"
            )

            try:

                with open(
                    debug_file,
                    "w",
                    encoding="utf-8"
                ) as f:

                    f.write(raw)

            except Exception:
                pass

            raise ValueError(
                f"Claude returned invalid JSON for question "
                f"{question_number}.\n\n"
                f"Parser error: {exc}\n\n"
                f"Raw response was saved to:\n"
                f"{debug_file}"
            ) from exc

        # ---------------------------------------------------------
        # Basic result validation
        # ---------------------------------------------------------

        if not isinstance(result, dict):

            raise ValueError(
                "Claude evaluation response must be a JSON object."
            )

        return result

    def _prompt(self, q, answer):

        return f"""
You are an academic answer evaluator.

Evaluate the student's answer ONLY against the supplied
question and marking rubric.

Do NOT invent:
- marking criteria
- marks
- facts
- evidence
- missing concepts

QUESTION SCHEMA:
{q}

STUDENT ANSWER:
{answer}

MARKING RULES:

1. Evaluate every rubric criterion separately.

2. Never award more than the maximum marks for a criterion.

3. Never award more than the total maximum marks for the question.

4. Give credit for correct equivalent wording even when the
   student's wording differs from the rubric.

5. Do not award marks when the required concept is absent
   or clearly incorrect.

6. Award partial marks only when the student's answer
   demonstrates partial fulfillment of the criterion.

7. For rule_type "any_n":
   - identify the valid points provided by the student
   - count only the best N valid points
   - do not double-count repeated ideas
   - do not exceed the criterion maximum

8. Evidence must come directly from the student's answer.

9. Never invent evidence.

10. Missing concepts must describe only requirements that
    were not demonstrated.

11. Be conservative when the student's answer is ambiguous.

12. The awarded_marks value must be numeric.

13. All marks must be greater than or equal to zero.

14. Return ONLY valid JSON.

IMPORTANT JSON REQUIREMENTS:

- Use double quotes around JSON keys and string values.
- Escape internal double quotes.
- Do not put raw newline characters inside JSON strings.
- Do not use markdown.
- Do not write explanations outside the JSON object.
- Do not wrap the JSON in ```json fences.

Return EXACTLY this structure:

{{
  "question_number": "...",
  "max_marks": 0,
  "awarded_marks": 0,
  "criteria": [
    {{
      "criterion_id": "...",
      "criterion_description": "...",
      "max_marks": 0,
      "awarded_marks": 0,
      "status": "full",
      "evidence": "brief evidence from the student's answer",
      "reason": "brief marking justification",
      "missing_concepts": []
    }}
  ],
  "overall_feedback": "brief overall feedback"
}}

Allowed status values:

"full"
"partial"
"not_met"

The JSON MUST be syntactically valid.
"""