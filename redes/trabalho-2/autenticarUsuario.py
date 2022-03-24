"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva" e "Aline Bravin Prasser"
Matrícula = "20181BSI0083" e "20181BSI0210"
"""

import csv


def lerUsuarios():
    f = open("usuarios.csv")
    csv_f = csv.reader(f, delimiter=';')
    produtos = {}
    for row in csv_f:
        produtos[row[0]] = row[1]
    return produtos


def autenticarUsuario(login, senhaEnviada):
    usuarios = lerUsuarios()
    senha = usuarios.get(login)

    if (senha == None):
        return False

    return senha == senhaEnviada
