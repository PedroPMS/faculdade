#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>
#include <unistd.h>

#define NUM_THREADS 8

typedef struct pacoteThread *PacoteThread;

struct pacoteThread
{
    pthread_t threadId; // id criado pelo pthread_create
    pthread_mutex_t *lock;
    int indiceThread;
    int *vetorNumAleatorios;
    double *saldo;
};

int randomNumber()
{
    return -100 + rand() / (RAND_MAX / (100 - (-100) + 1) + 1);
}

void *thread(void *arg)
{
    PacoteThread pacote = (PacoteThread)arg;
    double *saldo = pacote->saldo;
    int *vetorNumAleatorios = pacote->vetorNumAleatorios;
    int indiceThread = pacote->indiceThread;

    srand((int)time(NULL) ^ *((int *)pacote->threadId));
    int numeroAleatorio = randomNumber();

    pthread_mutex_lock(pacote->lock);
    *saldo = *saldo + numeroAleatorio;
    pthread_mutex_unlock(pacote->lock);

    vetorNumAleatorios[indiceThread] = numeroAleatorio;

    return 0;
}

int main()
{
    PacoteThread pacoteThread;
    pthread_mutex_t lock;
    int i;
    double saldo = 0;
    int *vetorNumAleatorios;

    vetorNumAleatorios = (int *)malloc(NUM_THREADS * sizeof(int));
    pacoteThread = (PacoteThread)malloc(sizeof(struct pacoteThread) * NUM_THREADS);
    pthread_mutex_init(&lock, NULL);

    srand(time(NULL));
    // criando as threads
    for (i = 0; i < NUM_THREADS; i++)
    {
        (pacoteThread + i)->saldo = &saldo;
        (pacoteThread + i)->indiceThread = i;
        (pacoteThread + i)->vetorNumAleatorios = vetorNumAleatorios;
        (pacoteThread + i)->lock = &lock;
        // printf("\nPosicao %d\n", (pacoteThread + i)->qtdSomas);
        pthread_create(&((pacoteThread + i)->threadId), NULL, thread, (void *)(pacoteThread + i));
    }

    // esperar todas as threads terminarem
    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join((pacoteThread + i)->threadId, NULL);
    }
    free(pacoteThread);

    int saldoVetor = 0;
    for (int i = 0; i < NUM_THREADS; i++)
    {
        saldoVetor = saldoVetor + vetorNumAleatorios[i];
        printf("\nValor %d\n", vetorNumAleatorios[i]);
    }
    printf("\nSaldo Thread %f\n", saldo);
    printf("\nSaldo Vetor %f\n", saldo);

    return 0;
}