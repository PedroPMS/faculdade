import numpy as np
import pandas
from scipy.spatial.distance import cityblock

delta = [
        [-1, 0], #cima
        [0, -1], #esquerda
        [1, 0], #baixo
        [0, 1] #direita
    ]
deltaSimbolo = ['^', '<', 'v', '>']

def busca(matrix, heuristica, inicio, objetivo, custo):
    fechado = [[0 for linha in range(len(matrix[0]))] for coluna in range(len(matrix))]
    fechado[inicio[0]][inicio[1]] = 1

    expandido = [[-1 for linha in range(len(matrix[0]))] for coluna in range(len(matrix))]
    acao = [[1 for linha in range(len(matrix[0]))] for coluna in range(len(matrix))]

    caminho = [[' ' for linha in range(len(matrix[0]))] for coluna in range(len(matrix))]

    x = inicio[0]
    y = inicio[1]

    g = 0
    f = g + heuristica[x][y]

    aberto = [[f, g, x, y]]
    encontrou = False
    contador = 0

    while not encontrou and len(aberto) != 0:
        aberto.sort()
        aberto.reverse()
        proximo = aberto.pop()
        f = proximo[0]
        g = proximo[1]
        x = proximo[2]
        y = proximo[3]

        expandido[x][y] = contador
        contador += 1

        if x == objetivo[0] and y == objetivo[1]:
            encontrou = True
        else:
            for i in range(len(delta)):
                x2 = x + delta[i][0]
                y2 = y + delta[i][1]
                if (x2 >= 0 and x2 < len(matrix) and y2 >= 0 and y2 < len(matrix[0])):
                    if fechado[x2][y2] == 0 and matrix[x2][y2] == 0:
                        g2 = g + custo
                        f2 = g2 + heuristica[x2][y2]

                        aberto.append([f2, g2, x2, y2])

                        fechado[x2][y2] = 1
                        acao[x][y] = i

    x = 0
    y = 0

    print(acao)
    while x != objetivo[0] or y != objetivo[1]:
        x2 = x + delta[acao[x][y]][0]
        y2 = y + delta[acao[x][y]][1]
        caminho[x][y] = deltaSimbolo[acao[x][y]]
        x = x2
        y = y2
    caminho[objetivo[0]][objetivo[1]] = '*'

    print (pandas.DataFrame(caminho))

    return expandido



def main(args):
    matrix = np.loadtxt('matrix.txt').astype(int)

    inicio = [0, 0]
    objetivo = [len(matrix) - 1, len(matrix[0]) - 1]

    # inicio = [0, 0]
    # objetivo = [len(matrix) - 1, len(matrix[0]) - 1]
    custo = 1

    heuristica = []

    maiorDistancia = cityblock([0, 0], [len(matrix) - 1, len(matrix[0]) - 1])
    for linha in range(len(matrix)):
        heuristicaLinha = []
        for coluna in range(len(matrix[0])):
            distanciaManhattan = cityblock([linha, coluna], objetivo)
            # vamos da um peso grande para os obstáculos do percusso
            if matrix[linha][coluna] == 1:
                distanciaManhattan = distanciaManhattan * maiorDistancia
            heuristicaLinha.append(distanciaManhattan)
        heuristica.append(heuristicaLinha)

    busca(matrix, heuristica, inicio, objetivo, custo)
    return 0

if __name__ == '__main__':
    import sys
    sys.exit(main(sys.argv))