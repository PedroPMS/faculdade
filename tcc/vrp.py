import pandas as pd
from datetime import datetime
from calcularCusto import calcularCusto
import dividirClientes
from twoOpt import twoOpt
from realocacao import realocacao
from troca import troca

from matplotlib import pyplot as plt
plt.style.use('bmh')

# ---------------------------------------------------------------------------------- #
start_time = datetime.now()
clientes = pd.read_csv('A-n32-k5.txt', sep=' ', header=None).values.tolist()
# print(clientes)
numVeiculos = 5

# rotas = [
#     [21, 25, 30, 31, 20, 2, 6],
#     [28, 4, 10, 14, 8, 18],
#     [23, 1, 29, 5, 24, 27],
#     [26, 3, 17, 7, 13, 11],
#     [16, 22, 19, 9, 12, 15]
# ]

for i in range(100):
    rotas = dividirClientes.gerarRotasIniciais(numVeiculos, clientes[:])
    distanciaTotal = calcularCusto(rotas, clientes)
    # print('Distancia Primeiro TSP =', distanciaTotal)

    for j in range(500):
        # print(j)
        rotas = twoOpt(rotas, clientes)
        rotas = troca(rotas, clientes)
        rotas = realocacao(rotas, clientes)
    distanciaTotal = calcularCusto(rotas, clientes)
    if(distanciaTotal <= 784):
        print(rotas, distanciaTotal)


end_time = datetime.now()
distanciaTotal = calcularCusto(rotas, clientes)
print('Distancia Final =', distanciaTotal, '\n')
print(rotas)
print('Duration: {}'.format(end_time - start_time))