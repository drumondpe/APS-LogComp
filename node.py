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
        return self.value

class StringNode(Node):
    def __init__(self, value):
        self.value = value

    def evaluate(self, symbol_table):
        return self.value

class BoolNode(Node):
    def __init__(self, value):
        self.value = value  # 1 para True, 0 para False

    def evaluate(self, symbol_table):
        return self.value

class IdentifierNode(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, symbol_table):
        var = symbol_table.get(self.name)
        return var['value']

class BinOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # '+', '-', '*', '/'
        self.right = right

    def evaluate(self, symbol_table):
        left_value = self.left.evaluate(symbol_table)
        right_value = self.right.evaluate(symbol_table)

        if self.op == '+':
            return left_value + right_value
        elif self.op == '-':
            return left_value - right_value
        elif self.op == '*':
            return left_value * right_value
        elif self.op == '/':
            if right_value == 0:
                raise Exception("Divisão por zero")
            return left_value // right_value
        else:
            raise Exception(f"Operador desconhecido: {self.op}")

class UnOpNode(Node):
    def __init__(self, op, node):
        self.op = op  # '+', '-', '!'
        self.node = node

    def evaluate(self, symbol_table):
        value = self.node.evaluate(symbol_table)
        if self.op == '+':
            return +value
        elif self.op == '-':
            return -value
        elif self.op == '!':
            return int(not value)
        else:
            raise Exception(f"Operador unário desconhecido: {self.op}")

class AssignmentNode(Node):
    def __init__(self, name, expression):
        self.name = name
        self.expression = expression

    def evaluate(self, symbol_table):
        value = self.expression.evaluate(symbol_table)
        symbol_table.set(self.name, value)
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
            value = 0 if self.var_type == 'INT' else '' if self.var_type == 'STR' else 0
        symbol_table.set(self.name, value, self.var_type)

class PrintNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, symbol_table):
        value = self.expression.evaluate(symbol_table)
        print(value)
        return value

class ReadNode(Node):
    def __init__(self, name):
        self.name = name

    def evaluate(self, symbol_table):
        value = input()
        var_type = symbol_table.get(self.name)['type']
        if var_type == 'INT':
            value = int(value)
        elif var_type == 'BOOL':
            value = int(value)
        symbol_table.set(self.name, value)
        return value

class IfNode(Node):
    def __init__(self, condition, true_block, false_block=None):
        self.condition = condition
        self.true_block = true_block
        self.false_block = false_block

    def evaluate(self, symbol_table):
        condition_value = self.condition.evaluate(symbol_table)
        if condition_value:
            return self.true_block.evaluate(symbol_table)
        elif self.false_block:
            return self.false_block.evaluate(symbol_table)

class WhileNode(Node):
    def __init__(self, condition, block):
        self.condition = condition
        self.block = block

    def evaluate(self, symbol_table):
        while self.condition.evaluate(symbol_table):
            self.block.evaluate(symbol_table)

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

        if step_value > 0:
            while symbol_table.get(self.var_name)['value'] <= end_value:
                self.block.evaluate(symbol_table)
                current_value = symbol_table.get(self.var_name)['value']
                symbol_table.set(self.var_name, current_value + step_value)
        else:
            while symbol_table.get(self.var_name)['value'] >= end_value:
                self.block.evaluate(symbol_table)
                current_value = symbol_table.get(self.var_name)['value']
                symbol_table.set(self.var_name, current_value + step_value)

class BlockNode(Node):
    def __init__(self, statements):
        self.statements = statements

    def evaluate(self, symbol_table):
        for statement in self.statements:
            result = statement.evaluate(symbol_table)
            if isinstance(result, ReturnNode):
                return result
        return result

class RelationalOpNode(Node):
    def __init__(self, left, op, right):
        self.left = left
        self.op = op  # 'IGUAL', 'DIFERENTE', 'MAIOR', etc.
        self.right = right

    def evaluate(self, symbol_table):
        left_value = self.left.evaluate(symbol_table)
        right_value = self.right.evaluate(symbol_table)

        if self.op == 'IGUAL':
            return int(left_value == right_value)
        elif self.op == 'DIFERENTE':
            return int(left_value != right_value)
        elif self.op == 'MAIOR':
            return int(left_value > right_value)
        elif self.op == 'MENOR':
            return int(left_value < right_value)
        elif self.op == 'MAIORIGUAL':
            return int(left_value >= right_value)
        elif self.op == 'MENORIGUAL':
            return int(left_value <= right_value)
        else:
            raise Exception(f"Operador relacional desconhecido: {self.op}")

class FuncDecNode(Node):
    def __init__(self, func_type, name, params, block):
        self.func_type = func_type
        self.name = name
        self.params = params  # Lista de tuplas (tipo, nome)
        self.block = block

    def evaluate(self, symbol_table):
        symbol_table.set(self.name, self, 'FUNCTION')

class FuncCallNode(Node):
    def __init__(self, name, args):
        self.name = name
        self.args = args  # Lista de expressões

    def evaluate(self, symbol_table):
        func_dec = symbol_table.get(self.name)
        if func_dec['type'] != 'FUNCTION':
            raise Exception(f"'{self.name}' não é uma função")
        func_node = func_dec['value']
        if len(self.args) != len(func_node.params):
            raise Exception(f"Quantidade de argumentos incorreta para a função '{self.name}'")
        local_table = SymbolTable(parent=symbol_table)
        for (param_type, param_name), arg_expr in zip(func_node.params, self.args):
            arg_value = arg_expr.evaluate(symbol_table)
            local_table.set(param_name, arg_value, param_type)
        result = func_node.block.evaluate(local_table)
        if isinstance(result, ReturnNode):
            return result.evaluate(local_table)
        else:
            return None

class ReturnNode(Node):
    def __init__(self, expression):
        self.expression = expression

    def evaluate(self, symbol_table):
        return self.expression.evaluate(symbol_table)
