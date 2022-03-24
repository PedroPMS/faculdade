"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""


class Mensagem():
    code = None  # inteiro de 4 bytes sem sinal
    length = None  # quantidade de bytes da mensagem
    msgtype = None  # tipo da mensagem

    def __init__(self):
        self.code = 0
        self.msgtype = ""
        self.length = 0

    def length(self):
        return self.length

    def description(self):
        return f"Código: {self.code} - Tipo: {self.msgtype} - Tamanho: {self.length}"

    def data(self):
        pass

    def unpack(self):
        pass
