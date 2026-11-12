# Module 8 - API-Free Explainability & Evaluation Report

This version does NOT call Claude or any external API.

It consumes the evaluation results produced by Module 7 and
presents the existing:
- awarded marks
- rubric criteria
- evidence
- reasons
- missing concepts
- strengths
- areas for improvement
- overall feedback

Outputs:
- output/module_8/explainability_results.json
- output/module_8/evaluation_report.html

Run from the project root:

python -m module8.test_module8 --evaluation "output\module_7\evaluation_results.json"

No API key is required for Module 8.
