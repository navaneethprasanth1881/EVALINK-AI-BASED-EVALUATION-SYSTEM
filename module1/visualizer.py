"""
Module 1 - Image Quality Assessment

Visualizer

Creates annotated images showing
quality assessment results.
"""

import os
import cv2

from config import QualityConfig


class QualityVisualizer:

    ###########################################################
    # Constructor
    ###########################################################

    def __init__(self):

        self.output_folder = os.path.join(
            QualityConfig.OUTPUT_FOLDER,
            "visualizations"
        )

        os.makedirs(
            self.output_folder,
            exist_ok=True
        )

    ###########################################################
    # Draw Quality Information
    ###########################################################

    def draw(self, image, page_number, metrics):

        output = image.copy()

        x = 30
        y = 40
        gap = 35

        status = self.page_status(metrics)

        if status == "GOOD":
            color = (0, 255, 0)

        elif status == "ACCEPTABLE":
            color = (0, 255, 255)

        else:
            color = (0, 0, 255)

        #######################################################

        cv2.putText(

            output,

            f"Page : {page_number}",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            color,

            2

        )

        y += gap

        cv2.putText(

            output,

            f"Status : {status}",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.8,

            color,

            2

        )

        y += gap

        cv2.putText(

            output,

            f"Blur : {metrics['blur']:.2f}",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        y += gap

        cv2.putText(

            output,

            f"Brightness : {metrics['brightness']:.2f}",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        y += gap

        cv2.putText(

            output,

            f"Contrast : {metrics['contrast']:.2f}",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        y += gap

        cv2.putText(

            output,

            f"Noise : {metrics['noise']:.2f}",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        y += gap

        cv2.putText(

            output,

            f"Shadow : {metrics['shadow_percentage']:.2f}%",

            (x, y),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (255, 255, 255),

            2

        )

        return output

    ###########################################################
    # Save Image
    ###########################################################

    def save(self, page_number, image):

        filename = os.path.join(

            self.output_folder,

            f"page_{page_number}.png"

        )

        cv2.imwrite(

            filename,

            image

        )

    ###########################################################
    # Status
    ###########################################################

    def page_status(self, metrics):

        checks = [

            metrics["blur_ok"],

            metrics["brightness_ok"],

            metrics["contrast_ok"],

            metrics["noise_ok"],

            metrics["shadow_ok"],

            metrics["resolution_ok"]

        ]

        if all(checks):

            return "GOOD"

        failed = sum(
            not c
            for c in checks
        )

        if failed <= 2:

            return "ACCEPTABLE"

        return "POOR"