import enum
from collections.abc import MutableSequence
from itertools import repeat
from typing import Callable, Iterator, Union, Tuple


def __terminal_input__():
    while True:
        yield int(input('Please enter a value: '))


TERMINAL_INPUT = __terminal_input__()

TERMINAL_OUTPUT = print


def parameter_input(*args: int) -> Iterator[int]:
    return iter(args)


class Memory(Iterator):
    """
    Stores any output from the IntCode machine in self.memory
    To access output, simply reference self.memory
    Can also be used as input to another IntCode machine, creating a pipe between them.
    """

    def __init__(self):
        self.memory = []

    def store(self, value: int):
        # print(value)
        self.memory.insert(0, value)

    def __next__(self):
        if len(self.memory) == 0:
            raise StopIteration()
        return self.memory.pop()


STATUS_CODES = enum.Enum('STATUS_CODES', 'INIT RUNNING PAUSED FINISHED')
PAUSE_CODES = enum.Enum('PAUSE_CODES', 'READING')


class Tape(MutableSequence):

    def __init__(self, data=()):
        self.relative_base = 0
        self.list = []
        self.extend(data)

    def __len__(self) -> int:
        return len(self.list)

    def insert(self, index: int, v) -> None:
        if index < 0:
            raise IndexError('Tape doesn\'t support negative indices')
        ext = len(self.list) - index
        if ext > 0:
            self.list.extend(repeat(0, ext))
        self.list.insert(index, v)

    def __getitem__(self, i: Union[int, slice, Tuple[int, int]]):
        if isinstance(i, tuple):
            mode, param = i
            return {
                0: lambda: self[param],
                1: lambda: param,
                2: lambda: self[self.relative_base + param]
            }[mode]()
        if isinstance(i, slice):
            return [self[j] for j in range(i.start, i.stop, 1 if i.step is None else i.step)]
        if i < 0:
            raise IndexError('Tape doesn\'t support negative indices')
        if len(self.list) <= i:
            return 0
        return self.list[i]

    def __setitem__(self, i: Union[int, slice, tuple], vs) -> None:
        if isinstance(i, tuple):
            mode, param = i
            if mode == 1:
                raise ValueError('Can only write to an address')
            index = param if mode == 0 else self.relative_base + param
            self[index] = vs
            return
        if isinstance(i, slice):
            for j, v in zip(range(i.start, i.stop, i.step), vs):
                self[j] = v
            return
        if i < 0:
            raise IndexError('Tape doesn\'t support negative indices')
        ext = i - len(self.list) + 1
        if ext > 0:
            self.list.extend(repeat(0, ext))
        self.list[i] = vs

    def __delitem__(self, i: int) -> None:
        del self.list[i]


class IntCode:
    """
    - The computer's available memory should be larger than the initial program
    - Reads to unwritten memory returns 0
    """

    def __init__(self, tape: [int], stdin: Iterator[int] = TERMINAL_INPUT,
                 stdout: Callable[[int], None] = TERMINAL_OUTPUT):
        self.relative_base = 0
        self.status = STATUS_CODES.INIT
        self.pause_code = None
        self.stdout: Callable[[int], None] = stdout
        self.stdin: Iterator[int] = stdin
        self.position = 0
        self.OPCODES = {
            1: (3, self.add_instruction),
            2: (3, self.mul_instruction),
            3: (1, self.input_instruction),
            4: (1, self.output_instruction),
            5: (2, self.jump_if_true_instruction),
            6: (2, self.jump_if_false_instruction),
            7: (3, self.less_than_instruction),
            8: (3, self.equals_instruction),
            9: (1, self.adjust_relative_base_instruction)
        }
        self.tape = Tape(tape)

    def adjust_relative_base_instruction(self, params: [(int, int)]):
        adjustment = self.tape[params[0]]
        self.tape.relative_base += adjustment

    def add_instruction(self, params: [(int, int)]):
        in_1, in_2 = [self.tape[i] for i in params[:2]]
        self.tape[params[2]] = in_1 + in_2

    def mul_instruction(self, params: [(int, int)]):
        in_1, in_2 = [self.tape[i] for i in params[:2]]
        self.tape[params[2]] = in_1 * in_2

    def input_instruction(self, params: [(int, int)]):
        try:
            in_1 = next(self.stdin)
        except StopIteration:
            self.status = STATUS_CODES.PAUSED
            self.pause_code = PAUSE_CODES.READING
            return
        self.tape[params[0]] = in_1

    def output_instruction(self, params: [(int, int)]):
        in_addr = self.tape[params[0]]
        self.stdout(in_addr)

    def jump_if_true_instruction(self, params: [(int, int)]):
        condition, new_position = [self.tape[i] for i in params]
        if condition != 0:
            self.position = new_position

    def jump_if_false_instruction(self, params: [(int, int)]):
        condition, new_position = [self.tape[i] for i in params]
        if condition == 0:
            self.position = new_position

    def less_than_instruction(self, params: [(int, int)]):
        in_1, in_2 = [self.tape[i] for i in params[:2]]
        out = int(in_1 < in_2)
        self.tape[params[2]] = out

    def equals_instruction(self, params: [(int, int)]):
        in_1, in_2 = [self.tape[i] for i in params[:2]]
        out = int(in_1 == in_2)
        self.tape[params[2]] = out

    def run(self):
        self.status = STATUS_CODES.RUNNING
        while True:
            instr = str(self.tape[self.position])
            op_code = int(instr[-2:])
            if op_code == 99:
                self.status = STATUS_CODES.FINISHED
                return
            (param_count, op) = self.OPCODES[op_code]

            raw_params = self.tape[self.position + 1:self.position + param_count + 1]
            # Any modes not declared are considered '0'
            param_modes = reversed(instr[:-2].zfill(len(raw_params)))
            param_modes = list(map(int, param_modes))

            assert len(raw_params) == len(param_modes)

            params = list(zip(param_modes, raw_params))
            self.position += param_count + 1
            op(params)
            if self.status == STATUS_CODES.PAUSED:
                self.position -= len(params) + 1
                return


