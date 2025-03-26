from hangul_utils import join_jamos

class hangul_text:
    def __init__(self):
        self.ko_map = {
            'r': 'ㄱ', 'R': 'ㄲ', 's': 'ㄴ', 'e': 'ㄷ', 'E': 'ㄸ', 'f': 'ㄹ', 'a': 'ㅁ',
            'q': 'ㅂ', 'Q': 'ㅃ', 't': 'ㅅ', 'T': 'ㅆ', 'd': 'ㅇ', 'w': 'ㅈ', 'W': 'ㅉ',
            'c': 'ㅊ', 'z': 'ㅋ', 'x': 'ㅌ', 'v': 'ㅍ', 'g': 'ㅎ',
            'k': 'ㅏ', 'i': 'ㅑ', 'j': 'ㅓ', 'u': 'ㅕ', 'h': 'ㅗ',
            'y': 'ㅛ', 'n': 'ㅜ', 'b': 'ㅠ', 'm': 'ㅡ', 'l': 'ㅣ',
            'o': 'ㅐ', 'O': 'ㅒ', 'p': 'ㅔ', 'P': 'ㅖ',
        }

    def ko_to_eng_keyboard(self, text: str) -> str:
        """
        영문 자판을 한글로 변환
        """
        return ''.join([self.ko_map.get(char, char) for char in text])

    def join_hangul(self, text: str) -> str:
        """
        한글 자모를 조합하여 완성형 한글로 변환
        """
        return join_jamos(text)
