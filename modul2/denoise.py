import cv2
from config2 import PreprocessingConfig

class Denoise:
    def __init__(self):
        self.h = PreprocessingConfig.DENOISE_H
        self.template_window = PreprocessingConfig.DENOISE_TEMPLATE_WINDOW
        self.search_window = PreprocessingConfig.DENOISE_SEARCH_WINDOW

    def process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.fastNlMeansDenoising(
            gray, None, self.h, self.template_window, self.search_window
        )
        denoised = cv2.cvtColor(denoised, cv2.COLOR_GRAY2BGR)
        
        report = {
            "enabled": True,
            "success": True,
            "details": {
                "method": "Fast Non Local Means",
                "h": self.h,
                "template_window": self.template_window,
                "search_window": self.search_window
            }
        }
        return denoised, report