from pathlib import Path
import json
from jinja2 import Template

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
<meta charset="utf-8">
<title>Answer Evaluation Report</title>
<style>
body { font-family: Arial, sans-serif; margin: 40px; line-height: 1.5; }
.card { border: 1px solid #ddd; border-radius: 8px; padding: 18px; margin: 16px 0; }
.score { font-size: 22px; font-weight: bold; }
.criterion { margin: 12px 0; padding: 12px; background: #f7f7f7; }
</style>
</head>
<body>
<h1>Answer Evaluation Report</h1>
{% if student %}<p><b>Student:</b> {{ student.get("student_name","") }}</p>{% endif %}
<p class="score">Total: {{ total }} / {{ maximum }}</p>

{% for item in items %}
<div class="card">
<h2>Question {{ item.question_number }}</h2>
<p class="score">{{ item.score }} / {{ item.max_marks }}</p>

{% for c in item.criterion_explanations %}
<div class="criterion">
<b>{{ c.criterion_id }}</b> — {{ c.status }}<br>
Marks: {{ c.awarded_marks }} / {{ c.max_marks }}<br>
<b>Evidence:</b> {{ c.evidence }}<br>
<b>Explanation:</b> {{ c.explanation }}<br>
{% if c.missing_concepts %}<b>Missing:</b> {{ c.missing_concepts | join(", ") }}{% endif %}
</div>
{% endfor %}

{% if item.strengths %}<p><b>Strengths:</b> {{ item.strengths | join(", ") }}</p>{% endif %}
{% if item.areas_for_improvement %}<p><b>Improve:</b> {{ item.areas_for_improvement | join(", ") }}</p>{% endif %}
<p><b>Overall feedback:</b> {{ item.overall_feedback }}</p>
</div>
{% endfor %}
</body>
</html>
"""

class ReportGenerator:
    def generate_html(self, evaluations, output_path, student=None):
        total = sum(float(x.get("score", x.get("awarded_marks", 0))) for x in evaluations)
        maximum = sum(float(x.get("max_marks", 0)) for x in evaluations)
        html = Template(HTML_TEMPLATE).render(
            items=evaluations, total=total, maximum=maximum, student=student or {}
        )
        Path(output_path).parent.mkdir(parents=True, exist_ok=True)
        Path(output_path).write_text(html, encoding="utf-8")
        return output_path
