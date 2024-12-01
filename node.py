# node.py
from abc import ABC, abstractmethod
from symboltable import SymbolTable

class Node(ABC):
    @abstractmethod
    def evaluate(self, symbol_table):
        pass

class NumberNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        print(f"DEBUG: Avaliando NumberNode com valor {self.value}")
        return self.value

class StringNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        print(f"DEBUG: Avaliando StringNode com valor '{self.value}'")
        return self.value

class BoolNode(Node):
    def __init__(self, value):
        self.value = value  # 1 para True, 0 para False

    def evaluate(self, symbol_table):
        print(f"DEBUG: Avaliando BoolNode com valor {self.value}")
        return self.value

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, symbol_table):
        var = symbol_table.get(self.name)
        if var is None:
            raise Exception(f"Variável '{self.name}' não definida")
        print(f"DEBUG: Avaliando IdentifierNode '{self.name}' com valor {var['value']}")
        return var['value']

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # '+', '-', '*', '/', 'AND', 'OR'
        self.right = right

    def evaluate(self, symbol_table):
        left_value = self.left.evaluate(symbol_table)
        right_value = self.right.evaluate(symbol_table)
        print(f"DEBUG: Avaliando BinOpNode: {left_value} {self.op} {right_value}")

        if self.op == '+':
            if isinstance(left_value, str) or isinstance(right_value, str):
                result = str(left_value) + str(right_value)
            else:
                result = left_value + right_value
        elif self.op == '-':
            result = left_value - right_value
        elif self.op == '*':
            result = left_value * right_value
        elif self.op == '/':
            if right_value == 0:
                raise Exception("Erro: Divisão por zero")
            result = left_value / right_value
        else:
            raise Exception(f"Operador desconhecido: {self.op}")

        print(f"DEBUG: Resultado de BinOpNode: {result}")
        return result

class UnOpNode(Node):
    def __init__(self, op, node):
        self.op = op  # '+', '-', '!'
        self.node = node

    def evaluate(self, symbol_table):
        value = self.node.evaluate(symbol_table)
        print(f"DEBUG: Avaliando UnOpNode: {self.op}{value}")
        if self.op == '+':
            result = +value
        elif self.op == '-':
            result = -value
        elif self.op == '!':
            result = int(not value)
        else:
            raise Exception(f"Operador unário desconhecido: {self.op}")
        print(f"DEBUG: Resultado de UnOpNode: {result}")
        return result

class AssignmentNode(Node):
    def __init__(self, var_name, expr):
        self.var_name = var_name
        self.expr = expr

    def evaluate(self, symbol_table):
        value = self.expr.evaluate(symbol_table)
        var_info = symbol_table.get(self.var_name)
        if var_info is None:
            raise Exception(f"Variável '{self.var_name}' não declarada")
        symbol_table.set(self.var_name, value, var_type=var_info['type'])
        print(f"DEBUG: Atribuição: {self.var_name} = {value}")
        return value

class VarDecNode(Node):
    def __init__(self, var_type, name, expression=None):
        self.var_type = var_type  # 'INT', 'STR', 'BOOL'
        self.name = name
        self.expression = expression

    def evaluate(self, symbol_table):
        if self.expression:
            value = self.expression.evaluate(symbol_table)
        else:
            if self.var_type == 'INT':
                value = 0
            elif self.var_type == 'STR':
                value = ''
            elif self.var_type == 'BOOL':
                value = 0
        symbol_table.set(self.name, value, self.var_type)
        print(f"DEBUG: Declaração de variável: {self.var_type} {self.name} = {value}")

class PrintNode(Node):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, symbol_table):
        value = self.expr.evaluate(symbol_table)
        print(f"DEBUG: PrintNode com valor: {value}")
        print(value)

class ReadNode(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, symbol_table):
        value = input()
        var = symbol_table.get(self.name)
        if var is None:
            raise Exception(f"Variável '{self.name}' não definida")
        var_type = var['type']
        if var_type == 'INT':
            value = int(value)
        elif var_type == 'BOOL':
            value = int(value)
        symbol_table.set(self.name, value)
        print(f"DEBUG: ReadNode: {self.name} = {value}")
        return value

class IfNode(Node):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def evaluate(self, symbol_table):
        condition_value = self.condition.evaluate(symbol_table)
        print(f"DEBUG: IfNode condição avaliada como {condition_value}")
        if condition_value:
            print(f"DEBUG: Executando bloco 'verdadeiro' do IfNode")
            return self.true_block.evaluate(symbol_table)
        elif self.false_block:
            print(f"DEBUG: Executando bloco 'falso' do IfNode")
            return self.false_block.evaluate(symbol_table)

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def evaluate(self, symbol_table):
        print(f"DEBUG: Entrando no WhileNode")
        while self.condition.evaluate(symbol_table):
            self.block.evaluate(symbol_table)
        print(f"DEBUG: Saindo do WhileNode")

