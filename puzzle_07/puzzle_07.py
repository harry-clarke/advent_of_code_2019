import itertools

from util.intcode import run_as_function, IntCode, Memory, STATUS_CODES


def read_tape():
    with open('input.txt') as f:
        s = f.readline()
        tape = list(map(int, s.split(',')))
    return tape


TAPE = read_tape()


def run_amplifiers(config: [int], tape=TAPE):
    v = 0
    for c in config:
        v = run_as_function(tape, [c, v])[0]
    return v


def run_amplifier_loop(config: [int], tape=TAPE):
    inputs = [Memory() for _ in config]
    outputs = [mem.store for mem in inputs]
    machines = []
    for x in range(len(config)):
        m_in = inputs[x]
        m_in.store(config[x])
        m_out = outputs[(x + 1) % len(config)]
        machines.append(IntCode(tape, m_in, m_out))

    inputs[0].store(0)

    while machines[-1].status != STATUS_CODES.FINISHED:
        for machine in machines:
            machine.run()
    return inputs[0].memory[0]


def test_1():
    r = run_amplifiers([4, 3, 2, 1, 0], [3, 15, 3, 16, 1002, 16, 10, 16, 1, 16, 15, 15, 4, 15, 99, 0, 0])
    assert 43210 == r
    r = run_amplifiers([0, 1, 2, 3, 4], [3, 23, 3, 24, 1002, 24, 10, 24, 1002, 23, -1, 23,
                                         101, 5, 23, 23, 1, 24, 23, 23, 4, 23, 99, 0, 0])
    assert 54321 == r
    r = run_amplifiers([1, 0, 4, 3, 2], [3, 31, 3, 32, 1002, 32, 10, 32, 1001, 31, -2, 31, 1007, 31, 0, 33,
                                         1002, 33, 7, 33, 1, 33, 31, 31, 1, 32, 31, 31, 4, 31, 99, 0, 0, 0])
    assert 65210 == r


def answer():
    configs = itertools.permutations(range(5), 5)
    best_value = None
    best_config = None
    for c in configs:
        v = run_amplifiers(c)
        if best_value is None or v > best_value:
            best_value = v
            best_config = c
    print('Answer 1: %s %s' % (best_value, best_config))


def test_2():
    # temp()
    r = run_amplifier_loop([9, 8, 7, 6, 5], [3, 26, 1001, 26, -4, 26, 3, 27, 1002, 27, 2, 27, 1, 27, 26,
                                             27, 4, 27, 1001, 28, -1, 28, 1005, 28, 6, 99, 0, 0, 5])
    assert 139629729 == r
    r = run_amplifier_loop([9, 7, 8, 5, 6],
                           [3, 52, 1001, 52, -5, 52, 3, 53, 1, 52, 56, 54, 1007, 54, 5, 55, 1005, 55, 26, 1001, 54,
                            -5, 54, 1105, 1, 12, 1, 53, 54, 53, 1008, 54, 0, 55, 1001, 55, 1, 55, 2, 53, 55, 53, 4,
                            53, 1001, 56, -1, 56, 1005, 56, 6, 99, 0, 0, 0, 0, 10])
    assert 18216 == r


def answer_2():
    configs = itertools.permutations(range(5, 10), 5)
    best_value = None
    best_config = None
    for c in configs:
        v = run_amplifier_loop(c)
        if best_value is None or v > best_value:
            best_value = v
            best_config = c
    print('Answer 2: %s %s' % (best_value, best_config))


if __name__ == '__main__':
    test_1()
    answer()
    answer_2()
    pass
