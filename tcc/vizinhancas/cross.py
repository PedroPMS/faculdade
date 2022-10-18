import random

def crossCliente(veiculo1, veiculo2, matrixCusto, demanda, capacidade):
    melhorMelhoria = 0
    node11 = -1
    node12 = -1
    node21 = -1
    node22 = -1

    for i in range(1, len(veiculo1) - 2):
        for k in range(i + 1, len(veiculo1) - 1):
            for j in range(1, len(veiculo2) - 2):
                for l in range(j + 1, len(veiculo2) - 1):
                    tour1_new_demand = sum(demanda[veiculo2[j:l + 1]]) + sum(demanda[veiculo1]) - sum(demanda[veiculo1[i:k + 1]])
                    tour2_new_demand = sum(demanda[veiculo1[i:k + 1]]) + sum(demanda[veiculo2]) - sum(demanda[veiculo2[j:l + 1]])

                    if (tour1_new_demand <= capacidade) and (tour2_new_demand <= capacidade):

                        # novaRota1 = veiculo1[:i] + veiculo2[j:l + 1] + veiculo1[k + 1:]
                        # novaRota2 = veiculo2[:j] + veiculo1[i:k + 1] + veiculo2[l + 1:]

                        cross1 = round(matrixCusto[veiculo1[i - 1]][veiculo2[j]] + matrixCusto[veiculo2[l]][veiculo1[k + 1]] +
                                        matrixCusto[veiculo2[j - 1]][veiculo1[i]] + matrixCusto[veiculo1[k]][veiculo2[l + 1]], 10)
                        cross2 = round(matrixCusto[veiculo1[i - 1]][veiculo1[i]] + matrixCusto[veiculo1[k]][veiculo1[k + 1]] +
                                        matrixCusto[veiculo2[j - 1]][veiculo2[j]] + matrixCusto[veiculo2[l]][veiculo2[l + 1]], 10)
                        melhoriaCross = cross1 - cross2
                        # print(melhoriaCross)

                        if melhoriaCross < melhorMelhoria:
                            melhorMelhoria = melhoriaCross
                            node11 = i
                            node12 = k
                            node21 = j
                            node22 = l

    return node11, node12, node21, node22, melhorMelhoria


def crossAleatorio(rotas, matrixCusto, demanda, capacidade):
    MelhorCusto = 0
    Veiculo1 = -1
    Veiculo2 = -1
    Node11 = -1
    Node12 = -1
    Node21 = -1
    Node22 = -1

    rotasCopy = rotas.copy()

    while True:
        veiculoAleatorio1 = random.choice(rotasCopy)
        veiculoAleatorio2 = random.choice(rotasCopy)

        [node11, node12, node21, node22, melhoria] = crossCliente(veiculoAleatorio1, veiculoAleatorio2, matrixCusto, demanda, capacidade)

        if(veiculoAleatorio1 != veiculoAleatorio2):
            break

    if melhoria < MelhorCusto:
        Veiculo1 = rotas.index(veiculoAleatorio1)
        Veiculo2 = rotas.index(veiculoAleatorio2)
        Node11 = node11
        Node12 = node12
        Node21 = node21
        Node22 = node22
        MelhorCusto = melhoria

    # print('antes', rotas[Veiculo1], rotas[Veiculo2])
    if(Veiculo1 != -1 and Veiculo2 != -1):
        NovaRota1 = rotas[Veiculo1][:Node11] + rotas[Veiculo2][Node21:Node22 + 1] + rotas[Veiculo1][Node12 + 1:]
        NovaRota2 = rotas[Veiculo2][:Node21] + rotas[Veiculo1][Node11:Node12 + 1] + rotas[Veiculo2][Node22 + 1:]
        rotas[Veiculo1] = NovaRota1
        rotas[Veiculo2] = NovaRota2
    # print('depois', rotas[Veiculo1], rotas[Veiculo2])

    return rotas