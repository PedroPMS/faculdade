"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import random
import traceback
import socket
import _thread
import struct

from autenticarUsuario import autenticarUsuario
import lerListaPedido
import lerProdutos
import criarPedido
from mensagem1 import Mensagem1
from mensagem2 import Mensagem2
from mensagem3 import Mensagem3
from mensagem4 import Mensagem4
from mensagem5 import Mensagem5
from mensagem6 import Mensagem6
from mensagem7 import Mensagem7
from mensagem8 import Mensagem8
from mensagem9 import Mensagem9
from mensagem10 import Mensagem10

HOST = ''              # Endereco IP do Servidor
PORT = 3333            # Porta que o Servidor esta
BUFFERSIZE = 5120


def recvMsg(socket, cliente, pedido):
    quantidadeProdutos, produtos = lerProdutos.lerProdutos()
    novoPedido = []
    try:
        buffer = socket.recv(BUFFERSIZE)
        msg = None
        print("######################################")
        print("Buffer: ", cliente, ": ", buffer)

        while len(buffer) != 0:
            codeData = buffer[:4]  # O código está nos 4 primeiros bytes
            code, = struct.unpack('!I', codeData)
            print("######################################")
            print("Código da mensagem recebida: ", cliente, ": ", code)

            if code == 1:
                isAutenticado, msg, buffer = receberMensagemTipo1(
                    buffer, cliente)
                msg = enviarMensagemTipo2(socket, isAutenticado)
            elif code == 3:
                login, msg, buffer = receberMensagemTipo3(buffer, cliente)
                msg = enviarMensagemTipo4(socket, login)
            elif code == 5:
                msg, buffer = receberMensagemTipo5(buffer, cliente)
                msg = enviarMensagemTipo6(socket, quantidadeProdutos, produtos)
            elif code == 7:
                novoPedido, msg, buffer = receberMensagemTipo7(
                    buffer, cliente, produtos)
                msg = enviarMensagemTipo8(socket, novoPedido)
            elif code == 9:
                isPedidoConfirmado, login, msg, buffer = receberMensagemTipo9(
                    buffer, cliente)
                persistirDados(login, pedido)
                msg = enviarMensagemTipo10(socket, isPedidoConfirmado)

        return msg, novoPedido

    except Exception as err:
        print(traceback.format_exc())
        return None


def persistirDados(login, pedido):
    criarPedido.atualizarListaPedidos(login, pedido)
    criarPedido.atualizarProdutos(pedido)


def enviarMensagemTipo10(con, isPedidoConfirmado):
    mensagem = "Pedido cancelado!"
    if(isPedidoConfirmado == True):
        mensagem = "Pedido confimado. Obrigado!"
    msg10 = Mensagem10()
    enviarMsg(con, msg10.pack(mensagem))
    return isPedidoConfirmado


def enviarMensagemTipo8(con, pedido):
    msg8 = Mensagem8()
    enviarMsg(con, msg8.pack(len(pedido), pedido))
    return pedido


def enviarMensagemTipo6(con, quantidadeProdutos, produtos):
    msg6 = Mensagem6()
    enviarMsg(con, msg6.pack(quantidadeProdutos, produtos))
    return produtos


def enviarMensagemTipo4(con, login):
    quantidadePedidos, pedidos = lerListaPedido.getPedidos(login)
    listaFormatada, tamanhoListaEmBytes = lerListaPedido.imprimirTodosPedidos(
        pedidos)
    msg4 = Mensagem4()
    msg4.setTamanhoListaEmBytes(tamanhoListaEmBytes)
    enviarMsg(con, msg4.pack(quantidadePedidos, listaFormatada))
    return listaFormatada


def enviarMensagemTipo2(con, isAutenticado):
    statusCode = 2
    statusMsg = "Usuário ou senha inválidos! Você foi desconectado!"
    token = '0'
    msg2 = Mensagem2()
    msg = None

    if(isAutenticado == True):
        statusCode = 1
        statusMsg = "Usuário autenticado!"
        msg = statusMsg
        token = str(random.randint(10000, 99999))

    enviarMsg(con, msg2.pack(statusCode, statusMsg, token))

    return msg


def receberMensagemTipo1(buffer, cliente):
    msg1 = Mensagem1()
    print("Descrição: ", cliente, ": ", msg1.description())
    length = msg1.length
    msg = buffer[: length]
    buffer = buffer[length:]
    msg1.unpack(msg)

    login, senha = msg1.login.decode().rstrip(
        '\x00'), msg1.senha.decode().rstrip('\x00')

    return autenticarUsuario(login, senha), msg, buffer


def receberMensagemTipo3(buffer, cliente):
    msg3 = Mensagem3()
    print("Descrição: ", cliente, ": ", msg3.description())
    length = msg3.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg3.unpack(msg)
    print("Mensagem decodificada: ", cliente, ": ", msg3.data())
    print("######################################")

    return msg3.getLogin(), msg, buffer


def receberMensagemTipo5(buffer, cliente):
    msg5 = Mensagem5()
    print("Descrição: ", cliente, ": ", msg5.description())
    length = msg5.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg5.unpack(msg)
    print("Mensagem decodificada: ", cliente, ": ", msg5.data())
    print("######################################")

    return msg, buffer


def receberMensagemTipo7(buffer, cliente, produtos):
    msg7 = Mensagem7()

    length = msg7.length
    msg = buffer[:length]
    msg7.getTamanhoLista(msg)

    print("Descrição: ", cliente, ": ", msg7.description())
    length = msg7.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg7.unpack(msg)

    listaPedido = criarPedido.processarPedido(
        msg7.login, msg7.listaPedido, produtos)
    return listaPedido, msg, buffer


def receberMensagemTipo9(buffer, cliente):
    msg9 = Mensagem9()
    print("Descrição: ", cliente, ": ", msg9.description())
    length = msg9.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg9.unpack(msg)
    print("Mensagem decodificada: ", cliente, ": ", msg9.data())
    print("######################################")

    return msg9.isPedidoConfirmado, msg9.login.decode().rstrip('\x00'), msg, buffer


def enviarMsg(con, msg):
    if (type(msg) is str):
        msg = msg.encode()
    con.send(msg)


def conectado(con, cliente):
    print("Conectado ao cliente: ", cliente)
    pedido = []
    while True:
        msg, novoPedido = recvMsg(con, cliente, pedido)
        if(len(novoPedido)):
            pedido = novoPedido

        if not msg:
            break

    print("Cliente desconectado: ", cliente)
    con.close()
    _thread.exit()

# Main


def main():
    # Inicio da execucao do programa
    print("Servidor iniciado")
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    orig = (HOST, PORT)
    tcp.bind(orig)
    tcp.listen(1)
    while True:
        con, cliente = tcp.accept()
        # Ler: https://realpython.com/intro-to-python-threading/
        _thread.start_new_thread(conectado, tuple([con, cliente]))

    tcp.close()


main()
