import copy

def twoOptVeiculo(rota, matrixCusto):
    menorCusto = 0
    node1 = -1
    node2 = -1

    if len(rota) >= 5:
        for i in range(len(rota) - 3):
            for j in range(i + 2, len(rota) - 1):
                novaRota = rota[0:i + 1] + rota[i + 1:j + 1][::-1] + rota[j + 1:]

                melhoriaCusto = matrixCusto[rota[i]][rota[j]] + matrixCusto[rota[i + 1]][rota[j + 1]] - matrixCusto[rota[i]][rota[i + 1]] - matrixCusto[rota[j]][rota[j + 1]]
                # print(novaRota, melhoriaCusto)
                if melhoriaCusto < menorCusto:
                    node1 = i
                    node2 = j
                    menorCusto = melhoriaCusto
    return node1, node2, menorCusto

def twoOpt(rotas, matrixCusto):
    MenorCusto = 0
    Rota = []
    Posicao1 = []
    Posicao2 = []

    for i in range(len(rotas)):
        # print('antiga', rota)
        [Node1, Node2, Melhoria] = twoOptVeiculo(rotas[i], matrixCusto)
        if Node1 != -1:
            MenorCusto += Melhoria
            Rota.append(i)
            Posicao1.append(Node1)
            Posicao2.append(Node2)
        # print('nova', novaRota)

    for t in range(len(Rota)):
        rota = rotas[Rota[t]]
        NovaRota = rota[0:Posicao1[t] + 1] + rota[Posicao1[t] + 1:Posicao2[t] + 1][::-1] + rota[Posicao2[t] + 1:]
        rotas[Rota[t]] = NovaRota

    return rotas