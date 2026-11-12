# Module 7 - Open Source LLM Evaluation

This version uses local open-source models through Ollama.
It does NOT use Claude, OpenAI, Gemini, or another paid API.

Recommended models:
- Qwen2.5 14B Instruct: qwen2.5:14b
- Llama 3.1 8B Instruct: llama3.1:8b

## 1. Install Ollama
Install Ollama on your computer from the official Ollama website.

## 2. Pull models
ollama pull qwen2.5:14b
ollama pull llama3.1:8b

## 3. Check Ollama
ollama list

## 4. Install Python dependency
pip install -r module7/requirements.txt

## 5. Run Qwen
python -m module7.test_module7 --model qwen2.5:14b --question-schema "output\module_6\question_schema.json" --student-answers "sample_student_ocr.json"

## 6. Run Llama
python -m module7.test_module7 --model llama3.1:8b --question-schema "output\module_6\question_schema.json" --student-answers "sample_student_ocr.json"

The two runs produce separate evaluation_results files so you can compare the models.

## Architecture
Student OCR -> Module 5 -> Module 6 rubric -> Module 7 (Qwen/Llama) -> evaluation results

Important:
Use the same question schema and same student OCR JSON for both models.
Do not change the prompt/rubric between model runs.
