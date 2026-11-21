import random
import string

# Parameters
GENOME_LENGTH = 100        # number of loci in a genome
POPULATION_SIZE = 50       # number of individuals per generation
GENERATIONS = 10           # how many generations to simulate
MUTATION_RATE = 0.01       # probability of a single locus mutating
FITNESS_FUNC = lambda genome: sum(v == 'A' for v in genome)  # example fitness

# Create an initial population with random genomes
def random_genome(length):
    return ''.join(random.choices(string.ascii_uppercase, k=length))

population = [random_genome(GENOME_LENGTH) for _ in range(POPULATION_SIZE)]

def reproduce(parent1, parent2):
    """Single-point crossover + mutation."""
    # Crossover
    point = random.randint(1, GENOME_LENGTH - 1)
    child = parent1[:point] + parent2[point:]
    # Mutation
    child_list = list(child)
    for i in range(GENOME_LENGTH):
        if random.random() < MUTATION_RATE:
            child_list[i] = random.choice(string.ascii_uppercase)
    return ''.join(child_list)

for gen in range(GENERATIONS):
    # Evaluate fitness
    fitness_scores = [(genome, FITNESS_FUNC(genome)) for genome in population]
    # Sort by fitness (descending)
    fitness_scores.sort(key=lambda x: x[1], reverse=True)
    # Keep the top 10% as parents (elitism)
    num_parents = max(1, POPULATION_SIZE // 10)
    parents = [genome for genome, _ in fitness_scores[:num_parents]]
    # Generate new population
    new_population = []
    while len(new_population) < POPULATION_SIZE:
        p1, p2 = random.sample(parents, 2)
        new_population.append(reproduce(p1, p2))
    population = new_population
    # Optionally print best fitness each generation
    best_genome, best_fit = fitness_scores[0]
    print(f"Generation {gen+1}: Best fitness = {best_fit}, Genome = {best_genome}")

# Final result
best_overall = max(population, key=FITNESS_FUNC)
print("\nFinal best genome:", best_overall)
print("Fitness:", FITNESS_FUNC(best_overall))