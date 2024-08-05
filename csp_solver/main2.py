# Autores: Leon Goncalves e Vitoria Stavis

from enum import Enum
import sys
import copy
import dimacs_translation
import argparse
import time

class t_restricao(Enum):
    V = 0,
    I = 1
    
def revisa(rest, var, lista_vars):
    dominio = busca_var(var, lista_vars)['dominio']
    posicao_escopo = rest['indices_escopo'].index(var)

    # verifica valores que não respeitam restrição
    remover = []

    # restrições do tipo válido
    if rest['tipo_restricao'] == t_restricao.V:
        for valor in dominio:
            eh_valido = False

            for tupla in rest["tuplas"]:
                # se o valor estiver registrado na restrição, ele pode ser válido
                if valor == tupla[posicao_escopo]:
                    relacionado_invalido = False

                    # se o valor estiver relacionado a um valor que não existe no domínio de outra variável, ele é inválido
                    for posicao_outra_var, valor_outra_var in enumerate(tupla):
                        if posicao_outra_var != posicao_escopo and not (valor_outra_var in busca_var(rest['indices_escopo'][posicao_outra_var], lista_vars)['dominio']):
                            relacionado_invalido = True

                    if not relacionado_invalido:
                        eh_valido = True
                        break

            if not eh_valido:
                remover.append(valor)

    # restrições do tipo inválido
    elif rest['tipo_restricao'] == t_restricao.I:
        for valor in dominio:
            eh_valido = True
            # remove o valor do domínio se ele for relacionado a outra variável que só possui o valor restrito no domínio
            for tupla in rest["tuplas"]:
                if valor == tupla[posicao_escopo]:
                    for posicao_outra_var, valor_outra_var in enumerate(tupla):
                        if posicao_outra_var != posicao_escopo and [valor_outra_var] == busca_var(rest['indices_escopo'][posicao_outra_var], lista_vars)['dominio']:
                            eh_valido = False
                            break

        if not eh_valido:
            remover.append(valor)

    # remove valores do domínio que não estão de acordo com restrição
    for valor in remover:
        dominio.remove(valor)

    return dominio

# Coloca consistencia de arco nas restrições
def gac(num_vars: int, lista_vars: list, num_restricoes: int, lista_restricoes: list):
    stack = []

    # Empilha restrições
    for rest in lista_restricoes:
        for var in rest['indices_escopo']:
            stack.append((rest, var))

    while stack != []:

        # Revisa restrição no topo da pilha
        rest, var = stack.pop()
        novo_dom = revisa(rest, var, lista_vars)
        alteracao = False

        # Aplica revisão
        for i in lista_vars:
            if i['indice_var'] == var and i['dominio'] != novo_dom:
                i['dominio'] = novo_dom
                alteracao = True
                break

        # Adiciona restrições que podem ter sido afetadas pela revisão
        if alteracao:
            for rest2 in lista_restricoes:
                if var in rest2['indices_escopo'] and rest2 != rest:
                    for var2 in rest2['indices_escopo']:
                        if var2 != var:
                            stack.append((rest2, var2))

    return lista_vars

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
        
# Recebe: lista de variaveis
# Retorna: dados da variavel i na lista,
# tal que a variavel é a que tem o menor dominio
def busca_mrv(lista_vars: list):

    menor_dominio = float('inf')
    var_escolhida = None

    for i in range(len(lista_vars)):
        var = lista_vars[i]
        dom = len(var['dominio'])        

        if dom < menor_dominio and var['escolhida'] == 0:
            menor_dominio = dom
            var_escolhida = var
                   
    return var_escolhida

