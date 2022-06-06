#ifdef _WIN32
#include <Windows.h>
#else
#include <unistd.h>
#endif

#include <pthread.h>
#include <semaphore.h>
#include <stdio.h>
#include <stdlib.h>
#include <time.h>

typedef enum
{
    false = 0,
    true = 1
} bool;

typedef struct
{
    pthread_t thread;
    int id;
    sem_t *barbeiroLiberado;
    sem_t *barbeirosAcordados;
    sem_t *barbeirosAtendeuCliente;
    int qtdMinimaClientes;
    int clientesAtendidos;
    sem_t *totalBarbeirosLiberados;
    sem_t *totalAtingiramObjetivo;
    int totalBarbeiros;
} pacoteBarbeiro;

typedef struct
{
    pthread_t thread;
    int id;
    sem_t *barbeirosLiberados;
    sem_t *cadeiraEspera;
    sem_t *barbeirosAcordados;
    sem_t *barbeirosAtendeuCliente;
    sem_t *totalBarbeirosLiberados;
    int totalBarbeiros;
    sem_t *totalAtingiramObjetivo;
    pthread_mutex_t *mutexClienteID;
    sem_t *barbeariaFechou;
    sem_t *totalClientesAtivo;
} pacoteCliente;

void *threadBarbeiro(void *argumento);

void *threadCliente(void *argumento);

