from calcularCusto import calcularCusto

def orOptVeiculo(veiculo, matrixCusto, K):
    menorCusto = 0
    node1 = -1
    node2 = -1
    node3 = -1

    print(veiculo, calcularCusto([veiculo], matrixCusto))
    if len(veiculo) >= K + 3:
        for i in range(len(veiculo) - K - 1):
            j = i + K
            for k in range(len(veiculo) - 1):
                if (k < i) or (j < k):
                    if k < i:
                        # print(veiculo[0:k + 1], veiculo[i + 1:j + 1], veiculo[k + 1:i + 1], veiculo[j + 1:])
                        novaRota = veiculo[0:k + 1] + veiculo[i + 1:j + 1] + veiculo[k + 1:i + 1] + veiculo[j + 1:]
                    else:
                        # print(veiculo[0:i + 1], veiculo[j + 1:k + 1], veiculo[i + 1:j + 1], veiculo[k + 1:])
                        novaRota = veiculo[0:i + 1] + veiculo[j + 1:k + 1] + veiculo[i + 1:j + 1] + veiculo[k + 1:]
                    print(novaRota, calcularCusto([novaRota], matrixCusto))

                    reducaoCusto = matrixCusto[veiculo[i]][veiculo[i + 1]] + matrixCusto[veiculo[j]][veiculo[j + 1]] + matrixCusto[veiculo[k]][veiculo[k + 1]]
                    melhoria = matrixCusto[veiculo[i]][veiculo[j + 1]] + matrixCusto[veiculo[k]][veiculo[i + 1]] + matrixCusto[veiculo[j]][veiculo[k + 1]] - reducaoCusto

                    if melhoria < menorCusto:
                        node1 = i
                        node2 = j
                        node3 = k
                        menorCusto = melhoria

    return node1, node2, node3, menorCusto


def orOpt(rotas, matrixCusto, K):
    MenorCusto = 0
    veiculo = []
    Position1 = []
    Position2 = []
    Position3 = []

    for i in range(len(rotas)):
        [Node1, Node2, Node3, Melhoria] = orOptVeiculo(rotas[i], matrixCusto, K)

        if Node1 != -1:
            MenorCusto += Melhoria
            veiculo.append(i)
            Position1.append(Node1)
            Position2.append(Node2)
            Position3.append(Node3)

    for t in range(len(veiculo)):
        tour = rotas[veiculo[t]]
        if Position3[t] < Position1[t]:
            New_tour = tour[:Position3[t] + 1] + tour[Position1[t] + 1:Position2[t] + 1] + tour[Position3[t] + 1:Position1[t] + 1] + tour[Position2[t] + 1:]
        else:
            New_tour = tour[:Position1[t] + 1] + tour[Position2[t] + 1:Position3[t] + 1] + tour[Position1[t] + 1:Position2[t] + 1] + tour[Position3[t] + 1:]
        rotas[veiculo[t]] = New_tour

    return rotas
    # return veiculo, Position1, Position2, Position3, MenorCusto
