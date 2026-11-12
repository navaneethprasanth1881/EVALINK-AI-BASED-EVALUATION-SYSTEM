import os
import time
import base64
import anthropic

class ClaudeClient:
    def __init__(self):
        self.api_key = os.getenv("ANTHROPIC_API_KEY")
        if not self.api_key:
            raise RuntimeError(
                "ANTHROPIC_API_KEY is not set.\n\n"
                "PowerShell:\n"
                "$env:ANTHROPIC_API_KEY=\"your_api_key_here\""
            )
            
        # FIXED: Reverted to the correct 2026 model string
        self.model = os.getenv("CLAUDE_MODEL", "claude-sonnet-4-6")
        self.max_tokens = int(os.getenv("CLAUDE_MAX_TOKENS", "8192"))
        self.max_retries = 3
        
        self.client = anthropic.Anthropic(api_key=self.api_key)
        print("\nClaude client initialized.")
        print(f"Claude model: {self.model}")

    def prepare_image(self, image_data):
        if isinstance(image_data, bytes):
            return base64.b64encode(image_data).decode("utf-8")
        if isinstance(image_data, bytearray):
            return base64.b64encode(bytes(image_data)).decode("utf-8")
        if isinstance(image_data, str):
            return image_data
        raise TypeError(f"Unsupported image_data type: {type(image_data)}")

    def send_with_retry(self, image_data, media_type, prompt):
        image_base64 = self.prepare_image(image_data)
        last_error = None
        
        for attempt in range(1, self.max_retries + 1):
            print(f"Claude API attempt {attempt}/{self.max_retries}...")
            try:
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=self.max_tokens,
                    messages=[{
                        "role": "user",
                        "content": [
                            {
                                "type": "image",
                                "source": {
                                    "type": "base64",
                                    "media_type": media_type,
                                    "data": image_base64
                                }
                            },
                            {
                                "type": "text",
                                "text": prompt
                            }
                        ]
                    }]
                )
                
                text_parts = []
                for block in response.content:
                    if hasattr(block, "text"):
                        text_parts.append(block.text)
                
                text = "\n".join(text_parts).strip()
                if not text:
                    raise RuntimeError("Claude returned an empty response.")
                
                print("Claude API request successful.")
                return {"text": text, "model": self.model}
                
            except anthropic.APIError as e:
                last_error = e
                status_code = getattr(e, "status_code", None)
                print(f"\nClaude API error:\nType: {type(e).__name__}\nStatus code: {status_code}\nMessage: {e}\n")
                
                if status_code in [400, 401, 403, 404]:
                    raise RuntimeError(f"Claude API request failed.\nHTTP status: {status_code}\nError: {e}") from e
                
                if attempt < self.max_retries:
                    wait_time = 2 ** (attempt - 1)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    
            except Exception as e:
                last_error = e
                print(f"\nUnexpected error on attempt {attempt}:\nType: {type(e).__name__}\nMessage: {e}\n")
                if attempt < self.max_retries:
                    wait_time = 2 ** (attempt - 1)
                    print(f"Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
                    
        raise RuntimeError(f"Claude OCR failed after {self.max_retries} attempts.\n\nLast error:\n{type(last_error).__name__}: {last_error}") from last_error

    def ocr_cover_page(self, image_data, media_type):
        prompt = """You are performing OCR on a handwritten examination answer-sheet cover page.
Extract the student information exactly as written.
Return ONLY valid JSON.
Use exactly this structure:
{
    "student": {
        "student_name": "",
        "register_number": "",
        "roll_number": "",
        "subject": "",
        "course": "",
        "semester": "",
        "examination": "",
        "date": "",
        "department": ""
    }
}
Rules:
1. Preserve the student's original spelling.
2. Do not correct spelling.
3. Do not invent information.
4. If a field cannot be read, use an empty string.
5. Do not add explanations.
6. Do not use Markdown.
7. Do not wrap JSON in ```json.
8. Return ONLY the JSON object."""
        return self.send_with_retry(image_data, media_type, prompt)

    def ocr_answer_page(self, image_data, media_type, page_number, previous_answer_number=None):
        if previous_answer_number is None:
            previous_context = """There is no previous answer page available.
Determine the top-level answer number directly from the current page."""
        else:
            previous_context = f"""The previous page ended while processing top-level answer {previous_answer_number}.
This page may continue answer {previous_answer_number}.
IMPORTANT: Do NOT assume that every number written on the page is a new examination answer.
Only create a NEW answer when the handwriting clearly shows a new TOP-LEVEL examination question."""

        prompt = f"""You are performing OCR and visual-content extraction on a handwritten examination answer sheet.
Current page: {page_number}
{previous_context}

Your task is to:
1. Identify TOP-LEVEL examination answers.
2. Transcribe handwritten text.
3. Detect equations, figures, graphs, and tables.

Return ONLY valid JSON. Use exactly this structure:
{{
    "answers": [
        {{
            "answer_number": "",
            "answer_text": "",
            "elements": [
                {{"type": "text", "content": "", "confidence": 1.0}}
            ],
            "continues_to_next_page": false
        }}
    ]
}}

OCR RULES:
1. Preserve the student's exact wording, spelling mistakes, and order.
2. Return JSON only. Do not use Markdown. Do not wrap JSON in ```json."""
        return self.send_with_retry(image_data, media_type, prompt)