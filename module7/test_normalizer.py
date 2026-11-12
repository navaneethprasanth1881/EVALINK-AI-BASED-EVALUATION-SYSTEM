from .answer_normalizer import StudentAnswerNormalizer


def test_project_ocr_format():
    data = {
        "pages": [
            {"page_number": 2, "page_type": "ANSWER", "answers": [
                {"answer_number": "1", "answer_text": "Part one", "source_page": 2}
            ]},
            {"page_number": 3, "page_type": "ANSWER", "answers": [
                {"answer_number": "1", "answer_text": "Part two", "source_page": 3},
                {"answer_number": "2", "answer_text": "Answer two", "source_page": 3}
            ]}
        ]
    }
    result = StudentAnswerNormalizer().normalize(data)
    assert result["1"]["answer_text"] == "Part one\n\nPart two"
    assert result["1"]["source_pages"] == [2, 3]
    assert result["2"]["answer_text"] == "Answer two"


if __name__ == "__main__":
    test_project_ocr_format()
    print("Normalizer test: PASS")
