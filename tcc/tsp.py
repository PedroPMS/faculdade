from sys import maxsize
import numpy as np
from itertools import permutations

def rodadaTsp(rotas, clientes):
    distanciaTotal = 0
    # print(clientes)
    for rota in rotas:
        rota = rota.copy()
        melhorRota, menorCusto = travellingSalesmanProblem(clientes, rota)

        distanciaTotal += menorCusto
    return distanciaTotal

def travellingSalesmanProblem(clientes, rotaVeiculo, s = 0):
    # store all vertex apart from source vertex
    vertex = []
    for i in range(len(rotaVeiculo)):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    menorCusto = maxsize
    melhorRota = []
    proximaPermutacao = permutations(vertex)
    for i in proximaPermutacao:

        # store current Path weight(cost)
        custoAtual = 0

        # compute current path weight
        rota = []
        k = s
        for j in i:
            rota.append(j)

            # teste para validação
            # if(graph[k][j] != clientes[rotaVeiculo[k]][rotaVeiculo[j]]):
            #     print('erro', graph[k][j], clientes[rotaVeiculo[k]][rotaVeiculo[j]])

            custoAtual += clientes[rotaVeiculo[k]][rotaVeiculo[j]]
            k = j
        rota.append(s)
        custoAtual += clientes[rotaVeiculo[k]][rotaVeiculo[s]]

        # update minimum
        if (custoAtual < menorCusto):
            menorCusto = custoAtual
            melhorRota = rota.copy()

    return melhorRota, menorCusto