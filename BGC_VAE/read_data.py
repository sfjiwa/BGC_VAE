import datetime as dt
import numpy as np
import pandas as pd
import re
from matplotlib import pyplot as plt
from netCDF4 import Dataset, date2index, num2date, date2num

def ReadData():
    print("reading data")

    past = 'data/tas_Amon_GFDL-ESM4_historical_r1i1p1f1_gr1_185001-194912.nc'
    nc = Dataset(past)
    print(nc.dimensions)
    print(nc.variables)

    print("done")