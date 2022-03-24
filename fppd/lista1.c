#define _CRT_SECURE_NO_WARNINGS 1
#define _WINSOCK_DEPRECATED_NO_WARNINGS 1

#include <pthread.h>
#include <stdlib.h>
#include <stdio.h>
#define NUM_THREADS 5

void *printHello(void *threadId)
{
    int tid;
    tid = (int)threadId;
    printf("Hello World! Sou a thread #%d!\n", tid);
    return 0;
}

int main()
{
    pthread_t threads[NUM_THREADS];
    int rc, t;

    for (t = 0; t < NUM_THREADS; t++)
    {
        printf("Main: criando a thread %d!\n", t);
        rc = pthread_create(&threads[t], NULL, printHello, (void *)t);
        if (rc)
        {
            printf("ERRO code is %d\n", rc);
            exit(-1);
        }
    }

    // esperar todas as threads terminarem
    for (int i = 0; i < NUM_THREADS; i++)
    {
        pthread_join(threads[i], NULL);
    }

    return 0;
}