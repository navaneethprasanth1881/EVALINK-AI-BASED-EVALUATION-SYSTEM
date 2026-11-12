"""
Module 4 - Claude OCR

PDF/Image Preparation

Prepares preprocessed page images for Claude OCR.

The actual PDF-to-image conversion happens in Module 2.
Therefore, this module works directly with the images
already stored inside the Document object.
"""

import base64
import cv2
import numpy as np

from config4 import ClaudeOCRConfig


class PDFConverter:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.max_width = (
            ClaudeOCRConfig.MAX_IMAGE_WIDTH
        )

        self.max_height = (
            ClaudeOCRConfig.MAX_IMAGE_HEIGHT
        )

        self.image_format = (
            ClaudeOCRConfig.IMAGE_FORMAT
        )

    ###########################################################
    # Resize Image
    ###########################################################

    def resize_if_needed(self, image):

        """
        Resize an image only when it exceeds the
        configured maximum dimensions.

        The aspect ratio is preserved.
        """

        height, width = image.shape[:2]

        #######################################################
        # Check whether resizing is necessary
        #######################################################

        if (
            width <= self.max_width
            and
            height <= self.max_height
        ):

            return image

        #######################################################
        # Calculate Scale
        #######################################################

        width_scale = (
            self.max_width / width
        )

        height_scale = (
            self.max_height / height
        )

        scale = min(
            width_scale,
            height_scale
        )

        new_width = int(
            width * scale
        )

        new_height = int(
            height * scale
        )

        #######################################################
        # Resize
        #######################################################

        resized = cv2.resize(

            image,

            (
                new_width,
                new_height
            ),

            interpolation=cv2.INTER_AREA

        )

        return resized

    ###########################################################
    # Encode Image
    ###########################################################

    def encode_image(self, image):

        """
        Convert an OpenCV image into Base64 PNG data.
        """

        success, encoded = cv2.imencode(

            ".png",

            image

        )

        if not success:

            raise ValueError(
                "Failed to encode image as PNG."
            )

        image_bytes = encoded.tobytes()

        base64_data = base64.b64encode(
            image_bytes
        ).decode("utf-8")

        return base64_data

    ###########################################################
    # Prepare Single Page
    ###########################################################

    def prepare_page(self, page):

        """
        Prepare one Page object for Claude.

        Returns
        -------
        dict
        """

        #######################################################
        # Select Preprocessed Image
        #######################################################

        image = page.preprocessed_image

        if image is None:

            raise ValueError(
                f"Page {page.page_number} "
                "does not contain a preprocessed image."
            )

        #######################################################
        # Resize
        #######################################################

        image = self.resize_if_needed(
            image
        )

        #######################################################
        # Encode
        #######################################################

        image_data = self.encode_image(
            image
        )

        #######################################################
        # Return Prepared Page
        #######################################################

        return {

            "page_number":
                page.page_number,

            "page_type":
                page.page_type,

            "is_cover":
                page.is_cover,

            "media_type":
                "image/png",

            "image_data":
                image_data

        }

    ###########################################################
    # Prepare Document
    ###########################################################

    def prepare_document(self, document):

        """
        Prepare all relevant pages from the Document.

        Returns
        -------
        list
            Prepared page dictionaries.
        """

        prepared_pages = []

        #######################################################
        # Determine Which Pages to Process
        #######################################################

        if ClaudeOCRConfig.PROCESS_ANSWER_PAGES_ONLY:

            page_numbers = set(
                document.answer_pages
            )

            if ClaudeOCRConfig.PROCESS_COVER_PAGE:

                if document.cover_page is not None:

                    page_numbers.add(
                        document.cover_page
                    )

        else:

            page_numbers = {
                page.page_number
                for page in document.pages
            }

        #######################################################
        # Preserve Original Page Order
        #######################################################

        for page in document.pages:

            if page.page_number not in page_numbers:

                continue

            prepared_page = self.prepare_page(
                page
            )

            prepared_pages.append(
                prepared_page
            )

        #######################################################
        # Return
        #######################################################

        return prepared_pages