import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import argparse

import re

from sklearn.metrics import r2_score

from scipy import ndimage
from scipy.optimize import curve_fit

def argParser():
    parser = argparse.ArgumentParser()
    parser.add_argument('-i', nargs=1, help='Trace')
    parser.add_argument('-s', nargs=1, help='Save')
    args=parser.parse_args()
    return args

class SpecData:
    def __init__(self, path,save=False):
        self.path=path
        self.save=save
        self.data = pd.read_csv(path)
        self.headers = pd.Series(self.data.columns[0::2])[:-1] # series to make it more workable #last col is blank
        self.substrateCols = self.regex_substrates()
        self.substrateConcs = self.regex_substrateConcs(self.substrateCols)

        self.wavelengths = self.Get_Wavelengths()
        self.data = self.Get_numericalData() # throws away the metadata
        self.data.index = self.headers
        self.data = self.Zero_at_800()
        self.data = self.data.iloc[self.substrateCols.index,:]
        self.data = self.GaussianFilterData()
        self.Diff = self.calcDiff(self.data)
        self.DiffDiff = self.calcDiffDiff()

    def Get_Wavelengths(self):
        wavelengths = self.data.iloc[:,0].dropna() # first column
        wavelengths = wavelengths[wavelengths.str.contains(r'\d\d\d.\d\d\d\d').dropna()].astype(float)
        # there's an integer in there somewhere!
        wavelengths = wavelengths.reset_index(drop=True).iloc[1:]
        # cba to sort this out now, I'm just going to plot it out of shift by one cell shit
        return wavelengths.reset_index(drop=True)

    def Get_numericalData(self):
        data = self.data
        data.columns = data.iloc[0,:]

        data = data.iloc[self.wavelengths.index,:].dropna(axis = 1)
        data = data.drop('Wavelength (nm)', axis = 1)
        data = data.iloc[1:,:] #drops strinds
        data.reset_index(inplace=True,drop=True)
        return data.transpose()

    def Zero_at_800(self):
        data = self.data.astype(float)
        data.columns = self.wavelengths[:-1]
        zero_vals = data.iloc[0,:] # starts with 800
        data = data.subtract(zero_vals,axis=1)
        return data

    def calc_conc(self):
        data = self.data
        data = data.loc[:,data.columns < 421]
        data = data.loc[:,data.columns > 419]
        A420 = data.iloc[:,0]
        ext = 95
        conc_mM = A420/ext
        conc_uM = conc_mM*1000
        conc_uM.reset_index(drop=True,inplace=True)
        conc_uM.name = 'P450 conc/uM'
        conc_uM.index=self.headers[:-1]
        return conc_uM

    def plot_traces(self, data,title=None):
        concs = self.substrateConcs
        fig, ax = plt.subplots(figsize=(10,6))
        ax.set_prop_cycle('color',plt.cm.inferno(np.linspace(0,0.9,len(data))))
        for i in range(len(data)):
            y = data.iloc[i,:]
            plt.plot(y, lw = 2)
        plt.xlim((250,800))
        plt.ylim((-0.1,0.6))
        plt.xticks(np.linspace(250,800,11))
        plt.xlabel('Wavlength nm')
        plt.ylabel('Absorbance')
        plt.legend(concs, title='Substrate conc/uM',loc = 'right')
        if title != None:
            plt.title(title)
        plt.show()

    def PlotMichaelesMenten(self,title = None):
        concs = self.substrateConcs
        km, vmax, loss = self.FitMichaelisMenten()
        km, vmax, loss  = km.item(), vmax.item(), loss.item()
        x = np.linspace(concs.min(),concs.max(),100)

        plt.figure(figsize=(7,7))
        plt.scatter(concs,self.DiffDiff)

        plt.plot(x, (vmax*x)/(km + x))
        plt.title(title)
        plt.xlabel('Concentration uM')
        plt.ylabel('Change in Absorbance')

        plt.text(concs.max()*0.7,vmax*0.2,'Km = '+str(np.around(km,2))+'\n'\
        +'Vmax = '+str(np.around(vmax,2))+'\n'\
        +'Loss = '+str(np.around(loss,5))+'\n'\
        'R squared = ' + str(round(1.-loss,3)))

        plt.show()


    def CalcRZ(self):
        #copy of the data
        data=self.data
        data.columns=self.wavelengths[:-1].round(0).astype(int)
        data.index=self.headers[:-1]
        RZ=self.data.loc[:,420]/self.data.loc[:,280]
        return RZ

    def regex_substrates(self):
        #substrates = self.headers.loc[self.headers.str.contains(expression, flags=re.IGNORECASE)]
        dmso = self.headers.loc[self.headers.str.contains('dmso', flags=re.IGNORECASE)]
        substrates = self.headers.loc[dmso.index.max()+1:]
        ProteinDMSO = pd.Series(self.headers.loc[(substrates.index.min() -1)])
        substrateCols = ProteinDMSO.append(substrates)

        # sort out index - DMSO needs to have index substrates.index.min() -1
        idx = list(substrateCols.index)
        idx[0] = substrates.index.min() -1
        substrateCols.index = idx
        return substrateCols

    def regex_substrateConcs(self,col_headers):
        vols =  col_headers[1:].str.extract('_(\d+(\.\d+)?)').astype(float)[0] # uls
        concs = (10_000*vols)/1000 # uM and ul
        concs = pd.Series([0.0]).append(concs)
        return concs

    def GaussianFilterData(self):
        data = pd.DataFrame(ndimage.gaussian_filter(self.data,2))
        data.columns = self.wavelengths[:-1]
        return data

    def calcDiff(self,data):
        return data-data.iloc[0,:]

    def calcDiffDiff(self):
        diff = self.Diff

        sec420 = diff.loc[:,diff.columns>416]
        sec420 = sec420.loc[:,sec420.columns<421]
        sec420 = sec420.loc[:,sec420.sum(axis=0).idxmax()]

        sec390 = diff.loc[:,diff.columns>385]
        sec390 = sec390.loc[:,sec390.columns<395]
        sec390 = sec390.loc[:,sec390.sum(axis=0).idxmax()]

        return (sec390 - sec420).abs()

    def FitMichaelisMenten(self):
        def michaelis_menten(x,km,vmax):
            return (vmax*x)/(km + x)
        params, covariance = curve_fit(michaelis_menten,
        self.substrateConcs,
        self.DiffDiff)
        km, vmax = params[0], params[1]
        pred = michaelis_menten(self.substrateConcs,km,vmax)
        r2 = r2_score(self.DiffDiff, pred)
        return km, vmax, r2

        '''
        x = self.substrateConcs.values
        x = torch.tensor(x,dtype=torch.float)

        y = self.DiffDiff.values
        y = torch.tensor(y,dtype=torch.float)

        km = torch.tensor([0.5],requires_grad=True,dtype=torch.float)
        vmax = torch.tensor([0.5],requires_grad=True,dtype=torch.float)
        optimizer = torch.optim.Adam({km,vmax},lr = 1e-2)
        loss_fn =  self.r_squared_torch

        for i in tqdm(range(5_000)):
            y_pred = (vmax*x)/(km + x) # scaling
            loss = 1 - loss_fn(y,y_pred) # 1 - r squared
            if km <0:
                # making sure that Km isn't negative
                loss -= km.item()
            loss.backward()
            optimizer.step()
            optimizer.zero_grad()
        return km, vmax, loss'''

    def r_squared_torch(self,y,yh):
        residuals = y-yh
        ss_res = (residuals**2).sum()
        ss_tot = (y-y.mean()**2).sum()
        r_squared = 1 - (ss_res / ss_tot)
        return r_squared


def main():
    args=argParser()
    path=args.i[0]

    Dataset = SpecData(path)
    Dataset.plot_traces(Dataset.data, 'UV-Vis absorbance of Arachadonic Acid Titration into P450 BM3 WT')
    Dataset.plot_traces(Dataset.Diff, 'Relative UV-vis shift of Arachadonic Acid Titration into P450 BM3 WT')
    Dataset.PlotMichaelesMenten('Response of P450 BM3 WT to Arachadonic Acid Titration \n and Michaelis-Menten Curve Fit ')


if __name__ == '__main__':
    main()
