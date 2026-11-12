import json

class OCRResponseParser:
    def parse_json(self, text):
        if not text:
            raise ValueError("Claude returned an empty response.")
        
        text = str(text).strip()
        
        # Attempt 1: Direct JSON
        try:
            data = json.loads(text)
            if not isinstance(data, dict):
                raise ValueError("Claude response must be a JSON object.")
            return data
        except json.JSONDecodeError:
            pass
            
        # Attempt 2: Markdown fence extraction
        cleaned = text
        if cleaned.startswith("```json"):
            cleaned = cleaned[len("```json"):].strip()
        elif cleaned.startswith("```"):
            cleaned = cleaned[len("```"):].strip()
            
        if cleaned.endswith("```"):
            cleaned = cleaned[:-3].strip()
            
        try:
            data = json.loads(cleaned)
            if not isinstance(data, dict):
                raise ValueError("Claude response must be a JSON object.")
            return data
        except json.JSONDecodeError:
            pass
            
        # Attempt 3: Extract JSON object using braces
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1:
            json_text = cleaned[start:end + 1]
            try:
                data = json.loads(json_text)
                if not isinstance(data, dict):
                    raise ValueError("Claude response must be a JSON object.")
                return data
            except json.JSONDecodeError:
                pass

        print("\n" + "=" * 60)
        print("INVALID CLAUDE JSON RESPONSE")
        print("=" * 60 + "\n")
        print(text)
        print("\n" + "=" * 60)
        raise ValueError("Claude response is not valid JSON.")

    def parse_element(self, element, page_number):
        if not isinstance(element, dict):
            raise ValueError(f"Page {page_number}: Invalid element object.")
            
        element_type = element.get("type")
        allowed_types = ["text", "equation", "figure", "graph", "table"]
        
        if element_type not in allowed_types:
            raise ValueError(f"Page {page_number}: Unknown element type: {element_type}")

        try:
            confidence = float(element.get("confidence", 1.0))
        except (TypeError, ValueError):
            confidence = 1.0
        confidence = max(0.0, min(1.0, confidence))

        if element_type == "text":
            content = element.get("content", "")
            if not isinstance(content, str):
                content = str(content)
            return {"type": "text", "content": content, "confidence": confidence}

        if element_type == "equation":
            content = element.get("content", "")
            if not isinstance(content, str):
                content = str(content)
            return {"type": "equation", "content": content, "confidence": confidence}

        if element_type == "figure":
            description = str(element.get("description", ""))
            labels = element.get("labels", [])
            relationships = element.get("relationships", [])
            if not isinstance(labels, list):
                labels = [str(labels)]
            if not isinstance(relationships, list):
                relationships = [str(relationships)]
            return {
                "type": "figure",
                "description": description,
                "labels": labels,
                "relationships": relationships,
                "confidence": confidence
            }

        if element_type == "graph":
            description = str(element.get("description", ""))
            axis_labels = element.get("axis_labels", [])
            visible_values = element.get("visible_values", [])
            if not isinstance(axis_labels, list):
                axis_labels = [str(axis_labels)]
            if not isinstance(visible_values, list):
                visible_values = [str(visible_values)]
            return {
                "type": "graph",
                "description": description,
                "axis_labels": axis_labels,
                "visible_values": visible_values,
                "confidence": confidence
            }

        if element_type == "table":
            content = element.get("content", [])
            if not isinstance(content, list):
                content = [content]
            return {"type": "table", "content": content, "confidence": confidence}

        return element

    def parse_answer_response(self, text, page_number):
        data = self.parse_json(text)
        
        if "answers" not in data:
            raise ValueError(f"Page {page_number}: 'answers' field is missing.")
        if not isinstance(data["answers"], list):
            raise ValueError(f"Page {page_number}: 'answers' must be a list.")
            
        parsed_answers = []
        for answer in data["answers"]:
            if not isinstance(answer, dict):
                raise ValueError(f"Page {page_number}: Invalid answer object.")
                
            if "answer_number" not in answer:
                raise ValueError(f"Page {page_number}: 'answer_number' is missing.")
                
            answer_number = answer["answer_number"]
            answer_text = answer.get("answer_text", "")
            if not isinstance(answer_text, str):
                answer_text = str(answer_text)
                
            raw_elements = answer.get("elements", [])
            if not isinstance(raw_elements, list):
                raise ValueError(f"Page {page_number}: 'elements' must be a list.")
                
            parsed_elements = []
            for element in raw_elements:
                parsed_elements.append(self.parse_element(element, page_number))
                
            continues = answer.get("continues_to_next_page", False)
            if not isinstance(continues, bool):
                if isinstance(continues, str):
                    continues = continues.lower() in ("true", "yes", "1")
                else:
                    continues = False
                    
            parsed_answers.append({
                "answer_number": answer_number,
                "answer_text": answer_text,
                "elements": parsed_elements,
                "continues_to_next_page": continues,
                "source_page": page_number
            })
            
        return {"page_number": page_number, "answers": parsed_answers}

    def parse_cover_response(self, text):
        data = self.parse_json(text)
        
        if "student" not in data:
            raise ValueError("'student' field is missing.")
        if not isinstance(data["student"], dict):
            raise ValueError("'student' must be an object.")
            
        raw_student = data["student"]
        
        def get_field(primary, alternatives=None):
            if primary in raw_student:
                return raw_student.get(primary)
            if alternatives:
                for name in alternatives:
                    if name in raw_student:
                        return raw_student.get(name)
            return None

        student = {
            "student_name": get_field("student_name", ["name"]),
            "register_number": get_field("register_number", ["registration_number", "reg_number"]),
            "roll_number": get_field("roll_number", ["roll_no"]),
            "subject": get_field("subject", ["subject_name"]),
            "course": get_field("course", ["course_name", "program", "degree"]),
            "semester": get_field("semester", ["sem"]),
            "examination": get_field("examination", ["exam", "exam_name"]),
            "date": get_field("date", ["exam_date"]),
            "department": get_field("department", ["branch"])
        }
        return {"student": student}

    def parse_response(self, text, page_number, is_cover=False):
        if is_cover:
            return self.parse_cover_response(text)
        return self.parse_answer_response(text, page_number)