import os
import numpy as np

def carregarDados():
    cust_size = 31
    file_name = os.path.join('teste.csv')
    data = np.genfromtxt(file_name, delimiter=',')
    df = data[1:cust_size + 2]
    xcoor = df[:, 1]
    ycoor = df[:, 2]
    demand = df[:, 3]

    dist_matrix = np.zeros((cust_size + 1, cust_size + 1))
    for i in range(cust_size + 1):
        for j in range(cust_size + 1):
            dist_matrix[i][j] = np.sqrt((xcoor[i] - xcoor[j]) ** 2 + (ycoor[i] - ycoor[j]) ** 2)
    return dist_matrix, demand, xcoor, ycoor

carregarDados()