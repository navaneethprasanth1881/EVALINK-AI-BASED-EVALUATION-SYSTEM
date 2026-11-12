from pathlib import Path
import json
from html import escape

class ReportGenerator:
    def _num(self, value):
        try:
            return float(value)
        except (TypeError, ValueError):
            return 0.0

    def generate(self, data, output_dir):
        out = Path(output_dir)
        out.mkdir(parents=True, exist_ok=True)

        evaluations = data.get("evaluations") if isinstance(data, dict) else data
        if evaluations is None:
            evaluations = data.get("results", data.get("questions", [])) if isinstance(data, dict) else []

        student = data.get("student", {}) if isinstance(data, dict) else {}

        total = sum(self._num(x.get("awarded_marks", x.get("score", 0))) for x in evaluations)
        maximum = sum(self._num(x.get("max_marks", 0)) for x in evaluations)

        html = self._html(evaluations, student, total, maximum)
        html_path = out / "evaluation_report.html"
        html_path.write_text(html, encoding="utf-8")

        result = {
            "student": student,
            "summary": {
                "total_marks": total,
                "maximum_marks": maximum,
                "percentage": round((total / maximum) * 100, 2) if maximum else 0
            },
            "evaluations": evaluations
        }

        json_path = out / "explainability_results.json"
        json_path.write_text(
            json.dumps(result, indent=2, ensure_ascii=False),
            encoding="utf-8"
        )

        return {
            "html_report": str(html_path),
            "explainability_json": str(json_path),
            "questions": len(evaluations)
        }

    def _html(self, evaluations, student, total, maximum):
        percentage = round((total / maximum) * 100, 2) if maximum else 0

        parts = [
            "<!doctype html><html><head><meta charset='utf-8'>",
            "<title>Answer Evaluation Report</title>",
            """<style>
            body{font-family:Arial,sans-serif;margin:35px;line-height:1.5}
            .header{border-bottom:2px solid #333;padding-bottom:15px}
            .summary{padding:15px;margin:20px 0;border:1px solid #ccc;border-radius:8px}
            .question{border:1px solid #ccc;border-radius:8px;padding:18px;margin:18px 0}
            .criterion{padding:12px;margin:10px 0;background:#f5f5f5;border-radius:6px}
            .score{font-size:20px;font-weight:bold}
            table{border-collapse:collapse;width:100%}
            th,td{border:1px solid #ccc;padding:8px;text-align:left}
            </style></head><body>"""
        ]

        name = escape(str(student.get("student_name", "")))
        subject = escape(str(student.get("subject", "")))
        course = escape(str(student.get("course", "")))

        parts.append("<div class='header'><h1>Answer Evaluation Report</h1>")
        if name:
            parts.append(f"<p><b>Student:</b> {name}</p>")
        if subject:
            parts.append(f"<p><b>Subject:</b> {subject}</p>")
        if course:
            parts.append(f"<p><b>Course:</b> {course}</p>")
        parts.append("</div>")

        parts.append(
            f"<div class='summary'><div class='score'>"
            f"Total: {total:g} / {maximum:g}</div>"
            f"<p>Percentage: {percentage}%</p></div>"
        )

        for item in evaluations:
            qno = escape(str(item.get("question_number", item.get("number", "?"))))
            score = self._num(item.get("awarded_marks", item.get("score", 0)))
            max_marks = self._num(item.get("max_marks", 0))

            parts.append(f"<div class='question'><h2>Question {qno}</h2>")
            parts.append(f"<p class='score'>{score:g} / {max_marks:g}</p>")

            criteria = item.get("criteria", item.get("criterion_explanations", [])) or []

            if criteria:
                parts.append("<h3>Criterion-level explanation</h3>")

                for c in criteria:
                    cid = escape(str(c.get("criterion_id", "")))
                    desc = escape(str(c.get("criterion_description", "")))
                    status = escape(str(c.get("status", "")))
                    awarded = self._num(c.get("awarded_marks", 0))
                    cmax = self._num(c.get("max_marks", 0))
                    evidence = escape(str(c.get("evidence", "")))
                    reason = escape(str(c.get("reason", c.get("explanation", ""))))
                    missing = c.get("missing_concepts", []) or []

                    parts.append("<div class='criterion'>")
                    if cid:
                        parts.append(f"<b>{cid}</b> ")
                    if desc:
                        parts.append(f"— {desc}<br>")
                    parts.append(f"<b>Status:</b> {status}<br>")
                    parts.append(f"<b>Marks:</b> {awarded:g} / {cmax:g}<br>")

                    if evidence:
                        parts.append(f"<b>Evidence:</b> {evidence}<br>")
                    if reason:
                        parts.append(f"<b>Reason:</b> {reason}<br>")
                    if missing:
                        missing_text = ", ".join(escape(str(x)) for x in missing)
                        parts.append(f"<b>Missing concepts:</b> {missing_text}")

                    parts.append("</div>")

            strengths = item.get("strengths", []) or []
            improvements = item.get("areas_for_improvement", []) or []
            feedback = item.get("overall_feedback", "")

            if strengths:
                parts.append(
                    "<p><b>Strengths:</b> " +
                    ", ".join(escape(str(x)) for x in strengths) +
                    "</p>"
                )

            if improvements:
                parts.append(
                    "<p><b>Areas for improvement:</b> " +
                    ", ".join(escape(str(x)) for x in improvements) +
                    "</p>"
                )

            if feedback:
                parts.append(
                    f"<p><b>Overall feedback:</b> {escape(str(feedback))}</p>"
                )

            parts.append("</div>")

        parts.append("</body></html>")
        return "".join(parts)
