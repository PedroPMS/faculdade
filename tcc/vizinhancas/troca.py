from calcularCusto import calcularCusto
def trocaCliente(veiculo1, veiculo2, matrixCusto, demanda, capacidade):
    menorCusto = 0
    posicao1 = -1
    posicao2 = -1

    # print([veiculo1, veiculo2], calcularCusto([veiculo1, veiculo2], matrixCusto))
    for i in range(1, len(veiculo1) - 1):
        for j in range(1, len(veiculo2) - 1):
            novaDemandaVeiculo1 = demanda[veiculo2[j]] + sum(demanda[veiculo1]) - demanda[veiculo1[i]]
            novaDemandaVeiculo2 = demanda[veiculo1[i]] + sum(demanda[veiculo2]) - demanda[veiculo2[j]]

            if (novaDemandaVeiculo1 <= capacidade) and (novaDemandaVeiculo2 <= capacidade):
                novaRota1 = veiculo1[:i] + [veiculo2[j]] + veiculo1[i + 1:]
                novaRota2 = veiculo2[:j] + [veiculo1[i]] + veiculo2[j + 1:]
                # print([novaRota1, novaRota2], calcularCusto([novaRota1, novaRota2], matrixCusto))

                custoTroca1 = matrixCusto[veiculo1[i - 1]][veiculo2[j]] + matrixCusto[veiculo2[j]][veiculo1[i + 1]] - matrixCusto[veiculo1[i - 1]][veiculo1[i]] - matrixCusto[veiculo1[i]][veiculo1[i + 1]]
                custoTroca2 = matrixCusto[veiculo2[j - 1]][veiculo1[i]] + matrixCusto[veiculo1[i]][veiculo2[j + 1]] - matrixCusto[veiculo2[j - 1]][veiculo2[j]] - matrixCusto[veiculo2[j]][veiculo2[j + 1]]

                melhoriaCusto = custoTroca1 + custoTroca2
                if melhoriaCusto < menorCusto:
                    menorCusto = melhoriaCusto
                    posicao1 = i
                    posicao2 = j
                # print(melhoriaCusto, novaRota1, novaRota2)

    return posicao1, posicao2, menorCusto

def troca(rotas, matrixCusto, demanda, capacidade):
    MenorCusto = 0
    Veiculo1 = -1
    Veiculo2 = -1
    Posicao1 = -1
    Posicao2 = -1

    for veiculo1 in range(len(rotas) - 1):
        for veiculo2 in range(veiculo1 + 1, len(rotas)):
            if veiculo1 != veiculo2:
                [posicao1, posicao2, menorCusto] = trocaCliente(rotas[veiculo1], rotas[veiculo2], matrixCusto, demanda, capacidade)

                if menorCusto < MenorCusto:
                    Veiculo1 = veiculo1
                    Veiculo2 = veiculo2
                    Posicao1 = posicao1
                    Posicao2 = posicao2
                    MenorCusto = menorCusto

    # print('antes', rotas[Veiculo1], rotas[Veiculo2])
    if(Veiculo1 != -1 and Veiculo2 != -1):
        New_tour1 = rotas[Veiculo1][:Posicao1] + [rotas[Veiculo2][Posicao2]] + rotas[Veiculo1][Posicao1 + 1:]
        New_tour2 = rotas[Veiculo2][:Posicao2] + [rotas[Veiculo1][Posicao1]] + rotas[Veiculo2][Posicao2 + 1:]
        rotas[Veiculo1] = New_tour1
        rotas[Veiculo2] = New_tour2
    # print('depois', rotas[Veiculo1], rotas[Veiculo2])

    return rotas