import json
import os
from config import QualityConfig

class QualityReport:
    def __init__(self):
        self.pages = []
        os.makedirs(QualityConfig.OUTPUT_FOLDER, exist_ok=True)

    def add_page(self, page_number, metrics):
        page_report = {
            "page_number": page_number,
            "blur": metrics["blur"],
            "brightness": metrics["brightness"],
            "contrast": metrics["contrast"],
            "noise": metrics["noise"],
            "shadow_percentage": metrics["shadow_percentage"],
            "width": metrics["width"],
            "height": metrics["height"],
            "status": self.page_status(metrics),
            "checks": {
                "blur": metrics["blur_ok"],
                "brightness": metrics["brightness_ok"],
                "contrast": metrics["contrast_ok"],
                "noise": metrics["noise_ok"],
                "shadow": metrics["shadow_ok"],
                "resolution": metrics["resolution_ok"]
            }
        }
        self.pages.append(page_report)

    def build(self):
        return {
            "total_pages": len(self.pages),
            "pages": self.pages
        }

    def save(self):
        report = self.build()
        filename = os.path.join(QualityConfig.OUTPUT_FOLDER, "quality_report.json")
        with open(filename, "w", encoding="utf-8") as file:
            json.dump(report, file, indent=4)

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
        
        failed = sum(not c for c in checks)
        if failed <= 2:
            return "ACCEPTABLE"
        return "POOR"