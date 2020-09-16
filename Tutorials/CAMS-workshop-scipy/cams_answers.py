import pandas as pd
import numpy as np
from scipy.ndimage import gaussian_filter1d
from scipy.optimize import curve_fit
import matplotlib.pyplot as plt
import re


def process_data(path):
    df = pd.read_csv(path,index_col=0)
    df = df.subtract(df.iloc[:,0], axis = 0) # 1st col = blank
    df = df.subtract(df.iloc[0,:]) # 1st row = 800 nm
    df =  df.iloc[:,1:] # drop 1st col
    df = pd.DataFrame(gaussian_filter1d(df,axis=1, sigma=2), columns = df.columns, index = df.index)

    return df


def magnitude_change(df):
    x = df.copy() # copy
    x = df.subtract(df.iloc[:,0], axis=0)
    return x.loc[390,:] - x.loc[420,:]

def michaelis_menten(x,km,vmax):
    return (vmax*x)/(km + x)

def calc_michaelis_menten(df):
    # takes normalized dataframe
    concs = get_concs(df)
    y = magnitude_change(df)
    params, cov = curve_fit(michaelis_menten, concs, y)
    km, vmax = params

    plt.scatter(concs,y)

    x = np.linspace(0,concs.max(),100)
    plt.plot(x, michaelis_menten(x, km,vmax))
    plt.xlabel('[substrate] / µM')
    plt.ylabel('Response |Δ $A_{420}$ | + |Δ $A_{390}$|')
    plt.text(x = 80, y = 0.05, s = f'km = {round(km,2)}\nvmax = {round(vmax, 2)}')
    plt.show()


def get_concs(df):
    # ['baseline', 'enzyme', 'ArachadionicAcid_0.5µl', ... 'ArachadionicAcid_10µl']
    vols  = [re.findall('\d+.\d+', i) for i in df.columns]
    vols = [float(i[0]) if len(i) == 1 else 0 for i in vols]
    calcConc = lambda v1:( v1* 10_000) / 1000 # c2 = (v1 * c1) / v2
    concs = [calcConc(i) for i in vols ]
    return np.array(concs)

def heatmap_colors(concentrations):
    # minmax scale
    concentrations = [i - min(concentrations) for i in concentrations]
    concentrations = [i/max(concentrations) for i in concentrations]
    colors = plt.cm.inferno(concentrations)
    return colors

def plot_titration(data, title = None):
    wavelenths = data.index # local variable
    concs = get_concs(data)
    scaledConcs = concs / concs.max()
    colors = plt.cm.inferno(scaledConcs)
    plt.figure(figsize = (10,5))
    wavelenths = data.index # index = rows = wavelengths

    for column_header, conc, color in zip(data.columns, concs, colors):
        column = data.loc[:,column_header] # locate row by columns name
        plt.plot(wavelenths, column, label = f'{conc} µM', c = color)

    plt.xticks(np.linspace(250,800,23))
    plt.ylim(-0.1,1.3)
    plt.xlim(250,800)
    plt.xlabel('wavelength (nm)')
    plt.ylabel('absorbance')
    plt.legend(loc = 'right', title = '[Substrate]')
    plt.vlines(390, -0.1,0.3,linestyles = '--', lw = 1)
    plt.vlines(418, -0.1,0.35,linestyles = '--', lw = 1)
    if title == None:
        plt.title('UV-Vis data traces')
    else:
        plt.title(title)
    plt.show()

def calc_concs_ans(v1,c1,v2):
    # solve the variable c2
    c2 = (v1 * c1)/v2
    return c2

def test():
    df = normalize(pd.read_csv('p450-bm3-arachadionic-acid-titration.csv', index_col = 0))
    df.drop('blank', axis=1, inplace=True)
    print(get_concs(df))

if __name__ == '__main__':
    test()
