from googletrans import Translator, LANGUAGES

translator = Translator()

def translate(params):
    text, dest = params
    return translator.translate(text= text, dest= dest).text
