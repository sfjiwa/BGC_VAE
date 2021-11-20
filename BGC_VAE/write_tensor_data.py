import os, os.path
import datetime as dt
import numpy as np
from numpy.core.defchararray import join
import pandas as pd
from matplotlib import pyplot as plt
from netCDF4 import Dataset, date2index, num2date, date2num
from torchvision.io import read_image

def WriteData(training=True):

    print("reading data")

    if training:
        data_type = 'training'
    else: data_type = 'test'

    # import input data from /data/

    filenames = os.listdir('data')

    if data_type not in filenames:
        dir_path = os.path.join(os.getcwd(), 'data/' + data_type)
        os.makedirs(dir_path, exist_ok=True)

    if 'training' in filenames: filenames.remove('training')
    if 'test' in filenames: filenames.remove('test')

    data_set = np.empty(len(filenames), dtype=object)
    output = []

    for i in range(0, len(filenames)):

        # get variable id

        var = ''
        for letter in filenames[i]:
            if letter != '_':
                var += letter
            else: break

        if os.path.exists('data/' + data_type + '/' + var + '.npy'):
            continue

        print()
        data_set[i] = Dataset('data/' + filenames[i])

        # input dimensions

        n_t = len(data_set[i].variables['time'])
        n_lat = len(data_set[i].variables['lat'])
        n_lon = len(data_set[i].variables['lon'])
        
        print('processing variable: ' + var)

    # flatten data to dimensions var x (lat*lon)

        data_out = data_set[i].variables[var]
        data_out = np.array(data_out)

    # average over depth if applicable

        for v in data_set[i].variables:
            if v == 'lev':
                depth_avg = np.empty([n_t, n_lat*n_lon])

                for t in range(0, n_t):
                    print('averaging over sea column: ', int(100*t/n_t), '%\r', end='')

                    for lat in range(0, n_lat):
                        for lon in range(0, n_lon):
                            depth_avg[t, lat*n_lon + lon] = data_out[t,:,lat,lon].mean()

                data_out = depth_avg
                break

        data_out = data_out.reshape(n_t, n_lat*n_lon)
        data_out = np.transpose(data_out)

        print('saving input file')

        np.save('data/' + data_type + '/' + var, data_out)

    print("done")