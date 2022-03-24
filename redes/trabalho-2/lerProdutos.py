"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import csv
import threading
lock = threading.Lock()


def lerProdutos():
    lock.acquire()
    f = open("produtos.csv")
    csv_f = csv.reader(f, delimiter=';')
    produtos = []
    for row in csv_f:
        produto = [
            float(row[0]),
            float(row[1]),
            float(row[2])
        ]
        produtos.append(produto)

    lock.release()
    f.close()
    return len(produtos), produtos


def imprimirTodosProdutosDoBuffer(produtos):
    chunks = [produtos[x:x+3] for x in range(0, len(produtos), 3)]
    listaFormatada = ("\n{:<10}  {:<10}  {:<10}").format(
        "Produto", "Quantidade", "Valor Unitário")+"\n"
    listaProdutos = []
    for item in chunks:
        produto = "{:.0f}".format(item[0])
        quantidade = "{:.0f}".format(item[1])
        valor = "{:.2f}".format(item[2])
        listaProdutos.append([produto, quantidade, float(valor)])
        listaFormatada += ("{:<10}  {:<10}  R${:<10}".format(produto,
                           quantidade, valor))+"\n"
    return listaProdutos, listaFormatada
