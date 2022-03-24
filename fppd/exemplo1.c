#define _CRT_SECURE_NO_WARNINGS 1
#define _WINSOCK_DEPRECATED_NO_WARNINGS 1

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>

void *thread(void *vargp)
{
    printf("Hello World da thread criada pela thread principal!\n");
    pthread_exit((void *)NULL);
}

int main()
{
    pthread_t tid; // estrutura que define a thread
    printf("Hello World da thread principal!\n");

    // cria uma thread com os atributos definidos em tid, opções padrão NULL
    // thread é a função que contém o código da thread e não há parametros de entrada (ou seja, NULL)
    pthread_create(&tid, NULL, thread, NULL);

    // espera a thread "tid" terminar e não captura seu vvalor de retorno (NULL)
    pthread_join(tid, NULL);
}