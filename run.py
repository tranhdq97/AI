from re import S
from src.ai.spelling_checker import SpellingChecker


spelling_checker = SpellingChecker()
rs = spelling_checker.check_spell('ca phe')
print(rs)