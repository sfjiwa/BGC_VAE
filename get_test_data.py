from BGC_VAE import *

## train a beta-VAE to encode a predictor field relevant to hypoxic events
## into a lower dimensional latent space and decode the latent space to return
## the predictors.
## encode an anthropogenic input feature using a linear function to determine 
## its contribution to hypoxic events 

## Gulf of Mexico box: 18-30 N, 80-97 W
# 108-120, 
# 263-280

## Mississippi River
#   Source: 47 N, 95 W
#   Mouth: 29 N, 89 W
#   Basin sample: 32-45 N, 82-105 W 

variables = ('tos', 'chl', 'wfo', 'o2')

#get_nc_data.GetData(variables)
#get_nc_data.GetData(('gpp',), freq='Lmon', grid='gr1')

get_nc_data.GetData(variables, exp='ssp245')
get_nc_data.GetData(('gpp',), freq='Lmon', grid='gr1', exp='ssp245')

write_tensor_data.WriteData(training=False)
# plot_variable.Plot('data/training/o2.npy', 100)
# plot_variable.Plot('data/training/chl.npy', 100)
# plot_variable.Plot('data/training/lev.npy', 100)