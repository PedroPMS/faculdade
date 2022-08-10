import copy

def twoOptVeiculo(rota, matrixCusto):
    menorCusto = 0
    melhorRota = copy.deepcopy(rota)

    if len(rota) >= 5:
        for i in range(len(rota) - 3):
            for j in range(i + 2, len(rota) - 1):
                novaRota = rota[0:i + 1] + rota[i + 1:j + 1][::-1] + rota[j + 1:]

                melhoriaCusto = matrixCusto[rota[i]][rota[j]] + matrixCusto[rota[i + 1]][rota[j + 1]] - matrixCusto[rota[i]][rota[i + 1]] - matrixCusto[rota[j]][rota[j + 1]]
                # print(novaRota, melhoriaCusto)
                if melhoriaCusto < menorCusto:
                    menorCusto = melhoriaCusto
                    melhorRota = copy.deepcopy(novaRota)
    return melhorRota

def twoOpt(rotas, matrixCusto):
    novasRotas = []
    for rota in rotas:
        # print('antiga', rota)
        novaRota = twoOptVeiculo(rota, matrixCusto)
        novasRotas.append(novaRota)
        # print('nova', novaRota)
    return novasRotas