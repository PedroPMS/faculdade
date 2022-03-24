"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import struct

from mensagem import *


class Mensagem4(Mensagem):

    # Campos da mensagem
    tamanhoLista = None  # inteiro de 4 bytes sem sinal
    tamanhoListaEmBytes = None  # inteiro de 4 bytes sem sinal
    listaPedidos = None  # String de tamanho indefinido

    def __init__(self):
        self.code = 4
        self.length = 12  # 4+4+4+indefinido
        self.msgtype = "Get Lista Pedidos"

    def setTamanhoListaEmBytes(self, tamanhoListaEmBytes):
        self.tamanhoListaEmBytes = tamanhoListaEmBytes
        self.length = self.length + tamanhoListaEmBytes

    def getTamanhoListaEmBytes(self, msg):
        code, self.tamanhoLista, self.tamanhoListaEmBytes = struct.unpack(
            '!III', msg)
        self.setTamanhoListaEmBytes(self.tamanhoListaEmBytes)

    def data(self):
        if(self.tamanhoLista != None and self.listaPedidos != None):
            return f"{self.code}, {self.tamanhoLista}, {self.listaPedidos.decode()}"
        else:
            return "Mensagem não inicializada"

    # ! network (= big-endian)
    # I unsigned int integer 4 bytes
    # H unsigned short integer 2  bytes
    # h short integer 2  bytes
    # s char[] bytes
    # Funcao de empacotamento de mensagem
    def pack(self, tamanhoLista, listaPedidos):
        self.tamanhoLista = tamanhoLista
        self.listaPedidos = listaPedidos.encode()
        msg = struct.pack(f"!III{self.tamanhoListaEmBytes}s",
                          self.code, self.tamanhoLista, self.tamanhoListaEmBytes, self.listaPedidos)
        return msg

    def unpack(self, msg):
        code, self.tamanhoLista, self.tamanhoListaEmBytes, self.listaPedidos = struct.unpack(
            f"!III{self.tamanhoListaEmBytes}s", msg)

    def getLogin(self):
        return self.login.decode().rstrip('\x00')