int main(int argc, char **argv)
{

    int i, qtdBarbeiros, qtdCadeirasEspera, qtdMinimaClientes, atingiramObjetivo, qtdThreadCriadas;
    pacoteBarbeiro *barbeiros;
    pacoteCliente *cliente;
    sem_t *barbeirosLiberados, *barbeirosAcordados, *barbeirosAtendeuCliente;
    sem_t cadeiraEspera, totalBarbeirosLiberados, totalAtingiramObjetivo, barbeariaFechou, totalClientesAtivo;
    pthread_mutex_t mutexClienteID;
    pthread_attr_t tattr;

    /* Validar entradas */
    if (argc != 4)
    {
        char *erro = "A quantidade de argumentos na linha de comando é inválida!\n"
                     "Você deve informar a quantidade de barbeiros, a quantidade de\n"
                     "cadeiras de espera e a quantidade mínima de atendimentos de cada barbeiro.\n";
        printf("%s", erro);
        return -1;
    }

    qtdBarbeiros = atoi(argv[1]);
    qtdCadeirasEspera = atoi(argv[2]);
    qtdMinimaClientes = atoi(argv[3]);
    if (qtdBarbeiros < 1 || qtdCadeirasEspera < 1 || qtdMinimaClientes < 1)
    {
        printf("\nO valor dos argumentos é inválido!\n\n");
        return -1;
    }

    /* Inicializar variaveis */
    barbeiros = (pacoteBarbeiro *)malloc(sizeof(pacoteBarbeiro) * qtdBarbeiros);
    barbeirosLiberados = (sem_t *)malloc(sizeof(sem_t) * qtdBarbeiros);
    barbeirosAcordados = (sem_t *)malloc(sizeof(sem_t) * qtdBarbeiros);
    barbeirosAtendeuCliente = (sem_t *)malloc(sizeof(sem_t) * qtdBarbeiros);
    cliente = (pacoteCliente *)malloc(sizeof(pacoteCliente));

    sem_init(&cadeiraEspera, 0, qtdCadeirasEspera);               // A barbearia abre com todas cadeiras de espera livres
    sem_init(&totalAtingiramObjetivo, 0, 0);                      // Contagem de barbeiros que atingiram objetivo
    sem_init(&totalBarbeirosLiberados, 0, 0);                     // Contagem de barbeiros liberados, isto é, os barbeiros que podem atender algum cliente se for acordado
    sem_init(&barbeariaFechou, 0, 0);                             // Sinalizar a main que o programa terminou
    sem_init(&totalClientesAtivo, 0, 0);                          // Contagem atual de clientes na barbearia (total de threads ativas que estão na funcao threadCliente)
    pthread_mutex_init(&mutexClienteID, NULL);                    // Garantir que apenas um cliente pegue o ID cliente por vez
    pthread_attr_init(&tattr);                                    // Inicializa variável atributo da thread
    pthread_attr_setdetachstate(&tattr, PTHREAD_CREATE_DETACHED); // Define atributo para detached (recursos podem ser reutilizados a medida que cada thread termina)

    // Inicializa barbeiros
    for (i = 0; i < qtdBarbeiros; i++)
    {
        barbeiros[i].id = i;
        barbeiros[i].qtdMinimaClientes = qtdMinimaClientes;
        barbeiros[i].clientesAtendidos = 0;
        barbeiros[i].totalAtingiramObjetivo = &totalAtingiramObjetivo;
        barbeiros[i].totalBarbeiros = qtdBarbeiros;
        barbeiros[i].barbeiroLiberado = &(barbeirosLiberados[i]);
        barbeiros[i].barbeirosAcordados = &(barbeirosAcordados[i]);
        barbeiros[i].barbeirosAtendeuCliente = &(barbeirosAtendeuCliente[i]);
        barbeiros[i].totalBarbeirosLiberados = &totalBarbeirosLiberados;

        sem_init(&(barbeirosLiberados[i]), 0, 0);      // Define se um barbeiro específico está livre (1) ou ocupado (0)
        sem_init(&(barbeirosAcordados[i]), 0, 0);      // Define se um barbeiro específico está acordado (1) ou dormindo (0)
        sem_init(&(barbeirosAtendeuCliente[i]), 0, 0); // Define se um barbeiro específico terminou o atendimento ao cliente (1) ou ainda vai terminar (0)
    }

    /* Cria barbeiros */
    for (i = 0; i < qtdBarbeiros; i++)
    {
        pthread_create(&(barbeiros[i].thread), NULL, threadBarbeiro, &(barbeiros[i]));
    }

    // Inicializa cliente
    cliente->barbeirosLiberados = barbeirosLiberados;
    cliente->cadeiraEspera = &cadeiraEspera;
    cliente->barbeirosAcordados = barbeirosAcordados;
    cliente->barbeirosAtendeuCliente = barbeirosAtendeuCliente;
    cliente->totalBarbeiros = qtdBarbeiros;
    cliente->mutexClienteID = &mutexClienteID;
    cliente->totalBarbeirosLiberados = &totalBarbeirosLiberados;
    cliente->totalAtingiramObjetivo = &totalAtingiramObjetivo;
    cliente->barbeariaFechou = &barbeariaFechou;
    cliente->totalClientesAtivo = &totalClientesAtivo;

    // Cria clientes enquanto todos os barbeiros ainda nao atingiram objetivo
    qtdThreadCriadas = 0;
    atingiramObjetivo = 0;

    while (atingiramObjetivo < qtdBarbeiros)
    {

        // Incrementa a quantidade de clientes ativos na barbearia para o programa saber que ainda vai ser enviado um novo cliente
        sem_post(&totalClientesAtivo);

        /* Thread criada com a propriedade detached, não precisa realizar join para liberar recurso,
         * os recursos são liberados automaticamente após o término da thread.
         */
        pthread_create(&(cliente->thread), &tattr, threadCliente, cliente);

        // Recupera a quantidade de barbeiros que já atingiram o objetivo
        sem_getvalue(&totalAtingiramObjetivo, &atingiramObjetivo);

        qtdThreadCriadas++;
    }

    // Espera o sinal que avisa que último cliente saiu da barbearia e ela fechou
    sem_wait(&barbeariaFechou);

    // Exibi a quantidade de clientes que cada barbeiro atendeu
    for (i = 0; i < qtdBarbeiros; i++)
    {
        printf("barbeiro %d atendeu %d clientes\n", barbeiros[i].id, barbeiros[i].clientesAtendidos);
    }

    // Cria pedido de cancelamento das threads barbeiros
    for (i = 0; i < qtdBarbeiros; i++)
    {
        pthread_cancel(barbeiros[i].thread);
    }

    // Acorda barbeiros para eles cairem no ponto de cancelamento
    for (i = 0; i < qtdBarbeiros; i++)
    {
        sem_post(barbeiros[i].barbeirosAcordados);
    }

    /* Libera recursos dos barbeiros */
    void *status = NULL;
    for (i = 0; i < qtdBarbeiros; i++)
    {

        /* quando uma thread cancelada é encerrada, uma junção usando pthread_join()
         * obtem PTHREAD_CANCELED como status de saida.
         * https://man7.org/linux/man-pages/man3/pthread_join.3.html
         */
        pthread_join(barbeiros[i].thread, &status);
    }

    /* Destroi variáveis e libera memória */
    pthread_attr_destroy(&tattr);
    for (i = 0; i < qtdBarbeiros; i++)
    {
        sem_destroy(&(barbeirosLiberados[i]));
        sem_destroy(&(barbeirosAcordados[i]));
        sem_destroy(&(barbeirosAtendeuCliente[i]));
    }
    sem_destroy(&barbeariaFechou);
    sem_destroy(&cadeiraEspera);
    sem_destroy(&totalBarbeirosLiberados);
    sem_destroy(&totalAtingiramObjetivo);
    sem_destroy(&totalClientesAtivo);
    pthread_mutex_destroy(&mutexClienteID);
    free(barbeiros);
    free(cliente);
    free(barbeirosLiberados);
    free(barbeirosAcordados);
    free(barbeirosAtendeuCliente);

    return 0;
}

