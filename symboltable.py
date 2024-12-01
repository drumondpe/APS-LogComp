# symboltable.py
class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent  # Referência à tabela pai

    def get(self, name):
        if name in self.table:
            return self.table[name]
        elif self.parent:
            return self.parent.get(name)
        else:
            raise Exception(f"Variável '{name}' não definida")

    def set(self, name, value, var_type=None):
        if var_type:
            self.table[name] = {'value': value, 'type': var_type}
        else:
            if name in self.table:
                self.table[name]['value'] = value
            else:
                raise Exception(f"Variável '{name}' não declarada")
