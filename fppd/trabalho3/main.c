#include <pthread.h>
#include <semaphore.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

typedef struct
{
    int numCanibaisCozinheiros;
    int minimo;
    int porcaoInicial;
    int numPorcoes;
    sem_t semaforoNumPorcoes;
    sem_t semaforoCozinheiro;
    sem_t semaforoCanibal;
    sem_t semaforoFinalizador;
} Travessa;

typedef struct
{
    int id;
    int servido;
    Travessa *travessa;
} Canibal;

typedef struct
{
    int servido;
    Travessa *travessa;
} Cozinheiro;

Travessa *criarTravessa(int numPorcoes, int minimo, int numPessoas)
{
    Travessa *travessa = malloc(sizeof(Travessa));
    travessa->numCanibaisCozinheiros = numPessoas - 1;
    travessa->minimo = minimo;
    travessa->numPorcoes = -1;
    travessa->porcaoInicial = numPorcoes;
    sem_init(&(travessa->semaforoNumPorcoes), 0, 0);
    sem_init(&(travessa->semaforoCozinheiro), 0, 1);
    sem_init(&(travessa->semaforoCanibal), 0, 0);
    sem_init(&(travessa->semaforoFinalizador), 0, 0);

    return travessa;
}

Cozinheiro *criarCozinheiro(Travessa *travessa)
{
    Cozinheiro *cozinheiro = malloc(sizeof(Cozinheiro));
    cozinheiro->travessa = travessa;
    cozinheiro->servido = 0;

    return cozinheiro;
}

void iniciarCanibal(Canibal *canibal, Travessa *travessa, int id)
{
    canibal->id = id;
    canibal->travessa = travessa;
    canibal->servido = 0;
}

void encherTravessa(Travessa *travessa)
{
    int i = 0;
    // printf("tentando encher travessa [esperando o cozinheiro acordar]\n");
    sem_wait(&(travessa->semaforoCozinheiro));
    // printf("enchendo a travessa [cozinheiro acordou]\n");
    // printf("porção antes: %d\n", travessa->numPorcoes);
    travessa->numPorcoes = travessa->porcaoInicial;
    // printf("porção depois: %d\n", travessa->numPorcoes);

    while (i < travessa->porcaoInicial)
    {
        sem_post(&(travessa->semaforoNumPorcoes));
        i++;
    }
    // printf("acordando canibais\n");
    sem_post(&(travessa->semaforoCanibal));
}

void *cozinhar(void *arg)
{
    int valor;
    int i = 0;
    char flag = 0;
    Cozinheiro *cozinheiro = (Cozinheiro *)arg;

    while (1)
    {
        // printf("enchendo pela %d vez\n", i++);
        encherTravessa(cozinheiro->travessa);
        cozinheiro->servido++;

        if (cozinheiro->servido > cozinheiro->travessa->minimo - 1 && flag == 0)
        {
            flag = 1;
            sem_post(&(cozinheiro->travessa->semaforoFinalizador));
        }

        sem_getvalue(&(cozinheiro->travessa->semaforoFinalizador), &valor);
        if (valor > cozinheiro->travessa->numCanibaisCozinheiros)
        {
            // printf("cozinheiro foi de base\n");
            return NULL;
        }

        // printf("enchido %d\n", i++);
    }
    return NULL;
}

int servir(Travessa *travessa)
{
    sem_wait(&(travessa->semaforoNumPorcoes));
    // printf("canibal tentando se servir\n");

    if (travessa->numPorcoes == 1)
    {
        // printf("ultima porção servida, acordando o cozinheiro\n");
        travessa->numPorcoes--;
        sem_wait(&(travessa->semaforoCanibal));
        // printf("acesso ao cozinheiro bloqueado\n");
        sem_post(&(travessa->semaforoCozinheiro));
        // printf("acordando cozinheiro\n");
        //  Thread.sleep(1000);
        return 0;
    }

    travessa->numPorcoes--;
    return 1;
}

void *comer(void *arg)
{
    int valor;
    char flag = 0;
    Canibal *canibal = (Canibal *)arg;

    while (1)
    {
        if (servir(canibal->travessa) == 1)
        {
            // printf("canibal %d já servido %d vezes\n", canibal->id, canibal->servido);
            canibal->servido++;

            if (canibal->servido > canibal->travessa->minimo - 1 && flag == 0)
            {
                flag = 1;
                sem_post(&(canibal->travessa->semaforoFinalizador));
            }

            sem_getvalue(&(canibal->travessa->semaforoFinalizador), &valor);
            if (valor > canibal->travessa->numCanibaisCozinheiros)
            {
                // printf("canibal foi de base\n");
                return NULL;
            }
        }

        // printf("travessa vazia, tem que acordar o cozinheiro\n");
    }
    return NULL;
}

int main(int argc, char **argv)
{
    int i, numMinimo, numPorcoes, numCanibais;
    Canibal *canibais;
    pthread_t *threadCanibais;
    Cozinheiro *cozinheiro;
    pthread_t threadCozinheiro;
    Travessa *travessa;

    numCanibais = 5;
    numPorcoes = 5;
    numMinimo = 30;

    travessa = criarTravessa(numPorcoes, numMinimo, numCanibais + 1);
    cozinheiro = criarCozinheiro(travessa);
    canibais = malloc(sizeof(Canibal) * numCanibais);

    pthread_create(&threadCozinheiro, NULL, cozinhar, cozinheiro);

    threadCanibais = malloc(sizeof(pthread_t) * numCanibais);
    for (i = 0; i < numCanibais; i++)
    {
        iniciarCanibal(canibais + i, travessa, i);
        pthread_create(&threadCanibais[i], NULL, comer, canibais + i);
    }

    // for (i = 0; i < numCanibais; i++)
    // {
    //     printf("Canibal %d foi servido %d vezes\n", (canibais + i)->id, 1);
    // }

    // Cria pedido de cancelamento das threads barbeiros
    for (i = 0; i < numCanibais; i++)
    {
        pthread_cancel(threadCanibais[i]);
    }

    pthread_join(threadCozinheiro, NULL);
    for (i = 0; i < numCanibais; i++)
    {
        pthread_join(threadCanibais[i], NULL);
    }

    free(canibais);
    free(travessa);
    free(cozinheiro);

    return 0;
}