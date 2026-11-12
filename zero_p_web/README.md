# Zero-P Connected Web Platform

This web layer is connected to the uploaded project's Python Modules 1-8.

## Workflow
Admin login -> upload question paper/rubric/answer scripts -> assign an answer script to a teacher -> teacher login -> evaluate -> Modules 1-8 -> database -> teacher review.

## Actual module integration
The backend `processing_service.py` calls:
1. module1 QualityAnalyzer
2. modul2 Preprocessor
3. module3 DocumentAnalyzer
4. module4 OCRProcessor (Claude)
5. module5 JSONValidator
6. module6 dynamic question/rubric schema
7. module7 open-source Qwen/Llama by default; GPT can be selected with WEB_EVALUATION_MODEL
8. module8_option1 API-free explainability/report

The backend then stores one `Evaluation` and question-level `Score` rows, including answer text, awarded mark, evidence, and why the mark was awarded.

## Run
From the `restart` project root:

```powershell
cd zero_p_web/backend
pip install -r requirements.txt
uvicorn main:app --reload
```

In another terminal:
```powershell
cd zero_p_web/frontend
npm install
npm run dev
```

## Demo accounts
Admin: admin@zerop.local / Admin@123
Teacher: teacher@zerop.local / Teacher@123

Change these before real use.

## Important
The existing Modules 1-6 use shared `output/module_*` folders. The connected backend therefore processes one evaluation job at a time. For production, move each job to its own workspace and use a background queue (Celery/RQ/Redis or a managed job system).

Module 4 requires `ANTHROPIC_API_KEY` and uses the project's `CLAUDE_MODEL` environment variable. Module 7 Qwen/Llama requires Ollama running locally. GPT requires `OPENAI_API_KEY` and `WEB_EVALUATION_MODEL` set to the desired GPT model.


## Evaluation model selection

Before a teacher starts evaluation, the website asks them to choose:
- GPT
- Claude
- Llama

Default backend model names:
- GPT: `gpt-5.6-luna`
- Claude: `claude-sonnet-4-6`
- Llama: `llama3.1:8b`

You can change them with environment variables:
```text
WEB_GPT_MODEL
WEB_CLAUDE_MODEL
WEB_LLAMA_MODEL
```

Required services:
- GPT -> `OPENAI_API_KEY`
- Claude -> `ANTHROPIC_API_KEY`
- Llama -> local Ollama with the selected model pulled

The selected model is passed into Module 7 and the resulting model name is stored in the `evaluations.model_name` database field.
