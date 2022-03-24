"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem10(Mensagem):

    # Campos da mensagem
    mensagem = None  # String até 30 bytes

    def __init__(self):
        self.code = 10
        self.length = 35  # 4+30
        self.msgtype = "Reply Confimar Pedido"

    def data(self):
        if(self.mensagem != None):
            return f"{self.code}, {self.mensagem.decode()}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, mensagem):
        self.mensagem = mensagem.encode()
        msg = struct.pack('!I30s', self.code, self.mensagem)
        return msg

    def unpack(self, msg):
        code, self.mensagem = struct.unpack('!I30s', msg)
