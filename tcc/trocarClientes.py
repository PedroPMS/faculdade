import random
import copy

def veiculosAleatorios(rotas):
    veiculosPossiveis = list(range(len(rotas)))
    random.shuffle(veiculosPossiveis)

    veiculo1 = veiculosPossiveis.pop()
    veiculo2 = veiculosPossiveis.pop()

    return veiculo1, veiculo2

def trocarClientes(rotas):
    veiculo1, veiculo2 = veiculosAleatorios(rotas)
    novasRotas = copy.deepcopy(rotas)

    # primeira troca
    cliente1 = random.choice(range(len(novasRotas[veiculo1])))
    cliente2 = random.choice(range(len(novasRotas[veiculo2])))
    aux = novasRotas[veiculo1][cliente1]
    novasRotas[veiculo1][cliente1] = novasRotas[veiculo2][cliente2]
    novasRotas[veiculo2][cliente2] = aux

    # segunda troca
    cliente1 = random.choice(range(len(novasRotas[veiculo1])))
    cliente2 = random.choice(range(len(novasRotas[veiculo2])))
    aux = novasRotas[veiculo1][cliente1]
    novasRotas[veiculo1][cliente1] = novasRotas[veiculo2][cliente2]
    novasRotas[veiculo2][cliente2] = aux

    return novasRotas