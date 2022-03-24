"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import lerListaPedido
import lerProdutos
import csv
import threading
lock = threading.Lock()


# Criar lista de pedido e lista com o estoque atualizado


def processarPedido(login, pedido, produtos):
    listaPedido = []
    novoPedido = []
    imprimirItens("Estoque antes", produtos)
    chunks = [pedido[x:x+3] for x in range(0, len(pedido), 3)]
    for itemPedido in chunks:
        produtoId = int(itemPedido[0])
        valorItem = produtos[produtoId][2]
        quantidadePedido = int(itemPedido[1])
        quantidadeEstoque = int(produtos[produtoId][1])
        hasProdutoPedidoNoEstoque = (
            produtoId-1 > len(produtos)) or (quantidadePedido > quantidadeEstoque)

        if(hasProdutoPedidoNoEstoque):
            msg = "Sua lista de pedido está incorreta! Finalizando a conexão..."
            print(msg)
            return False

        item = [produtoId+1, quantidadePedido, valorItem]
        listaPedido.append(item)

        item = {
            "produto": produtoId,
            "quantidade": quantidadePedido,
            "valor": valorItem
        }
        novoPedido.append(item)
    novoPedido = [login, novoPedido]

    return listaPedido


def atualizarProdutos(pedido):
    lock.acquire()
    produtosAtualizados = getListaProdutosAtualizada(pedido)
    f = open("produtos.csv", "w", newline="")

    writer = csv.writer(f, delimiter=';')

    for item in produtosAtualizados:
        writer.writerow(["{:.0f}".format(item[0]),
                        "{:.0f}".format(item[1]), item[2]])

    f.close()
    lock.release()


def getListaProdutosAtualizada(pedido):
    quantidade, produtos = lerProdutos.lerProdutos()
    produtosAtualizados = produtos

    for itemPedido in pedido:
        produtoId = int(itemPedido[0])
        quantidadePedido = int(itemPedido[1])
        quantidadeEstoque = int(produtos[produtoId-1][1])

        produtosAtualizados[produtoId -
                            1][1] = quantidadeEstoque-quantidadePedido

    return produtosAtualizados


def atualizarListaPedidos(login, pedido):
    lock.acquire()

    pedidos = getListaPedidosAtualizada(login, pedido)

    f = open("pedidos.csv", "w", newline="")

    writer = csv.writer(f, delimiter=';')

    for pedido in pedidos:
        login = pedido[0]
        itensPedido = pedido[1]
        linhaCsv = []
        linhaCsv.extend([login, len(itensPedido)])
        for itemPedido in itensPedido:
            linhaCsv.extend([itemPedido.get('produto'), itemPedido.get(
                'quantidade'), itemPedido.get('valor')])
        writer.writerow(linhaCsv)

    f.close()
    lock.release()


def getListaPedidosAtualizada(login, pedido):
    pedidos = lerListaPedido.getTodosPedidos()

    novoPedido = []
    for item in pedido:
        novoItem = {
            "produto": item[0],
            "quantidade": item[1],
            "valor": item[2]
        }
        novoPedido.append(novoItem)
    novoPedidoUsuario = []
    novoPedidoUsuario.extend([login, novoPedido])

    pedidos.append(novoPedidoUsuario)

    return pedidos


def imprimirItens(tipoItem, listaItens):
    print("{}: ".format(tipoItem))
    listaFormatada = ("\n{:<10}  {:<10}  {:<10}").format(
        "Produto", "Quantidade", "Valor Unitário")+"\n"
    for item in listaItens:
        produto = "{:.0f}".format(item[0])
        quantidade = "{:.0f}".format(item[1])
        valor = "{:.2f}".format(item[2])
        listaFormatada += ("{:<10}  {:<10}  R${:<10}".format(
            produto, quantidade, valor))+"\n"
    print(listaFormatada)
