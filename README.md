BGC_VAE
======
A tool for downloading Climate Model Intercomparison Project (CMIP) data and running it through a beta-variational autoencoder (Beta-VAE). Trains with an additional linear function for determining the contribution of individual climate variables producing the decoded output.

Dependencies
------
Anaconda3(64-bit)

PyTorch

Download Training and Test Data (Large)
------
```
python get_train_data.py
python get_test_data.py
```

Import Package (Anaconda3)
------
```
conda activate man_ccia
python
from BGC_VAE import *
```

Visualise Data
------
plot_variable.Plot(/path-to-data, time_index)

Setup Conda Environment
------
```
conda config --prepend channels conda-forge
conda config --append channels ConorIA
conda create -n "man_ccia" "python>=3.7.1" ec3 esgf-pyclient matplotlib netCDF4 pandas requests "seaborn>=0.9.0" xarray
```
