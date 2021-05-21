# enzyme design with ```enz```
## overview
enzymes can be re-designed to catalyse non-natural reactions by mutating amino acids in the active site. we can simulate the structure of new mutants and also how they might interact with a given compound. ```enz``` is a small homebrewed python package that can do both these things. it's an interface to some well established techniques for both structure prediction (pyrosetta) & molecular docking (autodock vina). It automates a large ammount of the work involved with these simulations & can itself be automated, which is useful for running large scale experiments.

```enz``` is experimental, so please report any issues @ #######. 

In this tutorial, I'll introduce ```enz```, its installation & ways to use it to design enzymes.

## theory
## caveats


## commands
```enz.protein``` - an object that handles protein structures. initialize it with a path to the ```pdb``` structure. additional arguments are ```cofactors = [...``` - a list of hetero (not protein) molecules to keep, use names as they appear in the pdb file. ```seq = 'MTIKEM...``` - string; sequence to align to structure, mutations mill map to the structure in ```refold()```. ```target_sites = [...``` - list of integers; when using ```dock(``` the ligand will be targetted top here. when initialised, the structure is cleaned: a chain is (default chain A) and ```cofactors``` are extracted.  an instance of ```enz.protein``` has the following methods:

	- ```.mutate(pos = int, aa = str)``` - replace a letter at ```pos``` in the sequence with ``aa``
	- ```.refold()``` - map mutations in ```protein.seq``` to the structure replace amino acid, repack sidechains with 5 Angstroms of the mutation site.  
	- ```.save(save_path)``` - save the current structure as a ```pdb``` at ```save_path```
	- ```.dock(smiles, target_residues)``` - dock ligand ```smiles``` (smiles str) to ```protein``` at site specified with ```target_residues``` - list of sequence positions as integers. if ```target_site``` has already been specified then this will be used. an optional argument is: ```exhaustiveness``` - exhaustiveness of the pose search in ```vina```, default ```8```, valid options are 1-16. low exhaustiveness docking runs are quicker, high exhaustiveness is more thorough. ```dock(``` returns a ```results``` object:
		- ```results``` contains the binding poses and calculated binding energies of each. ```results``` objects can be saved with ```.save(save_path)```, protein structure, all poses and a ```csv``` containing the calculated binding energies of each will be written to the directory ```save_path```. ```results.dictionary```  is a dictionary containg each pose as an ```enz.mol``` object, each of which has a ```df``` attribute containing a ```pandas``` dataframe with the coordinates and identity of each atom.

## example
```python
import enz

p = enz.protein('1bu7.pdb', cofactors = ['HEM'])

p.muate(82, 'F')
p.muate(87, 'v') # not case sensitive

p.refold() # takes a minute

results = p.dock('CCCCCCCCCCCC=O', target_sites = [49, 82, 87, 263, 330, 400]) # so does this

results.save('a82f-f87v--c16') # all relevant docking info -> directory

p.save('a82f-f87v.pdb') # just the structure
```

## analysis
both ```enz.protein``` and ```enz.mol``` have a dataframe attribute ```df```, which contains a ```pandas.DataFrame``` of atom coordinates ```x_coord, y_coord, z_coord```and identities ##### parsed directly from their temporary ```pdb``` files. spatial distance between two sets of coordinates can be found with ```numpy.linalg.norm(<numpy array>)``` where ```<numpy array>``` is ############################
distance metrics can be combined with the calculated energies of each docking pose to calculate an overall score for the docking experiment. 

## examples
### compound library screen
```python
import enz
import pandas as pd

p = protein('4KEY.pdb', target_sites = [49, 82, 87, 263, 330, 400])

df = pd.read_csv('compound_smiles.csv')

for name, smiles in zip(df['Name'], df['Smiles']):
	results = p.dock(smiles)
	results.save(name)
```
### alanine scan
one by one, muate each active site position and evaluate its effect on a custom binding score.
```python
import enz
from custom_scores import c2_score 
from my_sequences import bm3

active_site = [49, 51, 75, 82, 71, 181, 188, 263, 330]

scores = []
for position in active_site:
	p = enz.protein('1jme.pdb', cofactors = ['HEM'], seq = bm3)
	p.mutate(position, 'A')
	p.refold()
	results = p.dock('c1ccccc1', target_sites = active_site)
	scores.append(c2_score(p, results))

# save to csv
df = pd.Series(scores, index = active_site)
df.to_csv('alanine-scan-scores.csv')
```





## installation
- **conda**
- **manually**
