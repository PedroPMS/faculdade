"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import csv
from sys import getsizeof
import threading
lock = threading.Lock()


def listarPedidosUsuario(login):
    lock.acquire()

    f = open("pedidos.csv")
    csv_f = csv.reader(f, delimiter=';')
    pedidos = []
    for row in csv_f:
        usuarioPedido = row[0]
        if (usuarioPedido != login):
            continue

        pedido = []
        listaPedido = row[2:]
        quantidadeItensPedido = row[1]
        for i in range(int(quantidadeItensPedido)):
            itemPedido = listaPedido[i*3:(i+1)*3]
            itemPedidoFormatado = {
                "produto": itemPedido[0],
                "quantidade": itemPedido[1],
                "valor": itemPedido[2],
            }
            pedido.append(itemPedidoFormatado)
        pedidos.append(pedido)
    f.close()

    lock.release()
    return pedidos


def getTodosPedidos():
    lock.acquire()

    f = open("pedidos.csv")
    csv_f = csv.reader(f, delimiter=';')
    pedidos = []
    for row in csv_f:
        pedido = []
        listaPedido = row[2:]
        login = row[0]
        quantidadeItensPedido = row[1]
        for i in range(int(quantidadeItensPedido)):
            itemPedido = listaPedido[i*3:(i+1)*3]
            itemPedidoFormatado = {
                "produto": itemPedido[0],
                "quantidade": itemPedido[1],
                "valor": itemPedido[2],
            }
            pedido.append(itemPedidoFormatado)
        pedidos.append([login, pedido])

    f.close()
    lock.release()
    return pedidos


def getPedidos(login):
    pedidos = listarPedidosUsuario(login)
    return len(pedidos), pedidos


def imprimirTodosPedidos(pedidos):
    listaFormatada = ("\n{:<10}  {:<10}  {:<10}  {:<10}").format(
        "Pedido", "Produto", "Quantidade", "Valor Unitário")+"\n"
    for i in range(len(pedidos)):
        for item in pedidos[i]:
            listaFormatada += ("{:<10}  {:<10}  {:<10}  R${:<10}".format(
                i, item.get("produto"), item.get("quantidade"), float(item.get("valor"))))+"\n"
    return listaFormatada, getsizeof(listaFormatada)


def getDescricaoPedido(itens):
    listaFormatada = ("\n{:<10}  {:<10}  {:<10}").format(
        "Produto", "Quantidade", "Valor Unitário")+"\n"
    for item in itens:
        listaFormatada += ("{:<10}  {:<10}  R${:<10}".format(
            item.get("produto"), item.get("quantidade"), float(item.get("valor"))))+"\n"
    return listaFormatada, getsizeof(listaFormatada)
