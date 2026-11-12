"""
Module 2 - Image Preprocessing

PDF Builder

Converts preprocessed images back into a PDF.
"""

import os
import cv2
from PIL import Image

from config2 import PreprocessingConfig


class PDFBuilder:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.output_folder = (
            PreprocessingConfig.OUTPUT_FOLDER
        )

        os.makedirs(

            self.output_folder,

            exist_ok=True

        )

    ###########################################################
    # OpenCV -> PIL
    ###########################################################

    def cv_to_pil(self, image):

        rgb = cv2.cvtColor(

            image,

            cv2.COLOR_BGR2RGB

        )

        return Image.fromarray(rgb)

    ###########################################################
    # Build PDF
    ###########################################################

    def build(self, document):

        """
        Creates a PDF from all preprocessed pages.

        Parameters
        ----------
        document : Document

        Returns
        -------
        str
            Output PDF path.
        """

        pages = []

        for page in document.pages:

            if page.preprocessed_image is None:

                continue

            pil = self.cv_to_pil(

                page.preprocessed_image

            )

            pages.append(pil)

        if len(pages) == 0:

            raise ValueError(

                "No preprocessed images available."

            )

        output_path = os.path.join(

            self.output_folder,

            "preprocessed.pdf"

        )

        pages[0].save(

            output_path,

            save_all=True,

            append_images=pages[1:]

        )

        return output_path