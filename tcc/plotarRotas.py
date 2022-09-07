from matplotlib import pyplot as plt
plt.style.use('bmh')

def vrp_graph(tour, x, y, qntClientes, name):
    plt.figure(figsize=(16, 16), dpi=160)
    plt.plot(x[0], y[0], 'r^')
    plt.scatter(x[1:], y[1:], s=5, c='k', marker=',')
    for i in range(1, qntClientes):
        plt.annotate(i, (x[i] + 0.2, y[i] + 0.2), size=8)
    for i in range(len(tour)):
        plt.plot(x[tour[i]], y[tour[i]])

    plt.savefig(name)