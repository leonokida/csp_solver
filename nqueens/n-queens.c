#include <stdio.h>
#include <stdlib.h>
#include <string.h>

int MAX = 2000;

int *alocaVetor() {
	int *vetor = (int *) malloc(sizeof(int)*MAX);
	return vetor;
}

void realocaVetor(int *vetor, int n) {
	if (n == MAX) {
		MAX *= 2;
		vetor = (int *) realloc(vetor, sizeof(int)*MAX);
	}
}

void liberaVetor(int *vetor) {
	free(vetor);
}

int main(int argc, char **argv) {

	if (argc != 2) {
		printf("uso: %s <n>\n", argv[0]);
		exit(1);
	}

	int n = atoi(argv[1]);

	// quantidade de variaveis
	printf("%d\n", n);

	// tamanho do dominio (n) e valores (1...n) de cada variavel
	for (int i = 0; i < n; ++i) {
		printf("%d ", n);
		for (int j = 1; j < n; ++j)
			printf("%d ", j);
		printf("%d\n", n);
	}

	// quantidade de restricoes
	printf("%d\n", n*(n-1)/2);

	int *tuplas = alocaVetor();

	// cada variável tem restrição com todas as variáveis sucessoras
	for (int i = 1; i <= n; ++i)
		for (int j = i+1; j <= n; ++j) {

			// tipo da restricao
			printf("V\n");

			// escopo da restricao
			printf("2 %d %d\n", i, j);

			// calcular as tuplas
			int cont = 0;
			int dist = abs(i-j);
			for (int k = 1; k <= n; ++k)
				for (int l = 1; l <= n; ++l)
					if (abs(k-l) && abs(k-l) != dist) {
						tuplas[cont++] = k;
						tuplas[cont++] = l;
						realocaVetor(tuplas, cont);
					}

			// imprimir as tuplas
			printf("%d ", cont/2);
			for (int k = 0; k < cont-1; ++k)
				printf("%d ", tuplas[k]);
			printf("%d\n", tuplas[cont-1]);
		}
	liberaVetor(tuplas);
}
