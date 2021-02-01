from configparser import ConfigParser
from typing import Sequence, Tuple
from dataclasses import dataclass
from model import Target, Barrier
import pygame


def tuple_converter(string):
    string = string.strip('()')
    values = map(float, string.split(', '))
    return tuple(values)


config = ConfigParser(converters={'tuple': tuple_converter})
config.read('configuration.ini')


def left_screen(screen, rocket):
    width, height = screen.get_size()
    x, y = rocket.position
    return not (0 < x < width and 0 < y < height)


def hit_barrier(barrier, rocket):
    rectangle = pygame.Rect(barrier.position, barrier.size)
    return rectangle.collidepoint(rocket.position)


def reached_target(target, rocket):
    distance = target.position.distance_to(rocket.position)
    return distance <= target.radius


def check_collisions(screen, level, rocket):
    return left_screen(screen, rocket) or \
        reached_target(level.target, rocket) or \
        any(hit_barrier(barrier, rocket) for barrier in level.barriers)


@dataclass
class Information:
    average: float = 0.0
    generation: int = 0


@dataclass
class GameLevel:
    target: Target
    barriers: Sequence[Barrier]
    position: Tuple[float, float]
    background: str


def level(name):
    section = config[name]
    background = section['background']
    position = section.gettuple('initial-position')
    target = Target.fromtuple(section.gettuple('target'))
    barriers = [Barrier.fromtuple(tuple_converter(line)) for line in section['barriers'].splitlines()]
    return GameLevel(target, barriers, position, background)

