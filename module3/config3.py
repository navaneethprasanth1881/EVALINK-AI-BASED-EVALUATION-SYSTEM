"""
Module 3 - Document Management

Configuration
"""


class DocumentConfig:

    # ---------------------------------------------------------
    # College Answer Booklet Structure
    # ---------------------------------------------------------

    # Python uses zero-based indexing internally,
    # but page numbers exposed to the user start from 1.

    COVER_PAGE_NUMBER = 1

    ANSWER_START_PAGE = 2

    # ---------------------------------------------------------
    # Page Types
    # ---------------------------------------------------------

    COVER_PAGE = "COVER"

    ANSWER_PAGE = "ANSWER"

    UNKNOWN_PAGE = "UNKNOWN"

    # ---------------------------------------------------------
    # Validation
    # ---------------------------------------------------------

    MIN_TOTAL_PAGES = 2

    # ---------------------------------------------------------
    # Output
    # ---------------------------------------------------------

    OUTPUT_FOLDER = "output/module_3"

    SAVE_REPORT = True