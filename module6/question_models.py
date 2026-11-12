from dataclasses import dataclass, field
from typing import List, Optional, Dict, Any


# ============================================================
# MARKING CRITERION
# ============================================================

@dataclass
class MarkingCriterion:
    criterion_id: str
    description: str
    marks: float

    # Optional information for special rules
    scoring_type: str = "standard"

    # Example:
    # "any_two"
    # "any_three"
    # "any_relevant"

    required_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "criterion_id": self.criterion_id,
            "description": self.description,
            "marks": self.marks,
            "scoring_type": self.scoring_type,
            "required_count": self.required_count
        }


# ============================================================
# SUB QUESTION
# ============================================================

@dataclass
class SubQuestion:
    sub_question_id: str
    question_number: str
    text: str
    maximum_marks: float
    criteria: List[MarkingCriterion] = field(default_factory=list)

    def criteria_total(self) -> float:
        return sum(c.marks for c in self.criteria)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "sub_question_id": self.sub_question_id,
            "question_number": self.question_number,
            "text": self.text,
            "maximum_marks": self.maximum_marks,
            "criteria": [
                criterion.to_dict()
                for criterion in self.criteria
            ]
        }


# ============================================================
# QUESTION
# ============================================================

@dataclass
class Question:
    question_number: int
    section: str
    module: Optional[int]
    text: str
    maximum_marks: float
    co: str

    question_type: str = "standard"

    or_group_id: Optional[str] = None

    sub_questions: List[SubQuestion] = field(default_factory=list)

    criteria: List[MarkingCriterion] = field(default_factory=list)

    def criteria_total(self) -> float:
        direct_total = sum(c.marks for c in self.criteria)
        sub_total = sum(
            sq.criteria_total()
            for sq in self.sub_questions
        )

        return direct_total + sub_total

    def to_dict(self) -> Dict[str, Any]:
        return {
            "question_number": self.question_number,
            "section": self.section,
            "module": self.module,
            "text": self.text,
            "maximum_marks": self.maximum_marks,
            "co": self.co,
            "question_type": self.question_type,
            "or_group_id": self.or_group_id,
            "criteria": [
                criterion.to_dict()
                for criterion in self.criteria
            ],
            "sub_questions": [
                sub_question.to_dict()
                for sub_question in self.sub_questions
            ]
        }


# ============================================================
# OR GROUP
# ============================================================

@dataclass
class ORGroup:
    group_id: str
    questions: List[int]

    selection_rule: str = "highest_score"

    maximum_counted_marks: float = 0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "group_id": self.group_id,
            "questions": self.questions,
            "selection_rule": self.selection_rule,
            "maximum_counted_marks": self.maximum_counted_marks
        }


# ============================================================
# SECTION
# ============================================================

@dataclass
class Section:
    section_id: str
    name: str
    question_numbers: List[int]
    question_type: str
    maximum_marks: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "section_id": self.section_id,
            "name": self.name,
            "question_numbers": self.question_numbers,
            "question_type": self.question_type,
            "maximum_marks": self.maximum_marks
        }


# ============================================================
# EXAM SCHEMA
# ============================================================

@dataclass
class ExamSchema:
    course_code: str
    subject: str
    maximum_marks: float
    duration: str

    sections: List[Section] = field(default_factory=list)
    questions: List[Question] = field(default_factory=list)
    or_groups: List[ORGroup] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:

        return {
            "exam": {
                "course_code": self.course_code,
                "subject": self.subject,
                "maximum_marks": self.maximum_marks,
                "duration": self.duration
            },

            "sections": [
                section.to_dict()
                for section in self.sections
            ],

            "or_groups": [
                group.to_dict()
                for group in self.or_groups
            ],

            "questions": [
                question.to_dict()
                for question in self.questions
            ]
        }