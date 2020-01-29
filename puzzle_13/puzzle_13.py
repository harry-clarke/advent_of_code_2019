import math
from typing import Dict, Tuple

from util.intcode import IntCode


class Screen:

    def __init__(self):
        self.coords: Dict[Tuple[int, int], int] = {}
        self.width: int = 0
        self.height: int = 0

    def update_all(self, data: [int]):
        if data == []:
            return
        self.update(*data[:3])
        self.update_all(data[3:])

    def update(self, x, y, tile_id):
        self.width = x + 1 if x + 1 > self.width else self.width
        self.height = y + 1 if y + 1 > self.height else self.height
        if tile_id == 0:
            if (x, y) in self.coords:
                del self.coords[x, y]
        else:
            self.coords[x, y] = tile_id

    def __str_tile__(self, x, y):
        return {
            0: ' ',
            1: '+',
            2: '#',
            3: '-',
            4: 'o'
        }[
            0 if (x, y) not in self.coords else self.coords[x, y]
        ]

    def __str__(self) -> str:
        s = '+' * (self.width + 2) + '\n'
        for y in range(self.height):
            s += '+'
            for x in range(self.width):
                s += self.__str_tile__(x, y)
            s += '+\n'
        s += '+' * (self.width + 2)

        return s


def get_std_out(screen: Screen):
    vs = []
    while True:
        v = yield
        vs.append(v)
        if len(vs) == 3:
            screen.update_all(vs)
            vs = []


def create_arcade():
    with open('input.txt') as f:
        s = f.readline()
        tape = list(map(int, s.split(',')))
    screen = Screen()
    stdout = get_std_out(screen)
    next(stdout)
    intcode = IntCode(tape, stdout=stdout.send)
    return intcode, screen


def test_1():
    screen = Screen()
    stdout = get_std_out(screen)
    next(stdout)
    for v in [1, 2, 3, 6, 5, 4]:
        stdout.send(v)
    print(screen)


def answer_1():
    intcode, screen = create_arcade()
    intcode.run()
    print(screen)
    answer = len(list(filter(lambda tile_id: tile_id == 2, screen.coords.values())))
    print(f'Answer 1: {answer}')


if __name__ == '__main__':
    # test_1()
    answer_1()
