from configparser import ConfigParser
import pygame
import gentools
import simulation
import utils


config = ConfigParser(converters={'tuple': utils.tuple_converter})
config.read('configuration.ini')


def loop(screen, clock, level):
    section = config['genetic-algorithm']
    population_size = section.getint('population-size')
    chromosome_size = section.getint('chromosome-size')
    bounds = section.gettuple('mutation-bounds')
    information = utils.Information()
    generations = section.getint('generations')
    generation = 0

    population = gentools.initialize(population_size, chromosome_size, bounds)
    population, running = simulation.run(screen, clock, level, population, information)
    while running and generation < generations:
        generation += 1
        information.generation = generation
        selected = gentools.tournament_selection(population, section.getint('tournament-size'))
        offspring = gentools.single_point_crossover(selected, section.getfloat('crossover-rate'))
        offspring = gentools.uniform_mutation(offspring, bounds)
        offspring, running = simulation.run(screen, clock, level, offspring, information)
        population = gentools.elite_succession(population, offspring, section.getint('elite-size'))


def initialize(level):
    pygame.init()
    pygame.display.set_caption('Smart Rockets')
    screen = pygame.display.set_mode((600, 600))
    screen.fill(level.background)
    pygame.display.flip()
    return screen


def main():
    level = utils.level('level-one')
    screen = initialize(level)
    clock = pygame.time.Clock()
    loop(screen, clock, level)
    pygame.quit()


if __name__ == '__main__':
    main()
