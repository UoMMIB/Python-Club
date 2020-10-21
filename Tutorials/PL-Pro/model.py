from rdkit import Chem, SimDivFilters
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, random_split
import pandas as pd

class dataset(Dataset):
    def __init__(self,path, sample_size = 50):
        super().__init__()
        self.x, self.y = self.process(path, sample_size) 
    def __len__(self):
        return self.x.shape[0] 
    def __getitem__(self,idx):
        return self.x[idx], self.y[idx]
    def process(self, path, sample_size):
        df = pd.read_csv(path, index_col=0, nrows = 1000) # change this
        
        # diversity sampling
        mols = [Chem.MolFromSmiles(i) for i in df['smiles']]
        fps =  [Chem.RDKFingerprint(i) for i in mols]
        mmp = SimDivFilters.MaxMinPicker()
        picks = mmp.LazyBitVectorPick(fps, len(fps), sample_size)
        self.df = df.iloc[picks,:]

        x = torch.tensor([list(i) for i in fps]).float()
        y = torch.from_numpy((df['PUBCHEM_ACTIVITY_OUTCOME'] == 'Active').astype(int).values).float()
        return x, y


class Net(nn.Module):
    def __init__(self):
        super().__init__()
        self.l1 = nn.Linear(2048,32)
        self.l2 = nn.Linear(32,1)
    def forward(self,x):
        x = self.l1(x)
        x = torch.relu(x)
        x = self.l2(x)
        x = torch.sigmoid(x)
        return x

def main():
    data = dataset('AID_1706.csv')
    trainsize = int(0.8 * len(data))
    testsize = len(data) - trainsize
    train_data, test_data = random_split(data, (trainsize, testsize))
    train_loader = DataLoader(train_data, batch_size = 16, shuffle=True, num_workers=1)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=True, num_workers=1)

    net = Net()
    loss_fn = nn.BCELoss()
    opt = torch.optim.Adam(net.parameters(), lr=1e-4)

    # train
    epochs = 10
    loss_rcd = torch.tensor([])
    for epoch in range(epochs):
        for xi, yi in train_loader:
            yh = net(xi)
            loss = loss_fn(yh, yi)
            loss.backward()
            opt.step()
            opt.zero_grad()
            loss_rcd = torch.cat([loss_rcd, loss.detach().reshape(1,-1)])
        print(loss_rcd[-1000:].mean())

if __name__ == '__main__':
    main()
