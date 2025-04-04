# services/ocr_service.py

import easyocr
import numpy as np
import cv2

class OCRService:
    def __init__(self, lang_list=['ko', 'en'], use_gpu=True):
        self.reader = easyocr.Reader(lang_list, gpu=use_gpu)

    def run_ocr(self, image_bytes: bytes) -> list:
        # 바이트 데이터를 OpenCV 이미지로 디코딩
        np_arr = np.frombuffer(image_bytes, np.uint8)
        image = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)

        # OCR 수행 (텍스트만 추출, detail=0)
        results = self.reader.readtext(image, detail=0)

        return results