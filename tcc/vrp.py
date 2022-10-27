import sys
from datetime import datetime
import os
import csv

from prepararDados import carregarDados
import dividirClientes
from calcularCusto import calcularCusto

from vizinhancas.twoOpt import twoOpt
from vizinhancas.realocacao import realocacao
from vizinhancas.troca import troca
from vizinhancas.orOpt import orOpt
from vizinhancas.cross import crossAleatorio

from plotarRotas import vrp_graph

# ---------------------------------------------------------------------------------- #

def vrp(rodadas = 10, arquivo = 'test.txt'):
    clientes, demanda, xcoor, ycoor, capacidade, numVeiculos, qtdClientes, resultadoOtimo = carregarDados(arquivo)
    clientes = clientes.tolist()

    # print([numVeiculos, qtdClientes, resultadoOtimo])

    distanciaGeral = sys.maxsize
    start_time = datetime.now()

    media = []
    for i in range(1):
        rotas = dividirClientes.gerarRotasIniciais(numVeiculos, clientes[:], demanda, capacidade)
        distanciaTotal = calcularCusto(rotas, clientes)
        # print('distancia inicial', distanciaTotal)

        for j in range(rodadas):
            rotas = twoOpt(rotas, clientes)
            rotas = orOpt(rotas, clientes, 3)
            rotas = troca(rotas, clientes, demanda, capacidade)
            rotas = realocacao(rotas, clientes, demanda, capacidade)
            rotas = crossAleatorio(rotas, clientes, demanda, capacidade)
        distanciaTotal = calcularCusto(rotas, clientes)

        media.append(distanciaTotal)

        if(distanciaTotal < distanciaGeral):
            distanciaGeral = distanciaTotal


    end_time = datetime.now()
    tempoTotal = end_time - start_time

    melhorCusto = "{:.2f}".format(distanciaGeral)
    custoMedio = "{:.2f}".format(sum(media)/len(media))
    tempo = "{:.2f}".format(tempoTotal.total_seconds())

    # vrp_graph(rotas, xcoor, ycoor, qtdClientes, 'final')
    # print('Distancia Final =', melhorCusto, '\n')
    # print('Média Resultados =', custoMedio, media, '\n')
    # print(rotas)
    # print('Duration: ', tempo)
    return resultadoOtimo, melhorCusto, tempo

diretorio = 'instancias/G4'
with open('resultados.csv', 'a') as f:
    write = csv.writer(f)
    for (dirpath, dirnames, filenames) in os.walk(diretorio):
        for file in filenames:
            instancia = diretorio + '/'+ file
            print(instancia)
            resultadoOtimo, melhorCusto, tempo = vrp(500, instancia)
            write.writerow([file, resultadoOtimo, melhorCusto, tempo])


    # resultadoOtimo, melhorCusto, tempo = vrp(500, 'instancias/G4/M-n200-k16.txt')
    # write.writerow(['M-n200-k16', resultadoOtimo, melhorCusto, tempo])