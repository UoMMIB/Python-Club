import enz
import random
import heapq
import multiprocessing
import numpy as np
from tqdm import tqdm

AAS = ['A', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'K', 'L', 'M', 'N', 'P', 'Q', 'R', 'S', 'T', 'V', 'W', 'Y']

TARGET_SITES = [49, 51, 75, 82, 87, 181, 188, 263, 330]

BM3_DM='MTIKEMPQPKTFGELKNLPLLNTDKPVQALMKIADELGEIFKFEAPGRVTRYLSSQRLIKEACDESRFDKNLSQALKFVRDFFGDGLVTSWTHEKNWKKAHNILLPSFSQQAMKGYHAMMVDIAVQLVQKWERLNADEHIEVPEDMTRLTLDTIGLCGFNYRFNSFYRDQPHPFITSMVRALDEAMNKLQRANPDDPAYDENKRQFQEDIKVMNDLVDKIIADRKASGEQSDDLLTHMLNGKDPETGEPLDDENIRYQIITFLIAGHETTSGLLSFALYFLVKNPHVLQKAAEEAARVLVDPVPSYKQVKQLKYVGMVLNEALRLWPTAPAFSLYAKEDTVLGGEYPLEKGDELMVLIPQLHRDKTIWGDDVEEFRPERFENPSAIPQHAFKPFGNGQRACIGQQFALHEATLVLGMMLKHFDFEDHTNYELDIKETLTLKPEGFVVKAKSKKIPLGGIPSPSTEQSAKKVRK*'

def cross(a, b):
    cut_point = random.randint(0, min(len(a), len(b)))
    ab = a[:cut_point] + b[cut_point:]
    ba = b[:cut_point] + a[cut_point:]
    return random.choice([ab,ba])

def mutate(gene):
    gene = list(gene) # lists can be modified
    pos = random.randint(0, len(gene) - 1)
    gene[pos] = random.choice('ACTG')
    return ''.join(gene)

def c20_fe_distance(protein, vina_pose):
    fe = protein.df.loc[protein.df['element_symbol'] == 'FE',\
            ['x_coord', 'y_coord', 'z_coord']].values
    c20 = vina_pose.df.loc[vina_pose.df['atom_number'] == 20,\
            ['x_coord', 'y_coord', 'z_coord']].values
    return np.linalg.norm(fe - c20)

def score(protein, results):
    # low is better
    pose_dict = results.dictionary
    affinities = np.array([pose_dict[i]['affinity'] for i in pose_dict]).astype(float)
    distances = np.array([c20_fe_distance(protein, pose_dict[i]['mol']) for i in pose_dict])
    aff_sq = affinities ** 2
    return sum(distances / aff_sq)


def evaluate(gene):
    mutation_dictionary = dict(zip(TARGET_SITES, AAS))
    p = enz.protein('4KEY.pdb',
                    seq = BM3_DM, # my residue numbering system
                    cofactors = ['HEM']) # keep the heme

    for pos in mutation_dictionary:
        aa = mutation_dictionary[pos]
        p.mutate(pos, aa)
    p.refold()

    docking_results = p.dock('CCS(=O)(=O)C1=C(N2C=CC=CC2=N1)S(=O)(=O)NC(=O)NC3=NC(=CC(=N3)OC)OC',
                             target_residues = TARGET_SITES,
                             exhaustiveness = 1)
    return score(p, docking_results) 

def evaluate_batch(pop):
    with multiprocessing.Pool(len(pop)) as pool:
        results = pool.map(evaluate, pop)
    pool.join()
    return results

def select_parralel(pop, parralel_fn, frac = 0.1):
    scores_dict = dict(zip(pop, parralel_fn(pop)))
    return  heapq.nsmallest(round(len(pop) * frac), 
                           scores_dict.keys(), 
                           key = lambda i : scores_dict[i]) 

def main():
    pop_size = 8
    pop = [mutate('TYLFVLLIA') for i in range(pop_size)]
    # tqdm progress bar
    for i in tqdm(range(3)):
        pop = select_parralel(pop, evaluate_batch, frac = 0.25)
        pop = [cross(*random.choices(pop, k = 2)) for i in range(pop_size)]
        pop = [mutate(i) for i in pop]
        print(pop)

    # it'd be sensible to save the mutants and scores as you go ;)

if __name__ == '__main__':
    main()
