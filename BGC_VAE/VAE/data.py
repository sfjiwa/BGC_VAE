import numpy as np
import torch
from torch import nn

#get the data 
temp_data = np.swapaxes(np.load('tos.npy'),0,1)
#cmip filtering
temp_data[temp_data>100000] = 0
print(len(temp_data))
chlo_data = np.swapaxes(np.load('lev.npy'),0,1)
chlo_data[chlo_data>=9.999e+19] = 0
#chlo_data[chlo_data<=0.51]= 0
chlo_data = np.true_divide(chlo_data,1e19)
cD = torch.empty(240,1,20,20)
for i in range(0,240):
	p = chlo_data[i].reshape(180,360)
	p = p[105:125,260:280].reshape(20,20)
	t = torch.from_numpy(p)
	cD[i,0] = t
#torch tensor to feed to nn
tD = torch.empty(240,1,20,20)
for i in range(0,240):
	p = temp_data[i].reshape(180,360)
	p = p[105:125,260:280].reshape(20,20)
	t = torch.from_numpy(p)
	tD[i,0] = t
torch.save(tD,"tempData.pt")
torch.save(cD,"chloroData.pt")
print(cD)
