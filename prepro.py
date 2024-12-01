# prepro.py
import re

class PrePro:
    @staticmethod
    def filter(code):
        # Remove comentários iniciados por #
        code = re.sub(r'#.*', '', code)
        # Remove espaços extras
        code = re.sub(r'\s+', ' ', code)
        return code.strip()
