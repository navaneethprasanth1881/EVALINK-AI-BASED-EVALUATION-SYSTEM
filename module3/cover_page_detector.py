"""
Module 3 - Document Management

Cover Page Detector

Identifies the student-information page
using the known booklet structure.
"""

from module3.config3 import DocumentConfig


class CoverPageDetector:

    # ---------------------------------------------------------
    # Detect Cover Page
    # ---------------------------------------------------------

    def is_cover_page(self, page_number):
        """
        Determine whether a page is the cover page.

        Parameters
        ----------
        page_number : int
            1-based page number.

        Returns
        -------
        bool
        """

        return (
            page_number
            == DocumentConfig.COVER_PAGE_NUMBER
        )

    # ---------------------------------------------------------
    # Get Cover Page Number
    # ---------------------------------------------------------

    def get_cover_page(self, document):
        """
        Return the cover page number.

        Returns
        -------
        int or None
        """

        if document.total_pages == 0:

            return None

        return DocumentConfig.COVER_PAGE_NUMBER