import os

from deep_translator import DeeplTranslator

DEEPL_API_KEY = os.getenv("DEEPL_API_KEY")


def translate(text):
    translated = DeeplTranslator(api_key=DEEPL_API_KEY, source="en", target="uk", use_free_api=True).translate(text)
    print(translated)
    return translated
