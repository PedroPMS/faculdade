"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva"
Matrículo = "20181BSI0083"
"""

import csv


def atualizarProdutos(produtos):
    f = open("produtos.csv", "w")

    writer = csv.writer(f, delimiter=';')

    for item in produtos:
        writer.writerow(
            [item, produtos[item]['quantidade'], produtos[item]['valor']]
        )

    f.close()
