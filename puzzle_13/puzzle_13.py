import math
from functools import reduce
from getpass import getpass
from os import linesep
from time import sleep
from typing import Dict, Tuple, Optional, Iterator, Generator

from util.intcode import IntCode, STATUS_CODES


class Screen:

    def __init__(self):
        self.score = 0
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

    def __str_line(self) -> str:
        return '+' * (self.width + 2)

    def __str__(self) -> str:
        s = self.__str_line() + linesep \
            + f'+ Score: {self.score}' + linesep \
            + self.__str_line() + linesep
        for y in range(self.height):
            s += '+'
            for x in range(self.width):
                s += self.__str_tile__(x, y)
            s += '+\n'
        s += '+' * (self.width + 2)

        return s

    def update_score(self, score):
        self.score = score


class Bot:
    def __init__(self):
        self.ball_pos: Optional[Tuple[int, int]] = None
        self.ball_vel: Optional[Tuple[int, int]] = None
        self.pad_pos: Optional[Tuple[int, int]] = None
        self.arcade = None

    def set_arcade(self, arcade):
        self.arcade = arcade

    def std_in(self, x, y, tile_id):
        if tile_id == 3:
            self.pad_pos = x, y
        elif tile_id == 4:
            if self.ball_pos is not None:
                px, py = self.ball_pos
                self.ball_vel = x - px, y - py
            self.ball_pos = x, y

    def __move(self, move):
        return move

    def std_out(self) -> int:
        ball_x, ball_y = self.ball_pos
        pad_x, pad_y = self.pad_pos
        if self.ball_vel is None:
            move = int(math.copysign(1, ball_x - pad_x))
            return self.__move(move)

        if ball_x == pad_x and pad_y - ball_y == 1:  # If the pad is on the ball, don't move it
            return self.__move(0)
        move = int(math.copysign(1, self.ball_vel[0] + ball_x - pad_x))
        return self.__move(move)


class Manual:

    def __init__(self):
        self.arcade = None

    def set_arcade(self, arcade):
        self.arcade = arcade

    def std_in(self, _x, _y, _tile_id):
        pass

    def std_out(self):
        print(self.arcade)
        i = input()
        return {
            '': 0,
            's': 0,
            'a': -1,
            'd': 1
        }[i]


class Arcade:
    def __init__(self, player=None):
        self.screen: Screen = Screen()
        self.intcode: IntCode
        self.player = player if player is not None else Manual()
        self.player.set_arcade(self)

        self.stdout: Generator[None] = self.__get_std_out()

        with open('input.txt') as f:
            s = f.readline()
            tape = list(map(int, s.split(',')))

        next(self.stdout)
        self.intcode = IntCode(tape, stdin=self.__get_std_in(), stdout=self.stdout.send)

    def insert_coin(self):
        self.intcode.tape[0] = 2

    def __get_std_in(self):
        while True:
            yield self.player.std_out()

    def __get_std_out(self):
        vs = []
        while True:
            v = yield
            vs.append(v)
            if len(vs) == 3:
                if vs[0] == -1 and vs[1] == 0:
                    self.screen.update_score(vs[2])
                else:
                    self.screen.update(*vs)
                    self.player.std_in(*vs)
                vs = []

    def test_1(self):
        for v in [1, 2, 3, 6, 5, 4]:
            self.stdout.send(v)
        print(self.screen)

    def __str__(self):
        return str(self.screen)

    def run(self):
        while self.intcode.status is not STATUS_CODES.FINISHED:
            self.intcode.run()
        return self.screen.score


def test_1():
    Arcade().test_1()


def answer_1():
    arcade = Arcade()
    arcade.intcode.run()
    print(arcade)
    answer = len(list(filter(lambda tile_id: tile_id == 2, arcade.screen.coords.values())))
    print(f'Answer 1: {answer}')


def answer_2():
    player = Bot()
    arcade = Arcade(player)
    arcade.insert_coin()
    score = arcade.run()
    print(f'Answer 2: {score}')


if __name__ == '__main__':
    # test_1()
    # answer_1()
    answer_2()
