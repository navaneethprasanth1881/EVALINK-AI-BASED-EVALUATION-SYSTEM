import cv2
import numpy as np
from config2 import PreprocessingConfig

class Deskew:
    def __init__(self):
        self.max_angle = PreprocessingConfig.MAX_DESKEW_ANGLE

    def detect_angle(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        _, binary = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)
        
        coordinates = np.column_stack(np.where(binary > 0))
        if len(coordinates) == 0:
            return 0.0
        
        angle = cv2.minAreaRect(coordinates)[-1]
        if angle < -45:
            angle = 90 + angle
        else:
            angle = -angle
            
        if abs(angle) > self.max_angle:
            return 0.0
        return float(angle)

    def rotate(self, image, angle):
        h, w = image.shape[:2]
        center = (w // 2, h // 2)
        matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
        rotated = cv2.warpAffine(
            image, matrix, (w, h), 
            flags=cv2.INTER_CUBIC, 
            borderMode=cv2.BORDER_REPLICATE
        )
        return rotated

    def process(self, image):
        angle = self.detect_angle(image)
        corrected = self.rotate(image, angle)
        report = {
            "deskew_enabled": True,
            "detected_angle": angle,
            "corrected": abs(angle) > 0.1
        }
        return corrected, report