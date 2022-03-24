import heapq
import pandas
import numpy as np
from scipy.spatial.distance import cityblock

def heuristica(vector_a, vector_b):
    return cityblock([vector_a[0], vector_a[1]], [vector_b[0], vector_b[1]])

def astar(matrix, inicio, objetivo):
    # vizinho do local atual: cima, baixo, esqueda, direita
    vizinhos = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    listaFechada = set()
    posicaoAnterior = {}
    g = {inicio: 0}
    g = {inicio: heuristica(inicio, objetivo)}
    listaAberta = []

    # adiciona na lista aberta a posição inicial
    heapq.heappush(listaAberta, (g[inicio], inicio))

    # enquanto tiver elemntos na lista aberta
    while listaAberta:
        # recupera a posição atual na matix
        atual = heapq.heappop(listaAberta)[1]

        # se chegou no objetivo, retorna o caminho encontrado
        if atual == objetivo:
            data = []
            while atual in posicaoAnterior:
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
                    # encontrou em uma parede
                    continue
            else:
                # encontrou em uma parede
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


matrix = np.loadtxt('matrix.txt').astype(int)
inicio = (0, 0)
objetivo = (14, 14)

route = astar(matrix, inicio, objetivo)
# route = route + [inicio]
# route = route[::-1]

caminhoDesenhado = np.copy(matrix.astype(str))
caminhoDesenhado[objetivo[0]][objetivo[1]] = '*'

for i in range(len(route)):
    linhaAtual = route[i][0]
    colunaAtual = route[i][1]

    if linhaAtual != objetivo[0] or colunaAtual != objetivo[1]:
        linhaPosterior = route[i+1][0]
        colunaPosterior = route[i+1][1]

    if colunaAtual > colunaPosterior:
        caminhoDesenhado[linhaAtual][colunaAtual] = '<'
    if colunaAtual < colunaPosterior:
        caminhoDesenhado[linhaAtual][colunaAtual] = '>'
        # print (pandas.DataFrame(test))
    if linhaAtual > linhaPosterior:
        caminhoDesenhado[linhaAtual][colunaAtual] = '^'
    if linhaPosterior > linhaAtual:
        caminhoDesenhado[linhaAtual][colunaAtual] = 'v'
print (pandas.DataFrame(caminhoDesenhado))


# extract x and y coordinates from route list
# x_coords = []
# y_coords = []


# for i, item in enumerate(route):
#     with plt.xkcd():
#         x = route[i][0]
#         y = route[i][1]
#         x_coords.append(x)
#         y_coords.append(y)
#         fig, ax = plt.subplots(figsize=(8, 8))
#         ax.imshow(matrix, cmap=plt.cm.Dark2)
#         ax.scatter(inicio[1], inicio[0], marker="*", color="yellow", s=200)
#         ax.scatter(objetivo[1], objetivo[0], marker="+", color="red", s=200)
#         ax.plot(y_coords, x_coords, color="black")
#         plt.xticks([])
#         plt.yticks([])
#         plt.title("A* algorithm step " + str(i))

#         # Output numbering in a ffmpeg compatible way!
#         if i < 10:
#             filename = "mazestep_00%d.png" % i
#         elif (i > 9) & (i < 100):
#             filename = "mazestep_0%d.png" % i
#         else:
#             filename = "mazestep_%d.png" % i

#         plt.savefig(filename)
#         plt.close()
# plt.show()


# need to then run from the shell:
# ffmpeg -v warning -i mazestep_%03d.png -y out.gif