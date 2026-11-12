import argparse
from .pipeline import Module7Pipeline

def main():
    p=argparse.ArgumentParser(description="Module 7 - Rubric-grounded answer evaluation")
    p.add_argument("--question-schema",required=True)
    p.add_argument("--student-answers",required=True)
    p.add_argument("--model",default=None)
    a=p.parse_args()
    result=Module7Pipeline(model=a.model).run(a.question_schema,a.student_answers)
    print("\nMODULE 7 - RUBRIC-GROUNDED ANSWER EVALUATION")
    print("Questions evaluated:", result["summary"]["questions_evaluated"])
    print("Total awarded      :", result["summary"]["total_awarded_marks"])
    print("Validation         :", "PASS" if result["validation"]["valid"] else "FAIL")
    for e in result["validation"]["errors"]: print("  -",e)

if __name__=="__main__": main()
