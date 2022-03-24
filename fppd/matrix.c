#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#define TAMANHO_VETOR 100000000
#define NUM_COLUNAS 3
#define NUM_LINHAS 3
#define NUM_THREADS 7

typedef struct
{
    pthread_t threadId; // id criado pelo pthread_create
    int **matrix1;
    int **matrix2;
    int **resultado;
    int linhaInicial;
    int linhaFinal;
} PacoteThread;

void printMatrix(int **matrix)
{
    printf("\n --- Matrix ---\n\n");
    for (int x = 0; x < NUM_LINHAS; x++)
    {
        for (int y = 0; y < NUM_COLUNAS; y++)
        {
            printf("%5d", matrix[x][y]);
        }
        printf("\n\n");
    }
}

int **alocarMatrix()
{
    int **matrix;
    matrix = (int **)malloc(NUM_LINHAS * sizeof(int *));
    for (int j = 0; j < NUM_COLUNAS; j++)
    {
        matrix[j] = (int *)malloc(NUM_COLUNAS * sizeof(int));
    }

    return matrix;
}

int **criarMatrix()
{
    int **matrix;
    matrix = alocarMatrix();

    for (int i = 0; i < NUM_LINHAS; i++)
    {
        for (int j = 0; j < NUM_COLUNAS; j++)
        {
            matrix[i][j] = i + j + 1;
        }
    }
    printMatrix(matrix);

    return matrix;
}

void *thread(void *arg)
{
    PacoteThread *pacote = (PacoteThread *)arg;
    int linhaInicial = pacote->linhaInicial;
    int linhaFinal = pacote->linhaFinal;
    int **matrix1 = pacote->matrix1;
    int **matrix2 = pacote->matrix2;
    int **resultado = pacote->resultado;
    int aux = 0;

    // printf("\nThread %d - %d\n", linhaInicial, linhaFinal);

    for (int i = linhaInicial; i < linhaFinal; i++)
    {
        for (int j = 0; j < NUM_COLUNAS; j++)
        {

            resultado[i][j] = 0;
            for (int x = 0; x < NUM_COLUNAS; x++)
            {
                aux += matrix1[i][x] * matrix2[x][j];
            }

            resultado[i][j] = aux;
            aux = 0;
        }
    }
    return 0;
}

int multiplicar(int **matrix1, int **matrix2)
{
    PacoteThread *pacoteThread;
    int **resultado;
    resultado = alocarMatrix();
    int i;
    clock_t t;

    t = clock(); // armazena tempo inicial

    pacoteThread = malloc(sizeof(PacoteThread) * NUM_THREADS);

    int quantidadeThreads = NUM_THREADS;
    int linhasPorThread = NUM_LINHAS / NUM_THREADS;
    if (linhasPorThread == 0)
    {
        linhasPorThread = 1;
        quantidadeThreads = NUM_LINHAS;
    }

    int linhaInicial = 0;
    int linhaFinal;
    // populando o pacote de threads
    for (i = 0; i < quantidadeThreads; i++)
    {
        linhaFinal = linhaInicial + linhasPorThread;

        (pacoteThread + i)->linhaInicial = linhaInicial;
        (pacoteThread + i)->linhaFinal = linhaFinal;
        (pacoteThread + i)->matrix1 = matrix1;
        (pacoteThread + i)->matrix2 = matrix2;
        (pacoteThread + i)->resultado = resultado;

        linhaInicial = linhaFinal;
    }

    // criando as threads
    for (i = 0; i < NUM_THREADS; i++)
    {
        // printf("\nPosicao %d - %d\n", (pacoteThread + i)->posicaoInicial, (pacoteThread + i)->posicaoFinal);
        pthread_create(&((pacoteThread + i)->threadId), NULL, thread, (void *)(pacoteThread + i));
    }

    // esperar todas as threads terminarem
    for (i = 0; i < NUM_THREADS; i++)
    {
        pthread_join((pacoteThread + i)->threadId, NULL);
    }
    printMatrix(resultado);
    t = clock() - t; // tempo final - tempo inicial

    // printf("\nSoma da Thread: %lf\n", soma);
    printf("Tempo de Execução Threads: %lf\n", ((double)t));
    free(pacoteThread);

    return 0;
}

int main()
{
    int **matrix1;
    int **matrix2;

    matrix1 = criarMatrix();
    matrix2 = criarMatrix();
    multiplicar(matrix1, matrix2);

    free(matrix1);
    free(matrix2);
    return 0;
}