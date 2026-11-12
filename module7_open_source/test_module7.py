import argparse
from .pipeline import Module7Pipeline

def main():
    p = argparse.ArgumentParser(description="Module 7 - Open Source LLM Answer Evaluation")
    p.add_argument("--question-schema", required=True)
    p.add_argument("--student-answers", required=True)
    p.add_argument("--model", default=None)
    a = p.parse_args()

    result = Module7Pipeline(model=a.model).run(
        a.question_schema,
        a.student_answers
    )

    print("\nMODULE 7 - OPEN SOURCE LLM EVALUATION")
    print("Model:", result["model"])
    print("Questions evaluated:", result["questions_evaluated"])
    print("Generated:", result["output"])

if __name__ == "__main__":
    main()
