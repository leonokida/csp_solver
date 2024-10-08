import sys
import argparse

# Le a entrada
def parse_dimacs(dimacs_file):
    with open(dimacs_file, 'r') as file:
        linhas = file.readlines()
    
    variaveis = set()
    clausulas = []
    
    for linha in linhas:
        if linha.startswith('c') or len(linha) <= 2:
            continue
        # elif len(linha) == 2:
        #     print(linha)
        elif linha.startswith('p'):
            # Pega numero de variaveis e numero de clausulas
            _, _, n_vars, n_clausulas = linha.split()
            n_vars, n_clausulas = int(n_vars), int(n_clausulas)
        else:
            clausula = list(map(int, linha.strip().split()))
            # print(clausula)
            if clausula[-1] == 0:
                # Remove 0
                clausula = clausula[:-1]

            clausulas.append(clausula)

            # Indices das variaveis
            variaveis.update(abs(var) for var in clausula)

    variaveis = sorted(list(variaveis))
    
    return n_vars, n_clausulas, variaveis, clausulas

# Gera o dominio
def gera_dominio(variaveis):
    
    dominio = {var: set() for var in variaveis}
    for var in variaveis:
        # Assume dominio binario (0, 1) para SAT
        dominio[var].update([0, 1])  

    return dominio

# Encontra todas as combinacoes binarias validas para uma clausula booleana.
def encontra_tuplas(clausula):

    n_lit = len(clausula)
    tuplas_validas = []
    combinacoes = 2**n_lit

    for i in range(combinacoes):
        # Gera representacao binaria de 'i' com zero a esquerda para preencher ate 'n_literals' bits
        binario = bin(i)[2:].zfill(n_lit)
        # print(binario)
        eh_valid = False

        # Verifica se a tupla binaria eh valida para a clausula
        for j, literal in enumerate(clausula):

            # Verifica se o literal na posicao j eh satisfeito pela representação binaria atual:
            # Para um literal positivo, o bit correspondente deve ser 1
            # Para um literal negativo, o bit correspondente deve ser 0
            if (literal > 0 and (i >> (n_lit - j - 1)) & 1 == 1) or (literal < 0 and (i >> (n_lit - j - 1)) & 1 == 0):
                eh_valid = True
                break
        
        if eh_valid:
            tuplas_validas.append(binario)

    return tuplas_validas

# Traduz DIMACS para o formato requisitado
def traduz_dimacs(dimacs_file, output_file):

    n_vars, n_clausulas, variaveis, clausulas = parse_dimacs(dimacs_file)
    dominio = gera_dominio(variaveis)
    
    with open(output_file, 'w') as file:
        file.write(f"{n_vars}\n")
        
        # Escreve variaveis
        for var in variaveis:
            dominio_valores = ' '.join(map(str, sorted(dominio[var])))
            file.write(f"{len(dominio[var])} {dominio_valores}\n")
            
        # Escreve numero de restricoes
        file.write(f"{n_clausulas}\n")
        
        # Escreve restricoes
        for clausula in clausulas:

            # Indica que a restricao eh valida
            file.write("V\n")

            # Escreve o numero de literais e os literais
            file.write(f"{len(clausula)} {' '.join(map(str, map(abs, clausula)))}\n")

            # Encontra tuplas validas
            tuplas_validas = encontra_tuplas(clausula)
            tuplas_validas = [' '.join(t) for t in tuplas_validas]
            # Escreve tuplas validas
            file.write(f"{len(tuplas_validas)} {' '.join(tuplas_validas)}\n")

if __name__ == "__main__":

    # Lida com opcoes e argumentos
    parser = argparse.ArgumentParser()

    parser.add_argument('file_in', help="O input eh um arquivo .dimacs ou .cnf")  
    parser.add_argument('file_out', help="O output eh um arquivo de texto") 

    args = parser.parse_args()

    # Se arquivo for .DIMACS ou .cnf
    if args.file_in and args.file_out:
        arquivo_entrada = args.file_in
        nome_arquivo = arquivo_entrada.split(".")
        saida_traducao = args.file_out

        if nome_arquivo[-1] == 'dimacs' or nome_arquivo[-1] == 'cnf':
            # Converte para o formato de restricoes
            traduz_dimacs(arquivo_entrada, saida_traducao)
        
        else:
            print("Erro: a entrada eh um arquivo .cnf ou .DIMACS", file=sys.stderr)
            sys.exit(1)

 