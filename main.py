# Autores: Leon Goncalves e Vitoria Stavis

from enum import Enum
import sys
import copy
import dimacs_translation
import argparse

class t_restricao(Enum):
    V = 0,
    I = 1

# Recebe: indice de uma variavel e solucao parcial
# Retorna: boolean dizendo se a variavel esta na solucao parcial
def esta_na_solucao(var, solucao):
    for elem in solucao:
        if elem['var'] == var:
            return True
    return False

# Recebe: indice de uma variavel e solucao parcial
# Retorna: valor da variavel na solucao parcial
def obtem_valor_na_solucao(var, solucao):
    for elem in solucao:
        if elem['var'] == var:
            return elem['valor']
        
# Recebe: indice e valor de uma variavel, lista de restricoes
# Retorna: lista de restricoes que possuem a variavel com o valor especificado
def busca_rest(indice, valor, lista):
    retorno_lista = []
    for i in lista:
        if i[indice] == valor:
            retorno_lista.append(i)
    return retorno_lista

# Recebe: indice i da variavel sendo buscada e lista de variaveis
# Retorna: dados da variavel i na lista
def busca_var(indice: int, lista_vars: list):
    for var in lista_vars:
        if var['indice_var'] == indice:
            return var

# Recebe: indice da variavel que tem valor atribuido, numero e lista de variaveis, numero e lista de restricoes, lista para armazenar solucao
# Retorna: se csp eh ou nao valido
def csp_solver(indice: int, num_vars: int, lista_vars: list, num_restricoes: int, lista_restricoes: list, solucao: list):
    # retorna se solucao eh valida
    if indice == num_vars + 1:
        return True
    
    # obtem dominio da variavel
    dados_var = busca_var(indice, lista_vars)

    # lista de restricoes relevantes
    valores_validos = set(copy.deepcopy(dados_var['dominio']))

    # remove valores invalidos do dominio
    for rest in lista_restricoes:
        # testa se a variavel esta na restricao, se sim: obtem indice correspondente dentro do escopo
        if indice in rest['indices_escopo']:
            posicao_escopo = rest['indices_escopo'].index(indice)
            # analisa outras variaveis
            outras_vars = copy.deepcopy(rest['indices_escopo'])
            outras_vars.remove(indice)

            for outra_var in outras_vars:
                # se a outra variavel ja esta na solucao, o valor da variavel atual eh condicional
                # obtem valor e indice na tupla da outra variavel
                valor_na_solucao = obtem_valor_na_solucao(outra_var, solucao)
                indice_outra_var = rest['indices_escopo'].index(outra_var)

                if esta_na_solucao(outra_var, solucao):
                    if rest['tipo_restricao'] == t_restricao.V:
                        # conjunto de valores a serem inseridos no dominio valido
                        novos_valores = set()
                        # busca restricoes que possuem a outra variavel com o valor atual
                        for t in busca_rest(indice_outra_var, valor_na_solucao, rest['tuplas']):
                            # se for restricao valida, adiciona aos novos valores                            
                            novos_valores.add(t[posicao_escopo])

                        # atualiza valores validos com interseccao para nao afetar valores antigos   
                        valores_validos = valores_validos.intersection(novos_valores)

                    else:
                        for t in busca_rest(indice_outra_var, valor_na_solucao, rest['tuplas']):
                            if t[posicao_escopo] in valores_validos:
                                # remove valores invalidos do dominio
                                valores_validos.remove(t[posicao_escopo])

                # se a outra variavel ainda nao esta na solucao, o valor da variavel atual nao esta condicionada a ela
                else:
                    novos_valores = copy.deepcopy(valores_validos)
                    for t in rest['tuplas']:
                        novos_valores.add(t[posicao_escopo])
                    # atualiza valores validos com interseccao para nao afetar valores antigos
                    valores_validos = valores_validos.intersection(novos_valores)

    # gera dominio valido
    dom_valido = list(valores_validos)

    # testa valores do dominio na solucao
    for valor in dom_valido:
        solucao.append({
            'nome_var': dados_var['nome_var'],
            'var': indice,
            'valor': valor
        })
        if csp_solver(indice + 1, num_vars, lista_vars, num_restricoes, lista_restricoes, solucao):
            return True
        solucao.remove({
            'nome_var': dados_var['nome_var'],
            'var': indice,
            'valor': valor
        })

    # nao possui solucao valida
    return False

