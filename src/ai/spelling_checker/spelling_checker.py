import os
from serpapi import GoogleSearch
from dotenv import load_dotenv


load_dotenv()


class SpellingChecker:
    def __init__(self) -> None:
        self.hl = os.getenv('HL')
        self.gl = os.getenv('GL')
        self.__secret_key = os.getenv('SECRET_KEY')
        print(self.hl, self.gl, self.__secret_key)

    def check_spell(self, content):
        params = {
            'q': content,
            'hl': self.hl,
            'gl': self.gl,
            'secret_key': self.__secret_key
        }
        return GoogleSearch(params).get_dict()
