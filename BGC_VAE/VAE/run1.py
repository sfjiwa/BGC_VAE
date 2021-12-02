#find data to start working with batch size 1000 
#beta vae, extreme value
#SLP baseline test
#play with the param lambda

import torch; torch.manual_seed(0)
import torch.nn as nn
import torch.nn.functional as F
import torch.utils
import torch.distributions
import torchvision
import numpy as np
import matplotlib.pyplot as plt; 
device = 'cuda' if torch.cuda.is_available() else 'cpu'

class Encoder(nn.Module):#variational encoder
    def __init__(self, latent_dims):
        super().__init__()
        self.net1 = nn.Sequential(
            nn.Conv2d(1,1,3,stride=1,padding=1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Conv2d(1,1,3,stride=1,padding=1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
        )
        self.net2 = nn.Sequential(
        	nn.Conv2d(1,1,3,stride=1,padding=1),
        	nn.BatchNorm2d(1),
        	nn.ReLU()
        )
        self.linear1 = nn.Linear(400,latent_dims)
        self.linear2 = nn.Linear(400,latent_dims)
        self.N = torch.distributions.Normal(0, 1)
        self.N.loc = self.N.loc
        self.N.scale = self.N.scale
        self.kl = 0
    def forward(self, x, y=None):
        xy = x if y is None else torch.cat((x, y), dim=1)
        h1 = self.net1(xy) + xy #residual
        h = self.net2(h1)
        convOut = torch.flatten(h,start_dim = 1)
        mu = self.linear1(convOut)
        sigma = torch.exp(self.linear2(convOut))#for positivity sake
        z = mu + sigma*self.N.sample(mu.shape)
        self.kl = (sigma**2 + mu**2 - torch.log(sigma) - 0.5).sum()
        return z        


class LinearProx(nn.Module):
    def __init__(self,latent_dims):
        super().__init__()
        self.lin = nn.Linear(400,latent_dims)
    def forward(self,z,y=None):
        zy = z if y is None else torch.cat((z, y), dim=1)
        zy = torch.flatten(zy,start_dim=1)
        zy = self.lin(zy)
        return zy


class Decoder(nn.Module):
    def __init__(self, latent_dims):
        super().__init__()
        self.lin = nn.Linear(latent_dims,400)
        self.net1 = nn.Sequential(
            nn.Conv2d(1,1,3,stride=1,padding=1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
            nn.Conv2d(1,1,3,stride=1,padding=1),
            nn.BatchNorm2d(1),
            nn.ReLU(),
        )
        self.net2 = nn.Sequential(
        	nn.Conv2d(1,1,3,stride=1,padding=1),
        	nn.BatchNorm2d(1),
        	nn.ReLU()
        )

    def forward(self, z, y=None):
        zy = z if y is None else torch.cat((z, y), dim=1)

        zy = torch.reshape(self.lin(zy),(1,1,20,20))
        #residual layer
        
        zy = self.net2(self.net1(zy) + zy)
        return zy


class Autoencoder(nn.Module):
    def __init__(self, latent_dims):
        super(Autoencoder, self).__init__()
        self.encoder = Encoder(latent_dims)
        self.decoder = Decoder(latent_dims)
    def forward(self, x):
        z = self.encoder(x)
        return self.decoder(z)
    def latentForward(self,x):
        return self.encoder(x)


class LinearLatent(nn.Module):
    def __init__(self,latent_dims):
        super(LinearLatent, self).__init__()
        self.linearProx = LinearProx(latent_dims)
        self.decoder = Decoder(latent_dims)
    def forward(self, x):
        z = self.linearProx(x)
        return self.decoder(z)
    def latentForward(self,x):
        return self.linearProx(x)


def train(autoencoder, linearlatent,data, proxyData,epochs=10):
    lam = 1 #parameter lambda
    opt1 = torch.optim.Adam(autoencoder.parameters())
    opt2 = torch.optim.Adam(linearlatent.parameters())
    print(epochs)
    for epoch in range(epochs):
        # we train in alternate steps, first fixing h 
        if(epoch%2==0):
            for x,y in zip(data,proxyData): #range data to access both
                x = x.to(device) # GPU
                y = y.to(device)
                opt1.zero_grad()
                x_hat = autoencoder.forward(x)
                x_lin = linearlatent.forward(y)
                loss1 = ((x - x_hat)**2+(x_hat-x_lin)**2).sum()
                loss1.backward()
                opt1.step()
            print(loss1)
        else: #in the next step we optimize the linear latent model
            print('2')
            for x,y in zip(data,proxyData):
                x = x.to(device)
                y = y.to(device)
                opt2.zero_grad()
                z = autoencoder.latentForward(x)
                z_h = linearlatent.latentForward(y)
                loss2 = ((z-z_h)**2).sum()
                loss2.backward()
                opt2.step()
            print(loss2)
    
    plt.imshow(x[0][0].detach().numpy())
    #idk
    #plt.gca().invert_yaxis()
    plt.gca().invert_yaxis()
    plt.show()
    plt.imshow(x_hat[0][0].detach().numpy())
    plt.gca().invert_yaxis()
    plt.show()

    plt.imshow(x_lin[0][0].detach().numpy())
    plt.gca().invert_yaxis()
    plt.show()
    return autoencoder


latent_dims = 200
autoencoder = Autoencoder(latent_dims).to(device) # GPU
linearlatent = LinearLatent(latent_dims).to(device)
VAEdata = torch.utils.data.DataLoader(torch.load('chloroData.pt'))
proxyData = torch.utils.data.DataLoader(torch.load('tempData.pt'))
model = train(autoencoder, linearlatent, VAEdata, proxyData)