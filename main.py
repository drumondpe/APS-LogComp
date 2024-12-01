# main.py
from parser import Parser
from prepro import PrePro
from symboltable import SymbolTable
import sys

def main():
    if len(sys.argv) != 2:
        sys.stderr.write("Uso: python main.py 'caminho_para_o_arquivo.txt'\n")
        return

    file_path = sys.argv[1]
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            code = file.read()

        # Pré-processamento
        filtered_code = PrePro.filter(code)

        # Parsing
        ast = Parser.run(filtered_code)

        # Execução
        symbol_table = SymbolTable()
        ast.evaluate(symbol_table)

    except FileNotFoundError:
        sys.stderr.write("Erro: Arquivo não encontrado\n")
    except Exception as e:
        sys.stderr.write(f"Erro: {e}\n")

if __name__ == "__main__":
    main()