class ForNode(Node):
    def __init__(self, var_name, start_expr, end_expr, step_expr, block):
        self.var_name = var_name
        self.start_expr = start_expr
        self.end_expr = end_expr
        self.step_expr = step_expr
        self.block = block

    def evaluate(self, symbol_table):
        start_value = self.start_expr.evaluate(symbol_table)
        end_value = self.end_expr.evaluate(symbol_table)
        if self.step_expr:
            step_value = self.step_expr.evaluate(symbol_table)
        else:
            step_value = 1

        symbol_table.set(self.var_name, start_value, 'INT')
        print(f"DEBUG: Iniciando ForNode com {self.var_name} = {start_value}, até {end_value}, passo {step_value}")

        if step_value > 0:
            while symbol_table.get(self.var_name)['value'] <= end_value:
                self.block.evaluate(symbol_table)
                current_value = symbol_table.get(self.var_name)['value']
                symbol_table.set(self.var_name, current_value + step_value)
                print(f"DEBUG: ForNode {self.var_name} incrementado para {current_value + step_value}")
        else:
            while symbol_table.get(self.var_name)['value'] >= end_value:
                self.block.evaluate(symbol_table)
                current_value = symbol_table.get(self.var_name)['value']
                symbol_table.set(self.var_name, current_value + step_value)
                print(f"DEBUG: ForNode {self.var_name} decrementado para {current_value + step_value}")

        print(f"DEBUG: Saindo do ForNode")

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, symbol_table):
        print(f"DEBUG: Entrando em BlockNode")
        for statement in self.statements:
            result = statement.evaluate(symbol_table)
            if isinstance(result, ReturnException):
                print(f"DEBUG: ReturnException capturada em BlockNode")
                raise result  # Re-lança a exceção para propagar até a chamada da função
        print(f"DEBUG: Saindo de BlockNode")
        return None

class RelationalOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # 'IGUAL', 'DIFERENTE', 'MAIOR', etc.
        self.right = right

    def evaluate(self, symbol_table):
        left_value = self.left.evaluate(symbol_table)
        right_value = self.right.evaluate(symbol_table)
        print(f"DEBUG: Avaliando RelationalOpNode: {left_value} {self.op} {right_value}")

        if self.op == 'IGUAL':
            result = int(left_value == right_value)
        elif self.op == 'DIFERENTE':
            result = int(left_value != right_value)
        elif self.op == 'MAIOR':
            result = int(left_value > right_value)
        elif self.op == 'MENOR':
            result = int(left_value < right_value)
        elif self.op == 'MAIORIGUAL':
            result = int(left_value >= right_value)
        elif self.op == 'MENORIGUAL':
            result = int(left_value <= right_value)
        else:
            raise Exception(f"Operador relacional desconhecido: {self.op}")

        print(f"DEBUG: Resultado de RelationalOpNode: {result}")
        return result

class FuncDecNode(Node):
    def __init__(self, func_type, func_name, params, block):
        self.func_type = func_type
        self.func_name = func_name
        self.params = params  # Lista de tuplas (tipo, nome)
        self.block = block

    def evaluate(self, symbol_table):
        param_names = [name for _, name in self.params]
        print(f"DEBUG: Definindo função '{self.func_name}' com parâmetros {param_names}")

        # Percorre até a tabela de símbolos global
        global_symbol_table = symbol_table
        while global_symbol_table.parent is not None:
            global_symbol_table = global_symbol_table.parent

        # Armazena a função na tabela de símbolos global com o tipo 'FUNCTION'
        global_symbol_table.set(self.func_name, (self.func_type, param_names, self.block, global_symbol_table), var_type='FUNCTION')

class FuncCallNode(Node):
    def __init__(self, func_name, args):
        self.func_name = func_name
        self.args = args

    def evaluate(self, symbol_table):
        print(f"DEBUG: Chamando função '{self.func_name}' com argumentos {self.args}")
        # Percorre as tabelas de símbolos para encontrar a função
        current_table = symbol_table
        func_info = None
        while current_table is not None:
            func_info = current_table.get(self.func_name)
            if func_info is not None:
                break
            current_table = current_table.parent

        if func_info is None:
            raise Exception(f"Função '{self.func_name}' não definida")

        if func_info['type'] != 'FUNCTION':
            raise Exception(f"'{self.func_name}' não é uma função")

        func_value = func_info['value']
        func_type, param_names, func_block, func_table = func_value

        if len(self.args) != len(param_names):
            raise Exception("Número incorreto de argumentos")

        # Cria uma nova tabela de símbolos para a execução da função
        local_table = SymbolTable(func_table)

        # Avalia os argumentos e atribui aos parâmetros
        for param_name, arg_expr in zip(param_names, self.args):
            arg_value = arg_expr.evaluate(symbol_table)
            local_table.set(param_name, arg_value)
            print(f"DEBUG: Parâmetro '{param_name}' da função '{self.func_name}' = {arg_value}")

        # Executa o bloco da função
        try:
            print(f"DEBUG: Executando bloco da função '{self.func_name}'")
            func_block.evaluate(local_table)
            print(f"DEBUG: Função '{self.func_name}' executada sem retorno explícito")
            return None
        except ReturnException as ret:
            print(f"DEBUG: Função '{self.func_name}' retornou valor {ret.value}")
            return ret.value

class ReturnException(Exception):
    def __init__(self, value):
        self.value = value

class ReturnNode(Node):
    def __init__(self, expr):
        self.expr = expr

    def evaluate(self, symbol_table):
        value = self.expr.evaluate(symbol_table)
        print(f"DEBUG: ReturnNode retornando valor {value}")
        raise ReturnException(value)
