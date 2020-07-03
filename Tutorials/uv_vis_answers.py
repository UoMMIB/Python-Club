import pandas as pd
import matplotlib.pyplot as plt

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
    # transpose
    df = df.T # also works: df.transpose()
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
