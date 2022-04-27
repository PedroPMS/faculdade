import pyswarms as ps
from pyswarms.utils.functions import single_obj as fx
import matplotlib.pyplot as plt
from pyswarms.utils.plotters import plot_contour, plot_surface
from pyswarms.utils.plotters.formatters import Designer
from pyswarms.utils.plotters.formatters import Mesher
import numpy as np

# teste = [512, 404.3219] * np.ones(shape=(3, 2))
# func = fx.eggholder(teste)

options = {'c1': 0.5, 'c2': 0.3, 'w':0.9}
# Call instance of PSO
optimizer = ps.single.GlobalBestPSO(n_particles=10, dimensions=2, options=options)
# Perform optimization
cost, pos = optimizer.optimize(fx.eggholder, iters=1000)

# d = Designer(limits=[(-512,512), (-512,512)], label=['x-axis', 'y-axis'])
# m = Mesher(func=fx.eggholder)
# # Make animation
# animation = plot_contour(pos_history=optimizer.pos_history, designer=d,mesher=m,mark=(0,0)) # Mark minima
# animation.save('teste.gif')

# preprocessing
# pos_history_3d = m.compute_history_3d(optimizer.pos_history)
# # adjust the figure

# # Make animation
# animation3d = plot_surface(pos_history=pos_history_3d, mesher=m, designer=d, mark=(0,0))  # Mark minima
# animation3d.save('3d.gif')