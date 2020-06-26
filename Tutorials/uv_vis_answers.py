import pandas as pd

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
 
