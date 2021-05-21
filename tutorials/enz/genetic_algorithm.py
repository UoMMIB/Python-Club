import random
import heapq

ALPHABET = 'ACDEFGHIKLMNPQRSTVWY'


def random_pop(length, n):
    return [''.join(random.choices('ACTG', k = length)) for i in range(n)]

def mutate(s):
    x = list(s)
    pos = random.randint(0,len(x) - 1)
    x[pos] = random.choice(ALPHABET)
    return ''.join(x) 

def cross(a, b):
    cut = random.randint(0, min([len(a), len(b)]))
    ab = a[:cut] + b[cut:]
    ba = b[:cut] + a[cut:]
    return random.choice([ab, ba])

def select(pop, n):
    return heapq.nlargest(n, pop, key = score)

def score(s):
    return sum([1 for i in s if i == 'A']) / len(s) 

def iterate(pop, selection_frac = 0.2):
    max_pop_size = len(pop)
    pop = select(pop, round(len(pop) * selection_frac))
    pop = [cross(*random.choices(pop, k = 2)) for i in pop]
    pop += random.choices(pop, k = max_pop_size - len(pop))
    pop = [mutate(i) for i in pop]
    return pop

def test():
    import time

    pop = random_pop(length = 20, n = 20)

    best = lambda l : max([score(i) for i in l])

    for i in range(100):
        time.sleep(0.1)
        pop = iterate(pop)
        print(i, best(pop))

if __name__ == '__main__':
    test()
