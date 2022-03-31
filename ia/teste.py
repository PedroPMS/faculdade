import numpy as np
from matplotlib import pyplot as plt
from matplotlib import colors

matrix = np.loadtxt('matrix.txt').astype(int)

cmap = colors.ListedColormap(['white', 'black', 'green', 'blue', 'red'])
bounds=[0,1,2,3,8,9]
norm = colors.BoundaryNorm(bounds, cmap.N)

# tell imshow about color map so that only set colors are used
plt.imshow(matrix, interpolation='nearest', cmap=cmap, norm=norm)

# plt.imshow(matrix, interpolation='nearest')
plt.savefig('teste.png')