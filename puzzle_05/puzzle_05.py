class IntCode:

    def __init__(self, tape: [int]):
        self.OPCODES = {
            1: (3, self.add_instruction),
            2: (3, self.mul_instruction),
            3: (1, self.input_instruction),
            4: (1, self.output_instruction)
        }
        self.tape = tape

    def read(self, mode, param):
        return param if mode == 1 else self.tape[param]

    # Reads parameters, making addresss lookups when necessary.
    # Always assumes last parameter is an output, and therefore performs no lookup.
    def read_params_output_tail(self, unread: [(int, int)]):
        params = [self.read(p[0], p[1]) for p in unread[:-1]]
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
        in_1 = int(input('Please enter a value'))
        self.tape[out_addr] = in_1

    def output_instruction(self, params: [(int, int)]):
        in_addr = self.read(*params[0])
        print(in_addr)

    def run(self):
        pos = 0
        while True:
            instr = str(self.tape[pos])
            op_code = int(instr[-2:])
            if op_code == 99:
                return
            (param_count, op) = self.OPCODES[op_code]

            raw_params = self.tape[pos + 1:pos + param_count + 1]
            # Any modes not declared are considered '0'
            param_modes = reversed(instr[:-2].zfill(len(raw_params)))
            param_modes = list(map(int, param_modes))

            assert len(raw_params) == len(param_modes)

            params = list(zip(param_modes, raw_params))
            op(params)
            pos += param_count + 1


def test_1():
    tape = [3,0,4,0,99]
    m = IntCode(tape)
    m.run()

def answer_1():
    with open('input.txt') as f:
        s = f.readline()
        tape = list(map(int, s.split(',')))
        machine = IntCode(tape)
        machine.run()


if __name__ == '__main__':
    # test_1()
    answer_1()