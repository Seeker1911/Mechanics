import math

from geom2d.nums import are_close_enough
from geom2d.point import Point
from geom2d.polygon import Polygon
from geom2d.vectors import make_vector_between


class Circle:
    def __init__(self, center: Point, radius: float):
        self.center = center
        self.radius = radius

    def area(self):
        return math.pi * self.radius ** 2

    def circumference(self):
        return 2 * math.pi * self.radius

    def contains_point(self, point: Point):
        return point.distance_to(self.center) < self.radius

    def overlaps(self, other):
        centers_dist = self.center.distance_to(other.center)
        radii_sum = self.radius + other.radius
        return centers_dist < radii_sum

    def penetration_vector(self, other):
        if not self.overlaps(other):
            return None

        direction = make_vector_between(other.center, self.center)
        centers_dist = self.center.distance_to(other.center)
        radii_sum = self.radius + other.radius

        return direction.with_length(radii_sum - centers_dist)

    def to_polygon(self, divisions):
        angle_delta = 2 * math.pi / divisions
        return Polygon(
            [self.__point_at_angle(angle_delta * i)
             for i in range(divisions)]
        )

    def __point_at_angle(self, angle):
        return Point(
            self.center.x + self.radius * math.cos(angle),
            self.center.y + self.radius * math.sin(angle)
        )

    def __eq__(self, other):
        if self is other:
            return True

        if not isinstance(other, Circle):
            return False

        return self.center == other.center \
               and are_close_enough(self.radius, other.radius)

    def __str__(self):
        return f'circle c = {self.center}, r = {self.radius}'