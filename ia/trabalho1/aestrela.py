import heapq
import pandas
import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors
from scipy.spatial.distance import cityblock

def heuristica(vector_a, vector_b):
    # retorna o caminho de Manhattan
    return cityblock([vector_a[0], vector_a[1]], [vector_b[0], vector_b[1]])

def aestrela(matrix, inicio, objetivo):
    # vizinho do local atual: cima, baixo, esqueda, direita
    vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    listaFechada = set()
    posicaoAnterior = {}
    g = {inicio: 0}
    g = {inicio: heuristica(inicio, objetivo)}
    listaAberta = []

    # adiciona na lista aberta a posição inicial
    heapq.heappush(listaAberta, (g[inicio], inicio))

    # enquanto tiver elementos na lista aberta
    while listaAberta:
        # recupera a posição atual na matix
        atual = heapq.heappop(listaAberta)[1]

        # se chegou no objetivo, retorna o caminho encontrado
        if atual == objetivo:
            data = []
            while atual in posicaoAnterior:
                data.append(atual)
                atual = posicaoAnterior[atual]
            return data

        # a posição atual vai para a lista fechada
        listaFechada.add(atual)
        for i, j in vizinhos:
            vizinho = atual[0] + i, atual[1] + j
            tentativaCustoMinimo = g[atual] + heuristica(atual, vizinho)
            if 0 <= vizinho[0] < matrix.shape[0]:
                if 0 <= vizinho[1] < matrix.shape[1]:
                    if matrix[vizinho[0]][vizinho[1]] == 1:
                        continue
                else:
                    # encontrou uma parede
                    continue
            else:
                # encontrou uma parede
                continue

            # se já foi visitado, pula
            if vizinho in listaFechada and tentativaCustoMinimo >= g.get(vizinho, 0):
                continue

            # atualiza as variáveis de custo e a lista aberta
            if tentativaCustoMinimo < g.get(vizinho, 0) or vizinho not in [i[1] for i in listaAberta]:
                posicaoAnterior[vizinho] = atual
                g[vizinho] = tentativaCustoMinimo
                g[vizinho] = tentativaCustoMinimo + heuristica(vizinho, objetivo)
                heapq.heappush(listaAberta, (g[vizinho], vizinho))

    return False

def caminhoMatrix(matrix, rota, objetivo):
    caminhoDesenhado = np.copy(matrix.astype(str))
    caminhoDesenhado[objetivo[0]][objetivo[1]] = '*'

    for i in range(len(rota)):
        linhaAtual = rota[i][0]
        colunaAtual = rota[i][1]

        if linhaAtual != objetivo[0] or colunaAtual != objetivo[1]:
            linhaPosterior = rota[i+1][0]
            colunaPosterior = rota[i+1][1]

        if colunaAtual > colunaPosterior:
            caminhoDesenhado[linhaAtual][colunaAtual] = '<'
        if colunaAtual < colunaPosterior:
            caminhoDesenhado[linhaAtual][colunaAtual] = '>'
        if linhaAtual > linhaPosterior:
            caminhoDesenhado[linhaAtual][colunaAtual] = '^'
        if linhaPosterior > linhaAtual:
            caminhoDesenhado[linhaAtual][colunaAtual] = 'v'
    print (pandas.DataFrame(caminhoDesenhado))
    print('\n\n')

def caminhoImagem(matrix, rota, inicio, objetivo):
    caminhoDesenhado = np.copy(matrix.astype(int))

    for i in range(len(rota)):
        linhaAtual = rota[i][0]
        colunaAtual = rota[i][1]

        caminhoDesenhado[linhaAtual][colunaAtual] = 3

    caminhoDesenhado[inicio[0]][inicio[1]] = 2
    caminhoDesenhado[objetivo[0]][objetivo[1]] = 9
    # print (pandas.DataFrame(caminhoDesenhado))

    cmap = colors.ListedColormap(['white', 'black', 'green', 'blue', 'red'])
    bounds=[0,1,2,3,8,9]
    norm = colors.BoundaryNorm(bounds, cmap.N)

    plt.imshow(caminhoDesenhado, interpolation='nearest', cmap=cmap, norm=norm)
    plt.savefig('caminho.png')

################################# iniciar algoritmo #################################
nomeArquivo = 'matrix.txt'
inicio = (14, 14) #defina o ponto inicial
objetivo = (2, 10) #defina o ponto final
#################################### fim ############################################

matrix = np.loadtxt(nomeArquivo).astype(int) #defina o arquivo com o Grid
rota = aestrela(matrix, inicio, objetivo)
rota = rota + [inicio]
rota = rota[::-1]

caminhoMatrix(matrix, rota, objetivo)
caminhoImagem(matrix, rota, inicio, objetivo)



