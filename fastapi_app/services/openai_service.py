import openai
import os
from dotenv import load_dotenv

load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    def __init__(self, model="gpt-3.5-turbo"):
        self.model = model

    def ask_about_prescription(self, ocr_text: str) -> str:
        messages = [
            {"role": "system", "content": "당신은 약 봉투에서 추출한 내용을 분석해서 복약 정보를 요약해주는 약사입니다."},
            {"role": "user", "content": f"다음 텍스트를 분석해서 복약 시간, 약 이름, 주의사항 등을 정리해줘:\n\n{ocr_text}"}
        ]

        response = openai.ChatCompletion.create(
            model=self.model,
            messages=messages
        )
        return response.choices[0].message["content"]
