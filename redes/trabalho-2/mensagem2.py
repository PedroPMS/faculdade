"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem2(Mensagem):

    # Campos da mensagem
    statusCode = None  # inteiro de 4 bytes sem sinal
    statusMsg = None  # String de ate 20 bytes
    token = None  # String de ate 20 bytes

    def __init__(self):
        self.code = 2
        self.length = 88  # 4+4+60+20
        self.msgtype = "Auth Reply"

    def data(self):
        if(self.statusCode != None and self.statusMsg != None):
            return f"{self.code}, {self.statusCode}, {self.statusMsg.decode()}, {self.token.decode()}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, statusCode, statusMsg, token):
        self.statusCode = statusCode
        self.statusMsg = statusMsg.encode()
        self.token = token.encode()
        msg = struct.pack('!II53s20s', self.code,
                          self.statusCode, self.statusMsg, self.token)
        return msg

    def unpack(self, msg):
        code, self.statusCode, self.statusMsg, self.token = struct.unpack(
            '!II53s20s', msg)
