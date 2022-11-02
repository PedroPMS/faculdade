from calcularCusto import calcularCusto

def circOptrota(rota, matrixCusto):
    melhoria = 0

    novaRota = rota[1:-1]
    melhorRota = novaRota
    menorCusto = calcularCusto([novaRota], matrixCusto)

    print('inicial', melhorRota, menorCusto)

    for i in range(len(novaRota) - 1):
        novaRota = novaRota[-1:] + novaRota[:-1]
        novoCusto = calcularCusto([novaRota], matrixCusto)

        melhoriaCusto = calcularCusto([novaRota], matrixCusto) - menorCusto
        print(novaRota, novoCusto)
        # # print(novaRota, melhoriaCusto)
        if melhoriaCusto < melhoria:
            menorCusto = novoCusto
            melhorRota = novaRota
            melhoria = melhoriaCusto
    return melhoria, melhorRota, menorCusto

def circOpt(rotas, matrixCusto):
    MenorCusto = 0
    Rota = []
    Veiculo = -1

    for i in range(len(rotas)):
        [Melhoria, MelhorRota, MenorCusto] = circOptrota(rotas[i], matrixCusto)
        # print(Melhoria, MelhorRota, MenorCusto)

        if Melhoria < MenorCusto:
            MenorCusto = Melhoria
            Veiculo = i
            Rota = MelhorRota

    # print(rotas[Veiculo])
    if(Veiculo != -1):
        rotas[Veiculo] = [0] + Rota + [0]
    # print(rotas[Veiculo])
    print(rotas)
    return rotas
