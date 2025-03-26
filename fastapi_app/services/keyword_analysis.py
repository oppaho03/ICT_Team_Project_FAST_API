
from typing import Dict, List
from transformers import pipeline
import os

def load_keywords(file_path: str = "keywords.txt") -> List[str]:
    """키워드 파일을 읽어서 리스트로 반환"""
    if os.path.exists(file_path):
        with open(file_path, 'r', encoding='utf-8') as file:
            keywords = [line.strip() for line in file.readlines() if line.strip()]
        return keywords
    return []

def keyword_sentiment_analysis(text: str, keywords: List[str]) -> Dict[str, Dict[str, str or float]]:
    """키워드별 감성 분석"""
    classifier = pipeline("sentiment-analysis")
    result = {}
    for keyword in keywords:
        if keyword in text:
            keyword_result = classifier(keyword)[0]
            result[keyword] = {'sentiment': keyword_result['label'], 'score': keyword_result['score']}
    return result
