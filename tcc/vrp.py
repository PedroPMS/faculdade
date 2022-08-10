import copy
import pandas as pd
from datetime import datetime
import tsp
import dividirClientes
from trocarClientes import trocarClientes
from retirarClientes import retirarClientes
from twoOpt import twoOpt
from realocacao import realocacao

from matplotlib import pyplot as plt
plt.style.use('bmh')

# ---------------------------------------------------------------------------------- #
start_time = datetime.now()
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

distanciaTotal = tsp.rodadaTsp(rotas, clientes)
print('Distancia Primeiro TSP =', distanciaTotal)
melhorRota = copy.deepcopy(rotas)
novasRotas = twoOpt(melhorRota, clientes)
distanciaTotalAtual = tsp.rodadaTsp(novasRotas, clientes)
print('Distancia 2Opt =', distanciaTotalAtual, '\n')
realocacao(novasRotas, clientes)
distanciaTotalAtual = tsp.rodadaTsp(novasRotas, clientes)
print('Distancia Realocação =', distanciaTotalAtual, '\n')

# for i in range(1):
#     # novasRotas = trocarClientes(melhorRota) # VNS para troca entre clusters
#     # novasRotas = retirarClientes(rotas)
#     novasRotas = twoOpt(melhorRota, clientes)
#     distanciaTotalAtual = tsp.rodadaTsp(novasRotas, clientes)

#     distanciaTotalAtual = tsp.rodadaTsp(novasRotas, clientes)
#     if(distanciaTotalAtual < distanciaTotal):
#         print(novasRotas, 'i = ', i)
#         print('Distancia Total =', distanciaTotal)
#         print('Distancia Nova =', distanciaTotalAtual, '\n')
#         melhorRota = copy.deepcopy(novasRotas)
#         distanciaTotal = distanciaTotalAtual


end_time = datetime.now()
# print('\nDistancia Final =', distanciaTotal)
print('Duration: {}'.format(end_time - start_time))