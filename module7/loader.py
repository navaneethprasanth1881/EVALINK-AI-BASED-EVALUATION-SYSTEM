from pathlib import Path
import json

class InputLoader:
    def load_json(self, path):
        p = Path(path)
        with p.open("r", encoding="utf-8") as f:
            return json.load(f)

    def load_schema(self, path):
        data = self.load_json(path)
        # Accept either the complete normalized schema or an object containing it.
        if "questions" not in data:
            if "question_schema" in data:
                data = data["question_schema"]
        return data

    def load_student_answers(self, path):
        data = self.load_json(path)
        return data
