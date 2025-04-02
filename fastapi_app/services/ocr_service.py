import os
import shutil
import easyocr

class OCRService:
    def __init__(self, lang_list=['ko', 'en']):
        self.reader = easyocr.Reader(lang_list)

    def run_ocr(self, file: 'UploadFile') -> list:
        file_location = f"uploads/{file.filename}"
        os.makedirs("uploads", exist_ok=True)

        with open(file_location, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

        results = self.reader.readtext(file_location)

        # 삭제 처리 (선택)
        os.remove(file_location)

        return [
            {
                "text": text,
                "confidence": round(confidence, 2),
                "bbox": bbox
            }
            for bbox, text, confidence in results if confidence > 0.7
        ]
