#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#define TAMANHO_VETOR 100000
#define NUM_THREADS 2

typedef struct pacoteThread *PacoteThread;

struct pacoteThread
{
    pthread_t threadId; // id criado pelo pthread_create
    pthread_mutex_t *lock;
    int *vetor;
    double *globalIndex;
    double *soma;
};

int *criarVetor()
{
    int *vetor;

    vetor = (int *)malloc(TAMANHO_VETOR * sizeof(int));
    for (int i = 0; i < TAMANHO_VETOR; i++)
    {
        vetor[i] = i + 1;
    }

    return vetor;
}

void *thread(void *arg)
{
    double localSum = 0;
    int localIndex;

    PacoteThread pacote = (PacoteThread)arg;
    double *soma = pacote->soma;
    double *globalIndex = pacote->globalIndex;
    int *vetor = pacote->vetor;

    do
    {
        pthread_mutex_lock(pacote->lock);
        localIndex = *globalIndex;
        *globalIndex = localIndex + 1;
        pthread_mutex_unlock(pacote->lock);

        if (localIndex < TAMANHO_VETOR)
        {
            localSum += vetor[localIndex];
        }

    } while (localIndex < TAMANHO_VETOR);

    pthread_mutex_lock(pacote->lock);
    *soma = *soma + localSum;
    pthread_mutex_unlock(pacote->lock);
    return 0;
}

int somaSimples(int *vetor)
{
    clock_t t;

    t = clock(); // armazena tempo inicial
    double acumuladorSemThreads = 0;
    for (int j = 0; j < TAMANHO_VETOR; j++)
    {
        acumuladorSemThreads = acumuladorSemThreads + vetor[j];
    }
    t = clock() - t; // tempo final - tempo inicial

    printf("\nTempo de Execução Simples: %lf\n", ((double)t));
    printf("Soma do vetor: %lf\n", acumuladorSemThreads);

    return 0;
}

int somaThreads(int *vetor)
{
    PacoteThread pacoteThread;
    pthread_mutex_t lock;
    int i;
    double soma = 0;
    double globalIndex = 0;
    clock_t t;

    pacoteThread = (PacoteThread)malloc(sizeof(struct pacoteThread) * NUM_THREADS);
    pthread_mutex_init(&lock, NULL);

    // criando as threads
    for (i = 0; i < NUM_THREADS; i++)
    {
        (pacoteThread + i)->globalIndex = &globalIndex;
        (pacoteThread + i)->soma = &soma;
        (pacoteThread + i)->vetor = vetor;
        (pacoteThread + i)->lock = &lock;
        // printf("\nPosicao %d - %d\n", (pacoteThread + i)->posicaoInicial, (pacoteThread + i)->posicaoFinal);
        pthread_create(&((pacoteThread + i)->threadId), NULL, thread, (void *)(pacoteThread + i));
    }

    t = clock(); // armazena tempo inicial
    // esperar todas as threads terminarem
    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join((pacoteThread + i)->threadId, NULL);
    }
    t = clock() - t; // tempo final - tempo inicial

    printf("\nSoma Thread: %lf\n", soma);
    printf("Tempo de Execução Threads: %lf\n", ((double)t));
    free(pacoteThread);

    return 0;
}

int main()
{
    int *vetor;

    vetor = criarVetor();
    somaSimples(vetor);
    somaThreads(vetor);

    free(vetor);
    return 0;
}