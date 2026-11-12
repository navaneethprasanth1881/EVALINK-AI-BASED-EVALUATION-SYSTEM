from .models import Exam, Question, SubQuestion, Criterion, SelectionGroup


class SchemaNormalizer:

    def build(
        self,
        paper_data,
        scheme_data,
        detected_groups=None,
        exam_metadata=None
    ):
        exam_metadata = exam_metadata or {}
        detected_groups = detected_groups or []

        exam = Exam(
            course_code=exam_metadata.get("course_code"),
            subject=exam_metadata.get("subject"),
            maximum_marks=exam_metadata.get("maximum_marks"),
            duration=exam_metadata.get("duration"),
        )

        group_lookup = {}
        for g in detected_groups:
            group = SelectionGroup(**g)
            exam.selection_groups.append(group)
            for q in group.questions:
                group_lookup[q] = group.id

        scheme_questions = scheme_data.get("questions", {})

        for raw in paper_data:
            number = str(raw["number"])
            scheme = scheme_questions.get(number, {})

            criteria = []
            for index, c in enumerate(scheme.get("criteria", []), 1):
                criteria.append(Criterion(
                    id=f"Q{number}_C{index}",
                    description=c["description"],
                    marks=float(c["marks"]),
                    rule_type=c.get("rule_type", "standard"),
                    required_count=c.get("required_count"),
                ))

            sub_questions = []
            for sqid, sq in scheme.get("sub_questions", {}).items():
                sqcriteria = []
                for index, c in enumerate(sq.get("criteria", []), 1):
                    sqcriteria.append(Criterion(
                        id=f"Q{number}{sqid}_C{index}",
                        description=c["description"],
                        marks=float(c["marks"]),
                        rule_type=c.get("rule_type", "standard"),
                        required_count=c.get("required_count"),
                    ))

                paper_sq = next(
                    (
                        x for x in raw.get("sub_questions", [])
                        if x["id"].lower().endswith(sqid.lower())
                    ),
                    None
                )

                sub_questions.append(SubQuestion(
                    id=f"{number}{sqid}",
                    text=(paper_sq or {}).get("text", sq.get("title", "")),
                    marks=float(
                        (paper_sq or {}).get("marks")
                        or sum(c.marks for c in sqcriteria)
                    ),
                    criteria=sqcriteria,
                ))

            q_marks = raw.get("marks")
            if q_marks is None:
                q_marks = (
                    sum(c.marks for c in criteria)
                    + sum(s.marks for s in sub_questions)
                )

            exam.questions.append(Question(
                id=f"Q{number}",
                number=number,
                text=raw.get("text", ""),
                marks=float(q_marks or 0),
                section=raw.get("section"),
                module=raw.get("module"),
                co=raw.get("co"),
                criteria=criteria,
                sub_questions=sub_questions,
                selection_group_id=group_lookup.get(number),
            ))

        return exam
