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

def train(autoencoder, data, epochs=100):
    opt = torch.optim.Adam(autoencoder.parameters())
    for epoch in range(epochs):
        for x in data:
            x = x.to(device) # GPU
            opt.zero_grad()
            x_hat = autoencoder(x)
            loss = ((x - x_hat)**2).sum()
            loss.backward()
            opt.step()
    print(loss)
    print(x_hat[0][0].size())
    plt.imshow(x[0][0].detach().numpy())
    #idk
    #plt.gca().invert_yaxis()
    plt.gca().invert_yaxis()
    plt.show()
    plt.imshow(x_hat[0][0].detach().numpy())
    plt.gca().invert_yaxis()
    plt.show()
    return autoencoder

latent_dims = 4
autoencoder = Autoencoder(latent_dims).to(device) # GPU

data = torch.utils.data.DataLoader(torch.load('chloroData.pt'))
autoencoder = train(autoencoder, data)