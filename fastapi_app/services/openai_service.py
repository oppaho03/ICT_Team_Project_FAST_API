import os
from dotenv import load_dotenv
from openai import OpenAI

# .env 파일 로드 (위치가 루트일 경우 경로 지정)
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '..', '.env'))

api_key = os.getenv("OPENAI_API_KEY")

class OpenAIService:
    def __init__(self):
        self.client = OpenAI(api_key=api_key)

    def ask_about_prescription(self, text: str) -> str:
        response = self.client.chat.completions.create(
            model="gpt-4",
            messages=[
                {
                    "role": "system",
                    "content": """
            너는 아주 유명한 약사야.
            약품명을 기반으로 어떤 질병인지 예측해서 알려줘.
            길게 설명하지 말고 가능성이 제일 높은 병명 알려줘.
            약품에 대해선 설명 안해줘도 돼.
            병명만 딱 출력해.
            """
                },
                {"role": "user", "content": text}
            ]
        )
        return response.choices[0].message.content