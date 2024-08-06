# CSP Solver
Autores: Leon Goncalves e Vitoria Stavis

Este projeto é um solucionador de problemas de satisfação de restrições,
incluindo sua aplicação no problema do mundo de Wumpus.
O projeto contém três scripts principais:

    csp_solver/main.py: O script principal que realiza a resolução dos problemas.
    csp_solver/dimacs_translation.py: Um tradutor de arquivos .cnf e .DIMACS para o
        formato de restrições especificado no enunciado.



## USO DO MAIN.PY

O main.py é o ponto de entrada para a resolução de problemas.
Ele aceita arquivos de entrada tanto no formato DIMACS
quanto no formato de restrições criado.
Além disso, permite especificar o tipo de saída desejada.

usage: main.py [-h] [-s] [-v] [-t] [-d] filename

### Argumentos Posicionais

    filename: Nome do arquivo de entrada.

### Flags

    -h, --help: Mostra a mensagem de ajuda.   
    -s, --eh_sat: O output indicará se o problema é satisfatível ou não (SAT ou UNSAT).
    -v, --valores: O output será os valores encontrados para as variáveis.
    -t, --timer: Contar o tempo de execucao do solver
    -d, --debug: Coloca prints de debug

### Regras de Uso

    Deve ser especificada apenas uma flag relacionada à saída (-s ou -v).

### Exemplos de Uso

    python main.py -v star_wars.txt
    python main.py -v exemplo.dimacs

## USO DO DIMACS_TRANSLATION.PY

O dimacs_translation.py é utilizado para converter arquivos DIMACS ou em CNF
para o formato de restrições especificado.

### Sintaxe

usage: dimacs_translation.py [-h] file_in file_out

### Argumentos Posicionais

    file_in: Nome do arquivo de entrada no formato .dimacs ou .cnf.
    file_out: Nome do arquivo de saída no formato de texto.

### Flags

    -h, --help: Mostra a mensagem de ajuda.

### Exemplo de Uso

Para converter um arquivo DIMACS para o formato de restrições:
    python dimacs_translation.py exemplo2.dimacs saida.txt

## INTEGRACAO COM WUMPUS

O main.py foi integrado como SAT_SOLVER nos arquivos bc.h e bc.c
do código do Wumpus simplificado, localizado no diretório wumpus_sat.
O uso é o mesmo da versão anterior,
desde que a estrutura de pastas não seja alterada.

### Exemplo de Uso

    cd wumpus
    make 
    ./wumpus < exemplos/teste4.in

## OTIMIZAÇÃO

Foram implementadas a GAC (Consistência de Arco Genealizada) e a heurística MRV (Minimum Restraining Order). Os experimentos foram rodados em triplicata, e será apresentada a média dos tempos de execução.
Serão apresentados os valores para cada instância no Trabalho 4, seguidos do tempo no Trabalho 3.

## RESULTADOS DA OTIMIZAÇÃO

### SAT (retirados do SATLIB - Benchmark Problems)

    uf250-1065, 250 variáveis, 1065 cláusulas: 22,432s
    					   T3: 48,320s

    LRAN, Large Random-3-SAT instances: 1721,410s (28,690min)
				    T3: 2251,472s

### N-Queens

    N = 16: 92,021s (1,533min)
        T3: 6,242s

    N = 18: 724,210s (12,070min)
	T3: 11,230s

    N = 20: 5632,370s (93,872min)
	T3: 62,400s

### Wumpus

    teste7.in: 140,233s (2,337min)
	   T3: mais de 2h

    teste15.in: 932,446 (15,540min)
	    T3: mais de 3h

### Limitações

Para o problema SAT, algumas instâncias podem não dar o resultado correto.
No problema N-Queens, a velocidade aumentou com o N, diferente do esperado.

Esses dois pontos indicam uma possível falha na implementação.

Nos outros problemas, houve uma diminuição relativa dos tempos de execução.

A fim de melhorar mais a velocidade de execução, além da revisão do código,
podem ser implementadas mais otimizações. Entre elas: estruturas de dados diferentes, paralelização, utilização da memória e outras heurísticas, como LCV.

## ESTRUTURA DO TRABALHO

```
CSP_Solver/
│
├── LEIAME.txt
├── csp_solver/
│   ├── main.py
│   └── dimacs_translation.py
├── wumpus/
    ├── bc.h
    ├── bc.c
    └── ...

```
