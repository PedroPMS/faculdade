from sys import maxsize
import numpy as np
from itertools import permutations

def rodadaTsp(rotas, clientes):
    # rotas = [[0, 4, 30, 6, 10, 18, 9, 0]]
    # rotas = [[0, 4, 30, 6, 18, 10, 9, 0]]
    distanciaTotal = 0
    for rota in rotas:
        rota = rota.copy()
        custo = custoRota(clientes, rota)

        distanciaTotal += custo
    return distanciaTotal

def custoRota(clientes, rotaVeiculo):
    custo = 0
    i = 0
    while(i < len(rotaVeiculo)-1):
        if(i == 0 or i == len(rotaVeiculo)-1):
            # print(clientes[0][rotaVeiculo[i+1]])
            # print(0,rotaVeiculo[i+1])
            custo += clientes[0][rotaVeiculo[i+1]]
        else:
            # print(clientes[rotaVeiculo[i]][rotaVeiculo[i+1]])
            # print(rotaVeiculo[i], rotaVeiculo[i+1])
            custo += clientes[rotaVeiculo[i]][rotaVeiculo[i+1]]
        i += 1
    return custo

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