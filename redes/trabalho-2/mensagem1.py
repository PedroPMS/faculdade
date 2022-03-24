"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem1(Mensagem):

    # Campos da mensagem
    login = None  # String de ate 10 bytes
    senha = None  # String de ate 6 bytes

    def __init__(self):
        self.code = 1
        self.length = 20  # 4+10+6
        self.msgtype = "Auth Request"

    def data(self):
        if(self.login != None and self.senha != None):
            return f"{self.code}, {self.login.decode()}, {self.senha.decode()}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, login, senha):
        self.login = login.encode()
        self.senha = senha.encode()
        msg = struct.pack('!I10s6s', self.code, self.login, self.senha)
        return msg

    def unpack(self, msg):
        code, self.login, self.senha = struct.unpack('!I10s6s', msg)
