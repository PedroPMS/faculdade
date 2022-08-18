import math
import random


def gerarRotasIniciais(qtdVeiculos, clientes):
    clientes.pop(0)
    numeroMaxClientesPorVeiculo = math.floor(len(clientes)/qtdVeiculos)

    rotas = []
    qtdClientes = len(clientes)

    for i in range(qtdVeiculos):
        #Inicia no 0, depósito
        rotas.append([0])

    listaClientesDisponiveis = []
    for i in range(qtdClientes):
        listaClientesDisponiveis.append(i+1)

    i = 1
    while(i <= qtdClientes):
        clienteAleatorio = random.choice(listaClientesDisponiveis)
        listaClientesDisponiveis.remove(clienteAleatorio)
        for j in range(qtdVeiculos):
            tamanhoRota = len(rotas[j])
            if(tamanhoRota < numeroMaxClientesPorVeiculo or i == qtdClientes):
                rotas[j].append(clienteAleatorio)
                break
        i += 1
    for rota in rotas:
        #Finaliza no 0, depósito
        rota.append(0)
    return rotas


def construirMatrix(rota, deposito, clientes):
    matrix = []
    distanciasDeposito = [deposito[0]]
    for cliente in rota:
        distanciasDeposito.append(deposito[cliente])

    for cliente in rota:
        distancia = [deposito[cliente]]
        for clienteRota in rota:
            distancia.append(clientes[cliente][clienteRota])
        matrix.append(distancia)

    matrix.insert(0, distanciasDeposito)
    return matrix