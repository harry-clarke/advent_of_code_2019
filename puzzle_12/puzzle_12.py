from __future__ import annotations

import sys
from typing import Tuple

import humanfriendly
import time
from math import copysign

INPUT = (
    (-4, -9, -3),
    (-13, -11, 0),
    (-17, -7, 15),
    (-16, 4, 2)
)

TEST = (
    (-1, 0, 2),
    (2, -10, -7),
    (4, -8, 8),
    (3, 5, -1)
)


class Jupiter:
    moons: Tuple[Moon]

    def __init__(self, moons):
        self.moons = tuple([Moon(self, pos) for pos in moons])

    def step(self):
        for moon in self.moons:
            moon.velocity_step()
        for moon in self.moons:
            moon.position_step()

    def get_total_energy(self):
        return sum(moon.get_total_energy() for moon in self.moons)

    def get_state(self):
        return tuple(m.get_state() for m in self.moons)

    def __str__(self):
        return str(self.moons)


class Moon:
    jupiter: Jupiter
    pos: Tuple[int]
    vel: Tuple[int]

    def __init__(self, jupiter, pos):
        self.jupiter = jupiter
        self.pos = pos
        self.vel = tuple(0 for _ in pos)

    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()

    def get_potential_energy(self):
        return sum(map(abs, self.pos))

    def get_kinetic_energy(self):
        return sum(map(abs, self.vel))

    def velocity_step(self):
        self.vel = tuple(
            vel_n + sum(
                0 if (diff := moon.pos[n] - self.pos[n]) == 0 else int(copysign(1, diff))
                for moon in self.jupiter.moons
            )
            for n, vel_n in enumerate(self.vel)
        )

    def position_step(self):
        self.pos = tuple(p + v for p, v in zip(self.pos, self.vel))

    def get_state(self):
        return self.pos, self.vel

    def __repr__(self):
        return self.__str__()

    def __str__(self):
        return str({'pos': self.pos, 'vel': self.vel})


def test_1():
    j = Jupiter(TEST)
    for i in range(10):
        j.step()
    assert 9 == j.moons[1].get_potential_energy()
    assert 5 == j.moons[1].get_kinetic_energy()
    assert 179 == j.get_total_energy()


def answer_1():
    j = Jupiter(INPUT)
    for i in range(1000):
        j.step()
    print(f'Answer 1: {j.get_total_energy()}')


def find_dimensional_orbit(j, n):
    def map_state(s):
        return [[v[n] for v in m] for m in s]
    initial_state = map_state(j.get_state())
    i = 1
    it = int(time.perf_counter())
    ct = it
    j.step()
    while map_state(j.get_state()) != initial_state:
        i += 1
        j.step()
        if time.perf_counter() - ct >= 5:
            ct = int(time.perf_counter())
            print(
                f'@{ct - it}s: {i} steps ({i / ct - it}/s)'
            )
    return i, j


def find_complete_orbit(j):
    initial_state = j.get_state()



def test_2():
    j = Jupiter(TEST)
    i, j = find_complete_orbit(j)
    assert 2772 == i
    print(f'Answer 2, T1: {i} ({j}')


def answer_2():
    j = Jupiter(INPUT)
    i, j = find_complete_orbit(j)
    print(f'Answer 2: {i} ({j})')


if __name__ == '__main__':
    test_1()
    answer_1()
    test_2()
    answer_2()
