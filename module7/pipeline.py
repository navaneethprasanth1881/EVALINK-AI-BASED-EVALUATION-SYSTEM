from .loader import InputLoader
from .answer_normalizer import StudentAnswerNormalizer
from .evaluator import RubricEvaluator
from .rule_engine import MarkingRuleEngine
from .validator import EvaluationValidator
from .output_manager import OutputManager
from .config7 import OUTPUT_DIR

class Module7Pipeline:
    def __init__(self, model=None, output_dir=OUTPUT_DIR):
        self.loader=InputLoader(); self.normalizer=StudentAnswerNormalizer(); self.evaluator=RubricEvaluator(model); self.rules=MarkingRuleEngine(); self.validator=EvaluationValidator(); self.output=OutputManager(output_dir)

    def run(self, question_schema_path, student_answers_path):
        schema=self.loader.load_schema(question_schema_path)
        student=self.normalizer.normalize(self.loader.load_student_answers(student_answers_path))
        evaluations=[]
        for q in schema.get("questions", []):
            number=str(q.get("number"))
            # Only evaluate answered questions. This prevents treating omitted OR choices as blank answers.
            if number not in student:
                continue
            result=self.evaluator.evaluate(q, student[number]["answer_text"])
            result["student_answer_metadata"] = {k: v for k, v in student[number].items() if k != "answer_text"}
            result=self.rules.clamp(result, q)
            evaluations.append(result)
        total_awarded=sum(float(x.get("awarded_marks",0)) for x in evaluations)
        # Selection groups: count only the best answered question in each group when max_counted_marks is supplied.
        group_lookup={str(q.get("number")):q.get("selection_group_id") for q in schema.get("questions",[])}
        groups={str(g.get("id")):g for g in schema.get("selection_groups",[])}
        counted=set(x["question_number"] for x in evaluations)
        group_adjustments=[]
        for gid,g in groups.items():
            members=[x for x in evaluations if x["question_number"] in [str(n) for n in g.get("questions",[])]]
            if len(members)>1:
                best=max(members,key=lambda x:float(x.get("awarded_marks",0)))
                for m in members:
                    if m is not best: counted.discard(m["question_number"])
                group_adjustments.append({"group_id":gid,"counted_question":best["question_number"],"ignored_questions":[m["question_number"] for m in members if m is not best]})
        counted_total=sum(float(x.get("awarded_marks",0)) for x in evaluations if x["question_number"] in counted)
        result={"evaluations":evaluations,"summary":{"questions_evaluated":len(evaluations),"total_awarded_marks":counted_total,"selection_adjustments":group_adjustments}}
        validation=self.validator.validate(result); result["validation"]=validation
        self.output.write("evaluation_results.json",result); self.output.write("validation_report.json",validation)
        return result
