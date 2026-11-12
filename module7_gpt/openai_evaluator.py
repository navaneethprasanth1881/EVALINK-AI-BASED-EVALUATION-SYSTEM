import json,os
from openai import OpenAI
from .config7 import MODEL,MAX_OUTPUT_TOKENS
class OpenAIEvaluator:
    def __init__(self,model=None):
        self.model=model or MODEL
        key=os.getenv("OPENAI_API_KEY")
        if not key: raise RuntimeError("OPENAI_API_KEY environment variable is not set.")
        self.client=OpenAI(api_key=key)
    def evaluate(self,question,answer_text):
        prompt=f"""You are an academic examination answer evaluator.
Evaluate the student's answer ONLY against the supplied question schema and marking criteria.
QUESTION SCHEMA:
{json.dumps(question,ensure_ascii=False,indent=2)}
STUDENT ANSWER:
{answer_text}
Rules:
- Evaluate every criterion separately.
- Never exceed criterion or question maximum marks.
- Award partial marks when partially correct.
- Accept equivalent wording for correct concepts.
- For any_n rules, count only the best N distinct valid points.
- Evidence must come directly from the student answer.
- Never invent evidence, criteria, or facts.
- Missing concepts must only describe requirements not demonstrated.
Return ONLY valid JSON:
{{"question_number":"...","max_marks":0,"awarded_marks":0,"criteria":[{{"criterion_id":"...","criterion_description":"...","max_marks":0,"awarded_marks":0,"status":"full","evidence":"...","reason":"...","missing_concepts":[]}}],"overall_feedback":"..."}}
Allowed status: full, partial, not_met."""
        response=self.client.responses.create(
            model=self.model,
            instructions="You are a strict rubric-based examination evaluator. Return only valid JSON.",
            input=prompt,
            max_output_tokens=MAX_OUTPUT_TOKENS
        )
        raw=response.output_text.strip()
        try: return json.loads(raw)
        except json.JSONDecodeError:
            from .json_utils import extract_json
            return extract_json(raw)
