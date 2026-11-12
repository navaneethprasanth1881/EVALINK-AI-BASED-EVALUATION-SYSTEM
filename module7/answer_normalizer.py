from collections import OrderedDict


class StudentAnswerNormalizer:
    """Normalize the project's Module 4/5 OCR JSON and common variants.

    The project's OCR format stores answers inside pages[].answers[]. The same
    answer_number can appear on multiple pages when an answer continues.
    Those chunks are merged in page order before evaluation.
    """

    def normalize(self, data):
        # Project format: {document, student, pages: [{answers: [...]}, ...]}
        if isinstance(data, dict) and isinstance(data.get("pages"), list):
            return self._from_pages(data["pages"])

        # Common formats retained for compatibility.
        if isinstance(data, dict) and isinstance(data.get("answers"), dict):
            return OrderedDict(
                (str(k), self._normalize_item(v, str(k)))
                for k, v in data["answers"].items()
            )

        if isinstance(data, dict) and isinstance(data.get("answers"), list):
            return self._from_answer_list(data["answers"])

        if isinstance(data, dict) and isinstance(data.get("student_answers"), list):
            return self._from_answer_list(data["student_answers"])

        if isinstance(data, list):
            return self._from_answer_list(data)

        raise ValueError(
            "Unsupported student OCR JSON format. Expected the project's "
            "pages[].answers[] structure or a supported answers list/mapping."
        )

    def _from_pages(self, pages):
        grouped = OrderedDict()

        for page in sorted(
            (p for p in pages if isinstance(p, dict)),
            key=lambda p: self._page_number(p.get("page_number")),
        ):
            if str(page.get("page_type", "")).upper() == "COVER":
                continue

            answers = page.get("answers", [])
            if not isinstance(answers, list):
                continue

            page_number = page.get("page_number")
            for item in answers:
                if not isinstance(item, dict):
                    continue
                number = self._get_number(item)
                if number is None:
                    continue
                number = str(number).strip()
                text = self._text(item).strip()
                if not text:
                    continue

                if number not in grouped:
                    grouped[number] = {
                        "question_number": number,
                        "answer_text": text,
                        "source_pages": [page_number] if page_number is not None else [],
                        "ocr_confidence": self._confidence(item),
                        "continuation_chunks": 0,
                    }
                else:
                    # Same answer number on a later page = continuation.
                    grouped[number]["answer_text"] += "\n\n" + text
                    if page_number is not None and page_number not in grouped[number]["source_pages"]:
                        grouped[number]["source_pages"].append(page_number)
                    grouped[number]["ocr_confidence"] = self._merge_confidence(
                        grouped[number]["ocr_confidence"], self._confidence(item)
                    )
                    grouped[number]["continuation_chunks"] += 1

        return grouped

    def _from_answer_list(self, items):
        grouped = OrderedDict()
        for item in items:
            if not isinstance(item, dict):
                continue
            number = self._get_number(item)
            if number is None:
                continue
            number = str(number).strip()
            text = self._text(item).strip()
            if number not in grouped:
                grouped[number] = self._normalize_item(item, number)
            elif text:
                grouped[number]["answer_text"] += "\n\n" + text
                grouped[number]["continuation_chunks"] += 1
        return grouped

    def _normalize_item(self, item, number):
        text = self._text(item).strip()
        return {
            "question_number": number,
            "answer_text": text,
            "source_pages": self._pages(item),
            "ocr_confidence": self._confidence(item),
            "continuation_chunks": 0,
        }

    @staticmethod
    def _get_number(item):
        for key in ("answer_number", "question_number", "number", "question_no", "id"):
            value = item.get(key)
            if value is not None and str(value).strip() != "":
                return value
        return None

    def _text(self, item):
        if isinstance(item, str):
            return item
        if not isinstance(item, dict):
            return str(item)

        for key in ("answer_text", "text", "answer", "content", "transcription"):
            value = item.get(key)
            if isinstance(value, str) and value.strip():
                return value

        # Fallback: reconstruct from OCR elements.
        elements = item.get("elements")
        if isinstance(elements, list):
            parts = []
            for element in elements:
                if isinstance(element, dict):
                    content = element.get("content") or element.get("text")
                    if content:
                        parts.append(str(content))
                elif element:
                    parts.append(str(element))
            if parts:
                return "\n\n".join(parts)

        parts = []
        for key in ("sub_questions", "sections", "paragraphs"):
            value = item.get(key)
            if isinstance(value, list):
                parts.extend(self._text(x) for x in value)
        return "\n".join(p for p in parts if p)

    @staticmethod
    def _page_number(value):
        try:
            return int(value)
        except (TypeError, ValueError):
            return 10**9

    @staticmethod
    def _pages(item):
        page = item.get("source_page")
        if page is None:
            return []
        return [page]

    def _confidence(self, item):
        values = []
        if isinstance(item.get("confidence"), (int, float)):
            values.append(float(item["confidence"]))
        for element in item.get("elements", []) if isinstance(item.get("elements"), list) else []:
            if isinstance(element, dict) and isinstance(element.get("confidence"), (int, float)):
                values.append(float(element["confidence"]))
        return round(sum(values) / len(values), 4) if values else None

    @staticmethod
    def _merge_confidence(a, b):
        vals = [x for x in (a, b) if isinstance(x, (int, float))]
        return round(sum(vals) / len(vals), 4) if vals else None
