from pdf2image import convert_from_path
import cv2
import numpy as np
from config import QualityConfig

POPPLER_PATH = r"C:\Users\NAVANEETH\OneDrive\Desktop\poppler-26.02.0\Library\bin"

class PDFLoader:
    def __init__(self):
        self.dpi = QualityConfig.PDF_DPI

    def load(self, pdf_path):
        pages = convert_from_path(pdf_path, dpi=self.dpi, poppler_path=POPPLER_PATH)
        images = []
        for page in pages:
            image = np.array(page)
            image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
            images.append(image)
        return images

    def page_count(self, pdf_path):
        return len(convert_from_path(pdf_path, dpi=50, poppler_path=POPPLER_PATH))

    def load_page(self, pdf_path, page_number):
        pages = convert_from_path(
            pdf_path, dpi=self.dpi, first_page=page_number, 
            last_page=page_number, poppler_path=POPPLER_PATH
        )
        page = np.array(pages[0])
        return cv2.cvtColor(page, cv2.COLOR_RGB2BGR)