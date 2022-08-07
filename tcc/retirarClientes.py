import random
import copy

def veiculosAleatorios(rotas):
    veiculosPossiveis = list(range(len(rotas)))
    random.shuffle(veiculosPossiveis)

    veiculo1 = veiculosPossiveis.pop()
    veiculo2 = veiculosPossiveis.pop()

    return veiculo1, veiculo2

def retirarClientes(rotas):
    novasRotas = copy.deepcopy(rotas)

    # primeira retirada
    veiculo1, veiculo2 = veiculosAleatorios(novasRotas)
    while (len(novasRotas[veiculo1]) <= 5):
        veiculo1, veiculo2 = veiculosAleatorios(novasRotas)

    cliente1 = random.choice(range(len(novasRotas[veiculo1])))
    novasRotas[veiculo2].append(novasRotas[veiculo1][cliente1])
    novasRotas[veiculo1].pop(cliente1)

    return novasRotas