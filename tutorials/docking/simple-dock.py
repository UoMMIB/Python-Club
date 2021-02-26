import vdsl

def main():
    p = vdsl.protein('3b4y.pdb') ###
    results = p.dock('[O-][N+](=O)c1cn2C[C@@H](COc2n1)OCc3ccc(OC(F)(F)F)cc3', 
            target_sites = [38, 44, 175, 176, 199, 252, 256, 261, 283, 311],
            exhaustiveness=1)
    results.save('pa824')



if __name__ == '__main__':
    main()
