import numpy as np
import random
from pprint import pprint
import matplotlib.pyplot as plt

class Particula:
    def __init__(self, inicio):
        self.posicaoAtual=[]    # posicaoAtual da particula
        self.velocidade=[]      # velocidade da particula
        self.melhorPosicao=[]   # melhor posicaoAtual da particula
        self.melhorCusto=-1      # melhor custoAtual da particula
        self.custoAtual=-1       # custoAtual da particula

        for i in range(0, numDimensoes):
            self.velocidade.append(random.uniform(-1,1))
            self.posicaoAtual.append(inicio[i])

    # calcular fitness atual
    def calcularFitness(self,costFunc):
        self.custoAtual = costFunc(self.posicaoAtual)

        # veifica se a posição atual é a melhor posição da particula
        if (self.custoAtual < self.melhorCusto or self.melhorCusto == -1):
            self.melhorPosicao = self.posicaoAtual.copy()
            self.melhorCusto = self.custoAtual

    # atualiza a velocidade da particula
    def atualizarVelocidade(self,melhorPosicaoBando):
        w = 0.5       # peso de inecia
        c1 = 1        # peso individual
        c2 = 2        # peso do bando

        for i in range(0, numDimensoes):
            r1 = random.random()
            r2 = random.random()

            velocidadeIndividuo = c1 * r1 * (self.melhorPosicao[i] - self.posicaoAtual[i])
            velocidadeBando = c2 * r2 *(melhorPosicaoBando[i] - self.posicaoAtual[i])
            self.velocidade[i] = w * self.velocidade[i] + velocidadeIndividuo + velocidadeBando

    # atualiza a posição da particula baseada nas novas velocidades
    def atualizarPosicao(self, limites):
        for i in range(0, numDimensoes):
            self.posicaoAtual[i] = self.posicaoAtual[i] + self.velocidade[i]

            # retona a particula para os limites se necessários
            if (self.posicaoAtual[i] > limites[i][1]):
                self.posicaoAtual[i] = limites[i][1]

            # retona a particula para os limites se necessário
            if (self.posicaoAtual[i] < limites[i][0]):
                self.posicaoAtual[i] = limites[i][0]


def otimizar(costFunc, limites, numParticulas, numIteracoes, verbose=True):
    solucoes = []
    medias = []
    melhorCustoBando = -1
    melhorPosicaoBando = []
    limitX = limites[0]
    limiteY = limites[1]

    enxame = []
    for i in range(0, numParticulas):
        x = random.randint(limitX[0], limitX[1])
        y = random.randint(limiteY[0], limiteY[1])
        enxame.append(Particula([x, y]))

    i=0
    while i < numIteracoes:
        solucoes.append(melhorCustoBando)
        medias.append(np.mean(solucoes))
        if verbose:
            print(f'Itereção: {i:>4d}, Melhor Solução: {melhorCustoBando:10.6f}')

        # calcula o fitness de cada particula
        for j in range(0, numParticulas):
            enxame[j].calcularFitness(costFunc)

            # verifica se a particula atual é a melhor do bando
            if (enxame[j].custoAtual < melhorCustoBando) or (melhorCustoBando == -1):
                melhorPosicaoBando = list(enxame[j].posicaoAtual)
                melhorCustoBando = float(enxame[j].custoAtual)

        # atualiza as velocidade e posição de cada particula
        for j in range(0, numParticulas):
            enxame[j].atualizarVelocidade(melhorPosicaoBando)
            enxame[j].atualizarPosicao(limites)
        i+=1

    if verbose:
        x = list(range(0, numIteracoes))
        print('\nSOLUÇÃO FINAL:')
        print(f'   > Melhor Posição {melhorPosicaoBando}')
        print(f'   > Melhor Resultado {melhorCustoBando}')
        plt.plot(x, solucoes, color='red')
        plt.plot(x, medias, color='blue')
        plt.savefig('rodadapso.png')

    return melhorCustoBando, melhorPosicaoBando, solucoes

def eggholder(x):
    x_ = x[0]
    y_ = x[1]

    return -(y_ + 47) * np.sin(np.sqrt(np.abs((x_ / 2) + y_ + 47))) - x_ * np.sin(np.sqrt(np.abs(x_ - (y_ + 47))))

###################### iniciar ######################
limite = [(-512,512),(-512,512)]
numDimensoes = len(limite)
numParticulas = 50
numIteracoes = 20

melhorSolucao = [0]
solucoesEncontradas = []
for i in range(10):
    melhorCustoBando, melhorPosicaoBando, solucoes = otimizar(eggholder, limite, numParticulas, numIteracoes, verbose=False)

    solucoesEncontradas.append(solucoes.copy())
    # se a solução for menor (minimização) que a melhor até o momento, troca
    if(solucoes[-1] < melhorSolucao[-1]):
        melhorSolucao = solucoes.copy()

media = []
for j in range(len(solucoesEncontradas[0])): # para da iteração
    iteracaoPso = []
    for i in range(len(solucoesEncontradas)): # para cada execução do pso
        iteracaoPso.append(solucoesEncontradas[i][j])
    media.append(np.mean(iteracaoPso))

print(media, '\n\n', melhorSolucao)
x = list(range(0, numIteracoes))
plt.plot(x, melhorSolucao, color='red')
plt.plot(x, media, color='blue')
plt.savefig('resultado.png')