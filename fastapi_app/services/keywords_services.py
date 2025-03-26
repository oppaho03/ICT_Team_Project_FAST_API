from konlpy.tag import Kkma, Okt, Hannanum, Komoran, Mecab
from typing import List, Tuple

class HannanumService:
    def __init__(self):
        self.hannanum = Hannanum()

    def analyze(self, text: str) -> List[Tuple[str, str]]:
        return self.hannanum.pos(text)

    def extract_nouns(self, text: str) -> List[str]:
        return self.hannanum.nouns(text)


class KkmaService:
    def __init__(self):
        self.kkma = Kkma()

    def analyze(self, text: str) -> List[Tuple[str, str]]:
        return self.kkma.pos(text)

    def extract_nouns(self, text: str) -> List[str]:
        return self.kkma.nouns(text)


class KomoranService:
    def __init__(self):
        self.komoran = Komoran()

    def analyze(self, text: str) -> List[Tuple[str, str]]:
        return self.komoran.pos(text)

    def extract_nouns(self, text: str) -> List[str]:
        return self.komoran.nouns(text)


class MecabService:
    def __init__(self):
        self.mecab = Mecab()

    def analyze(self, text: str) -> List[Tuple[str, str]]:
        return self.mecab.pos(text)

    def extract_nouns(self, text: str) -> List[str]:
        return self.mecab.nouns(text)


class text_to_keyword:
    def __init__(self):
        self.okt = Okt()

    def text_to_keywords(self, text: str) -> List[Tuple[str, str]]:
        return self.okt.pos(text)

    def extract_nouns(self, text: str) -> List[str]:
        return self.okt.nouns(text)
