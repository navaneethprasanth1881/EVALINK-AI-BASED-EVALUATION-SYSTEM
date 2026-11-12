# Module 8 - Explainability & Evaluation Report

Consumes Module 7 evaluation_results.json and produces:
- explainability_results.json
- evaluation_report.html

The module is dynamic and does not hardcode subjects, questions, or marks.

## Install
pip install -r requirements.txt

## Environment
PowerShell:
$env:ANTHROPIC_API_KEY="YOUR_API_KEY"
$env:MODULE8_MODEL="claude-sonnet-4-6"

## Run
From project root:
python -m module8.test_module8 --evaluation "output\module_7\evaluation_results.json"

## Pipeline
Module 7 -> Module 8 -> explainability JSON + HTML report

PDF generation can be added after the evaluation JSON/report structure is confirmed.
