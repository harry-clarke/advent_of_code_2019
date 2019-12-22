from enum import Enum

from util.intcode import IntCode, STATUS_CODES, Memory


class Panel:
    rendered_cells: {(int, int): int}
    start_x: int
    end_x: int
    start_y: int
    end_y: int

    def __init__(self):
        self.start_x = 0
        self.end_x = 0
        self.start_y = 0
        self.end_y = 0
        self.rendered_cells = {}

    def get(self, coord):
        if coord not in self.rendered_cells:
            self.rendered_cells[coord] = 0
            self.__adjust_size(coord)
        return self.rendered_cells[coord]

    def set(self, coord, colour):
        self.__adjust_size(coord)
        self.rendered_cells[coord] = colour

    def __adjust_size(self, coord):
        x, y = coord

        if x > self.end_x:
            self.end_x = x
        elif x < self.start_x:
            self.start_x = x

        if y > self.end_y:
            self.end_y = y
        elif y < self.start_y:
            self.start_y = y

    def __str__(self) -> str:
        s = ''
        for y in reversed(range(self.start_y, self.end_y + 1)):
            for x in range(self.start_x, self.end_x + 1):
                if (x, y) in self.rendered_cells and self.rendered_cells[(x, y)] == 1:
                    s += '#'
                else:
                    s += ' '
            s += '\n'
        return s


class Robot:
    DIRECTION = Enum('DIRECTION', 'UP RIGHT DOWN LEFT')

    direction: DIRECTION
    coord: (int, int)
    brain: IntCode
    panel: Panel
    memory: Memory

    def __init__(self, coord, panel: Panel):
        self.panel = panel
        self.direction = Robot.DIRECTION.UP
        self.coord = coord
        self.memory = Memory()
        with open('input.txt') as f:
            s = f.readline()
            tape = list(map(int, s.split(',')))
        self.brain = IntCode(tape, self.__brain_input(), self.__brain_output)

    def run(self):
        self.brain.run()

    def act(self, colour, rotation_bit):
        self.panel.set(self.coord, colour)
        self.change_direction(rotation_bit)
        self.move_forward()

    def move_forward(self):
        dx, dy = {
            Robot.DIRECTION.UP: (0, 1),
            Robot.DIRECTION.RIGHT: (1, 0),
            Robot.DIRECTION.DOWN: (0, -1),
            Robot.DIRECTION.LEFT: (-1, 0)
        }[self.direction]
        x, y = self.coord
        self.coord = (x + dx, y + dy)

    def change_direction(self, rotation_bit):
        if rotation_bit == 0:
            self.__turn_left()
        elif rotation_bit == 1:
            self.__turn_right()
        else:
            raise ValueError()

    def __turn_left(self):
        self.direction = {
            Robot.DIRECTION.UP: Robot.DIRECTION.LEFT,
            Robot.DIRECTION.RIGHT: Robot.DIRECTION.UP,
            Robot.DIRECTION.DOWN: Robot.DIRECTION.RIGHT,
            Robot.DIRECTION.LEFT: Robot.DIRECTION.DOWN
        }[self.direction]

    def __turn_right(self):
        self.direction = {
            Robot.DIRECTION.UP: Robot.DIRECTION.RIGHT,
            Robot.DIRECTION.RIGHT: Robot.DIRECTION.DOWN,
            Robot.DIRECTION.DOWN: Robot.DIRECTION.LEFT,
            Robot.DIRECTION.LEFT: Robot.DIRECTION.UP
        }[self.direction]

    def __brain_output(self, v):
        self.memory.store(v)
        assert len(self.memory.memory) <= 2
        if len(self.memory.memory) == 2:
            self.act(*list(self.memory))

    def __brain_input(self):
        while True:
            yield self.panel.get(self.coord)


def answer_1():
    p = Panel()
    r = Robot((0, 0), p)
    r.run()
    cell_count = len(p.rendered_cells)
    print(f'Answer 1: {cell_count}')


def answer_2():
    p = Panel()
    p.set((0, 0), 1)
    r = Robot((0, 0), p)
    r.run()
    print(p)


if __name__ == '__main__':
    answer_1()
    answer_2()
