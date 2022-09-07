import sys
from datetime import datetime

from prepararDados import carregarDados
import dividirClientes
from calcularCusto import calcularCusto

from vizinhancas.twoOpt import twoOpt
from vizinhancas.realocacao import realocacao
from vizinhancas.troca import troca
from vizinhancas.orOpt import orOpt
from plotarRotas import vrp_graph

# ---------------------------------------------------------------------------------- #

clientes, demanda, xcoor, ycoor, capacidade, numVeiculos, qtdClientes, resultadoOtimo = carregarDados('A-n32-k5vrp.txt')
clientes = clientes.tolist()

distanciaGeral = sys.maxsize
start_time = datetime.now()
for i in range(1):
    rotas = dividirClientes.gerarRotasIniciais(numVeiculos, clientes[:], demanda, capacidade)
    backup = rotas.copy()
    distanciaTotal = calcularCusto(rotas, clientes)

    for j in range(1):
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
vrp_graph(backup, xcoor, ycoor, qtdClientes, 'inicial')
vrp_graph(rotas, xcoor, ycoor, qtdClientes, 'final')
print('Distancia Final =', distanciaGeral, '\n')
print(rotas)
print('Duration: {}'.format(end_time - start_time))