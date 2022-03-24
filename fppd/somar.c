#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <time.h>
#include <string.h>

#define TAMANHO_VETOR 100000000
#define NUM_THREADS 100

typedef struct
{
    pthread_t threadId; // id criado pelo pthread_create
    int *vetor;
    int posicaoInicial;
    int posicaoFinal;
    double soma;
} PacoteThread;

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
    PacoteThread *pacote = (PacoteThread *)arg;
    int posicaoInicial = pacote->posicaoInicial;
    int posicaoFinal = pacote->posicaoFinal;
    int *vetor = pacote->vetor;

    pacote->soma = 0;
    for (int j = posicaoInicial; j < posicaoFinal; j++)
    {
        pacote->soma = pacote->soma + vetor[j];
    }
    // printf("\nThread %d - %d\n", posicaoInicial, posicaoFinal);
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
    PacoteThread *pacoteThread;
    int i;
    double soma;
    clock_t t;

    t = clock(); // armazena tempo inicial

    pacoteThread = malloc(sizeof(PacoteThread) * NUM_THREADS);

    int tamanhoVetorDividido = TAMANHO_VETOR / NUM_THREADS;
    int posicaoInicial = 0;
    int posicaoFinal;
    // populando o pacote de threads
    for (i = 0; i < NUM_THREADS; i++)
    {
        posicaoFinal = posicaoInicial + tamanhoVetorDividido;

        (pacoteThread + i)->posicaoInicial = posicaoInicial;
        (pacoteThread + i)->posicaoFinal = posicaoFinal;
        (pacoteThread + i)->vetor = vetor;

        posicaoInicial = posicaoFinal;
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
        soma = soma + (pacoteThread + i)->soma;
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

// int main()
// {
//     PacoteThread *structThread;
//     int *vetor;

//     vetor = criarVetor();
//     // somaSimples(vetor);

//     pthread_t threads[NUM_THREADS];
//     int rc, t;

//     int tamanhoVetorDividido = TAMANHO_VETOR / NUM_THREADS;
//     int posicaoAtual = 0;
//     int posicaoFinal;

//     for (t = 0; t < NUM_THREADS; t++)
//     {
//         posicaoFinal = posicaoAtual + tamanhoVetorDividido;
//         printf("\nThread %d - %d\n", posicaoAtual, posicaoFinal);

//         structThread = malloc(sizeof(PacoteThread));
//         structThread->vetor = vetor;
//         structThread->posicaoInicial = posicaoAtual;
//         structThread->posicaoFinal = posicaoFinal;

//         printf("\nStruct %d - %d\n", structThread->posicaoInicial, structThread->posicaoFinal);

//         // printf("Main: criando a thread %d!\n", t);
//         rc = pthread_create(&threads[t], NULL, thread, (void *)structThread);
//         if (rc)
//         {
//             printf("ERRO code is %d\n", rc);
//             exit(-1);
//         }
//         posicaoAtual = posicaoFinal;
//     }

//     // esperar todas as threads terminarem
//     for (int i = 0; i < NUM_THREADS; i++)
//     {
//         pthread_join(threads[i], NULL);
//     }

//     free(vetor);
//     return 0;
// }