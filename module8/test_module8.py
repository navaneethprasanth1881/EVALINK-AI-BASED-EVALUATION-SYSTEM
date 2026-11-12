import argparse
from .pipeline import Module8Pipeline

def main():
    p = argparse.ArgumentParser(description="Module 8 - Explainability & Evaluation Report")
    p.add_argument("--evaluation", required=True, help="Module 7 evaluation_results.json")
    p.add_argument("--model", default=None)
    a = p.parse_args()

    result = Module8Pipeline(model=a.model).run(a.evaluation)

    print("\nMODULE 8 - EXPLAINABILITY & REPORT")
    print("Questions processed:", result["questions"])
    print("Generated:")
    print(result["explainability_json"])
    print(result["html_report"])

if __name__ == "__main__":
    main()
