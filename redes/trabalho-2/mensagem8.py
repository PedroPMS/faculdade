"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem8(Mensagem):

    # Campos da mensagem
    tamanhoLista = None  # Unsigned Integer 4 bytes
    listaPedido = None  # String tamanho indefinido

    def __init__(self):
        self.code = 8
        self.length = 8  # 4+4+indefinido
        self.msgtype = "Reply Confirmação Pedido"

    def setTamanhoLista(self, tamanhoLista):
        # Lista de produto + tamanho de cada item + 4 bytes para float
        self.length = self.length + tamanhoLista*3*4

    def getTamanhoLista(self, msg):
        code, self.tamanhoLista = struct.unpack('!II', msg)
        self.setTamanhoLista(self.tamanhoLista)

    def data(self):
        if(self.tamanhoLista != None and self.listaPedido != None):
            return f"{self.code}, {self.tamanhoLista}, {self.listaPedido}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, tamanhoLista, listaPedido):
        self.tamanhoLista = tamanhoLista
        self.listaPedido = listaPedido
        msg = struct.pack(f"!II{self.tamanhoLista*3}f", self.code,
                          self.tamanhoLista, *(j for i in self.listaPedido for j in i))
        return msg

    def unpack(self, msg):
        unpack = struct.unpack(f"!II{self.tamanhoLista*3}f", msg)
        code = unpack[0]
        self.tamanhoLista = unpack[1]
        self.listaPedido = unpack[2:]
