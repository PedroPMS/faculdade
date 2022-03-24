"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem5(Mensagem):

    # Campos da mensagem
    login = None  # String de ate 10 bytes
    token = None  # String de ate 20 bytes

    def __init__(self):
        self.code = 5
        self.length = 34  # 4+10+20
        self.msgtype = "Get Lista Estoque"

    def data(self):
        if(self.login != None and self.token != None):
            return f"{self.code}, {self.login.decode()}, {self.token.decode()}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, login, token):
        self.login = login.encode()
        self.token = token.encode()
        msg = struct.pack('!I10s20s', self.code, self.login, self.token)
        return msg

    def unpack(self, msg):
        code, self.login, self.token = struct.unpack('!I10s20s', msg)
