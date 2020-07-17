from rdkit import Chem
from rdkit.Chem import AllChem, Crippen, Draw
import pandas as pd

def featurize(aa):
    mol = Chem.MolFromFASTA(aa)
    mol = Chem.AddHs(mol)
    descriptors = {'MolWT':AllChem.CalcExactMolWt(mol),
                  'LogP':Chem.Crippen.MolLogP(mol),
                  'HBondDonors': AllChem.CalcNumLipinskiHBD(mol),
                  'HBondAcceptors': AllChem.CalcNumLipinskiHBA(mol),
                  'nAromaticRings':AllChem.CalcNumAromaticRings(mol),
                  'nHeteroAtoms':AllChem.CalcNumHeteroatoms(mol),
                  'nRotatableBonds':AllChem.CalcNumRotatableBonds(mol)}


def draw_aas_grid():
    aas = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P',
           'Q', 'R', 'S', 'T', 'V', 'W', 'Y']
    f = Draw.MolsToGridImage([Chem.MolFromFASTA(i) for i in aas], legends=aas, molsPerRow=5)
    f.toqimage().save('amino-acids.png')

def draw_glycine():
    Draw.MolToImageFile(Chem.MolFromFASTA('G'), 'glycine.png')
