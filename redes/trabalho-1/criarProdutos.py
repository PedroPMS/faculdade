"""
Disciplina de Redes de Computadores
Semestre: 2021/2
Trabalho = "Loja de Produtos Esportivos"
Nome = "Pedro Paulo Mauro e Silva"
Matrículo = "20181BSI0083"
"""

import csv
import random

with open('produtos.csv', mode='w') as produtos:
    produtosWriter = csv.writer(
        produtos, delimiter=';', quotechar='"', quoting=csv.QUOTE_MINIMAL)

    for i in range(20):
        quantidade = random.randint(0, 100)
        valor = round(random.uniform(10, 150), 2)
        produtosWriter.writerow([i + 1, quantidade, valor])
