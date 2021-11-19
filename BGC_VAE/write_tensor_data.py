import datetime as dt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from netCDF4 import Dataset, date2index, num2date, date2num
from torchvision.io import read_image

def WriteTrainingData():
    print("reading data")

    # import x and y data from /data/

    nc_x = 'data/tos_Omon_GFDL-ESM4_historical_r1i1p1f1_gr_185001-186912.nc'
    nc_y = 'data/chl_Omon_GFDL-ESM4_historical_r1i1p1f1_gr_185001-186912.nc'
    nc_x = Dataset(nc_x)
    nc_y = Dataset(nc_y)

    # x_data dimensions

    n_t = len(nc_x.variables['time'])
    n_lat = len(nc_x.variables['lat'])
    n_lon = len(nc_x.variables['lon'])

    # flatten x_data from x_(t, lat, lon) to x_(t, lat*lon)

    x_data = nc_x.variables['tos']
    x_data = np.array(x_data)
    x_data = x_data.reshape(n_t, n_lat*n_lon)

    y_data = nc_y.variables['chl']
    y_data = np.array(y_data)

    # get depth average of y data

    y_depth_avg = np.empty([n_t, n_lat*n_lon])

    for t in range(0, n_t):
        for lat in range(0, n_lat):
            for lon in range(0, n_lon):
                y_depth_avg[t, lat*n_lon + lon] = y_data[t,:,lat,lon].mean()

    # combine x and y data into x_y_data(t, [x_data + y_data])

    x_y_data = np.empty([n_t, 2, n_lat*n_lon])

    for t in range(0, n_t):
        x_y_data[t, 0] = x_data[t]
        x_y_data[t, 1] = y_depth_avg[t]

    print("done")