import numpy as np
import matplotlib
from matplotlib import pyplot as plt

def Plot(data_path, time):

    data = np.load(data_path)
    data = data[:, time]

    # for i in range(0, len(data)):
    #     if data[i] > 10^19:
    #         data[i] = 0

    data = data.reshape(180, int(len(data)/180))
    data = np.flip(data, 0)

    plt.rcParams["figure.figsize"] = [7.00, 3.50]
    plt.rcParams["figure.autolayout"] = True
    im = plt.imshow(data, cmap="ocean")
    plt.colorbar(im)
    plt.show()
    