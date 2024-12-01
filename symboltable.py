# symboltable.py
class SymbolTable:
    def __init__(self, parent=None):
        self.table = {}
        self.parent = parent

    def set(self, name, value, var_type=None):
        self.table[name] = {'value': value, 'type': var_type}

    def get(self, name):
        if name in self.table:
            return self.table[name]
        elif self.parent is not None:
            return self.parent.get(name)
        else:
            return None
