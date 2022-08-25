import numpy as np

def carregarDados(nomeArquivo):
    clientes, capacidade, qtdClientes, numVeiculos, resultadoOtimo = carregar(nomeArquivo)

    data = np.array(clientes)
    xcoor = data[:, 1]
    ycoor = data[:, 2]
    demanda = data[:, 3]

    matrixCusto = np.zeros((qtdClientes + 1, qtdClientes + 1))
    for i in range(qtdClientes + 1):
        for j in range(qtdClientes + 1):
            matrixCusto[i][j] = np.sqrt((xcoor[i] - xcoor[j]) ** 2 + (ycoor[i] - ycoor[j]) ** 2)

    return matrixCusto, demanda, xcoor, ycoor, capacidade, numVeiculos, resultadoOtimo

def carregar(nomeArquivo):
    linhasArquivo = []
    with open(nomeArquivo, "r+") as fp:
        while True:
            line = fp.readline()
            if not line:
                break
            linhasArquivo.append(line.strip())

    cabecalho = linhasArquivo[1].split(',')
    numVeiculos = int(cabecalho[1].split(' ')[-1])
    resultadoOtimo = int(cabecalho[2].split(' ')[-1].replace(')', ''))
    qtdClientes = int(linhasArquivo[3].split(' ')[-1])
    capacidade = int(linhasArquivo[5].split(' ')[-1])

    inicioCoordenadas = 7
    inicioDemandas = 40
    clientes = []

    for i in range(inicioCoordenadas, inicioCoordenadas + int(qtdClientes)):
        coordenadas = [int(i) for i in linhasArquivo[i].split()]
        clientes.append(coordenadas)

    for i in range(inicioDemandas, inicioDemandas + int(qtdClientes)):
        demanda = [int(i) for i in linhasArquivo[i].split()]
        clientes[demanda[0]-1].append(demanda[1])

    return clientes, capacidade, qtdClientes - 1, numVeiculos, resultadoOtimo