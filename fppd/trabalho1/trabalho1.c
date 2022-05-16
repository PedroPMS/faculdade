#if defined(_WIN32) || defined(__CYGWIN__)
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>

#define CAPACIDADE_MESA 6
#define QTD_LABORATORIOS 3
#define QTD_INFECTADOS 3
#define QTD_TIPOS_DE_INSUMO 3

typedef enum
{
    false = 0,
    true = 1
} bool;

typedef enum
{
    Virus = 0,
    Injecao = 1,
    insumoSecreto = 2
} tipoInsumo;

typedef struct
{
    sem_t total;
    tipoInsumo tipo;
} insumo;

typedef struct
{
    pthread_t thread;
    int id;
    int qtdMinimaDoses;
    int ciclosAtual;
    insumo *insumo1;
    insumo *insumo2;
    pthread_mutex_t *mesaMutex;
    sem_t *atingiramObjetivo;
} pacoteLaboratorio;

typedef struct
{
    pthread_t thread;
    int id;
    int qtdMinimaDoses;
    int ciclosAtual;
    tipoInsumo insumoInfinito;
    insumo *mesa;
    pthread_mutex_t *mesaMutex;
    sem_t *atingiramObjetivo;
} pacoteInfectado;

/* preenche os indices da mesa que tem disponível os insumos que o infectado necessita */
void indicesProdutosFaltantes(insumo *mesa, int capacidadeDaBancada, tipoInsumo insumoDoInfectado, int *indiceProduto1, int *indiceProduto2)
{
    tipoInsumo insumo1Tipo;
    tipoInsumo insumo2Tipo;
    int totalProduto;
    int produtoVerificados;
    int i;

    switch (insumoDoInfectado)
    {
    case Virus:
    {
        insumo1Tipo = Injecao;
        insumo2Tipo = insumoSecreto;
    }
    break;
    case Injecao:
    {
        insumo1Tipo = Virus;
        insumo2Tipo = insumoSecreto;
    }
    break;
    case insumoSecreto:
    {
        insumo1Tipo = Virus;
        insumo2Tipo = Injecao;
    }
    break;
    }

    *indiceProduto1 = -1;
    *indiceProduto2 = -1;
    totalProduto = -1;
    produtoVerificados = 0;
    i = (rand() % capacidadeDaBancada);

    while ((*indiceProduto1 == -1 || *indiceProduto2 == -1) && (produtoVerificados <= capacidadeDaBancada))
    {

        if (sem_getvalue(&(mesa[i].total), &totalProduto) == 0)
        {
            if ((totalProduto > 0) && (mesa[i].tipo == insumo1Tipo) && (*indiceProduto1 == -1))
            {
                *indiceProduto1 = i;
            }
            else if ((totalProduto > 0) && (mesa[i].tipo == insumo2Tipo) && (*indiceProduto2 == -1))
            {
                *indiceProduto2 = i;
            }

            i++;
            i = (i == capacidadeDaBancada) ? 0 : i;
            produtoVerificados++;
        }
    }
}

void *threadLaboratorio(void *argumento)
{

    pacoteLaboratorio *laboratorio = (pacoteLaboratorio *)argumento;

    bool continuarOperando = true;
    int totalProduto1;
    int totalProduto2;
    int atingiramObjetivo;
    int tempo = 0.3;

    while (continuarOperando == true)
    {

        totalProduto1 = 0;
        totalProduto2 = 0;

        if ((sem_getvalue(&(laboratorio->insumo1->total), &totalProduto1) == 0) && (sem_getvalue(&(laboratorio->insumo2->total), &totalProduto2) == 0))
        {

            if ((totalProduto1 == 0) && (totalProduto2 == 0))
            {

                pthread_mutex_lock(laboratorio->mesaMutex);

                if ((sem_post(&(laboratorio->insumo1->total)) == 0) && (sem_post(&(laboratorio->insumo2->total)) == 0))
                {
                    laboratorio->ciclosAtual++;
                    if (laboratorio->ciclosAtual == laboratorio->qtdMinimaDoses)
                    {
                        sem_post(laboratorio->atingiramObjetivo);
                    }
                }

                pthread_mutex_unlock(laboratorio->mesaMutex);

                sleep(tempo);
            }
        }

        if (sem_getvalue(laboratorio->atingiramObjetivo, &atingiramObjetivo) == 0)
        {
            if (atingiramObjetivo == (QTD_LABORATORIOS + QTD_INFECTADOS))
            {
                continuarOperando = false;
            }
        }
    }

    return 0;
}

