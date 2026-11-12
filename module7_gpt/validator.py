class EvaluationValidator:
    def validate(self,result,question):
        if not isinstance(result,dict): raise ValueError("Evaluation result must be an object.")
        mx=float(question.get("max_marks",result.get("max_marks",0)) or 0)
        score=float(result.get("awarded_marks",result.get("score",0)) or 0)
        result["max_marks"]=mx
        result["awarded_marks"]=max(0.0,min(score,mx))
        for c in result.get("criteria",[]) or []:
            cm=float(c.get("max_marks",0) or 0); cs=float(c.get("awarded_marks",0) or 0)
            c["max_marks"]=cm; c["awarded_marks"]=max(0.0,min(cs,cm))
        return result
