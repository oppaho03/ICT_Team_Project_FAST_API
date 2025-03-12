import re
from services.translation_services import translate_text
from services.keywords_services import text_to_keyword
from services.hangul_service import hangul_text
from services.db_service import save_text_processing_result

class TextProcessingService:
    def __init__(self):
        self.translation_service = translate_text()
        self.keyword_service = text_to_keyword()
        self.hangul_service = hangul_text()

    def count_korean_chars(self, text: str) -> int:
        """한글 문자 개수"""
        return len(re.findall(r"[가-힣]", text))

    def count_english_chars(self, text: str) -> int:
        """영어 문자 개수"""
        return len(re.findall(r"[a-zA-Z]", text))

    def clean_text(self, text: str) -> str:
        """공백 제거 및 한글 자모 결합"""
        text = re.sub(r"\s+", "", text)  # 모든 공백 제거
        text = self.hangul_service.join_hangul(text)  # 한글 자모 결합
        return text

    def process_text(self, text: str):
        """
        1. 번역을 먼저 시도
        2. 번역 후 한글이 많으면 그대로 사용, 영어가 많으면 한글 자판 변환
        3. 한글 자모 조합 (ㅇㅏㄴㄴㅕㅇ → 안녕)
        4. 키워드 추출 (2글자 이상, 의미 없는 단어 제거)
        5. 데이터 저장
        """

        text = text.strip()  # 앞뒤 공백 제거

        # **🔹 1) 번역 먼저 수행**
        translated_text = self.translation_service.translate_to_ko(text)

        # **🔹 2) 번역된 문장에서 한글 vs 영어 개수 비교**
        korean_count = self.count_korean_chars(translated_text)
        english_count = self.count_english_chars(translated_text)

        if korean_count >= english_count:
            processed_text = translated_text  # 번역된 문장 사용
        else:
            processed_text = self.hangul_service.ko_to_eng_keyboard(text)  # 한글 자판 변환

        # **🔹 3) 한글 자모 조합 (조합되지 않은 문자 처리)**
        processed_text = self.hangul_service.join_hangul(processed_text)

        # **🔹 4) 키워드 추출 (불필요한 단어 제거)**
        keywords = self.keyword_service.extract_nouns(processed_text)
        keywords = list(set(filter(lambda x: len(x) >= 1, keywords)))  # 2글자 이상 단어만 유지

        # **🔹 5) 키워드가 없으면 공백 제거 및 다시 한글 조합**
        if not keywords:
            processed_text = self.clean_text(processed_text)

        # **🔹 6) 결과 저장**
        save_text_processing_result(text, processed_text, keywords)

        return {"original_text": text, "processed_text": processed_text, "keywords": keywords}
