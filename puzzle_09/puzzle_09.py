from util.intcode import IntCode, run_as_function


def read_tape():
    with open('input.txt') as f:
        s = f.readline()
        return list(map(int, s.split(',')))


TAPE = read_tape()


def answer_1():
    r = run_as_function(TAPE, [1])
    print('Answer 1: %s' % r[0])


def answer_2():
    r = run_as_function(TAPE, [2])
    print('Answer 2: %s' % r[0])


if __name__ == '__main__':
    answer_1()
    answer_2()
