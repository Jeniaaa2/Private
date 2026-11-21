import random
import math
import statistics

# Simple genetic programming to approximate a target function
# We aim to evolve a population of arithmetic expressions that
# produce values close to a predetermined set of (x, y) points.
#
# Using only the standard library: random, math, statistics

# ------------------------------------------------------------------
# Configuration
# ------------------------------------------------------------------
POPULATION_SIZE = 200
NUM_GENERATIONS = 40
TOURNAMENT_SIZE = 5
MUTATION_RATE   = 0.3
CROSSOVER_RATE  = 0.7

# Target points: approximate sin(x) on [0, 2π]
TARGET_X = [i * 2 * math.pi / 10 for i in range(11)]
TARGET_Y = [math.sin(x) for x in TARGET_X]

# ------------------------------------------------------------------
# Helper functions for the genetic representation
# ------------------------------------------------------------------
def create_random_chromosome():
    """
    Generate a random mathematical expression in the form:
    a * sin(b*x + c) + d
    All coefficients are floats in [-5, 5].
    """
    return {
        'a': random.uniform(-5, 5),
        'b': random.uniform(-5, 5),
        'c': random.uniform(-5, 5),
        'd': random.uniform(-5, 5)
    }

def evaluate_chromosome(chromosome, x):
    """Compute the expression value for a given x."""
    a, b, c, d = chromosome['a'], chromosome['b'], chromosome['c'], chromosome['d']
    return a * math.sin(b * x + c) + d

def fitness(chromosome):
    """Mean squared error over all target points."""
    errors = [(evaluate_chromosome(chromosome, x) - y)**2
              for x, y in zip(TARGET_X, TARGET_Y)]
    return statistics.mean(errors)

# ------------------------------------------------------------------
# Evolutionary operators
# ------------------------------------------------------------------
def tournament_selection(population):
    """Choose the best chromosome among a subset."""
    competitors = random.sample(population, TOURNAMENT_SIZE)
    return min(competitors, key=fitness)

def crossover(parent1, parent2):
    """Arithmetic crossover: average coefficients."""
    child = {}
    for key in parent1:
        if random.random() < 0.5:
            child[key] = parent1[key]
        else:
            child[key] = parent2[key]
    return child

def mutate(chromosome):
    """Small random perturbation to each coefficient."""
    for key in chromosome:
        if random.random() < MUTATION_RATE:
            chromosome[key] += random.gauss(0, 0.5)
    return chromosome

# ------------------------------------------------------------------
# Main evolutionary loop
# ------------------------------------------------------------------
def main():
    # Initial population
    population = [create_random_chromosome() for _ in range(POPULATION_SIZE)]

    for generation in range(NUM_GENERATIONS):
        # Evaluate fitness and keep track of best
        best = min(population, key=fitness)
        best_fitness = fitness(best)

        # Logging every 5 generations
        if generation % 5 == 0 or generation == NUM_GENERATIONS - 1:
            print(f"Gen {generation:02d} | Best MSE: {best_fitness:.6f} | "
                  f"Chromosome: {best}")

        # New generation
        new_population = []

        # Elitism: carry the best chromosome unchanged
        new_population.append(best.copy())

        while len(new_population) < POPULATION_SIZE:
            # Selection
            parent1 = tournament_selection(population)
            parent2 = tournament_selection(population)

            # Crossover
            if random.random() < CROSSOVER_RATE:
                child = crossover(parent1, parent2)
            else:
                child = parent1.copy()

            # Mutation
            child = mutate(child)

            new_population.append(child)

        population = new_population

    # Final best candidate
    final_best = min(population, key=fitness)
    print("\n=== Final Result ===")
    print(f"Fitness (MSE): {fitness(final_best):.6f}")
    print(f"Chromosome: {final_best}")

    # Verify against target points
    print("\nValues at target x:")
    for x, y in zip(TARGET_X, TARGET_Y):
        print(f"x={x:.3f} | target={y:.3f} | approx={evaluate_chromosome(final_best, x):.3f}")

if __name__ == "__main__":
    main()