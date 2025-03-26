from services.text_processing_service import TextProcessingService

# ✅ 텍스트 처리 서비스 인스턴스 생성
text_processor = TextProcessingService()

# ✅ 사용자 입력 받기
input_text = input("변환할 텍스트를 입력하세요: ")

# ✅ 텍스트 처리 실행
result = text_processor.process_text(input_text)

# ✅ 결과 출력
print("\n=== 변환 결과 ===")
print(f"원본 텍스트: {result['original_text']}")
print(f"처리된 텍스트: {result['processed_text']}")
print(f"추출된 키워드: {result['keywords']}")
