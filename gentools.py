import copy
import random
from operator import attrgetter

from pygame import Vector2


class Chromosome:

    def __init__(self, genes, score=100000):
        self.genes = genes
        self.score = score
        self.adaptation_index = 0

    @staticmethod
    def random(size, bounds):
        random_x = [random.uniform(bounds[0], bounds[1]) for _ in range(size)]
        random_y = [random.uniform(bounds[0], bounds[1]) for _ in range(size)]
        genes = [Vector2(x, y) for x, y in zip(random_x, random_y)]
        return Chromosome(genes)

    def __len__(self):
        return len(self.genes)

    def __getitem__(self, item):
        return self.genes[item]

    def __repr__(self):
        return f'{self.__class__.__name__}(score={self.score}, ' \
               f'adaptation_index={self.adaptation_index}, genes={self.genes})'


def initialize(population_size, chromosome_size, bounds):
    return [Chromosome.random(chromosome_size, bounds) for _ in range(population_size)]


def tournament_selection(population, size=20):
    selected = []
    for _ in range(len(population)):
        tournament = random.choices(population, k=size)
        winner = min(tournament, key=attrgetter('score'))
        selected.append(copy.deepcopy(winner))
    return selected


def single_point_crossover(population, rate=0.3):
    offsprings = []
    pairs = [random.sample(population, k=2) for _ in range((len(population) + 1) // 2)]
    for parents in pairs:
        offspring = parents if random.random() > rate else _produce_offspring(*parents)
        offsprings.extend(offspring)
    return offsprings


def _produce_offspring(father, mother):
    cut_point = random.randint(0, len(father))
    genes_one = father[:cut_point] + mother[cut_point:]
    genes_two = mother[:cut_point] + father[cut_point:]
    return Chromosome(genes_one), Chromosome(genes_two)


def uniform_mutation(population, bounds, rate=0.3):
    mutated = []
    for chromosome in population:
        mutant = chromosome if random.random() > rate else _mutate(chromosome, bounds)
        mutated.append(mutant)
    return mutated


def _mutate(chromosome, bounds):
    mutated = []
    lower, upper = bounds
    for index, gene in enumerate(chromosome):
        if index > chromosome.adaptation_index and random.random() < 0.5:
            x = random.uniform(lower, upper)
            y = random.uniform(lower, upper)
            mutated.append(Vector2(x, y))
        else:
            mutated.append(gene)
    return Chromosome(mutated)


def elite_succession(parents, offspring, size=10):
    elite = sorted(offspring + parents, key=attrgetter('score'))
    return elite if size >= len(parents) else elite[:size] + offspring[size:]



