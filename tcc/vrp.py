import sys
from datetime import datetime

from prepararDados import carregarDados
import dividirClientes
from calcularCusto import calcularCusto

from vizinhancas.twoOpt import twoOpt
from vizinhancas.realocacao import realocacao
from vizinhancas.troca import troca
from vizinhancas.orOpt import orOpt

from matplotlib import pyplot as plt
plt.style.use('bmh')

def vrp_graph(tour, x, y, name):
    plt.figure(figsize=(16, 16), dpi=160)
    plt.plot(x[0], y[0], 'r^')
    plt.scatter(x[1:], y[1:], s=5, c='k', marker=',')
    for i in range(1, 31 + 1):
        plt.annotate(i, (x[i] + 0.2, y[i] + 0.2), size=8)
    for i in range(len(tour)):
        plt.plot(x[tour[i]], y[tour[i]])

    plt.savefig(name)

# ---------------------------------------------------------------------------------- #

clientes, demanda, xcoor, ycoor, capacidade, numVeiculos, resultadoOtimo = carregarDados('A-n32-k5vrp.txt')
clientes = clientes.tolist()

distanciaGeral = sys.maxsize
start_time = datetime.now()
for i in range(50):
    rotas = dividirClientes.gerarRotasIniciais(numVeiculos, clientes[:], demanda, capacidade)
    backup = rotas.copy()
    distanciaTotal = calcularCusto(rotas, clientes)

    for j in range(50):
        rotas = twoOpt(rotas, clientes)
        rotas = troca(rotas, clientes, demanda, capacidade)
        rotas = orOpt(rotas, clientes, 1)
        rotas = orOpt(rotas, clientes, 2)
        rotas = orOpt(rotas, clientes, 3)
        rotas = realocacao(rotas, clientes, demanda, capacidade)
    distanciaTotal = calcularCusto(rotas, clientes)

    if(distanciaTotal < distanciaGeral):
        distanciaGeral = distanciaTotal


end_time = datetime.now()
vrp_graph(backup, xcoor, ycoor, 'inicial')
vrp_graph(rotas, xcoor, ycoor, 'final')
print('Distancia Final =', distanciaGeral, '\n')
print(rotas)
print('Duration: {}'.format(end_time - start_time))