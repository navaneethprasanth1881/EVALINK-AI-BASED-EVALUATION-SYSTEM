import cv2
import numpy as np
from config2 import PreprocessingConfig

class ShadowRemoval:
    def __init__(self):
        self.blur_kernel = PreprocessingConfig.SHADOW_BLUR_KERNEL

    def estimate_background(self, gray):
        kernel = self.blur_kernel
        if kernel % 2 == 0:
            kernel += 1
        background = cv2.GaussianBlur(gray, (kernel, kernel), 0)
        return background

    def process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        background = self.estimate_background(gray)
        
        normalized = cv2.divide(gray, background, scale=255)
        output = cv2.cvtColor(normalized, cv2.COLOR_GRAY2BGR)
        
        report = {
            "enabled": True,
            "success": True,
            "details": {
                "method": "Background Normalization",
                "blur_kernel": self.blur_kernel
            }
        }
        return output, report