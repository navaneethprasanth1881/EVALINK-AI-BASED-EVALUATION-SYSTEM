import argparse
from .pipeline import Module7Pipeline
def main():
    p=argparse.ArgumentParser()
    p.add_argument("--question-schema",required=True); p.add_argument("--student-answers",required=True); p.add_argument("--model",default=None)
    a=p.parse_args()
    r=Module7Pipeline(a.model).run(a.question_schema,a.student_answers)
    print("\nMODULE 7 - GPT EVALUATION")
    print("Model:",r["model"]); print("Questions evaluated:",r["questions_evaluated"]); print("Generated:",r["output"])
if __name__=="__main__": main()
