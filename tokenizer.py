# tokenizer.py
from token import Token

RESERVED_WORDS = [
    'IMPRIME', 'LEIA', 'SE', 'SENÃO', 'ENTAO', 'ENQUANTO', 'PARA', 'DE', 'ATÉ', 'FAÇA',
    'FIMSE', 'FIMENQUANTO', 'FIMPARA', 'RECEBE', 'SOMA', 'SUBTRAI', 'MULTIPLICA',
    'DIVIDE', 'PASSO', 'RETORNA', 'INT', 'STR', 'BOOL', 'IGUAL', 'DIFERENTE',
    'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL'
]

class Tokenizer:
    def __init__(self, source):
        self.source = source.strip()
        self.position = 0
        self.next = None
        self.select_next()

    def select_next(self):
        while self.position < len(self.source) and self.source[self.position].isspace():
            self.position += 1

        if self.position >= len(self.source):
            self.next = Token('EOF', None)
            return

        current_char = self.source[self.position]

        # Comentários
        if current_char == '#':
            while self.position < len(self.source) and self.source[self.position] != '\n':
                self.position += 1
            self.select_next()
            return

        # Números
        elif current_char.isdigit():
            num = ''
            while self.position < len(self.source) and self.source[self.position].isdigit():
                num += self.source[self.position]
                self.position += 1
            self.next = Token('NUMBER', int(num))
            return

        # Strings
        elif current_char == '"':
            self.position += 1  # Consumir a aspa inicial
            string_value = ''
            while self.position < len(self.source) and self.source[self.position] != '"':
                string_value += self.source[self.position]
                self.position += 1
            if self.position >= len(self.source):
                raise Exception("String não terminada")
            self.position += 1  # Consumir a aspa final
            self.next = Token('STRING', string_value)
            return

        # Identificadores e palavras reservadas
        elif current_char.isalpha() or current_char == '_':
            ident = ''
            while (self.position < len(self.source) and
                   (self.source[self.position].isalnum() or self.source[self.position] == '_')):
                ident += self.source[self.position]
                self.position += 1
            ident_upper = ident.upper()
            if ident_upper in RESERVED_WORDS:
                self.next = Token('RESERVED', ident_upper)
            else:
                self.next = Token('IDENTIFIER', ident)
            return

        # Operadores e símbolos especiais
        elif current_char in '+-*/();<>!':
            self.next = Token('SYMBOL', current_char)
            self.position += 1
            return

        else:
            raise Exception(f"Caractere inesperado: {current_char}")
