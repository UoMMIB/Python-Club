import pandas as pd
import numpy as np
import re
import matplotlib.pyplot as plt

def clean_data(path):
    df = pd.read_csv(path).iloc[6:,:]
    # why not .dropna()? - the row with the timestamps has an NaN in
    df.columns = df.loc[6,:] # set time stamps as columns
    df = df.drop(6) # drop timestamps
    df.index = df.loc[:,np.nan] # set well IDs as index
    # could also usse df.iloc[:,0]
    df = df.drop([np.nan, 'Time'], axis=1) # drop two columns

    return df

def process_time_headers(headers):
    mins_secs = [re.findall('\d+', i) for i in headers]
    times = [int(i[0])*60 + int(i[1]) if len(i) == 2  else int(i[0])*60 for i in mins_secs ]
    return times

def quick_plot(data):
    plt.figure(figsize=(10,5))
    for i in data.index:
        plt.plot(data.loc[i,:], label=i)
    plt.xlabel('Time/mins')
    plt.ylabel('OD 600')
    plt.legend()
    plt.show()
