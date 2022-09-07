from calcularCusto import calcularCusto
def realocacaoCliente(veiculo1, veiculo2, matrixCusto, demanda, capacidade):
    menorCusto = 0
    cliente = -1
    posicao = -1

    # print([veiculo1, veiculo2], ';', calcularCusto([veiculo1, veiculo2], matrixCusto))
    for i in range(1, len(veiculo1) - 1):
        if (demanda[veiculo1[i]] + sum(demanda[veiculo2]) <= capacidade) and (sum(demanda[veiculo1]) - demanda[veiculo1[i]] > 0):
            for j in range(1, len(veiculo2) - 1):
                novaRota1 = veiculo1.copy()
                del novaRota1[i]
                novaRota2 = veiculo2[:j + 1] + [veiculo1[i]] + veiculo2[j + 1:]
                # print([novaRota1, novaRota2], ';', calcularCusto([novaRota1, novaRota2], matrixCusto))


                melhoriaVeiculo1 = matrixCusto[veiculo1[i - 1]][veiculo1[i]] + matrixCusto[veiculo1[i]][veiculo1[i + 1]] - matrixCusto[veiculo1[i - 1]][veiculo1[i + 1]]
                pioraVeiculo2 = matrixCusto[veiculo2[j]][veiculo1[i]] + matrixCusto[veiculo1[i]][veiculo2[j + 1]] - matrixCusto[veiculo2[j]][veiculo2[j + 1]]
                melhoriaCusto = pioraVeiculo2 - melhoriaVeiculo1
                if melhoriaCusto < menorCusto:
                    # print(novaRota, melhoriaVeiculo1 - pioraVeiculo2)
                    menorCusto = melhoriaCusto
                    cliente = i
                    posicao = j

    return cliente, posicao, menorCusto

def realocacao(rotas, matrixCusto, demanda, capacidade):
    MenorCusto = 0
    Veiculo1 = -1
    Veiculo2 = -1
    Cliente = -1
    Posicao = -1

    for veiculo1 in range(len(rotas)):
        for veiculo2 in range(len(rotas)):
            if veiculo1 != veiculo2:
                [cliente, posicao, menorCusto] = realocacaoCliente(rotas[veiculo1], rotas[veiculo2], matrixCusto, demanda, capacidade)

                if menorCusto < MenorCusto:
                    Veiculo1 = veiculo1
                    Veiculo2 = veiculo2
                    Cliente = cliente
                    Posicao = posicao
                    MenorCusto = menorCusto

    # print(rotas[Veiculo1], rotas[Veiculo2])
    if(Veiculo1 != -1 and Veiculo2 != -1):
        rotas[Veiculo2].insert(Posicao + 1, rotas[Veiculo1][Cliente])
        del rotas[Veiculo1][Cliente]
    # print(rotas[Veiculo1], rotas[Veiculo2])

    return rotas