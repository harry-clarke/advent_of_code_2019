from __future__ import annotations
from functools import reduce
from math import pi, hypot, atan, copysign, degrees, atan2
from typing import Callable, Union, List, Tuple, Optional

TEST_1 = (
    ['.#..#', '.....', '#####', '....#', '...##'],
    ['.7..7', '.....', '67775', '....7', '...87']
)


class AsteroidField:
    COORD = Tuple[int, int]
    DISTANCE = float
    BEARING = float
    # Where a given coordinate is in relation to the current object
    RELATIVE_LOCATION = {COORD: (BEARING, DISTANCE)}
    RELATIVE_LOCATIONS = {COORD: RELATIVE_LOCATION}
    # What is in the immediate line of sight for an object at a given bearing
    LINE_OF_SIGHT = {BEARING: COORD}
    LINES_OF_SIGHT = {COORD: LINE_OF_SIGHT}

    asteroids: {COORD}
    # Only maps asteroids that are reachable through a line of sight
    asteroid_map: RELATIVE_LOCATIONS

    def __init__(self, asteroids: Union[List[COORD], List[str]]):
        if isinstance(asteroids[0], str):
            asteroids = AsteroidField.__parse_asteroid_field(asteroids)
        self.asteroids = set(asteroids)
        self.asteroid_map = {}

    def calc_all_lines_of_site(self) -> LINES_OF_SIGHT:
        for coords in self.asteroids:
            asteroid = Asteroid(self, coords)
            asteroid.calc_lines_of_sight()
        return self.asteroid_map

    def show_field_los(self) -> str:
        return self.__define_field(lambda *coord: str(len(self.asteroid_map[coord])))

    def __define_field(self, f: Callable[[int, int], str]):
        def tuple_max(a, b):
            ax, ay = a
            bx, by = b
            return max(ax, bx), max(ay, by)

        width, height = reduce(tuple_max, self.asteroids)
        width += 1
        height += 1

        field = [['.' for _ in range(width)] for _ in range(height)]
        for x, y in self.asteroids:
            field[y][x] = f(x, y)
        field_str = ''.join([''.join(row) + '\n' for row in field])
        return field_str

    def __str__(self) -> str:
        return self.__define_field(lambda *_: '#')

    @staticmethod
    def __parse_asteroid_field(lines: [str]) -> [(int, int)]:
        """
        Returns asteroid coords as a list sorted left-right top-bottom
        """
        asteroids = []
        for y, line in enumerate(lines):
            for x, cell in enumerate(line.strip()):
                if cell == '#':
                    asteroids.append((x, y))
        return asteroids


class Asteroid:
    def __init__(self, asteroid_field: AsteroidField, coords: AsteroidField.COORD):
        self.asteroid_field = asteroid_field
        self.coords = coords
        self.res = {}
        self.los: AsteroidField.LINE_OF_SIGHT = {}

    def calc_lines_of_sight(self) -> AsteroidField.LINE_OF_SIGHT:
        if self.coords in self.asteroid_field.asteroid_map:
            return self.asteroid_field.asteroid_map[self.coords]

        for remote in self.asteroid_field.asteroids:
            if remote == self.coords:
                continue
            displacement = self.calc_line_of_sight(remote)
            if displacement is not None:
                self.res[remote] = displacement
                bearing, distance = displacement
                self.los[bearing] = remote

        self.asteroid_field.asteroid_map[self.coords] = self.res
        return self.res

    def calc_line_of_sight(self: Asteroid, remote: AsteroidField.COORD) -> Optional[
            Tuple[AsteroidField.BEARING, AsteroidField.DISTANCE]]:
        if remote in self.asteroid_field.asteroid_map:
            if self.coords in self.asteroid_field.asteroid_map[remote]:
                recip_bearing, distance = self.asteroid_field.asteroid_map[remote][self.coords]
                bearing = (recip_bearing + 180) % 360
                return bearing, distance
            else:
                return
        else:
            bearing, distance = Asteroid.__calc_los(self.coords, remote)
            if bearing in self.los:
                other = self.los[bearing]
                if self.res[other][1] > distance:
                    del self.res[other]
                    return bearing, distance
            else:
                return bearing, distance

    @staticmethod
    def __calc_los(a1: AsteroidField.COORD, a2: AsteroidField.COORD) -> (AsteroidField.BEARING, AsteroidField.DISTANCE):
        (x1, y1), (x2, y2) = a1, a2
        dx, dy = x2 - x1, y1 - y2
        dist = hypot(dx, dy)
        bearing = int((90 - degrees(atan2(dy, dx))) % 360)
        return bearing, dist


def test_1():
    af = AsteroidField(TEST_1[0])
    af.calc_all_lines_of_site()
    # los = af.calc_asteroid_los((1, 0))
    # print(af.asteroid_map[(1, 0)])
    # for l in los:
    #     print(l)
    print(af.show_field_los())
    # print(af)


if __name__ == '__main__':
    test_1()
