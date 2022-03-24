import socket
import traceback
import struct
import random

import lerProdutos
import criarListaPedido
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

HOST = '127.0.0.1'     # Endereco IP do Servidor
PORT = 3333
BUFFERSIZE = 5120         # Porta que o Servidor esta

# Funcao de envio de da mensagem


def carregarBuffer(socket):
    return socket.recv(BUFFERSIZE)


def enviarMsg(socket, msg):
    print("Mensagem a ser enviada: ", msg)
    socket.send(msg)


def receberMensagemTipo2(buffer):
    msg2 = Mensagem2()
    print("Descrição: ", msg2.description())
    length = msg2.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg2.unpack(msg)

    print(msg2.statusMsg.decode())
    token = msg2.token.decode().rstrip('\x00')
    return token, buffer


def receberMensagemTipo4(buffer):
    msg4 = Mensagem4()

    length = msg4.length
    msg = buffer[:length]
    msg4.getTamanhoListaEmBytes(msg)

    print("Descrição: ", msg4.description())
    length = msg4.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg4.unpack(msg)

    print(msg4.listaPedidos.decode())
    return msg, buffer


def receberMensagemTipo6(buffer):
    msg6 = Mensagem6()

    length = msg6.length
    msg = buffer[:length]
    msg6.getTamanhoLista(msg)

    print("Descrição: ", msg6.description())
    length = msg6.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg6.unpack(msg)

    listaProdutos, listaFormatada = lerProdutos.imprimirTodosProdutosDoBuffer(
        msg6.listaProdutos)
    print(listaFormatada)
    return listaProdutos, msg, buffer


def receberMensagemTipo8(buffer):
    msg8 = Mensagem8()

    length = msg8.length
    msg = buffer[:length]
    msg8.getTamanhoLista(msg)

    print("Descrição: ", msg8.description())
    length = msg8.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg8.unpack(msg)

    listaPedido = [msg8.listaPedido[x:x+3]
                   for x in range(0, msg8.tamanhoLista*3, 3)]
    criarPedido.imprimirItens("Pedido", listaPedido)
    return msg, buffer


def receberMensagemTipo10(buffer):
    msg10 = Mensagem10()
    print("Descrição: ", msg10.description())
    length = msg10.length
    msg = buffer[:length]
    buffer = buffer[length:]
    msg10.unpack(msg)

    mensagem = msg10.mensagem.decode().rstrip('\x00')
    print(mensagem)
    return mensagem, buffer


def recvMsg(socket):
    try:
        buffer = socket.recv(BUFFERSIZE)
        print('inicio', len(buffer))

        while len(buffer) != 0:
            codeData = buffer[:4]  # O código está nos 4 primeiros bytes
            code, = struct.unpack('!I', codeData)
            print("######################################")
            print("Código da mensagem recebida: ", code)

            if code == 2:
                msg, buffer = receberMensagemTipo2(buffer)
            if code == 4:
                msg, buffer = receberMensagemTipo4(buffer)
            if code == 6:
                listaProdutos, msg, buffer = receberMensagemTipo6(buffer)
                msg = listaProdutos
            if code == 8:
                msg, buffer = receberMensagemTipo8(buffer)
            if code == 10:
                msg, buffer = receberMensagemTipo10(buffer)
        return msg

    except Exception as err:
        print(traceback.format_exc())
        return None


def confirmarPedido():
    cmd = input("Confirmar pedido? (1 = Sim; 2 = Não): ")
    if cmd == '1':
        return True
    return False

# Main


def main():
    # Inicio do programa
    tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    dest = (HOST, PORT)
    tcp.connect(dest)
    token = '1'

    # Envia uma mensagem
    print('Para sair use CTRL+X\n')
    login = 'Pedro'  # input("Login: ")
    senha = '123'  # input("Senha: ")
    msg1 = Mensagem1()
    enviarMsg(tcp, msg1.pack(login, senha))
    token = recvMsg(tcp)
    cmd = ''

    while cmd != '\x18' and token != '0':
        msg3 = Mensagem3()
        enviarMsg(tcp, msg3.pack(login, token))
        recvMsg(tcp)

        msg5 = Mensagem5()
        enviarMsg(tcp, msg5.pack(login, token))
        listaProdutos = recvMsg(tcp)

        cmd = 1  # input("Enviar lista de pedido? (1 = Sim; 2 = Não): ")

        if int(cmd) != 1:
            break

        listaPedido = criarListaPedido.criarListaPedido(listaProdutos)
        msg7 = Mensagem7()
        enviarMsg(tcp, msg7.pack(login, token, len(listaPedido), listaPedido))
        recvMsg(tcp)
        isPedidoConfirmado = True  # confirmarPedido()

        msg9 = Mensagem9()
        enviarMsg(tcp, msg9.pack(login, token, isPedidoConfirmado))
        recvMsg(tcp)

        cmd = input("Para sair use CTRL+X: ")

    print("Finalizando conexão...")
    tcp.close()


main()
