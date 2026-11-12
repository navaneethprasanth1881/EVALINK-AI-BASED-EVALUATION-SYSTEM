from dataclasses import dataclass, field, asdict
from typing import Any, Dict, List, Optional


@dataclass
class Criterion:
    id: str
    description: str
    marks: float
    rule_type: str = "standard"
    required_count: Optional[int] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class SubQuestion:
    id: str
    text: str
    marks: float
    criteria: List[Criterion] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "text": self.text,
            "marks": self.marks,
            "criteria": [c.to_dict() for c in self.criteria],
        }


@dataclass
class Question:
    id: str
    number: str
    text: str
    marks: float
    section: Optional[str] = None
    module: Optional[str] = None
    co: Optional[str] = None
    criteria: List[Criterion] = field(default_factory=list)
    sub_questions: List[SubQuestion] = field(default_factory=list)
    selection_group_id: Optional[str] = None

    def to_dict(self) -> Dict[str, Any]:
        return {
            "id": self.id,
            "number": self.number,
            "text": self.text,
            "marks": self.marks,
            "section": self.section,
            "module": self.module,
            "co": self.co,
            "selection_group_id": self.selection_group_id,
            "criteria": [c.to_dict() for c in self.criteria],
            "sub_questions": [s.to_dict() for s in self.sub_questions],
        }


@dataclass
class SelectionGroup:
    id: str
    selection_type: str
    questions: List[str]
    selection_rule: str = "highest_score"
    maximum_counted_marks: Optional[float] = None

    def to_dict(self) -> Dict[str, Any]:
        return asdict(self)


@dataclass
class Exam:
    course_code: Optional[str] = None
    subject: Optional[str] = None
    maximum_marks: Optional[float] = None
    duration: Optional[str] = None
    sections: List[Dict[str, Any]] = field(default_factory=list)
    questions: List[Question] = field(default_factory=list)
    selection_groups: List[SelectionGroup] = field(default_factory=list)

    def to_dict(self) -> Dict[str, Any]:
        return {
            "exam": {
                "course_code": self.course_code,
                "subject": self.subject,
                "maximum_marks": self.maximum_marks,
                "duration": self.duration,
            },
            "sections": self.sections,
            "questions": [q.to_dict() for q in self.questions],
            "selection_groups": [g.to_dict() for g in self.selection_groups],
        }