# Recebe: nome do arquivo com entrada
# Retorna: variaveis com dominio e restricoes
def le_entrada(nome_arq: str):
    arq = open(nome_arq, "r")

    # obtem numero de variaveis
    linha = arq.readline()
    num_vars = int(linha)

    # obtem tamanho do dominio e valores
    lista_vars = list()
    for i in range(1, num_vars+1):
        # gera nome da variavel
        nome_var = 'x' + str(i)

        # divide a linha
        linha = arq.readline()
        valores_var = linha.split(' ')

        # obtem tamanho do dominio
        tam_dominio_var = int(valores_var[0])

        # le valores do dominio
        dominio = list()
        for valor in range(1, len(valores_var)):
            dominio.append(int(valores_var[valor]))

        # adiciona valores na lista de variaveis    
        lista_vars.append({
            'indice_var': i,
            'nome_var': nome_var,
            'tam_dominio': tam_dominio_var,
            'dominio': dominio
        })
    
    # obtem numero de restricoes
    linha = arq.readline()
    num_restricoes = int(linha)
    
    # obtem tipo, tamanho e indice das variaveis do escopo, quantidade de tuplas e tuplas da restrição
    lista_restricoes = list()
    for i in range(1, num_restricoes+1):
        # gera nome da restricao
        nome_restricao = 'R' + str(i)

        # obtem tipo da restricao
        linha = arq.readline()
        tipo_restricao = t_restricao.V if linha[0] == 'V' else t_restricao.I

        # obtem tamanho e indices das variaveis do escopo
        linha = arq.readline()
        valores_escopo = linha.split(' ')

        indices_escopo = list()
        tam_escopo = int(valores_escopo[0])
        for indice in range(1, len(valores_escopo)):
            indices_escopo.append(int(valores_escopo[indice]))

        # obtem quantidade de tuplas e tuplas
        linha = arq.readline()
        valores_tupla = linha.split(' ')
        num_tuplas = int(valores_tupla[0])
        tuplas = list()
        for ind_tupla in range(1, len(valores_tupla), tam_escopo):
            tupla = list()
            for i in range(0, tam_escopo):
                tupla.append(int(valores_tupla[ind_tupla+i]))
            tuplas.append(tupla)
        
        # adiciona na lista de restricoes
        lista_restricoes.append({
            'indice_restricao': i,
            'nome_restricao': nome_restricao,
            'tipo_restricao': tipo_restricao,
            'tam_escopo': tam_escopo,
            'indices_escopo': indices_escopo,
            'num_tuplas': num_tuplas,
            'tuplas': tuplas
        })

    return (num_vars, lista_vars, num_restricoes, lista_restricoes)

if __name__ == "__main__":

    # Lida com opcoes e argumentos
    parser = argparse.ArgumentParser()

    parser.add_argument('-d', '--dimacs', action='store_true',
                        help="O input eh um arquivo .dimacs")  
    parser.add_argument('-r', '--restricoes', action='store_true',
                        help="O input esta no formato de restricoes criado")  
    parser.add_argument('-s', '--eh_sat', action='store_true',
                        help="O output dira se eh sat ou nao")  
    parser.add_argument('-v', '--valores', action='store_true',
                        help="O output sera os valores encontrados para as variaveis")  
    parser.add_argument('filename')  

    args = parser.parse_args()

    # Checa entrada
    arquivo_entrada = args.filename

    # Se arquivo for .DIMACS
    if args.dimacs:
        nome_arquivo = arquivo_entrada.split(".")

        if nome_arquivo[-1] == 'dimacs':
            # Converte para o formato de restricoes
            saida_txt = f'{nome_arquivo[0]}.txt'
            dimacs_translation.traduz_dimacs(arquivo_entrada, saida_txt)

            # Faz a leitura das restricoes
            n_vars, vars, n_rest, rest = le_entrada(saida_txt)
        
        else:
            print("Erro: a flag -d deve vir com um arquivo .DIMACS", file=sys.stderr)
            sys.exit(1)

    # Se o arquivo for restricoes .txt, faz a leitura
    elif args.restricoes:
        nome_arquivo = arquivo_entrada.split(".")

        if nome_arquivo[-1] == 'txt':
            n_vars, vars, n_rest, rest = le_entrada(arquivo_entrada)
        else:
            print("Erro: a flag -r deve vir com um arquivo .txt", file=sys.stderr)
            sys.exit(1)

    # Checa a saida
    solucao = []
    if csp_solver(1, n_vars, vars, n_rest, rest, solucao):
        if args.valores:
            for i in solucao:
                print(i['nome_var'] + " = " + str(i['valor']))      
        elif args.eh_sat:
            with open("tmp.out", 'w') as file:
                file.write("NAO_SAT")  
        else:
            print("Erro: escreva -v ou -s para a saida", file=sys.stderr)
            sys.exit(1)
    else:
        if args.valores:           
            print("INVALIDO")
        elif args.eh_sat:
            with open("tmp.out", 'w') as file:
                file.write("SAT")
        else:
            print("Erro: escreva -v ou -s para a saida", file=sys.stderr)
            sys.exit(1)