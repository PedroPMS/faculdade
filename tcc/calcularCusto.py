from sys import maxsize
import numpy as np
from itertools import permutations

def calcularCusto(rotas, clientes):
    # rotas = [[0, 4, 30, 6, 10, 18, 9, 0]]
    # rotas = [[0, 4, 30, 6, 18, 10, 9, 0]]
    # rotas = [[0, 26, 29, 0]]
    distanciaTotal = 0
    for rota in rotas:
        rota = rota.copy()
        # print(rota)
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