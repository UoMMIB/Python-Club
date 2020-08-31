# Python Club @ the [Manchester Institute of Biotechnology](https://en.wikipedia.org/wiki/Manchester_Institute_of_Biotechnology) 🐍

## What is python club 🐍
- Python club runs tutorials every Friday 12-1pm on zoom @  **929 5820 5206 / https://zoom.us/j/92958205206** 🎥
- hosted by [jamesengleback](https://github.com/jamesengleback) 
- The tutorials are orientated towards scientific data analysis, experiment design, bio/cheminformatics & machine learning 📈 
- tutorials are interactive! We work with Google Colab hosted python notebooks  
- Python club is free for everyone
- Python club isn't a cult 🤫

# Tutorials
## [Basic bits python](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/BasicBitsPython.ipynb) 
One of the first ever 👶 covers the very basics, including an exercise on DNA translation with ```dictionaries```

## [Back to basics](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/BackToBasics.ipynb)
7 part series on some useful basics in python/jupyter, based around the DNA sequence we translated in [Basic bits python](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/BasicBitsPython.ipynb). Includes:
- ```string ``` parsing - quick tricks with copy + pasted tables; 
- ```bash``` commands in the jupyter notebook; opening & closing files; manually parsing a ```.pdb``` file containing the 3D structure of a protein using the context manager and the ```filter``` function
- 🐼 ```pandas```  for tabular data analysis 
- distance in 3D space and touching on computational complexity; shortcuts with the ```KD-Tree``` algorithm (```scipy``` implementation)
- sparse matrices and graphs - representiong the protein structure as a graph; finding atomic neighborhoods
- objects 📦 - custom objects with ```class``` ; saving attributes with ```__init__``` and ```self``` ; inheritace

## [UV-Vis data analysis](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/uv-vis-data.ipynb)
A few sessions analysing some experimental UV-Vis spectroscopy data gathered at the MIB. The experiment measures the affinity between a cytochrome P450 enzyme and a fatty acid. Includes:
- Lots of data wrangling with ```pandas``` 🐼 
- Plotting the traces with ```matplotlib.pyplot``` 
- Extracting substrate concentrations with ```regex```
- Colormaps - mapping concentration to color in ```matplotlib.pyplot```
- Curve fitting (Michaelis-Menten) with ```scipy.optimize```

# [Curve fitting - Michaelis-Menten](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/Curve-Fitting.ipynb)
Quick one on curve fitting (Michaelis-Menten again) with ```scipy.optimize```

# [Curve Fitting - Growth Curves & the Gomperz Equation](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/Growth-Curve/growthCurve.ipynb)
Fitting a Gomperz curve to a bacterial growth data. Includes bootstrapping to estimate the uncertainty in our predictions, by [Steve](https://github.com/SOH9797) 

# [List comprehensions](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/ListComprehensions.ipynb)
One of the most useful tricks I know. Squeeze a ```for``` loop into a single line. 

# [Basic Cheminformatics](https://github.com/UoMMIB/Python-Club/blob/master/Tutorials/IntroToCheminformatics.ipynb)
In this tutorial, we look at some compounds that were in clinical trials for COVID-19 treatment at the time. Includes:
- Using the PubChem API - ```pubchempy``` to retreive & analyze the compounds
- Using ```rdkit``` for more cheminformatic analysis

 
