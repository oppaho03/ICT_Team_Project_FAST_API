import whisper

def transcribe_audio(file_path: str) -> str:
    """OpenAI Whisper로 음성을 텍스트로 변환"""
    model = whisper.load_model("base") # Whisper라는 인공지능 모델을 불러옴
    result = model.transcribe(file_path)  # 파일을 Whisper에게 넘기고 결과를 받아옴
    return result['text']  # 변환된 텍스트를 반환

