import math
import random


def gerarRotasIniciais(qtdVeiculos, matrixCusto, demanda, capacidade):
    matrixCusto.pop(0) #retirando depósito

    rotas = []
    qtdClientes = len(matrixCusto)

    for i in range(qtdVeiculos):
        #Inicia no 0, depósito
        rotas.append([0])

    listaClientesDisponiveis = []
    for i in range(qtdClientes):
        listaClientesDisponiveis.append(i+1)

    i = 1
    ultimoVeiculo = 0
    while(i <= qtdClientes):
        clienteAleatorio = random.choice(listaClientesDisponiveis)
        listaClientesDisponiveis.remove(clienteAleatorio)
        if(ultimoVeiculo == qtdVeiculos):
            ultimoVeiculo = 0
        for j in range(ultimoVeiculo, qtdVeiculos):
            demandaVeiculo = sum(demanda[rotas[j]])
            if(demandaVeiculo < capacidade):
                rotas[j].append(clienteAleatorio)
                ultimoVeiculo += 1
                break
        i += 1

    for rota in rotas:
        #Finaliza no 0, depósito
        rota.append(0)
    return rotas


def construirMatrix(rota, deposito, matrixCusto):
    matrix = []
    distanciasDeposito = [deposito[0]]
    for cliente in rota:
        distanciasDeposito.append(deposito[cliente])

    for cliente in rota:
        distancia = [deposito[cliente]]
        for clienteRota in rota:
            distancia.append(matrixCusto[cliente][clienteRota])
        matrix.append(distancia)

    matrix.insert(0, distanciasDeposito)
    return matrix
