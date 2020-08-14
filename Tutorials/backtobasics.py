import requests
import numpy as np
import pandas as pd

def extract_data_with_for_loops(data):
    # data: string of a table
    table = [] # ready to catch our lists of row items
    # loop through each row by splitting in '\n'  (newline)
    for i in data.split('\n'):
        # i.split('\t') = list of values in each row
        table.append(i.split('\t') ) # add to list
    header = table[0] # first row -

    index = []
    for i in table[1:]:
        index.append(i[0]) # first item in each row (except the headers)

    values = []
    for i in table[1:]:
        values.append(i[1:])
    # make the strings of numbers into floats
    float_values = []
    for row in values:
        float_row = []
        for val in row:
            float_row.append(float(val))
        float_values.append(float_row)

    # we're maing a dictionary of dictionaries
    d1 = {} # d1 will contain {amino_acid1: {property1: 0.2, ...}, amino_acid2: {...} ... }
    for aa, row in zip(index, values): # use zip(iterable1, iterable2,...) to iterate through multiple variables at once
        # we have the amino_acid name  as a string and the row of properties as a list
        # we want to label each property with its name with another dictionary
        d2 = {}
        for val, feature in zip(row, header):
            d2[feature] = val
        d1[aa] = d2
    return d1


def extract_data_with_list_comprehensions(data):
    # data: string of a table
    table = [i.split('\t') for i in data.split('\n')]
    header = table[0]
    index = [i[0] for i in table[1:]]
    values = [[float(val) for val in i[1:]] for i in table[1:]]
    dictionary = {j:dict(zip(header, i)) for i,j in zip(values, index)}
    return dictionary

def clean_seq(seq):
    seq = seq.replace('\n','')
    seq = seq.replace('*','')
    return seq

def find_mw(sequence, dictionary):
    weight = 0
    for aa in sequence:
        aa_info = dictionary[aa]
        aa_weight = aa_info['MolWT']
        weight += aa_weight
    return weight


def get_1bu7():
    try:
        r = requests.get('https://files.rcsb.org/download/1BU7.pdb')
    except:
        print('Failed to get 1BU7.pdb')

    with open('1BU7.pdb','w') as f:
        f.write(r.content.decode("utf-8") )

def get_atoms_from_pdb(pdb_text):
    atoms = [i for i in pdb_text if 'ATOM ' in i][3:] # first few lines aren't what we want,
    # be careful if applying this to other cases
    atoms = [i.split() for i in atoms] # split on whitespace
    return atoms

def get_hetatms_from_pdb(pdb_text):
    hetatms = [i for i in pdb_text if 'HETATM ' in i][1:]
    hetatms = [i.split() for i in hetatms]
    return hetatms


def pairwise_euc_distance(coords):
    l1 = []
    for i in coords:
        l2 = []
        for j in coords:
            d = np.linalg.norm(i-j)
            l2.append(d)
        l1.append(l2)
    return np.array(l1)

def pairwise_euc_distance_1line(coords):
    return np.array([[np.linalg.norm(i-j) for i in coords] for j in coords])

def get_atom_identities(df):
    elements = df.loc[df['Type'] == 'ATOM', 'Element symbol'].dropna() # 2 None values in there
    hem = df.loc[df['Type'] == 'HETATM','Element symbol'].dropna()
    missing = df.loc[df['Element symbol'].isna(), '??']
    atom_ids = pd.concat([elements, missing, hem])
    atom_ids.index = df['ID'].astype(int)
    return atom_ids.sort_index()
