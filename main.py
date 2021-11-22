from BGC_VAE import *

## predicting hypoxic ocean conditions out of Mississippi - manmade or physical?
## measure: o2, algae
## proxies: N2O (agricultural activity)

## Gulf of Mexico box: 18-30 N, 80-97 W

## Mississippi River
#   Source: 47 N, 95 W
#   Mouth: 29 N, 89 W
#   Basin sample: 32-45 N, 82-105 W 


variables = ('tos', 'o2', 'wfo')

get_nc_data.GetData(variables)
get_nc_data.GetData(('gpp',), freq='Emon', grid='gr1')
write_tensor_data.WriteData()