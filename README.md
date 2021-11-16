BGC_VAE
======

Run:
------
```
python main.py
```

Dependencies
------
Anaconda3(64-bit)
PyTorch

Setup Conda Environment
------
```
conda config --prepend channels conda-forge
conda config --append channels ConorIA
conda create -n "man_ccia" "python>=3.7.1" ec3 esgf-pyclient matplotlib netCDF4 pandas requests "seaborn>=0.9.0" xarray
```
