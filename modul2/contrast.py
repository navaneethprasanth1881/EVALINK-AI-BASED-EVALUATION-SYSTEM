import cv2
from config2 import PreprocessingConfig

class Contrast:
    def __init__(self):
        self.clip_limit = PreprocessingConfig.CLAHE_CLIP_LIMIT
        self.grid_size = PreprocessingConfig.CLAHE_GRID_SIZE

    def process(self, image):
        lab = cv2.cvtColor(image, cv2.COLOR_BGR2LAB)
        l, a, b = cv2.split(lab)
        
        clahe = cv2.createCLAHE(clipLimit=self.clip_limit, tileGridSize=self.grid_size)
        l = clahe.apply(l)
        
        enhanced = cv2.merge((l, a, b))
        enhanced = cv2.cvtColor(enhanced, cv2.COLOR_LAB2BGR)
        
        report = {
            "enabled": True,
            "success": True,
            "details": {
                "method": "CLAHE",
                "clip_limit": self.clip_limit,
                "grid_size": self.grid_size
            }
        }
        return enhanced, report