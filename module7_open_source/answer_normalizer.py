class AnswerNormalizer:
    """Normalizes the actual Module 4/5 OCR format used by this project."""

    def normalize(self, data):
        pages = data.get("pages", []) if isinstance(data, dict) else []
        grouped = {}

        for page in pages:
            if page.get("page_type") != "ANSWER":
                continue

            for answer in page.get("answers", []) or []:
                number = str(answer.get("answer_number", "")).strip()
                if not number:
                    continue

                text = answer.get("answer_text", "") or ""
                entry = grouped.setdefault(number, {
                    "question_number": number,
                    "answer_text": "",
                    "source_pages": [],
                    "ocr_confidence": []
                })

                if entry["answer_text"]:
                    entry["answer_text"] += "\n\n"
                entry["answer_text"] += text

                page_number = answer.get("source_page", page.get("page_number"))
                if page_number is not None and page_number not in entry["source_pages"]:
                    entry["source_pages"].append(page_number)

                for element in answer.get("elements", []) or []:
                    confidence = element.get("confidence")
                    if isinstance(confidence, (int, float)):
                        entry["ocr_confidence"].append(confidence)

        for entry in grouped.values():
            values = entry["ocr_confidence"]
            entry["ocr_confidence"] = round(sum(values) / len(values), 4) if values else None

        return grouped
