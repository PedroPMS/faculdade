import pandas as pd
from datetime import datetime
from calcularCusto import calcularCusto
import dividirClientes
from twoOpt import twoOpt
from realocacao import realocacao
from troca import troca
from lambdaInterchange import lambdaInterchange

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

distanciaGeral = 0
for i in range(1):
    rotas = dividirClientes.gerarRotasIniciais(numVeiculos, clientes[:])
    distanciaTotal = calcularCusto(rotas, clientes)
    # print('Distancia Primeiro TSP =', distanciaTotal)

    for j in range(50):
        # print(j)
        rotas = twoOpt(rotas, clientes)
        rotas = troca(rotas, clientes)
        # rotas = lambdaInterchange(rotas, clientes, 2)
        # rotas = realocacao(rotas, clientes)
    distanciaTotal = calcularCusto(rotas, clientes)
    distanciaGeral = distanciaTotal
    if(distanciaTotal <= 784):
        print(rotas, distanciaTotal)


end_time = datetime.now()
print('Distancia Final =', distanciaGeral, '\n')
print(rotas)
print('Duration: {}'.format(end_time - start_time))