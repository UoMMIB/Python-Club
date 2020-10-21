from rdkit import Chem, SimDivFilters
import torch
import torch.nn as nn
from torch.utils.data import DataLoader, Dataset, random_split
import pandas as pd
import argparse
from tqdm import tqdm


class dataset(Dataset):
    def __init__(self,path, sample_size = 50, test=True):
        super().__init__()
        self.test = test
        self.x, self.y = self.process(path, sample_size) 
    def __len__(self):
        return self.x.shape[0] 
    def __getitem__(self,idx):
        return self.x[idx], self.y[idx]
    def process(self, path, sample_size):
        if self.test:
            df = pd.read_csv(path, index_col=0, nrows = 10000) 
        else:
            df = pd.read_csv(path, index_col=0)
        
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


def main(args):
    data = dataset('AID_1706.csv', args.n_samples, args.test)
    trainsize = int(0.8 * len(data))
    testsize = len(data) - trainsize
    train_data, test_data = random_split(data, (trainsize, testsize))
    train_loader = DataLoader(train_data, batch_size = 16, shuffle=True, num_workers=1)
    test_loader = DataLoader(test_data, batch_size=16, shuffle=True, num_workers=1)

    net = Net()
    loss_fn = nn.BCELoss()
    opt = torch.optim.Adam(net.parameters(), lr=args.lr)

    # train
    loss_rcd = torch.tensor([])
    for epoch in range(args.epochs):
        for xi, yi in tqdm(train_loader):
            yh = net(xi)
            loss = loss_fn(yh.reshape(-1), yi)
            loss.backward()
            opt.step()
            opt.zero_grad()
            loss_rcd = torch.cat([loss_rcd, loss.detach().reshape(1,-1)])
        print(f'epoch: {epoch +1} \t loss = {loss_rcd[-trainsize:].mean().detach().item()}')

    # test
    true_values = torch.tensor([])
    pred_values = torch.tensor([])
    test_losses = torch.tensor([])
    net.eval()
    for xi, yi in test_loader:
        yh = net(xi)
        true_values = torch.cat([true_values.reshape(-1), yi])
        pred_values = torch.cat([pred_values.reshape(-1), (yh > 0.5).reshape(-1).float()])
        loss = loss_fn(yh.reshape(-1), yi)
        test_losses = torch.cat([test_losses.reshape(-1), loss.reshape(-1)])
    print(f'accuracy = {round(((true_values == pred_values).sum().float() / len(pred_values) * 100).item(), 2)} %')

    # confusion matrix
    confusion = pd.crosstab(pd.Series(true_values), pd.Series(pred_values),
            rownames=['true'],
            colnames=['pred'])
    print(confusion)

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('-t', '--test', action='store_true', default=False)
    parser.add_argument('-n', '--n_samples', default = 1000, type=int)
    parser.add_argument('-e', '--epochs', default = 10, type=int)
    parser.add_argument('-l','--lr', default = 1e-4, type=float)
    args = parser.parse_args()
    main(args)
