import pygame
from dataclasses import dataclass
from pygame import Vector2


def triangle_points(position, scale):
    x, y = position
    change = 10 * scale
    points = [(x, y - change),
              (x - (change / 2), y + change),
              (x + (change / 2), y + change)]
    return [Vector2(point) for point in points]


class Rocket:

    def __init__(self, position, scale=1):
        self.points = triangle_points(position, scale)
        self._speed = Vector2(0, -1)
        self.disabled = False

    @property
    def position(self):
        x = sum(point.x for point in self.points) / len(self.points)
        y = sum(point.y for point in self.points) / len(self.points)
        return Vector2(x, y)

    def _angle(self, acceleration):
        new_speed = self._speed + acceleration
        return self._speed.angle_to(new_speed)

    def _rotate(self, point, angle):
        center = self.position
        translated = point - center
        translated = translated.rotate(angle)
        return translated + center

    def boost(self, acceleration):
        acceleration = Vector2(acceleration)
        angle = self._angle(acceleration)
        self._speed += acceleration
        if not self.disabled:
            self.points = [self._rotate(point, angle) + self._speed for point in self.points]

    def draw(self, screen, color='#cb9ca1'):
        color = '#8c0032' if self.disabled else color
        pygame.draw.polygon(screen, color, self.points)


@dataclass
class Barrier:
    position: Vector2
    size: Vector2

    @staticmethod
    def fromtuple(values):
        x, y, width, height = values
        return Barrier(Vector2(x, y), Vector2(width, height))

    def draw(self, screen, color='#cb9ca1'):
        pygame.draw.rect(screen, color, (self.position, self.size))


@dataclass
class Target:
    position: Vector2
    radius: int

    @staticmethod
    def fromtuple(values):
        x, y, radius = values
        return Target(Vector2(x, y), radius)

    def draw(self, screen, color='#a8b545'):
        pygame.draw.circle(screen, color, self.position, self.radius)



