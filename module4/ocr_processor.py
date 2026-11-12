from pdf_converter import PDFConverter
from claude_client import ClaudeClient
from response_parser import OCRResponseParser

class OCRProcessor:
    def __init__(self):
        self.converter = PDFConverter()
        self.client = ClaudeClient()
        self.parser = OCRResponseParser()

    def process(self, document):
        prepared_pages = self.converter.prepare_document(document)
        
        page_results = []
        previous_answer_number = None
        
        for prepared_page in prepared_pages:
            page_number = prepared_page["page_number"]
            page_type = prepared_page["page_type"]
            image_data = prepared_page["image_data"]
            media_type = prepared_page["media_type"]
            is_cover = prepared_page["is_cover"]
            
            print(f"\nOCR processing page {page_number}...")
            
            if is_cover:
                result = self.client.ocr_cover_page(image_data, media_type)
                parsed = self.parser.parse_response(result["text"], page_number, is_cover=True)
                document.student_details = parsed["student"]
                page_result = {
                    "page_number": page_number,
                    "page_type": page_type,
                    "student": parsed["student"]
                }
            else:
                result = self.client.ocr_answer_page(
                    image_data, media_type, page_number, previous_answer_number
                )
                parsed = self.parser.parse_response(result["text"], page_number, is_cover=False)
                page_result = {
                    "page_number": page_number,
                    "page_type": page_type,
                    "answers": parsed["answers"]
                }
                
                if parsed.get("answers"):
                    last_answer = parsed["answers"][-1]
                    previous_answer_number = last_answer["answer_number"]
                    
            page_results.append(page_result)
            
            for page in document.pages:
                if page.page_number == page_number:
                    page.ocr_result = page_result
                    if not is_cover:
                        page.answers = parsed.get("answers", [])
                    break
                    
        self._detect_continuations(page_results)
        
        document.ocr_json = {
            "student": getattr(document, 'student_details', {}),
            "pages": page_results
        }
        return document

    def _detect_continuations(self, page_results):
        for i in range(len(page_results) - 1):
            current_page = page_results[i]
            next_page = page_results[i+1]
            
            if "answers" not in current_page:
                continue
            if "answers" not in next_page:
                continue
            if not current_page["answers"]:
                continue
            if not next_page["answers"]:
                continue
                
            current_last_answer = current_page["answers"][-1]
            next_first_answer = next_page["answers"][0]
            
            if current_last_answer["answer_number"] == next_first_answer["answer_number"]:
                current_last_answer["continues_to_next_page"] = True

    def get_combined_answers(self, document):
        combined = {}
        for page in document.ocr_json.get("pages", []):
            if "answers" not in page:
                continue
                
            for answer in page["answers"]:
                number = str(answer["answer_number"])
                
                if number not in combined:
                    combined[number] = {
                        "answer_number": number,
                        "answer_text": "",
                        "elements": [],
                        "source_pages": []
                    }
                    
                if answer.get("answer_text"):
                    if combined[number]["answer_text"]:
                        combined[number]["answer_text"] += "\n\n"
                    combined[number]["answer_text"] += answer["answer_text"]
                    
                combined[number]["elements"].extend(answer.get("elements", []))
                
                source_page = answer["source_page"]
                if source_page not in combined[number]["source_pages"]:
                    combined[number]["source_pages"].append(source_page)
                    
        return list(combined.values())