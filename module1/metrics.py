import cv2
import numpy as np
from config import QualityConfig

class QualityMetrics:
    def blur_score(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        score = cv2.Laplacian(gray, cv2.CV_64F).var()
        return float(score)

    def brightness_score(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return float(np.mean(gray))

    def contrast_score(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        return float(np.std(gray))

    def noise_score(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        denoised = cv2.GaussianBlur(gray, (5, 5), 0)
        noise = gray.astype(np.float32) - denoised.astype(np.float32)
        return float(np.std(noise))

    def shadow_percentage(self, image):
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        dark_pixels = np.sum(gray < 60)
        total_pixels = gray.size
        percentage = (dark_pixels / total_pixels) * 100
        return float(percentage)

    def resolution(self, image):
        h, w = image.shape[:2]
        return w, h

    def evaluate(self, image):
        blur = self.blur_score(image)
        brightness = self.brightness_score(image)
        contrast = self.contrast_score(image)
        noise = self.noise_score(image)
        shadow = self.shadow_percentage(image)
        width, height = self.resolution(image)

        report = {
            "blur": blur,
            "brightness": brightness,
            "contrast": contrast,
            "noise": noise,
            "shadow_percentage": shadow,
            "width": width,
            "height": height,
            "blur_ok": blur >= QualityConfig.BLUR_THRESHOLD,
            "brightness_ok": QualityConfig.MIN_BRIGHTNESS <= brightness <= QualityConfig.MAX_BRIGHTNESS,
            "contrast_ok": contrast >= QualityConfig.MIN_CONTRAST,
            "noise_ok": noise <= QualityConfig.MAX_NOISE,
            "shadow_ok": shadow <= QualityConfig.MAX_SHADOW_PERCENTAGE,
            "resolution_ok": width >= QualityConfig.MIN_WIDTH and height >= QualityConfig.MIN_HEIGHT
        }
        return report