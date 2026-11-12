"""
Core Page Object

Represents one page of the answer booklet.
"""

from dataclasses import dataclass, field
from typing import Optional, Any

import numpy as np


@dataclass
class Page:

    # ---------------------------------------------------------
    # Basic page information
    # ---------------------------------------------------------

    page_number: int

    original_image: np.ndarray

    # ---------------------------------------------------------
    # Module 1 - Image Quality
    # ---------------------------------------------------------

    quality_metrics: dict = field(default_factory=dict)

    # ---------------------------------------------------------
    # Module 2 - Preprocessing
    # ---------------------------------------------------------

    preprocessed_image: Optional[np.ndarray] = None

    preprocessing_report: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Module 3 - Document Management
    # ---------------------------------------------------------

    page_type: Optional[str] = None

    is_cover: bool = False

    # ---------------------------------------------------------
    # Module 4 - Claude OCR
    # ---------------------------------------------------------

    ocr_result: dict = field(
        default_factory=dict
    )

    # ---------------------------------------------------------
    # Future answer information
    # ---------------------------------------------------------

    answers: list = field(
        default_factory=list
    )