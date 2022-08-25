def calcularCusto(rotas, matrixCusto):
    distanciaTotal = 0
    for rota in rotas:
        rota = rota.copy()
        custo = custoRota(matrixCusto, rota)

        distanciaTotal += custo
    return distanciaTotal

def custoRota(matrixCusto, rotaVeiculo):
    custo = 0
    i = 0
    while(i < len(rotaVeiculo)-1):
        if(i == 0 or i == len(rotaVeiculo)-1):
            # print(matrixCusto[0][rotaVeiculo[i+1]])
            # print(0,rotaVeiculo[i+1])
            custo += matrixCusto[0][rotaVeiculo[i+1]]
        else:
            # print(matrixCusto[rotaVeiculo[i]][rotaVeiculo[i+1]])
            # print(rotaVeiculo[i], rotaVeiculo[i+1])
            custo += matrixCusto[rotaVeiculo[i]][rotaVeiculo[i+1]]
        i += 1
    return custo