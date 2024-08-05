CSP Solver
Autores: Leon Goncalves e Vitoria Stavis

Este projeto é um solucionador de problemas de satisfação de restrições,
incluindo sua aplicação no problema do mundo de Wumpus.
O projeto contém três scripts principais:

    csp_solver/main.py: O script principal que realiza a resolução dos problemas.
    csp_solver/dimacs_translation.py: Um tradutor de arquivos .cnf e .DIMACS para o
        formato de restrições especificado no enunciado.



- USO DO MAIN.PY

O main.py é o ponto de entrada para a resolução de problemas.
Ele aceita arquivos de entrada tanto no formato DIMACS
quanto no formato de restrições criado.
Além disso, permite especificar o tipo de saída desejada.

usage: main.py [-h] [-c] [-r] [-s] [-v] [-d] filename

Argumentos Posicionais

    filename: Nome do arquivo de entrada.

Flags

    -h, --help: Mostra a mensagem de ajuda.
    -c, --cnf: Indica que o input é um arquivo .dimacs ou .cnf.
    -r, --restricoes: Indica que o input está no formato de restrições criado.
    -s, --eh_sat: O output indicará se o problema é satisfatível ou não (SAT ou UNSAT).
    -v, --valores: O output será os valores encontrados para as variáveis.
    -t, --timer: Contar o tempo de execucao do solver
    -d, --debug: Coloca prints de debug

Regras de Uso

    Deve ser especificada apenas uma flag relacionada à entrada (-c ou -r).
    Deve ser especificada apenas uma flag relacionada à saída (-s ou -v).

Exemplos de Uso

Para devolver os valores do problema especificado em um arquivo no formato de restrições:

    python main.py -r -v star_wars.txt

Para devolver os valores das variáveis de um problema especificado em um arquivo DIMACS:

    python main.py -c -v exemplo.dimacs



- USO DO DIMACS_TRANSLATION.PY

O dimacs_translation.py é utilizado para converter arquivos DIMACS ou em CNF
para o formato de restrições especificado.

Sintaxe

usage: dimacs_translation.py [-h] file_in file_out

Argumentos Posicionais

    file_in: Nome do arquivo de entrada no formato .dimacs ou .cnf.
    file_out: Nome do arquivo de saída no formato de texto.

Flags

    -h, --help: Mostra a mensagem de ajuda.

Exemplo de Uso

Para converter um arquivo DIMACS para o formato de restrições:
    python dimacs_translation.py exemplo2.dimacs saida.txt



- INTEGRACAO COM WUMPUS

O main.py foi integrado como SAT_SOLVER nos arquivos bc.h e bc.c
do código do Wumpus simplificado, localizado no diretório wumpus_sat.
O uso é o mesmo da versão anterior,
desde que a estrutura de pastas não seja alterada.

O comando make é usado para compilar, e o make show, para compilar
de forma que o mapa será mostrado.
Depois, é necessário rodar o executável, colocando o mapa como entrada.

Exemplo de Uso

cd wumpus_sat
make show
./wumpus < exemplos/teste4.in




- ALTERAÇÕES 

Foram implementadas a GAC (Consistência de Arco Genealizada) e a heurística MRV (Minimum Restraining Order). Os experimentos foram rodados em triplicata, e será apresentada a média dos tempos de execução.



- RESULTADOS

> SAT

250 variáveis, 1065 clauses: 22,732s
100 variables, 449 clauses, backbone size 90: 1,814s

> N-Queens

N = 16: 92,021s
N = 24:
N = 32: mais de 2h

> Wumpus

teste7.in: 140,233s 
teste15-dificil.in: 



- ESTRUTURA DO TRABALHO

CSP_Solver/
│
├── LEIAME.txt
├── csp_solver/
│   ├── main.py
│   └── dimacs_translation.py
├── wumpus/
│   ├── bc.h
│   ├── bc.c
│   └── ...
├── nqueens/
└── sat/