def run_as_function(tape: [int], parameters: [int]) -> [int]:
    mem = Memory()
    m = IntCode(tape, parameter_input(*parameters), mem.store)
    m.run()
    return mem.memory


def run(tape: [int], stdin: Iterator[int] = TERMINAL_INPUT):
    m = IntCode(tape, stdin)
    m.run()


def test_1():
    run([3, 0, 4, 0, 99])


def test_2():
    print('Answer 2 T1:')  # Input == 8
    run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8])
    print('Answer 2 T2:')  # Input < 8
    run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8])
    print('Answer 2 T3:')  # Input == 8
    run([3, 3, 1108, -1, 8, 3, 4, 3, 99])
    print('Answer 2 T4:')  # Input < 8
    run([3, 3, 1107, -1, 8, 3, 4, 3, 99])
    print('Answer 2 T5:')  # Boolean Input
    run([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9])
    print('Answer 2 T5:')  # Boolean Input
    run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1])


def test_parameter_input():
    print('Answer 2 T1:')  # Input == 8
    run([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], parameter_input(8))
    print('Answer 2 T2:')  # Input < 8
    run([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], parameter_input(1))
    print('Answer 2 T3:')  # Input == 8
    run([3, 3, 1108, -1, 8, 3, 4, 3, 99], parameter_input(9))
    print('Answer 2 T4:')  # Input < 8
    run([3, 3, 1107, -1, 8, 3, 4, 3, 99], parameter_input(9))
    print('Answer 2 T5:')  # Boolean Input
    run([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], parameter_input(2))
    print('Answer 2 T5:')  # Boolean Input
    run([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], parameter_input(0))


def test_memory():
    r = run_as_function([3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8], [8])
    assert 1 == r[0]
    r = run_as_function([3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8], [1])
    assert 1 == r[0]
    r = run_as_function([3, 3, 1108, -1, 8, 3, 4, 3, 99], [9])
    assert 0 == r[0]
    r = run_as_function([3, 3, 1107, -1, 8, 3, 4, 3, 99], [9])
    assert 0 == r[0]
    r = run_as_function([3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9], [2])
    assert 1 == r[0]
    r = run_as_function([3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1], [0])
    assert 0 == r[0]


def test_relative_base():
    r = run_as_function([109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99], [])
    assert [109, 1, 204, -1, 1001, 100, 1, 100, 1008, 100, 16, 101, 1006, 101, 0, 99] == r
    r = run_as_function([1102, 34915192, 34915192, 7, 4, 7, 99, 0], [])
    assert 16 == len(str(r[0]))


def test_large_numbers():
    r = run_as_function([104, 1125899906842624, 99], [])
    assert 1125899906842624 == r[0]


if __name__ == '__main__':
    # test_1()
    # test_2()
    # test_parameter_input()
    # test_memory()
    # test_large_numbers()
    pass
