import datetime as dt
import numpy as np
import pandas as pd
from matplotlib import pyplot as plt
from netCDF4 import Dataset, date2index, num2date, date2num
from torchvision.io import read_image

def WriteTrainingData():
    print("reading data")

    x = 'data/tos_Omon_GFDL-ESM4_historical_r1i1p1f1_gr_185001-186912.nc'
    y = 'data/chl_Omon_GFDL-ESM4_historical_r1i1p1f1_gr_185001-186912.nc'

    nc_x = Dataset(x)
    nc_y = Dataset(y)

    print(nc_y.dimensions)
    print(nc_y.variables)

    # store grid data implicitly [[x1, x2, x3... y1, y2, y3...,t]]


    print("done")