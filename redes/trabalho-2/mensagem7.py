"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem7(Mensagem):

    # Campos da mensagem
    login = None  # String de ate 10 bytes
    token = None  # String de ate 20 bytes
    tamanhoLista = None  # Unsigned Integer 4 bytes
    listaPedido = None  # String tamanho indefinido

    def __init__(self):
        self.code = 7
        self.length = 38  # 10+20+4+4+indefinido
        self.msgtype = "Send Pedido"

    def setTamanhoLista(self, tamanhoLista):
        # Lista de produto + tamanho de cada item + 4 bytes para float
        self.length = self.length + tamanhoLista*3*4

    def getTamanhoLista(self, msg):
        code, self.login, self.token, self.tamanhoLista = struct.unpack(
            '!I10s20sI', msg)
        self.setTamanhoLista(self.tamanhoLista)

    def data(self):
        if(self.login != None and self.token != None and self.tamanhoLista != None and self.listaPedido != None):
            return f"{self.code}, {self.login}, {self.token}, {self.tamanhoLista}, {self.listaPedido}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, login, token, tamanhoLista, listaPedido):
        self.login = login
        self.token = token
        self.tamanhoLista = tamanhoLista
        self.listaPedido = listaPedido
        msg = struct.pack(f"!I10s20sI{self.tamanhoLista*3}f", self.code, self.login.encode(),
                          self.token.encode(), self.tamanhoLista, *(j for i in self.listaPedido for j in i))
        return msg

    def unpack(self, msg):
        unpack = struct.unpack(f"!I10s20sI{self.tamanhoLista*3}f", msg)
        code = unpack[0]
        self.login = unpack[1].decode().rstrip('\x00')
        self.token = unpack[2].decode().rstrip('\x00')
        self.tamanhoLista = unpack[3]
        self.listaPedido = unpack[4:]
        print(self.listaPedido)