def csp_solver(num_vars: int, lista_vars: list, num_restricoes: int, lista_restricoes: list, solucao: list):
    
    # aplica consistência de arco ac-3
    lista_vars = gac(num_vars, lista_vars, num_restricoes, lista_restricoes)
  
    # obtem dados da variavel
    dados_var = busca_mrv(lista_vars)
    
    # todas as variaveis ja foram escolhidas
    if dados_var == None:
        if DEBUG:
            print(f"\nSolucao encontrada: {solucao}\n")
        return True    
    
    # pega o indice da variavel 
    indice = dados_var['indice_var']

    # lista de restricoes relevantes
    valores_validos = set(copy.deepcopy(dados_var['dominio']))

    if DEBUG:
        print(f"Valores válidos antes de remover inválidos para var {indice}: {valores_validos}")

    # remove valores invalidos do dominio
    for rest in lista_restricoes:
        # testa se a variavel esta na restricao, se sim: obtem indice correspondente dentro do escopo
        if indice in rest['indices_escopo']:

            posicao_escopo = rest['indices_escopo'].index(indice)

            # analisa outras variaveis
            outras_vars = copy.deepcopy(rest['indices_escopo'])
            outras_vars.remove(indice)         

            # tratamento quando a restrição possui apenas 1 variável
            if (outras_vars == []):
                if rest['tipo_restricao'] == t_restricao.V:
                    novos_valores = set()
                    for t in rest['tuplas']:
                        novos_valores.add(t[posicao_escopo])
                    # atualiza valores validos com interseccao para nao afetar valores antigos
                    valores_validos = valores_validos.intersection(novos_valores)
                    
                else:
                    for t in busca_rest(indice_outra_var, valor_na_solucao, rest['tuplas']):
                        if t[posicao_escopo] in valores_validos:
                            # remove valores invalidos do dominio
                            valores_validos.remove(t[posicao_escopo])
            
            # tratamento quando a restrição possui múltiplas variáveis
            else:
                # se a outra vaiavel ja esta na solucao, o valor da variavel atual eh condicional
                for outra_var in outras_vars:
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

                            if DEBUG:
                                print(f"Novos valores para var {indice} com outra var {outra_var}: {novos_valores}")

                            # atualiza valores validos com interseccao para nao afetar valores antigos   
                            valores_validos = valores_validos.intersection(novos_valores)

                        else:
                            for t in busca_rest(indice_outra_var, valor_na_solucao, rest['tuplas']):
                                if t[posicao_escopo] in valores_validos:
                                    # remove valores invalidos do dominio
                                    valores_validos.remove(t[posicao_escopo])

                    # se a outra variavel ainda nao esta na solucao, o valor da variavel atual nao esta condicionada a ela
                    else:
                        novos_valores = set()
                        for t in rest['tuplas']:
                            novos_valores.add(t[posicao_escopo])
                        # atualiza valores validos com interseccao para nao afetar valores antigos
                        valores_validos = valores_validos.intersection(novos_valores)

    # gera dominio valido
    dom_valido = list(valores_validos)

    # testa valores do dominio na solucao
    for valor in dom_valido:

        if DEBUG:
            print(f"Tentando valor {valor} para var {dados_var['nome_var']} na solução {solucao}")

        solucao.append({
            'nome_var': dados_var['nome_var'],
            'var': indice,
            'valor': valor
        })

        var = lista_vars[indice-1]
        var['escolhida'] = 1
        lista_vars[indice-1] = var

        if csp_solver(num_vars, lista_vars, num_restricoes, lista_restricoes, solucao):
            return True
        
        var['escolhida'] = 0
        solucao.pop()  

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
            'dominio': dominio,
            'escolhida': 0
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
            for j in range(0, tam_escopo):
                tupla.append(int(valores_tupla[ind_tupla+j]))
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

