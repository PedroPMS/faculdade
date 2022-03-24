"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import random


def criarListaPedido(produtos):
    listaPedido = []
    produtosNaLista = []
    numeroProdutos = len(produtos)

    # Enquanto a lista do pedido for menor que 5
    while len(listaPedido) < 5:
        # Escolhe um produto aleatoriamente
        produto = random.randint(1, numeroProdutos - 1)
        quantidadeProduto = int(produtos[produto][1])

        # Se o produto já existe na lista do pedido, pula para a próxima iteração e verifica se o produto tem estoque
        if produto in produtosNaLista or quantidadeProduto == 0:
            continue

        # Escolhe a quantidade do produto no pedido
        quantidadePedido = quantidadeProduto if quantidadeProduto == 1 else random.randint(
            1, quantidadeProduto)

        # Inseri o item na lista de já pedidos
        produtosNaLista.append(produto)
        listaPedido.append([produto, quantidadePedido, produtos[produto][2]])
    return listaPedido
