import pandas as pd
import matplotlib.pyplot as plt
import re


def clean_data_ans(path):
    df = pd.read_csv(path) # dataframe object from csv
    headers = df.columns # save column headers
    df = df.iloc[1:,:] # trim top row
    df.columns = headers # replace with old headers
    ### to do: #####
    ## make wavelengths index
    df.index = df.iloc[:,0]
    ## remove wavelength cols
    df = df.iloc[:,1::2]
    ## remove machine info (remove nan rows)
    df = df.dropna()
    ## get sample names from headers
    ## col headers to sample names
    df.columns = headers[::2][:-1]
    # round wavelenths
    df.index = [round(float(i)) for i in df.index]
    return df

def plot_traces(df):
    plt.figure(figsize=(15,7)) # manually make canvas
    for col in df: # loop through columns
        plt.plot(df[col], # plot columns
                 label=col) # set trace label as col name - for legend

    plt.legend(loc='right') # detects 'label' in plot
    plt.xlabel('wavelength nm')
    plt.ylabel('absorbance')
    plt.ylim(-0.1,1)
    plt.xlim(250,800)
    plt.xticks(range(250,800,50)) # x axis ticks every 50 nm
    plt.title('UV-Vis absorbance of P450 BM3 with additions of arachadionic acid')
    plt.show()

def regex_substrate_vols_ans(cols):
    # find only column headers with 'Arachadonic_acid'
    Arachadonic_acid_cols = [i for i in cols if 'acid' in i]
    # from those, extract numbers (volume of arachadionic acid added in µl)
    vols = [re.search('\d+\.\d',i).group() for i in Arachadonic_acid_cols]
    # also works
    # vols = [re.findall('\d+\.\d',i)[0] for i in Arachadonic_acid_cols]
    # convert the strings of the numebrs to floats
    vols = [float(i) for i in vols]
    # return the vol
    return vols

def calc_concentrations_ans(v1,v2, c1):
    return (c1*v1)/v2

def calc_change_a420_a390_ans(x):
    x = x.subtract(x.iloc[:,0], axis =0)
    a420 = x.loc[420,:]
    a390 = x.loc[390]
    total_change = a420.abs() + a390.abs()
    return total_change
