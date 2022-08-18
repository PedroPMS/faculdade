def interchange(veiculo1, veiculo2, matrixCusto, lamda):
    best_imp = 0
    node11 = -1
    node12 = -1
    node21 = -1
    node22 = -1

    for i in range(1, len(veiculo1) - lamda):
        for k in range(i - 1, i + lamda):
            for j in range(1, len(veiculo2) - lamda):
                for l in range(j - 1, j + lamda):
                    novaRota1 = veiculo1[:i] + veiculo2[j:l + 1] + veiculo1[k + 1:]
                    novaRota2 = veiculo2[:j] + veiculo1[i:k + 1] + veiculo2[l + 1:]

                    interchange1 = round(total_distance([novaRota1], matrixCusto) + total_distance([novaRota2], matrixCusto), 5)
                    interchange2 = round(total_distance([veiculo1], matrixCusto) + total_distance([veiculo2], matrixCusto), 5)
                    interchange_cost = interchange1 - interchange2

                    if interchange_cost < best_imp:
                        best_imp = interchange_cost
                        node11 = i
                        node12 = k
                        node21 = j
                        node22 = l

    return node11, node12, node21, node22, best_imp

def total_distance(tours, distance):
    total_distance = 0
    for tour in tours:
        tour_distance = 0
        for i in range(len(tour) - 1):
            tour_distance += distance[tour[i]][tour[i + 1]]
        total_distance += tour_distance
    return total_distance

def lambdaInterchange(rotas, matrixCusto, lamda):
    MenorCusto = 0
    Veiculo1 = -1
    Veiculo2 = -1
    Node11 = -1
    Node12 = -1
    Node21 = -1
    Node22 = -1

    for veiculo1 in range(len(rotas) - 1):
        for veiculo2 in range(veiculo1 + 1, len(rotas)):
            [node11, node12, node21, node22, melhora] = interchange(rotas[veiculo1], rotas[veiculo2], matrixCusto, lamda)

            if melhora < MenorCusto:
                Veiculo1 = veiculo1
                Veiculo2 = veiculo2
                Node11 = node11
                Node12 = node12
                Node21 = node21
                Node22 = node22
                MenorCusto = melhora

    # print('antes', rotas[Veiculo1], rotas[Veiculo2])
    if(Veiculo1 != -1 and Veiculo2 != -1):
        New_tour1 = rotas[Veiculo1][:Node11] + rotas[Veiculo2][Node21:Node22 + 1] + rotas[Veiculo1][Node12 + 1:]
        New_tour2 = rotas[Veiculo2][:Node21] + rotas[Veiculo1][Node11:Node12 + 1] + rotas[Veiculo2][Node22 + 1:]
        rotas[Veiculo1] = New_tour1
        rotas[Veiculo2] = New_tour2
    # print('depois', rotas[Veiculo1], rotas[Veiculo2])

    return rotas