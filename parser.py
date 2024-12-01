# parser.py
from tokenizer import Tokenizer
from node import *
from symboltable import SymbolTable

class Parser:
    tokens = None
    current_token = None

    @staticmethod
    def parse_program():
        statements = []
        while Parser.current_token.type != 'EOF':
            statements.append(Parser.parse_command())
        return BlockNode(statements)

    @staticmethod
    def parse_command():
        if Parser.current_token.type == 'RESERVED':
            if Parser.current_token.value == 'IMPRIME':
                Parser.advance()
                expr = Parser.parse_expression()
                if Parser.current_token.value != ';':
                    raise Exception("Esperado ';' após expressão")
                Parser.advance()
                return PrintNode(expr)
            elif Parser.current_token.value == 'LEIA':
                Parser.advance()
                if Parser.current_token.type != 'IDENTIFIER':
                    raise Exception("Esperado identificador após 'LEIA'")
                var_name = Parser.current_token.value
                Parser.advance()
                if Parser.current_token.value != ';':
                    raise Exception("Esperado ';' após identificador")
                Parser.advance()
                return ReadNode(var_name)
            elif Parser.current_token.value == 'SE':
                Parser.advance()
                condition = Parser.parse_condition()
                if Parser.current_token.value != 'ENTAO':
                    raise Exception("Esperado 'ENTAO' após condição")
                Parser.advance()
                true_block = Parser.parse_block()
                false_block = None
                if Parser.current_token.value == 'SENAO':
                    Parser.advance()
                    false_block = Parser.parse_block()
                if Parser.current_token.value != 'FIMSE':
                    raise Exception("Esperado 'FIMSE' após bloco 'SE'")
                Parser.advance()
                return IfNode(condition, true_block, false_block)
            elif Parser.current_token.value == 'ENQUANTO':
                Parser.advance()
                condition = Parser.parse_condition()
                if Parser.current_token.value != 'FACA':
                    raise Exception("Esperado 'FACA' após condição")
                Parser.advance()
                block = Parser.parse_block()
                if Parser.current_token.value != 'FIMENQUANTO':
                    raise Exception("Esperado 'FIMENQUANTO' após bloco 'ENQUANTO'")
                Parser.advance()
                return WhileNode(condition, block)
            elif Parser.current_token.value == 'PARA':
                Parser.advance()
                if Parser.current_token.value not in ['INT', 'STR', 'BOOL']:
                    raise Exception("Esperado tipo após 'PARA'")
                var_type = Parser.current_token.value
                Parser.advance()
                if Parser.current_token.type != 'IDENTIFIER':
                    raise Exception("Esperado identificador após tipo em 'PARA'")
                var_name = Parser.current_token.value
                Parser.advance()
                if Parser.current_token.value != 'DE':
                    raise Exception("Esperado 'DE' após identificador")
                Parser.advance()
                start_expr = Parser.parse_expression()
                if Parser.current_token.value != 'ATE':
                    raise Exception("Esperado 'ATE' após expressão inicial")
                Parser.advance()
                end_expr = Parser.parse_expression()
                step_expr = None
                if Parser.current_token.value == 'PASSO':
                    Parser.advance()
                    step_expr = Parser.parse_expression()
                if Parser.current_token.value != 'FACA':
                    raise Exception("Esperado 'FACA' para iniciar o bloco do 'PARA'")
                Parser.advance()
                block = Parser.parse_block()
                if Parser.current_token.value != 'FIMPARA':
                    raise Exception("Esperado 'FIMPARA' após bloco 'PARA'")
                Parser.advance()
                return ForNode(var_name, start_expr, end_expr, step_expr, block)
            elif Parser.current_token.value == 'FUNCAO':
                Parser.advance()
                if Parser.current_token.value not in ['INT', 'STR', 'BOOL']:
                    raise Exception("Esperado tipo após 'FUNCAO'")
                func_type = Parser.current_token.value
                Parser.advance()
                if Parser.current_token.type != 'IDENTIFIER':
                    raise Exception("Esperado identificador após tipo na declaração de função")
                func_name = Parser.current_token.value
                Parser.advance()
                if Parser.current_token.value != '(':
                    raise Exception("Esperado '(' após nome da função")
                Parser.advance()
                params = []
                if Parser.current_token.value != ')':
                    while True:
                        param_type = Parser.current_token.value
                        if param_type not in ['INT', 'STR', 'BOOL']:
                            raise Exception("Tipo de parâmetro inválido")
                        Parser.advance()
                        if Parser.current_token.type != 'IDENTIFIER':
                            raise Exception("Esperado identificador do parâmetro")
                        param_name = Parser.current_token.value
                        Parser.advance()
                        params.append((param_type, param_name))
                        if Parser.current_token.value == ',':
                            Parser.advance()
                        else:
                            break
                if Parser.current_token.value != ')':
                    raise Exception("Esperado ')' após parâmetros")
                Parser.advance()
                block = Parser.parse_block()
                return FuncDecNode(func_type, func_name, params, block)
            elif Parser.current_token.value in ['INT', 'STR', 'BOOL']:
                # Declaração de variáveis (possivelmente múltiplas)
                declarations = []
                while True:
                    var_type = Parser.current_token.value
                    Parser.advance()
                    if Parser.current_token.type != 'IDENTIFIER':
                        raise Exception("Esperado identificador após tipo")
                    var_name = Parser.current_token.value
                    Parser.advance()
                    expr = None
                    if Parser.current_token.value == 'RECEBE':
                        Parser.advance()
                        expr = Parser.parse_expression()
                    declarations.append(VarDecNode(var_type, var_name, expr))
                    if Parser.current_token.value == ',':
                        Parser.advance()
                        if Parser.current_token.value not in ['INT', 'STR', 'BOOL']:
                            raise Exception("Esperado tipo após ',' em declaração múltipla")
                        continue
                    elif Parser.current_token.value == ';':
                        Parser.advance()
                        break
                    else:
                        raise Exception("Esperado ',', 'RECEBE' ou ';' após declaração")
                if len(declarations) == 1:
                    return declarations[0]
                else:
                    return BlockNode(declarations)
            elif Parser.current_token.value == 'RETORNA':
                Parser.advance()
                expr = Parser.parse_expression()
                if Parser.current_token.value != ';':
                    raise Exception("Esperado ';' após expressão")
                Parser.advance()
                return ReturnNode(expr)
            else:
                raise Exception(f"Comando desconhecido: {Parser.current_token.value}")
        elif Parser.current_token.type == 'IDENTIFIER':
            var_name = Parser.current_token.value
            Parser.advance()
            if Parser.current_token.value == 'RECEBE':
                Parser.advance()
                expr = Parser.parse_expression()
                if Parser.current_token.value != ';':
                    raise Exception("Esperado ';' após expressão")
                Parser.advance()
                return AssignmentNode(var_name, expr)
            elif Parser.current_token.value == '(':
                # Chamada de função
                Parser.advance()
                args = []
                if Parser.current_token.value != ')':
                    while True:
                        arg_expr = Parser.parse_expression()
                        args.append(arg_expr)
                        if Parser.current_token.value == ',':
                            Parser.advance()
                        else:
                            break
                if Parser.current_token.value != ')':
                    raise Exception("Esperado ')' após argumentos")
                Parser.advance()
                if Parser.current_token.value != ';':
                    raise Exception("Esperado ';' após chamada de função")
                Parser.advance()
                return FuncCallNode(var_name, args)
            else:
                raise Exception(f"Comando desconhecido após identificador: {Parser.current_token.value}")
        else:
            raise Exception(f"Comando inválido: {Parser.current_token}")

    @staticmethod
    def parse_block():
        if Parser.current_token.value != '{':
            raise Exception("Esperado '{' para iniciar o bloco")
        Parser.advance()
        statements = []
        while Parser.current_token.value != '}':
            statements.append(Parser.parse_command())
        Parser.advance()
        return BlockNode(statements)

    @staticmethod
    def parse_expression():
        node = Parser.parse_term()
        while Parser.current_token.value in ['+', '-']:
            op = Parser.current_token.value
            Parser.advance()
            right = Parser.parse_term()
            node = BinOpNode(node, op, right)
        return node

    @staticmethod
    def parse_term():
        node = Parser.parse_factor()
        while Parser.current_token.value in ['*', '/']:
            op = Parser.current_token.value
            Parser.advance()
            right = Parser.parse_factor()
            node = BinOpNode(node, op, right)
        return node

    @staticmethod
    def parse_factor():
        if Parser.current_token.type == 'NUMBER':
            node = NumberNode(Parser.current_token.value)
            Parser.advance()
            return node
        elif Parser.current_token.type == 'STRING':
            node = StringNode(Parser.current_token.value)
            Parser.advance()
            return node
        elif Parser.current_token.type == 'IDENTIFIER':
            var_name = Parser.current_token.value
            Parser.advance()
            if Parser.current_token.value == '(':
                # Chamada de função
                Parser.advance()
                args = []
                if Parser.current_token.value != ')':
                    while True:
                        arg_expr = Parser.parse_expression()
                        args.append(arg_expr)
                        if Parser.current_token.value == ',':
                            Parser.advance()
                        else:
                            break
                if Parser.current_token.value != ')':
                    raise Exception("Esperado ')' após argumentos")
                Parser.advance()
                return FuncCallNode(var_name, args)
            else:
                return IdentifierNode(var_name)
        elif Parser.current_token.value == '(':
            Parser.advance()
            node = Parser.parse_expression()
            if Parser.current_token.value != ')':
                raise Exception("Esperado ')'")
            Parser.advance()
            return node
        elif Parser.current_token.value in ['+', '-', '!']:
            op = Parser.current_token.value
            Parser.advance()
            node = UnOpNode(op, Parser.parse_factor())
            return node
        else:
            raise Exception(f"Fator inválido: {Parser.current_token}")

    @staticmethod
    def parse_condition():
        left = Parser.parse_expression()
        if Parser.current_token.value in ['IGUAL', 'DIFERENTE', 'MAIOR', 'MENOR', 'MAIORIGUAL', 'MENORIGUAL']:
            op = Parser.current_token.value
            Parser.advance()
            right = Parser.parse_expression()
            return RelationalOpNode(left, op, right)
        else:
            raise Exception(f"Operador relacional esperado, encontrado: {Parser.current_token.value}")

    @staticmethod
    def advance():
        Parser.tokens.select_next()
        Parser.current_token = Parser.tokens.next

    @staticmethod
    def run(code):
        Parser.tokens = Tokenizer(code)
        Parser.current_token = Parser.tokens.next
        root = Parser.parse_program()
        if Parser.current_token.type != 'EOF':
            raise Exception("Código após o final do programa")
        return root
