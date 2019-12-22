from __future__ import annotations

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
    moons: list[Moon]

    def __init__(self, moons: set[tuple[int]]):
        self.moons = list([Moon(self, pos) for pos in moons])

    def step(self):
        for moon in self.moons:
            moon.velocity_step()
        for moon in self.moons:
            moon.position_step()

    def get_total_energy(self):
        return sum(moon.get_total_energy() for moon in self.moons)

    def __str__(self):
        return str(self.moons)


class Moon:
    jupiter: Jupiter
    pos: [int]
    vel: [int]

    def __init__(self, jupiter, pos):
        self.jupiter = jupiter
        self.pos = pos
        self.vel = [0 for _ in pos]

    def get_total_energy(self):
        return self.get_potential_energy() * self.get_kinetic_energy()

    def get_potential_energy(self):
        return sum(map(abs, self.pos))

    def get_kinetic_energy(self):
        return sum(map(abs, self.vel))

    def velocity_step(self):
        self.vel = [
            vel_n + sum([
                0 if (diff := moon.pos[n] - self.pos[n]) == 0 else copysign(1, diff)
                for moon in self.jupiter.moons
            ])
            for n, vel_n in enumerate(self.vel)
        ]

    def position_step(self):
        self.pos = [p + v for p, v in zip(self.pos, self.vel)]

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


if __name__ == '__main__':
    test_1()
    answer_1()
