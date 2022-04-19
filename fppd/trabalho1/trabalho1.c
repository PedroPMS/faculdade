#if defined(_WIN32) || defined(__CYGWIN__)
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>

#define CAPACIDADE_BANCADA 6
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
    pthread_mutex_t *bancadaMutex;
    sem_t *atingiramObjetivo;
} pacoteLaboratorio;

typedef struct
{
    pthread_t thread;
    int id;
    int qtdMinimaDoses;
    int ciclosAtual;
    tipoInsumo insumoInfinito;
    insumo *bancada;
    pthread_mutex_t *bancadaMutex;
    sem_t *atingiramObjetivo;
} pacoteInfectado;

/* realiza os prints das informações do infectado e labotório */
void print_tipo_insumo(tipoInsumo tipo_insumo);
void print_laboratorio(int id, tipoInsumo tipo_insumo);
void print_infectado(int id, tipoInsumo tipo_insumo);

/* preenche os indices da bancada que tem disponível os insumos que o infectado necessita */
void indicesProdutosFaltantes(insumo *bancada, int capacidadeDaBancada, tipoInsumo insumoDoInfectado, int *indiceProduto1, int *indiceProduto2)
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

        if (sem_getvalue(&(bancada[i].total), &totalProduto) == 0)
        {
            if ((totalProduto > 0) && (bancada[i].tipo == insumo1Tipo) && (*indiceProduto1 == -1))
            {
                *indiceProduto1 = i;
            }
            else if ((totalProduto > 0) && (bancada[i].tipo == insumo2Tipo) && (*indiceProduto2 == -1))
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

                pthread_mutex_lock(laboratorio->bancadaMutex);

                if ((sem_post(&(laboratorio->insumo1->total)) == 0) && (sem_post(&(laboratorio->insumo2->total)) == 0))
                {
                    laboratorio->ciclosAtual++;
                    if (laboratorio->ciclosAtual == laboratorio->qtdMinimaDoses)
                    {
                        sem_post(laboratorio->atingiramObjetivo);
                    }
                }

                pthread_mutex_unlock(laboratorio->bancadaMutex);

                // #if defined(_WIN32) || defined(__CYGWIN__)
                //                 Sleep(tempo * 1000);
                // #else
                sleep(tempo);
                // #endif
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

        indicesProdutosFaltantes(infectado->bancada, CAPACIDADE_BANCADA, infectado->insumoInfinito, &indiceProduto1, &indiceProduto2);

        if ((indiceProduto1 != -1) && (indiceProduto2 != -1))
        {

            pthread_mutex_lock(infectado->bancadaMutex);

            indiceProduto1 = -1;
            indiceProduto2 = -1;

            indicesProdutosFaltantes(infectado->bancada, CAPACIDADE_BANCADA, infectado->insumoInfinito, &indiceProduto1, &indiceProduto2);

            if ((indiceProduto1 != -1) && (indiceProduto2 != -1))
            {

                if ((sem_wait(&(infectado->bancada[indiceProduto1].total)) == 0) && (sem_wait(&(infectado->bancada[indiceProduto2].total)) == 0))
                {
                    infectado->ciclosAtual++;
                    if (infectado->ciclosAtual == infectado->qtdMinimaDoses)
                    {
                        sem_post(infectado->atingiramObjetivo);
                    }
                }
            }

            pthread_mutex_unlock(infectado->bancadaMutex);
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
    insumo *bancada;
    pacoteLaboratorio *laboratorios;
    pacoteInfectado *infectados;
    pthread_mutex_t bancadaMutex;
    sem_t atingiramObjetivo;

    /* VALIDAÇÃO DE ENTRADAS */
    if (argc != 2)
    {
        printf("\nA quantidade de argumentos eh invalida!\n");
        printf("\nO unico argumento esperado eh o numero minimo de vezes que cada um deve realizar seu objetivo primordial.\n\n");
        return -1;
    }
    else if (atoi(argv[1]) < 1)
    {
        printf("\nO valor do argumento eh invalido!\n\n");
        return -1;
    }

    /* INICIALIZAÇÃO DAS VARIÁVEIS */
    qtdMinimaDoses = atoi(argv[1]);
    laboratorios = malloc(sizeof(pacoteLaboratorio) * QTD_LABORATORIOS);
    bancada = malloc(sizeof(insumo) * CAPACIDADE_BANCADA); // A bancada terá o tamanho necessário para receber 2 insumos de cada laboratório, totalizando 6
    infectados = malloc(sizeof(pacoteInfectado) * QTD_INFECTADOS);
    pthread_mutex_init(&bancadaMutex, NULL);
    sem_init(&atingiramObjetivo, 0, 0);

    /* INICIALIZA BANCADA */
    for (i = 0; i < CAPACIDADE_BANCADA; i++)
    {
        sem_init(&(bancada[i].total), 0, 0);
        bancada[i].tipo = (tipoInsumo)i % QTD_TIPOS_DE_INSUMO;
    }

    /* INICIALIZA LABORATÓRIOS */
    int produto = 0;
    for (i = 0; i < QTD_LABORATORIOS; i++)
    {
        laboratorios[i].id = i + 1;
        laboratorios[i].qtdMinimaDoses = qtdMinimaDoses;
        laboratorios[i].ciclosAtual = 0;
        laboratorios[i].bancadaMutex = &bancadaMutex;
        laboratorios[i].atingiramObjetivo = &atingiramObjetivo;
        laboratorios[i].insumo1 = &(bancada[produto]);
        produto++;
        laboratorios[i].insumo2 = &(bancada[produto]);
        produto++;
        // print_laboratorio(laboratorios[i].id, laboratorios[i].insumo1->tipo);
        // print_laboratorio(laboratorios[i].id, laboratorios[i].insumo2->tipo);
    }

    /* INICIALIZA INFECTADOS */
    for (i = 0; i < QTD_INFECTADOS; i++)
    {
        infectados[i].id = i + 1;
        infectados[i].bancada = bancada;
        infectados[i].qtdMinimaDoses = qtdMinimaDoses;
        infectados[i].ciclosAtual = 0;
        infectados[i].bancadaMutex = &bancadaMutex;
        infectados[i].atingiramObjetivo = &atingiramObjetivo;
        infectados[i].insumoInfinito = (tipoInsumo)i;
        // print_infectado(infectados[i].id, infectados[i].insumoInfinito);
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
    for (i = 0; i < (CAPACIDADE_BANCADA); i++)
    {
        sem_destroy(&(bancada[i].total));
    }
    pthread_mutex_destroy(&bancadaMutex);
    sem_destroy(&atingiramObjetivo);
    free(laboratorios);
    free(infectados);
    free(bancada);

    return 0;
}

/* funções extras para mostrar as informações do laboratorio e infectado */

void print_laboratorio(int id, tipoInsumo tipo_insumo)
{
    printf("LAB %d Tem ", id);
    print_tipo_insumo(tipo_insumo);
    printf("\n");
}

void print_infectado(int id, tipoInsumo tipo_insumo)
{
    printf("INF %d Tem ", id);
    print_tipo_insumo(tipo_insumo);
    printf("\n");
}

void print_tipo_insumo(tipoInsumo tipo_insumo)
{
    switch (tipo_insumo)
    {
    case Virus:
        printf("virus");
        break;
    case Injecao:
        printf("injecao");
        break;
    case insumoSecreto:
        printf("insumoSecreto");
        break;
    }
}