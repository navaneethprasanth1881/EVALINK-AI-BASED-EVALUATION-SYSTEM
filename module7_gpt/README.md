# Module 7 - GPT Evaluation
Uses the OpenAI Responses API for the evaluation model.
Default model: gpt-5.6-luna.
Set OPENAI_API_KEY and run:
python -m module7.test_module7 --model gpt-5.6-luna --question-schema "output\\module_6\\question_schema.json" --student-answers "sample_student_ocr.json"
Use the same schema and student OCR as Qwen/Llama for a fair comparison.
