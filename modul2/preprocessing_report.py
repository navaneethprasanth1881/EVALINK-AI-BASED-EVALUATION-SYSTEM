"""
Module 2 - Image Preprocessing

Preprocessing Report

Stores preprocessing information for each page.
"""

import json
import os

from config2 import PreprocessingConfig


class PreprocessingReport:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.pages = []

        os.makedirs(
            PreprocessingConfig.OUTPUT_FOLDER,
            exist_ok=True
        )

    ###########################################################
    # Add Page Report
    ###########################################################

    def add_page(

        self,

        page_number,

        deskew,

        denoise,

        contrast,

        shadow,

        threshold

    ):

        page_report = {

            "page_number": page_number,

            "deskew": deskew,

            "denoise": denoise,

            "contrast": contrast,

            "shadow_removal": shadow,

            "thresholding": threshold

        }

        self.pages.append(page_report)

    ###########################################################
    # Build Report
    ###########################################################

    def build(self):

        return {

            "total_pages": len(self.pages),

            "pages": self.pages

        }

    ###########################################################
    # Save JSON
    ###########################################################

    def save(self):

        filename = os.path.join(

            PreprocessingConfig.OUTPUT_FOLDER,

            "preprocessing_report.json"

        )

        with open(

            filename,

            "w",

            encoding="utf-8"

        ) as file:

            json.dump(

                self.build(),

                file,

                indent=4

            )

    ###########################################################
    # Print Summary
    ###########################################################

    def print_summary(self):

        print()

        print("=" * 60)

        print("PREPROCESSING REPORT")

        print("=" * 60)

        for page in self.pages:

            print()

            print(f"Page {page['page_number']}")

            print("-" * 40)

            print(

                f"Deskew         : "

                f"{page['deskew']['success']}"

            )

            print(

                f"Denoise        : "

                f"{page['denoise']['success']}"

            )

            print(

                f"Contrast       : "

                f"{page['contrast']['success']}"

            )

            print(

                f"Shadow Removal : "

                f"{page['shadow_removal']['success']}"

            )

            print(

                f"Thresholding   : "

                f"{page['thresholding']['success']}"

            )

            print("-" * 40)