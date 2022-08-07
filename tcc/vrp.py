import copy
import pandas as pd
import tsp
import dividirClientes
from trocarClientes import trocarClientes
from retirarClientes import retirarClientes

from matplotlib import pyplot as plt
plt.style.use('bmh')

# ---------------------------------------------------------------------------------- #
clientes = pd.read_csv('A-n32-k5.txt', sep=' ', header=None)
numVeiculos = 5

clientes = clientes.values
clientes = clientes.tolist()
deposito = clientes[0]

rotas = dividirClientes.gerarRotasIniciais(numVeiculos, clientes[:])
# rotas = [
#     [21, 25, 30, 31, 20, 2, 6],
#     [28, 4, 10, 14, 8, 18],
#     [23, 1, 29, 5, 24, 27],
#     [26, 3, 17, 7, 13, 11],
#     [16, 22, 19, 9, 12, 15]
# ]

distanciaTotal = tsp.rodadaTsp(rotas, deposito, clientes)
print('Distancia Primeiro TSP =', distanciaTotal)
melhorRota = copy.deepcopy(rotas)
contadorDeNaoMelhoras = 0 # contador para acumular quantas vezes houve troca de rota sem melhora na rota final

for i in range(100):
    novasRotas = trocarClientes(melhorRota) # VNS para troca entre clusters

    distanciaTotalAtual = tsp.rodadaTsp(novasRotas, deposito, clientes)
    if(distanciaTotalAtual < distanciaTotal):
        print('Distancia Total =', distanciaTotal)
        print('Distancia Troca Clientes =', distanciaTotalAtual, '\n')
        melhorRota = copy.deepcopy(novasRotas)
        distanciaTotal = distanciaTotalAtual

    novasRotas = retirarClientes(rotas)

    # distanciaTotalAtual = tsp.rodadaTsp(novasRotas, deposito, clientes)
    # if(distanciaTotalAtual < distanciaTotal):
    #     print('Distancia Total =', distanciaTotal)
    #     print('Distancia Retirar Clientes =', distanciaTotalAtual, '\n')
    #     melhorRota = copy.deepcopy(novasRotas)
    #     distanciaTotal = distanciaTotalAtual

    if(distanciaTotalAtual < distanciaTotal):
        print('Distancia Total =', distanciaTotal)
        print('Distancia Nova =', distanciaTotalAtual, '\n')
        melhorRota = copy.deepcopy(novasRotas)
        distanciaTotal = distanciaTotalAtual


print('\nDistancia Final =', distanciaTotal)