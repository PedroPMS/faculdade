"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva"
Matrículo = "20181BSI0083"
"""

import csv
import json


def lerProdutos():
    f = open("produtos.csv")
    csv_f = csv.reader(f, delimiter=';')
    produtos = {}
    for row in csv_f:
        produto = {
            "quantidade": row[1],
            "valor": row[2]
        }
        produtos[row[0]] = produto
    return json.dumps(produtos)
