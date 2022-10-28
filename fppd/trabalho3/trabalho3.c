#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#include <unistd.h>

typedef struct
{
    pthread_mutex_t mutex;
    pthread_cond_t cozinheiro;
    pthread_cond_t canibal;
    int comida;
    int numPreparoPorcoes;
} Travessa;

typedef struct
{
    int id;
    int qtdPorcoes;
    Travessa *travessa;
} Canibal;

void *Servir(void *arg)
{
    Canibal *canibal = (Canibal *)arg;
    Travessa *travessa = canibal->travessa;

    while (1)
    {
        pthread_mutex_lock(&(travessa->mutex));
        while (!travessa->comida)
        {
            printf("Canibal %d: esperando comida\n", canibal->id);
            pthread_cond_wait(&(travessa->canibal), &(travessa->mutex));
        }
        printf("Canibal %d: servindo durante 1 segundo, tem %d porcoes\n", canibal->id, travessa->comida);
        sleep(1);
        travessa->comida--;
        if (travessa->comida == 0)
        {
            printf("Canibal %d: vai acordar o cozinheiro\n", canibal->id);
            pthread_cond_signal(&(travessa->cozinheiro));
        }

        pthread_mutex_unlock(&(travessa->mutex));
        printf("Canibal %d: comendo durante 3 segundos\n", canibal->id);
        sleep(3);
        canibal->qtdPorcoes++;
    }
    return NULL;
}

void *EncherTravessa(int m, Travessa *travessa, time_t tempoExecucao)
{
    while (time(NULL) < tempoExecucao)
    {
        pthread_mutex_lock(&(travessa->mutex));
        printf("Enchendo Travessa, tem %d porcoes\n", travessa->comida);
        while (travessa->comida)
        {
            pthread_cond_wait(&(travessa->cozinheiro), &(travessa->mutex));
        }
        travessa->comida += m;
        pthread_cond_broadcast(&(travessa->canibal));
        printf("cozinhando durante 5 segundos\n");
        sleep(5);
        travessa->numPreparoPorcoes++;
        pthread_mutex_unlock(&(travessa->mutex));
    }
    pthread_mutex_lock(&(travessa->mutex));
    return NULL;
}

int main(int argc, char **argv)
{
    Travessa *travessa = malloc(sizeof(Travessa));
    travessa->mutex = (pthread_mutex_t)PTHREAD_MUTEX_INITIALIZER;
    travessa->cozinheiro = (pthread_cond_t)PTHREAD_COND_INITIALIZER;
    travessa->canibal = (pthread_cond_t)PTHREAD_COND_INITIALIZER;
    travessa->comida = 0;
    travessa->numPreparoPorcoes = 0;

    int erro;
    int i, numCanibais, numPorcoes, segundosExecucao;

    Canibal *canibais;
    pthread_t *threadsCanibais;

    if (argc != 4)
    {
        printf("erro na chamada do programa: jantar <#canibais> <#comida> <#tempoExecucao>\n");
        exit(1);
    }

    numCanibais = atoi(argv[1]);
    numPorcoes = atoi(argv[2]);
    segundosExecucao = atoi(argv[3]);
    printf("numero de canibais: %d -- quantidade de comida: %d\n", numCanibais, numPorcoes);

    canibais = (Canibal *)malloc(sizeof(Canibal) * numCanibais);
    threadsCanibais = malloc(sizeof(pthread_t) * numCanibais);

    for (i = 0; i < numCanibais; i++)
    {
        canibais[i].id = i;
        canibais[i].qtdPorcoes = 0;
        canibais[i].travessa = travessa;

        erro = pthread_create(&threadsCanibais[i], NULL, Servir, &(canibais[i]));
        if (erro)
        {
            printf("erro na criacao do thread %d\n", i);
            exit(1);
        }
    }

    time_t tempoExecucao = time(NULL) + segundosExecucao;
    EncherTravessa(numPorcoes, travessa, tempoExecucao);

    printf("\n\n-----------\n\n");
    printf("Cozinheiro preparou %d vezes\n", canibais[0].travessa->numPreparoPorcoes - 1);
    for (i = 0; i < numCanibais; i++)
    {
        printf("Canibal %d comeu %d vezes\n", canibais[i].id, canibais[i].qtdPorcoes);
    }
}