void *threadBarbeiro(void *argumento)
{

    pacoteBarbeiro *barbeiro = (pacoteBarbeiro *)argumento;
    // printf("barbeiro %d entrou\n", barbeiro->id);

    sem_post(barbeiro->barbeiroLiberado);        // Barbeiro chegou e está livre
    sem_post(barbeiro->totalBarbeirosLiberados); // Incrementa total barbeiros liberados

    while (true)
    {

        sem_wait(barbeiro->barbeirosAcordados); // Bbarbeiro está dormindo

        /* Ponto de cancelamento
         * se nenhum pedido de cancelamento está pendente, então uma chamada para
         * pthread_testcancel() não tem efeito.
         * https://man7.org/linux/man-pages/man3/pthread_testcancel.3.html
         */
        pthread_testcancel();

        // printf("barbeiro %d acordou e está atendendo um cliente\n", barbeiro->id);
        barbeiro->clientesAtendidos++;

        if (barbeiro->clientesAtendidos == barbeiro->qtdMinimaClientes)
        {
            // printf("barbeiro %d atingiu seu objetivo!\n", barbeiro->id);
            sem_post(barbeiro->totalAtingiramObjetivo);
        }

        // printf("barbeiro %d terminou de atender o cliente e está livre!\n", barbeiro->id);
        sem_post(barbeiro->barbeirosAtendeuCliente); // Barbeiro terminou de atender o cliente
        sem_post(barbeiro->barbeiroLiberado);        // Barbeiro está livre
        sem_post(barbeiro->totalBarbeirosLiberados); // Incrementa total barbeiros liberados
    }

    return NULL;
}

void *threadCliente(void *argumento)
{

    pacoteCliente *cliente = (pacoteCliente *)argumento;

    bool clienteAtendido = false;
    int i, barbeirosVerificados;

    // ocupa cadeira de espera se alguma estiver livre
    if (sem_trywait(cliente->cadeiraEspera) == 0)
    {
        // printf("cliente %d entrou\n", clienteID);
        while (clienteAtendido == false)
        {

            sem_wait(cliente->totalBarbeirosLiberados); // Caso não tenha barbeiros livres o cliente vai esperar aqui */

            srand(time(NULL));                      // muda semente do rand()
            i = (rand() % cliente->totalBarbeiros); // indice inicial
            barbeirosVerificados = 0;

            while (barbeirosVerificados < cliente->totalBarbeiros)
            {

                // vai ao encontro do barbeiro livre
                if (sem_trywait(&(cliente->barbeirosLiberados[i])) == 0)
                {
                    // printf("cliente %d acorda o barbeiro %d e está esperando por ele\n", clienteID, i);
                    sem_post(cliente->cadeiraEspera);                 // libera cadeira de espera
                    sem_post(&(cliente->barbeirosAcordados[i]));      // acorda barbeiro
                    sem_wait(&(cliente->barbeirosAtendeuCliente[i])); // cliente espera, na cadeira do barbeiro, o fim do atendimento
                    clienteAtendido = true;
                    // printf("cliente %d ja foi atendido pelo barbeiro %d e está saindo!\n", clienteID, i);
                    break;
                }

                i++;
                i = (i >= cliente->totalBarbeiros) ? 0 : i;
                barbeirosVerificados++;
            }
        }
    }
    else
    {
        // printf("cliente %d nao entrou\n", clienteID);
    }

    // Decrementa total clientes ativos
    sem_wait(cliente->totalClientesAtivo);

    int totalBarbeirosConcluiramObjetivo = 0;

    // Obtem a quantidade de barbeiros que já atingiram o objetivo
    sem_getvalue(cliente->totalAtingiramObjetivo, &totalBarbeirosConcluiramObjetivo);

    // Se todos barbeiros já atingiram objetivo, entao verifica quantos clientes ainda estao ativos
    if (totalBarbeirosConcluiramObjetivo == cliente->totalBarbeiros)
    {

        int totalClientesAtual = 0;

        // Obtem a quantidade atual de clientes que estao ativos
        sem_getvalue(cliente->totalClientesAtivo, &totalClientesAtual);

        if (totalClientesAtual == 0)
        {
            // Sinalizar na main que saiu o último cliente que entrou/visitou a barbearia após todos barbeiros atingirem o objetivo
            sem_post(cliente->barbeariaFechou);
        }
    }

    return NULL;
}