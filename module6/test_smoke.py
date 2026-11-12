from module6.question_extractor import QuestionExtractor
from module6.schema_extractor import SchemaExtractor


def main():
    paper = """Part A\n1. Define a term. (3 Marks)\n2. Explain a process. (3 Marks)\n9. Discuss the topic. (9 Marks)\n(a) First part. (5 Marks)\n(b) Second part. (4 Marks)"""
    scheme = """1\nDefinition 1 mark\nPurpose 2 marks\n9 (a)\nCore explanation 3 marks\nAny two valid points 2 marks\n9 (b)\nCorrect method 4 marks"""
    qs = QuestionExtractor().extract(paper)
    ss = SchemaExtractor().extract(scheme)
    assert len(qs) == 3, qs
    assert "1" in ss["questions"]
    print("Module 6 smoke test: PASS")


if __name__ == "__main__":
    main()
