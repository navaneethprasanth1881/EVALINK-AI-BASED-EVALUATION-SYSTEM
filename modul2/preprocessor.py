"""
Module 2 - Image Preprocessing

Preprocessor

Main controller for Module 2.
"""

from config2 import PreprocessingConfig

from deskew import Deskew
from denoise import Denoise
from contrast import Contrast
from shadow_removal import ShadowRemoval
from thresholding import Thresholding
from pdfbuilder import PDFBuilder
from preprocessing_report import PreprocessingReport


class Preprocessor:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.deskew = Deskew()

        self.denoise = Denoise()

        self.contrast = Contrast()

        self.shadow = ShadowRemoval()

        self.threshold = Thresholding()

        self.report = PreprocessingReport()

        self.builder = PDFBuilder()

    ###########################################################
    # Process Document
    ###########################################################

    def process(self, document):

        """
        Process every page inside the document.

        Parameters
        ----------
        document : Document

        Returns
        -------
        Document
        """

        #######################################################
        # Process Each Page
        #######################################################

        for page in document.pages:

            image = page.original_image

            ###################################################
            # Deskew
            ###################################################

            if PreprocessingConfig.ENABLE_DESKEW:

                image, deskew_report = self.deskew.process(image)

            else:

                deskew_report = {

                    "enabled": False,

                    "success": False,

                    "details": {}

                }

            ###################################################
            # Denoise
            ###################################################

            if PreprocessingConfig.ENABLE_DENOISE:

                image, denoise_report = self.denoise.process(image)

            else:

                denoise_report = {

                    "enabled": False,

                    "success": False,

                    "details": {}

                }

            ###################################################
            # Contrast
            ###################################################

            if PreprocessingConfig.ENABLE_CONTRAST:

                image, contrast_report = self.contrast.process(image)

            else:

                contrast_report = {

                    "enabled": False,

                    "success": False,

                    "details": {}

                }

            ###################################################
            # Shadow Removal
            ###################################################

            if PreprocessingConfig.ENABLE_SHADOW_REMOVAL:

                image, shadow_report = self.shadow.process(image)

            else:

                shadow_report = {

                    "enabled": False,

                    "success": False,

                    "details": {}

                }

            ###################################################
            # Threshold
            ###################################################

            if PreprocessingConfig.ENABLE_THRESHOLDING:

                image, threshold_report = self.threshold.process(image)

            else:

                threshold_report = {

                    "enabled": False,

                    "success": False,

                    "details": {}

                }

            ###################################################
            # Store Final Image
            ###################################################

            page.preprocessed_image = image

            ###################################################
            # Store Report Inside Page
            ###################################################

            page.preprocessing_report = {

                "deskew": deskew_report,

                "denoise": denoise_report,

                "contrast": contrast_report,

                "shadow_removal": shadow_report,

                "thresholding": threshold_report

            }

            ###################################################
            # Global Report
            ###################################################

            self.report.add_page(

                page.page_number,

                deskew_report,

                denoise_report,

                contrast_report,

                shadow_report,

                threshold_report

            )

        #######################################################
        # Save JSON Report
        #######################################################

        self.report.save()

        #######################################################
        # Build Preprocessed PDF
        #######################################################

        pdf_path = self.builder.build(document)

        document.preprocessed_pdf_path = pdf_path

        #######################################################
        # Store Global Report
        #######################################################

        document.preprocessing_report = self.report.build()

        #######################################################
        # Return Document
        #######################################################

        return document