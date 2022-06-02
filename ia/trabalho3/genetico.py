import numpy as np
import random
from pprint import pprint
import matplotlib.pyplot as plt

class Individuo:
    def __init__(self, binario, limites):
        self.binario = binario    # binario do indivíduo
        self.fitness = None       # aptidão do indivíduo
        self.limites = limites

    def calcularFitness(self, costFunc, qntBits):
        binario = self.binario
        self.fitness = costFunc(converteBinario(limite=limites, binario=binario, qntBits=qntBits))

def converteBinario(limite, binario, qntBits):
    min = limite[0]
    max = limite[1]
    inteiro = int(str(binario), 2)

    x = min + (max - min) * inteiro / (2**qntBits - 1)
    return round(x, 3)

def funcaoCusto(x):
    return round(np.cos(x) * x + 2, 3)

def gerarBinarioAleatorio(qntBits):
    binario = ""

    for i in range(qntBits):
        temp = str(random.randint(0, 1))
        binario += temp
    return binario

def selecaoPorTorneio(populacao, numIndividuos):
    selecionados = []
    melhorIndividuo = None
    # Loop para o processo de seleção, irá rodar o número de indivíduos/2. 10 indivíduos = 5 seleções = 10 filhos
    for i in range(0, numIndividuos):
        individuo1 = random.randint(0, numIndividuos - 1)
        individuo2 = random.randint(0, numIndividuos - 1)

        if(min(populacao[individuo1].fitness, populacao[individuo2].fitness) == populacao[individuo1].fitness):
            selecionado = populacao[individuo1]
        else:
            selecionado = populacao[individuo2]

        selecionados.append(selecionado)
        if(melhorIndividuo == None or selecionado.fitness < melhorIndividuo.fitness):
            melhorIndividuo = selecionado
    return [selecionados, melhorIndividuo]

def crossover(individuo1, individuo2):
    binarioIndividuo1 = individuo1.binario
    binarioIndividuo2 = individuo2.binario

    aleatorio = random.uniform(0, 1)
    if(aleatorio <= 0.7):
        # print('antes', [binarioIndividuo1, binarioIndividuo2])
        filho1 = binarioIndividuo1[:8] + binarioIndividuo2[8:]
        filho2 = binarioIndividuo2[:8] + binarioIndividuo1[8:]
        binarioIndividuo1 = filho1
        binarioIndividuo2 = filho2
        # print('depois', [binarioIndividuo1, binarioIndividuo2])
    return [binarioIndividuo1, binarioIndividuo2]

def mutacao(binario):
    binario = [caracter for caracter in binario]
    # print('antes', binario)
    for i in range(len(binario)):
        if random.uniform(0, 1) <= 0.1:
			# inverter o bit
            binario[i] = str(1 - int(binario[i]))
    # print('depoois', ''.join(binario))
    return ''.join(binario)

def gerarNovaPopulacao(costFunc, selecionados, numIndividuos):
    novaPopulacao = []
    for j in range(0, numIndividuos, 2):
        pai1, pai2 = selecionados[j], selecionados[j+1]
        [binarioIndividuo1, binarioIndividuo2] = crossover(pai1, pai2)
        binarioIndividuo1 = mutacao(binarioIndividuo1)
        binarioIndividuo2 = mutacao(binarioIndividuo2)

        individuo1 = Individuo(binarioIndividuo1, limites)
        individuo2 = Individuo(binarioIndividuo2, limites)

        individuo1.calcularFitness(costFunc, qntBits)
        individuo2.calcularFitness(costFunc, qntBits)

        novaPopulacao.append(individuo1)
        novaPopulacao.append(individuo2)
    return novaPopulacao


def otimizar(costFunc, limites, numIndividuos, numGeracoes, qntBits):
    solucoes = []

    # Inicia população
    populacao = []
    for i in range(0, numIndividuos):
        x = gerarBinarioAleatorio(qntBits)
        individuo = Individuo(x, limites)
        individuo.calcularFitness(costFunc, qntBits)
        populacao.append(individuo)

    i=0
    while i < numGeracoes:
        [selecionados, melhorIndividuo] = selecaoPorTorneio(populacao, numIndividuos)
        solucoes.append(melhorIndividuo.fitness)
        # print(melhorIndividuo.fitness, converteBinario(limites, melhorIndividuo.binario, qntBits))

        novaPopulacao = gerarNovaPopulacao(costFunc, selecionados, numIndividuos)
        novaPopulacao.pop(random.randint(0, numIndividuos - 1))
        novaPopulacao.append(melhorIndividuo)

        populacao = novaPopulacao.copy()
        i+=1
    return solucoes

###################### iniciar ######################
limites = [-20,20]
numIndividuos = 10
numGeracoes = 20
qntBits = 16
otimizar(funcaoCusto, limites, numIndividuos, numGeracoes, qntBits)

melhorSolucao = [0]
solucoesEncontradas = []
for i in range(1):
    solucoes = otimizar(funcaoCusto, limites, numIndividuos, numGeracoes, qntBits)
    print('solucu', solucoes)

    solucoesEncontradas.append(solucoes.copy())
    # se a solução for menor (minimização) que a melhor até o momento, troca
    if(solucoes[-1] < melhorSolucao[-1]):
        melhorSolucao = solucoes.copy()

media = []
for j in range(len(solucoesEncontradas[0])): # para da iteração
    iteracaoAlgoritimo = []
    for i in range(len(solucoesEncontradas)): # para cada execução do pso
        iteracaoAlgoritimo.append(solucoesEncontradas[i][j])
    media.append(np.mean(iteracaoAlgoritimo))

# print(media, '\n\n', melhorSolucao)
x = list(range(0, numGeracoes))
plt.plot(x, melhorSolucao, color='red')
plt.plot(x, media, color='blue')
plt.savefig('resultado.png')

