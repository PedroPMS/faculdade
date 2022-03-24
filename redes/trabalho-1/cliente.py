"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva"
Matrículo = "20181BSI0083"
"""

# ------------------------------------------------------------------
# Aplicacao Cliente
# ------------------------------------------------------------------

import socket
import json
import random

HOST = "127.0.0.1"     # Endereco IP do Servidor (loopback)
# Porta que o Servidor esta usando (identifica qual a aplicacao)
PORT = 5000
BYTES_BY_MSG = 1024     # Numero de bytes que recebe por mensagem
CODING = "utf-8"        # Codificacao utilizada para comunicacao


# Cria um pedido com produtos válidos
def criarListaProdutos(produtos, tipoCliente):
    listaProdutos = {}
    listaChaves = map(int, produtos.keys())
    numeroProdutos = max(listaChaves)

    # Enquanto a lista do pedido for menor que 5
    while len(listaProdutos) < 5:
        # Escolhe um produto aleatoriamente
        produto = random.randint(1, numeroProdutos)
        quantidadeProduto = int(produtos[str(produto)]["quantidade"])

        # Se o produto já existe na lista do pedido, pula para a próxima iteração
        if produto in listaProdutos:
            continue

        # Se o usuário for um Cliente, verifica se o produto tem estoque
        if tipoCliente == 'Cliente' and quantidadeProduto == 0:
            continue
        # Se for Fornecedor, escolhe uma quantidade entre 1 e 200
        if tipoCliente == 'Fornecedor':
            quantidadeProduto = random.randint(1, 200)

        # Inseri o item e a quantidade na lista de pedido
        listaProdutos[str(produto)] = quantidadeProduto if quantidadeProduto == 1 else random.randint(
            1, quantidadeProduto)
    return listaProdutos


# Imprime a lista com o pedido do usuário
def imprimirPedido(pedido, tipoCliente):
    if(tipoCliente == "Cliente"):
        print("Compra")
    else:
        print("Venda")

    valorTotal = 0
    pedido = json.loads(pedido)
    for itemPedido in pedido:
        valorTotal += float(pedido[itemPedido]["valor"]) * \
            int(pedido[itemPedido]["quantidade"])

        print("Produto: {} Quantidade: {} Valor Unitário: R${:.2f}".format(
            itemPedido, pedido[itemPedido]["quantidade"], float(pedido[itemPedido]["valor"])))
    print("Valor total: R${:.2f}".format(valorTotal))


def protocoloPedido(tcp, dest):
    msg_dest = "Bom dia!"
    print(msg_dest)
    msg_dest = msg_dest.encode(CODING)
    tcp.send(msg_dest)

    # Olá, por favor identifique-se (Cliente ou Fornecedor)!
    msg_recv = tcp.recv(BYTES_BY_MSG)
    msg_recv = msg_recv.decode(CODING)
    print(dest, "Servidor: "+msg_recv)

    tipoCliente = input("~")
    msg_dest = tipoCliente
    msg_dest = msg_dest.encode(CODING)
    tcp.send(msg_dest)

    # Receber Lista de produtos
    msg_recv = tcp.recv(BYTES_BY_MSG)
    msg_recv = msg_recv.decode(CODING)
    if "Finalizando a conexão..." in msg_recv:
        print("~", msg_recv)
        return
    produtos = json.loads(msg_recv)
    listaProdutos = criarListaProdutos(produtos, tipoCliente)

    # Enviar lista de produtos
    print("~", listaProdutos)
    msg_dest = json.dumps(listaProdutos)
    msg_dest = msg_dest.encode(CODING)
    tcp.send(msg_dest)

    # Receber confirmação do pedido
    msg_recv = tcp.recv(BYTES_BY_MSG)
    msg_recv = msg_recv.decode(CODING)
    if "Finalizando a conexão..." in msg_recv:
        print("~", msg_recv)
        return
    imprimirPedido(msg_recv, tipoCliente)

    # Confirmar pedido
    msg_dest = "S"
    print("~", msg_dest)
    msg_dest = msg_dest.encode(CODING)
    tcp.send(msg_dest)

    # Mensagem finalizando o pedido
    msg_recv = tcp.recv(BYTES_BY_MSG)
    msg_recv = msg_recv.decode(CODING)
    print(dest, "Servidor: "+msg_recv)


def main():
    # Cria o socket do cliente
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)    # Forma a tupla de host, porta

    tcp.connect(dest)      # Estabelece a conexao
    print("Pressione ENTER para mensagem seguinte.")

    # ---------------- inicio protocolo --------------
    protocoloPedido(tcp, dest)

    print("Finalizando conexao com o servidor")

    # ---------------- fim do protocolo --------------

    tcp.close()  # fecha a conexao com o servidor


# ------- Início do programa ---------
if __name__ == "__main__":
    exit(main())