def le_argumentos():

    # Lida com opcoes e argumentos
    parser = argparse.ArgumentParser()

    parser.add_argument('-c', '--cnf', action='store_true',
                        help="O input eh um arquivo .dimacs ou .cnf")  
    parser.add_argument('-r', '--restricoes', action='store_true',
                        help="O input esta no formato de restricoes criado")  
    parser.add_argument('-s', '--eh_sat', action='store_true',
                        help="O output dira se eh sat ou nao")  
    parser.add_argument('-v', '--valores', action='store_true',
                        help="O output sera os valores encontrados para as variaveis")  
    parser.add_argument('-d', '--debug', action='store_true',
                    help="Coloca prints de debug")  
    parser.add_argument('filename')  

    args = parser.parse_args()

    # Prints para debugar
    global DEBUG
    DEBUG = args.debug

    # Checa entrada
    arquivo_entrada = args.filename

    # Se ha duas flags de entrada
    if args.restricoes and args.cnf:
        print("Erro: Inclua somente uma flag de entrada, -c ou -r", file=sys.stderr)
        sys.exit(1)
    # Se ha duas flags de saida
    elif args.valores and args.eh_sat:
        print("Erro: Inclua somente uma flag de saida, -s ou -v", file=sys.stderr)
        sys.exit(1)
    # Se nao ha flag de saida
    elif not args.valores and not args.eh_sat:
        print("Erro: Inclua uma flag de saida, -s ou -v", file=sys.stderr)
        sys.exit(1)
    # Se nao ha flag de entrada
    elif not args.restricoes and not args.cnf:
        print("Erro: Inclua uma flag de entrada, -c ou -r", file=sys.stderr)
        sys.exit(1)
    # Se arquivo for .DIMACS ou .cnf
    elif args.cnf:
        nome_arquivo = arquivo_entrada.split(".")

        if nome_arquivo[-1] == 'dimacs' or nome_arquivo[-1] == 'cnf':
            # Converte para o formato de restricoes
            saida_traducao = 'tmp.out'
            dimacs_translation.traduz_dimacs(arquivo_entrada, saida_traducao)

            # Faz a leitura das variaveis e restricoes
            n_vars, vars, n_rest, rest = le_entrada(saida_traducao)
        
        else:
            print("Erro: a flag -c deve vir com um arquivo .cnf ou .DIMACS", file=sys.stderr)
            sys.exit(1)

    # Se o arquivo for restricoes, faz a leitura
    elif args.restricoes:
        nome_arquivo = arquivo_entrada.split(".")

        # if nome_arquivo[-1] == 'txt':
            # Faz a leitura das variaveis e restricoes
        n_vars, vars, n_rest, rest = le_entrada(arquivo_entrada)
        # else:
        #     print("Erro: a flag -r deve vir com um arquivo .txt", file=sys.stderr)
        #     sys.exit(1)

    if DEBUG:
        print(f"Variaveis:")
        for i in range(len(vars)):
            print(vars[i])            
        
        print(f"\nRestricoes:")
        for i in range(len(rest)):
            print(rest[i])

        print(f"\n")

    return (n_vars, vars, n_rest, rest, args)

if __name__ == "__main__":

    n_vars, vars, n_rest, rest, args = le_argumentos()
    
    # Roda o solver    
    solucao = []

    start = time.time()

    # Se achou solucao
    if csp_solver(n_vars, vars, n_rest, rest, solucao):
        # Se a saida for os valores das variaveis
        if args.valores:
            for i in solucao:
                print(i['nome_var'] + " = " + str(i['valor']))   
                # print('\n')   
        # Se a saida for sat ou nao sat
        elif args.eh_sat:
            with open("tmp.out", 'w') as file:
                file.write("SAT")  
        else:
            print("Erro: escreva -v ou -s para a saida", file=sys.stderr)
            sys.exit(1)
    # Se nao achou solucao
    else:
        # Se a saida for os valores das variaveis
        if args.valores:           
            print("INVALIDO")
        # Se a saida for sat ou nao sat    
        elif args.eh_sat:
            with open("tmp.out", 'w') as file:
                file.write("UNSAT")
        else:
            print("Erro: escreva -v ou -s para a saida", file=sys.stderr)
            sys.exit(1)

    end = time.time()
    total = round(end-start, 5)
    print(f'tempo de execucao: {total}')