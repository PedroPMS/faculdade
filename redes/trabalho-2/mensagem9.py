"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem9(Mensagem):

    # Campos da mensagem
    login = None  # String de ate 10 bytes
    token = None  # String de ate 20 bytes
    isPedidoConfirmado = None  # Bool 1 byte

    def __init__(self):
        self.code = 9
        self.length = 35  # 4+10+20+1
        self.msgtype = "Confimar Pedido"

    def data(self):
        if(self.login != None and self.token != None and self.isPedidoConfirmado != None):
            return f"{self.code}, {self.login.decode()}, {self.token.decode()}, {self.isPedidoConfirmado}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, login, token, isPedidoConfirmado):
        self.login = login.encode()
        self.token = token.encode()
        self.isPedidoConfirmado = isPedidoConfirmado
        msg = struct.pack('!I10s20s?', self.code, self.login,
                          self.token, self.isPedidoConfirmado)
        return msg

    def unpack(self, msg):
        code, self.login, self.token, self.isPedidoConfirmado = struct.unpack(
            '!I10s20s?', msg)