void *threadInfectado(void *argumento)
{

    pacoteInfectado *infectado = (pacoteInfectado *)argumento;

    bool continuarOperando = true;
    int indiceProduto1;
    int indiceProduto2;
    int atingiramObjetivo;

    while (continuarOperando == true)
    {

        indiceProduto1 = -1;
        indiceProduto2 = -1;

        indicesProdutosFaltantes(infectado->mesa, CAPACIDADE_MESA, infectado->insumoInfinito, &indiceProduto1, &indiceProduto2);

        if ((indiceProduto1 != -1) && (indiceProduto2 != -1))
        {

            pthread_mutex_lock(infectado->mesaMutex);

            indiceProduto1 = -1;
            indiceProduto2 = -1;

            indicesProdutosFaltantes(infectado->mesa, CAPACIDADE_MESA, infectado->insumoInfinito, &indiceProduto1, &indiceProduto2);

            if ((indiceProduto1 != -1) && (indiceProduto2 != -1))
            {

                if ((sem_wait(&(infectado->mesa[indiceProduto1].total)) == 0) && (sem_wait(&(infectado->mesa[indiceProduto2].total)) == 0))
                {
                    infectado->ciclosAtual++;
                    if (infectado->ciclosAtual == infectado->qtdMinimaDoses)
                    {
                        sem_post(infectado->atingiramObjetivo);
                    }
                }
            }

            pthread_mutex_unlock(infectado->mesaMutex);
        }

        if (sem_getvalue(infectado->atingiramObjetivo, &atingiramObjetivo) == 0)
        {
            if (atingiramObjetivo == (QTD_INFECTADOS + QTD_LABORATORIOS))
            {
                continuarOperando = false;
            }
        }
    }

    return 0;
}

int main(int argc, char **argv)
{

    /* DECLARAÇÃO DAS VARIÁVEIS */
    int i, qtdMinimaDoses;
    insumo *mesa;
    pacoteLaboratorio *laboratorios;
    pacoteInfectado *infectados;
    pthread_mutex_t mesaMutex;
    sem_t atingiramObjetivo;

    /* VALIDAÇÃO DE ENTRADAS */
    if (argc != 2)
    {
        printf("\nO objetivo primordial é inválido!\n\n");
        return -1;
    }
    else if (atoi(argv[1]) < 1)
    {
        printf("\nO objetivo primordial é inválido!\n\n");
        return -1;
    }

    /* INICIALIZAÇÃO DAS VARIÁVEIS */
    qtdMinimaDoses = atoi(argv[1]);
    laboratorios = malloc(sizeof(pacoteLaboratorio) * QTD_LABORATORIOS);
    mesa = malloc(sizeof(insumo) * CAPACIDADE_MESA); // A mesa terá o tamanho necessário para receber 2 insumos de cada laboratório, totalizando 6
    infectados = malloc(sizeof(pacoteInfectado) * QTD_INFECTADOS);
    pthread_mutex_init(&mesaMutex, NULL);
    sem_init(&atingiramObjetivo, 0, 0);

    /* INICIALIZA MESA */
    for (i = 0; i < CAPACIDADE_MESA; i++)
    {
        sem_init(&(mesa[i].total), 0, 0);
        mesa[i].tipo = (tipoInsumo)i % QTD_TIPOS_DE_INSUMO;
    }

    /* INICIALIZA LABORATÓRIOS */
    int produto = 0;
    for (i = 0; i < QTD_LABORATORIOS; i++)
    {
        laboratorios[i].id = i + 1;
        laboratorios[i].qtdMinimaDoses = qtdMinimaDoses;
        laboratorios[i].ciclosAtual = 0;
        laboratorios[i].mesaMutex = &mesaMutex;
        laboratorios[i].atingiramObjetivo = &atingiramObjetivo;
        laboratorios[i].insumo1 = &(mesa[produto]);
        produto++;
        laboratorios[i].insumo2 = &(mesa[produto]);
        produto++;
    }

    /* INICIALIZA INFECTADOS */
    for (i = 0; i < QTD_INFECTADOS; i++)
    {
        infectados[i].id = i + 1;
        infectados[i].mesa = mesa;
        infectados[i].qtdMinimaDoses = qtdMinimaDoses;
        infectados[i].ciclosAtual = 0;
        infectados[i].mesaMutex = &mesaMutex;
        infectados[i].atingiramObjetivo = &atingiramObjetivo;
        infectados[i].insumoInfinito = (tipoInsumo)i;
    }

    /* EXECUTA AS THREADS */
    for (i = 0; i < QTD_LABORATORIOS; i++)
    {
        pthread_create(&(laboratorios[i].thread), NULL, threadLaboratorio, &(laboratorios[i]));
    }

    for (i = 0; i < QTD_INFECTADOS; i++)
    {
        pthread_create(&(infectados[i].thread), NULL, threadInfectado, &(infectados[i]));
    }

    /* ESPERA AS THREADS TERMINAREM */
    for (i = 0; i < QTD_LABORATORIOS; i++)
    {
        pthread_join(laboratorios[i].thread, NULL);
    }

    for (i = 0; i < QTD_INFECTADOS; i++)
    {
        pthread_join(infectados[i].thread, NULL);
    }

    /* APRESENTA O RESULTADO */
    for (i = 0; i < QTD_LABORATORIOS; i++)
    {
        printf("Laboratorio %d: %d\n", laboratorios[i].id, laboratorios[i].ciclosAtual);
    }
    for (i = 0; i < QTD_INFECTADOS; i++)
    {
        printf("Infectado %d: %d\n", infectados[i].id, infectados[i].ciclosAtual);
    }

    /* DESTRÓI MEMÓRIA ALOCADA */
    for (i = 0; i < (CAPACIDADE_MESA); i++)
    {
        sem_destroy(&(mesa[i].total));
    }
    pthread_mutex_destroy(&mesaMutex);
    sem_destroy(&atingiramObjetivo);
    free(laboratorios);
    free(infectados);
    free(mesa);

    return 0;
}