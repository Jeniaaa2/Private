import random
import math

# ---------- Problem: Maximize function f(x) = sin(x) * x on interval [0, 10] ----------
def fitness(x):
    return math.sin(x) * x

# Population parameters
POP_SIZE = 30
GENES = 1  # one variable
MUT_PROB = 0.1
CROSS_PROB = 0.7
ELITE_FRACTION = 0.1
TARGET_FITNESS = 9.0
MAX_GENS = 200

# Gene bounds
LOW, HIGH = 0.0, 10.0

def random_individual():
    return [random.uniform(LOW, HIGH)]

def crossover(parent1, parent2):
    if random.random() < CROSS_PROB:
        return [[p1 if random.random() < 0.5 else p2] for p1, p2 in zip(parent1, parent2)][0]
    return parent1[:]

def mutate(individual):
    if random.random() < MUT_PROB:
        individual[0] = random.uniform(LOW, HIGH)
    return individual

def select(pop, scores):
    # roulette wheel selection
    total = sum(scores)
    picks = []
    for _ in range(len(pop)):
        r = random.uniform(0, total)
        accum = 0
        for ind, sc in zip(pop, scores):
            accum += sc
            if accum >= r:
                picks.append(ind[:])
                break
    return picks

def genetic_algorithm():
    # initialize population
    population = [random_individual() for _ in range(POP_SIZE)]
    for gen in range(MAX_GENS):
        # evaluate
        scores = [fitness(ind[0]) for ind in population]
        # check target
        if max(scores) >= TARGET_FITNESS:
            break
        # elitism
        elite_count = int(ELITE_FRACTION * POP_SIZE)
        elites = [ind for _, ind in sorted(zip(scores, population), reverse=True)[:elite_count]]
        # selection
        mate_pool = select(population, scores)
        # create next generation
        next_pop = elites[:]
        while len(next_pop) < POP_SIZE:
            p1 = random.choice(mate_pool)
            p2 = random.choice(mate_pool)
            child = crossover(p1, p2)
            child = mutate(child)
            next_pop.append(child)
        population = next_pop
    # return best result
    best_ind = max(population, key=lambda ind: fitness(ind[0]))
    return best_ind[0], fitness(best_ind[0])

best_x, best_val = genetic_algorithm()
print(f"Best x = {best_x:.6f}, fitness = {best_val:.6f}")