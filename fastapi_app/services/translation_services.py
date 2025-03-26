from deep_translator import GoogleTranslator

class translate_text:
    def __init__(self):
        self.translator = GoogleTranslator(source='en', target='ko')

    def translate_to_ko(self, text: str):
        return GoogleTranslator(source='en', target='ko').translate(text)
