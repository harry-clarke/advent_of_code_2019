from util.intcode import run


def answer():
    with open('input.txt') as f:
        s = f.readline()
        tape = list(map(int, s.split(',')))
        run(tape)