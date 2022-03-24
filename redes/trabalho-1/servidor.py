"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva"
Matrículo = "20181BSI0083"
"""

# ------------------------------------------------------------------
# Aplicacao Servidor
# ------------------------------------------------------------------

import lerProdutos
import atualizarProdutos
import socket
import json


HOST = "127.0.0.1"      # Endereco IP do Servidor e o endereco atual do computador
# Porta que o Servidor esta usando (identifica qual a aplicacao)
PORT = 5000
BYTES_BY_MSG = 1024     # Numero de bytes que recebe por mensagem
CODING = "utf-8"        # Codificacao utilizada para comunicacao


# Identificac se o usuário é um Cliente ou Fornecedor
def identificar(con, cliente):
    msg_recv = con.recv(BYTES_BY_MSG)
    msg_recv = msg_recv.decode(CODING)
    if not msg_recv:
        return False
    print(cliente, "Cliente: "+msg_recv)

    msg = "Olá, por favor identifique-se (Cliente ou Fornecedor)!"
    print("~"+msg)
    msg = msg.encode(CODING)
    con.send(msg)

    # Identificar usuário
    msg_recv = con.recv(BYTES_BY_MSG)
    nome = msg_recv.decode(CODING)
    if(nome != "Cliente" and nome != "Fornecedor"):
        msg = "Esse tipo de cliente não é valido! Finalizando a conexão..."
        print("~"+msg)
        msg = msg.encode(CODING)
        con.send(msg)
        return False
    print(cliente, "Cliente: "+nome)

    return nome


def enviarListaProdutos(con):
    # Enviar a lista de produtos para o cliente/fornecedor
    produtos = lerProdutos.lerProdutos()
    msg = produtos.encode(CODING)
    con.send(msg)
    return produtos


# Retorna a quantidade de itens do produto atualizada
def tipoClienteatualizarQuantidadeItemEstoque(tipoCliente, itemEstoque, itemPedido):
    if(tipoCliente == "Cliente"):
        return str(int(itemEstoque) - int(itemPedido))
    return str(int(itemEstoque) + int(itemPedido))


# Criar lista de pedido e lista com o estoque atualizado
def processarPedido(con, tipoCliente, pedido, produtos):
    produtosAtualizados = produtos
    pedido = json.loads(pedido)
    listaPedido = {}
    imprimirItens("Estoque antes", produtos)
    for itemPedido in pedido:
        if((itemPedido not in produtos) or (int(pedido[itemPedido]) > int(produtos[itemPedido]["quantidade"]) and tipoCliente == "Cliente")):
            msg = "Sua lista de pedido está incorreta! Finalizando a conexão..."
            msg = msg.encode(CODING)
            con.send(msg)
            return False, False

        estoqueItem = produtos[itemPedido]["quantidade"]
        pedidoItem = pedido[itemPedido]
        produtosAtualizados[itemPedido]["quantidade"] = tipoClienteatualizarQuantidadeItemEstoque(
            tipoCliente, estoqueItem, pedidoItem
        )

        listaPedido[itemPedido] = {
            "quantidade": str(pedidoItem),
            "valor": produtos[itemPedido]["valor"]
        }

    return listaPedido, produtosAtualizados


def imprimirItens(tipoItem, listaItens):
    print("{}: ".format(tipoItem))
    listaFormatada = ("\n{:<10}  {:<10}  {:<10}").format(
        "Produto", "Quantidade", "Valor Unitário")+"\n"
    for item in listaItens:
        listaFormatada += ("{:<10}  {:<10}  R${:<10}".format(
            item, listaItens[item]["quantidade"], listaItens[item]["valor"]))+"\n"
    print(listaFormatada)


def finalizarConexao(con, cliente):
    # Fecha a conexao com o cliente
    print("Finalizando conexao com o cliente", cliente)
    con.close()


def main():
    # Cria o socket do servidor
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)     # Forma a tupla de host, porta

    tcp.bind(orig)		# Solicita ao S.O. acesso exclusivo a porta 5000
    tcp.listen(10)		# Entra no modo de escuta

    print("Aguardando...")

    # ------- inicio do protocolo --------------
    while True:
        con, cliente = tcp.accept()  # Aceita conexao do cliente
        print("Conectado com", cliente)

        # Identificar o tipo de cliente conectado
        tipoCliente = identificar(con, cliente)
        if(tipoCliente == False):
            finalizarConexao(con, cliente)
            continue

        # Enviar lista de produtos para o cliente TCP
        produtos = enviarListaProdutos(con)
        produtos = json.loads(produtos)

        # Lista de pedidos
        pedido = con.recv(BYTES_BY_MSG)
        pedido = pedido.decode(CODING)
        print(cliente, "Cliente: ", pedido)

        listaPedido, produtosAtualizados = processarPedido(
            con, tipoCliente, pedido, produtos
        )
        if(listaPedido == False):
            finalizarConexao(con, cliente)
            continue

        # Enviar lista de produtos processada e pede confirmação do cliente
        msg = json.dumps(listaPedido)
        msg = msg.encode(CODING)
        con.send(msg)

        # Confirmação
        msg_recv = con.recv(BYTES_BY_MSG)
        confirmacao = msg_recv.decode(CODING)
        if(confirmacao == "N"):
            msg = "Pedido negado, finalizando conexão..."
            msg = msg.encode(CODING)
            con.send(msg)
            finalizarConexao(con, cliente)
            continue

        # Imprime pedido e estoque
        imprimirItens("Lista pedido", listaPedido)
        imprimirItens("Estoque depois", produtosAtualizados)

        # Atualizar estoque
        atualizarProdutos.atualizarProdutos(produtosAtualizados)

        msg = "Pedido confirmado! Obrigado!"
        msg = msg.encode(CODING)
        con.send(msg)

        print("Finalizando conexao com o cliente", cliente)
        con.close()		# fecha a conexao com o cliente

    # ---------------- fim do protocolo --------------


# ------- Início do programa ---------
if __name__ == "__main__":
    exit(main())
