from configparser import ConfigParser

import pygame

from model import Rocket
from utils import check_collisions, tuple_converter, reached_target

config = ConfigParser(converters={'tuple': tuple_converter})
config.read('configuration.ini')


def stop():
    return any(event.type == pygame.QUIT for event in pygame.event.get())


def rocket_dictionary(population, level):
    return {chromosome: Rocket(level.position) for chromosome in population}


def adapt(chromosome, distance, max_distance):
    parentage = max(0, max_distance - distance) / max_distance
    return int(len(chromosome) * parentage)


def calculate_score(rockets, level):
    max_distance = level.target.position.distance_to(level.position)
    for chromosome, rocket in rockets.items():
        reached = reached_target(level.target, rocket)
        distance = 0 if reached else rocket.position.distance_to(level.target.position)
        chromosome.score = distance if not reached else 0
        chromosome.adaptation_index = adapt(chromosome, distance, max_distance)


def run(screen, clock, level, population, information):
    rockets = rocket_dictionary(population, level)
    frames, frame = config['genetic-algorithm'].getint('chromosome-size'), 0
    while not stop() and frame < frames:
        render_frame(screen, frame, level, rockets, information)
        frame += 1
        clock.tick(120)
    calculate_score(rockets, level)
    information.average = average(population)
    return population, frame == frames


def render_frame(screen, frame, level, rockets, information):
    screen.fill(level.background)
    for chromosome, rocket in rockets.items():
        rocket.boost(chromosome[frame])
        rocket.disabled = check_collisions(screen, level, rocket)
        rocket.draw(screen)
    for barrier in level.barriers:
        barrier.draw(screen, '#836fa9')
    level.target.draw(screen)
    render_information(screen, information)
    pygame.display.update()


def render_information(screen, information):
    font = pygame.font.SysFont('consolas', 15)
    generation_surface = font.render(f'Generation: {information.generation}', True, (0, 0, 0))
    average_surface = font.render(f'Average fitness: {information.average:.2f}', True, (0, 0, 0))
    screen.blit(generation_surface, (10, 10))
    screen.blit(average_surface, (10, 30))


def average(population):
    return sum(chromosome.score for chromosome in population) / len(population)

