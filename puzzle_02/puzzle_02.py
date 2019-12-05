from _operator import add, mul
from math import ceil

TEST_INPUT_1 = [
    ([1, 9, 10, 3, 2, 3, 11, 0, 99, 30, 40, 50], [3500, 9, 10, 70, 2, 3, 11, 0, 99, 30, 40, 50]),
    ([1, 0, 0, 0, 99], [2, 0, 0, 0, 99]),
    ([2, 3, 0, 3, 99], [2, 3, 0, 6, 99]),
    ([2, 4, 4, 5, 99, 0], [2, 4, 4, 5, 99, 9801]),
    ([1, 1, 1, 4, 99, 5, 6, 0, 99], [30, 1, 1, 4, 2, 5, 6, 0, 99])
]

OP_CODES = {
    1: add,
    2: mul
}

TARGET = 19690720


def int_code(original_tape):
    tape = list(original_tape)
    for i in map(lambda i: i * 4, range(ceil(len(tape) / 4))):
        if tape[i] == 99:
            return tape
        (op_code, input_1_index, input_2_index, output_index) = tape[i:i + 4]
        input_1 = tape[input_1_index]
        input_2 = tape[input_2_index]
        output = OP_CODES[op_code](input_1, input_2)
        tape[output_index] = output
    return tape


def run_test_1():
    for i in range(len(TEST_INPUT_1)):
        (test_input, test_expectation) = TEST_INPUT_1[i]
        test_result = int_code(test_input)
        passed = test_result == test_expectation
        print('Answer 1 T%d(%s): %s' % (i, 'Pass' if passed else 'Fail', test_result))


def answer_2(tape, target):
    for noun in range(100):
        for verb in range(100):
            t = list(tape)
            t[1] = noun
            t[2] = verb
            r = int_code(t)[0]
            if r == target:
                return noun * 100 + verb
    return None


def main():
    with open('input.txt') as f:
        run_test_1()
        s = f.readline()
        t = list(map(int, s.split(',')))
        t[1] = 12
        t[2] = 2
        print('Answer 1: %s' % int_code(t)[0])
        print('Answer 2: %s' % answer_2(t, TARGET))


if __name__ == '__main__':
    main()
