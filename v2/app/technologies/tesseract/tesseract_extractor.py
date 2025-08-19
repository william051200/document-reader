"""
Tesseract OCR implementation.
Uses pytesseract for extraction.
"""

import pytesseract
from app.core.base import BaseExtractor

class TesseractExtractor(BaseExtractor):
    def run(self, image):
        return pytesseract.image_to_string(image)
