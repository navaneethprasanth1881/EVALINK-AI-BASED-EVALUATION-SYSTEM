import cv2
from config2 import PreprocessingConfig

class Thresholding:
    def __init__(self):
        self.method = PreprocessingConfig.THRESHOLD_METHOD
        self.block_size = PreprocessingConfig.ADAPTIVE_BLOCK_SIZE
        self.c = PreprocessingConfig.ADAPTIVE_C

    def adaptive(self, gray):
        block = self.block_size
        if block % 2 == 0:
            block += 1
        binary = cv2.adaptiveThreshold(
            gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, 
            cv2.THRESH_BINARY, block, self.c
        )
        return binary

    def otsu(self, gray):
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        return binary

    def process(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        
        if self.method.lower() == "adaptive":
            binary = self.adaptive(gray)
            method_used = "Adaptive Gaussian"
        elif self.method.lower() == "otsu":
            binary = self.otsu(gray)
            method_used = "Otsu"
        else:
            raise ValueError(f"Unknown threshold method: {self.method}")
        
        binary = cv2.cvtColor(binary, cv2.COLOR_GRAY2BGR)
        
        report = {
            "enabled": True,
            "success": True,
            "details": {
                "method": method_used,
                "block_size": self.block_size,
                "c": self.c
            }
        }
        return binary, report