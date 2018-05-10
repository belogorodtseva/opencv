import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import numpy

numpy.random.seed(29)


z = ['sadness', 'neutral', 'contempt', 'disgust', 'anger', 'surprise', 'fear', 'happiness']
x = [0.0, 0.5, 0.0, 0.5, 1.0, 0.5, 1.0]
y = [1, 2, 3, 4, 5, 4, 5]
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(x, y, z, zdir='z', c= 'blue')
plt.show()
plt.savefig("demo.png")
