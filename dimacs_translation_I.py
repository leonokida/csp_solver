import sys

# Le a entrada
def parse_dimacs(dimacs_file):
    with open(dimacs_file, 'r') as file:
        lines = file.readlines()
    
    variables = set()
    clauses = []
    
    for line in lines:
        if line.startswith('c'):
            continue
        elif line.startswith('p'):
            _, _, num_vars, num_clauses = line.split()
            num_vars, num_clauses = int(num_vars), int(num_clauses)
        else:
            clause = list(map(int, line.strip().split()))
            if clause[-1] == 0:
                clause = clause[:-1]
            clauses.append(clause)
            variables.update(abs(var) for var in clause)
    
    return num_vars, num_clauses, sorted(list(variables)), clauses

# Gera o dominio
def generate_domain(variables):
    domain = {var: set() for var in variables}
    for var in variables:
        domain[var].update([0, 1])  # Assuming binary domain (0, 1) for SAT problems
    return domain

# Traduz DIMACS para o formato requisitado
def dimacs_to_custom_format(dimacs_file, output_file):
    num_vars, num_clauses, variables, clauses = parse_dimacs(dimacs_file)
    domain = generate_domain(variables)
    
    with open(output_file, 'w') as file:
        file.write(f"{num_vars}\n")
        
        # Escreve variaveis
        for var in variables:
            domain_values = ' '.join(map(str, sorted(domain[var])))
            file.write(f"{len(domain[var])} {domain_values}\n")
            
        file.write(f"{num_clauses}\n")
        
        # Escreve restricoes
        for clause in clauses:
            file.write("V\n")
            file.write(f"{len(clause)} {' '.join(map(str, map(abs, clause)))}\n")
            valid_tuples = [bin(i)[2:].zfill(len(clause)) for i in range(2 ** len(clause)) if any((literal > 0 and (i >> (len(clause) - j - 1)) & 1 == 1) or (literal < 0 and (i >> (len(clause) - j - 1)) & 1 == 0) for j, literal in enumerate(clause))]
            valid_tuples = [' '.join(t) for t in valid_tuples]
            file.write(f"{len(valid_tuples)} {' '.join(valid_tuples)}\n")
            
            file.write("I\n")
            file.write(f"{len(clause)} {' '.join(map(str, map(abs, clause)))}\n")
            invalid_tuples = [bin(i)[2:].zfill(len(clause)) for i in range(2 ** len(clause)) if not any((literal > 0 and (i >> (len(clause) - j - 1)) & 1 == 1) or (literal < 0 and (i >> (len(clause) - j - 1)) & 1 == 0) for j, literal in enumerate(clause))]
            invalid_tuples = [' '.join(t) for t in invalid_tuples]
            file.write(f"{len(invalid_tuples)} {' '.join(invalid_tuples)}\n")

dimacs_file = sys.argv[1]  # Caminho para o arquivo DIMACS
output_file = sys.argv[2]  # Caminho para o arquivo de saída CNF
dimacs_to_custom_format(dimacs_file, output_file)
