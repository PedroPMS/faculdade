from sys import maxsize
import numpy as np
from itertools import permutations
from python_tsp.exact import solve_tsp_dynamic_programming
import dividirClientes

def rodadaTsp(rotas, deposito, clientes):
    distanciaTotal = 0
    for rota in rotas:
        rota = rota.copy()
        matrix = dividirClientes.construirMatrix(rota, deposito, clientes)
        distance_matrix = np.array(matrix)
        rota.insert(0, 0)
        # print('Clients of vehicle =', rota)

        melhorRota, menorCusto = solve_tsp_dynamic_programming(distance_matrix)

        # print(melhorRota)
        distanciaTotal += menorCusto
    return distanciaTotal

def travellingSalesmanProblem(graph, s = 0):
    # store all vertex apart from source vertex
    vertex = []
    for i in range(len(graph)):
        if i != s:
            vertex.append(i)

    # store minimum weight Hamiltonian Cycle
    menorCusto = maxsize
    melhorRota = []
    next_permutation = permutations(vertex)
    for i in next_permutation:

        # store current Path weight(cost)
        current_pathweight = 0

        # compute current path weight
        rota = []
        k = s
        for j in i:
            rota.append(j)
            current_pathweight += graph[k][j]
            k = j
        rota.append(s)
        current_pathweight += graph[k][s]

        # update minimum
        if (current_pathweight < menorCusto):
            menorCusto = current_pathweight
            melhorRota = rota.copy()

    return melhorRota, menorCusto