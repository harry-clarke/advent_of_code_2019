class IntCode:

    def __init__(self, tape: [int]):
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
        }
        self.tape = tape

    def read(self, mode, param):
        return param if mode == 1 else self.tape[param]

    def read_params(self, unread: [(int, int)]):
        return [self.read(*p) for p in unread]

    # Reads parameters, making addresss lookups when necessary.
    # Always assumes last parameter is an output, and therefore performs no lookup.
    def read_params_output_tail(self, unread: [(int, int)]):
        params = [self.read(*p) for p in unread[:-1]]
        params.append(unread[-1][1])
        return params

    def add_instruction(self, params: [(int, int)]):
        in_1, in_2, out_addr = self.read_params_output_tail(params)
        self.tape[out_addr] = in_1 + in_2

    def mul_instruction(self, params: [(int, int)]):
        in_1, in_2, out_addr = self.read_params_output_tail(params)
        self.tape[out_addr] = in_1 * in_2

    def input_instruction(self, params: [(int, int)]):
        out_addr = params[0][1]
        in_1 = int(input('Please enter a value: '))
        self.tape[out_addr] = in_1

    def output_instruction(self, params: [(int, int)]):
        in_addr = self.read(*params[0])
        print(in_addr)

    def jump_if_true_instruction(self, params: [(int, int)]):
        condition, new_position = self.read_params(params)
        if condition != 0:
            self.position = new_position

    def jump_if_false_instruction(self, params: [(int, int)]):
        condition, new_position = self.read_params(params)
        if condition == 0:
            self.position = new_position

    def less_than_instruction(self, params: [(int, int)]):
        in_1, in_2, out_addr = self.read_params_output_tail(params)
        out = int(in_1 < in_2)
        self.tape[out_addr] = out

    def equals_instruction(self, params: [(int, int)]):
        in_1, in_2, out_addr = self.read_params_output_tail(params)
        out = int(in_1 == in_2)
        self.tape[out_addr] = out

    def run(self):
        while True:
            instr = str(self.tape[self.position])
            op_code = int(instr[-2:])
            if op_code == 99:
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


def run(tape: [int]):
    m = IntCode(tape)
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
