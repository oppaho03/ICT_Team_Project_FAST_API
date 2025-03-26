from transformers import pipeline
from typing import Dict

def sentiment_analysis(text: str) -> Dict[str, str or float]:
    """텍스트 감성 분석"""
    classifier = pipeline("sentiment-analysis")
    result = classifier(text)[0]
    return {'sentiment': result['label'], 'score': result['score']}
