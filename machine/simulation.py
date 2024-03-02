from machine.isa import Opcode, OperandType


class DataPath:
    def __init__(self, memory_size: int, data_mem_init_state, input_buffer: list):
        self.min_val: int = -2 ** 31
        self.max_val: int = 2 ** 31 - 1

        self.data_mem = [0] * memory_size

        self.input_buffer = input_buffer
        self.output_buffer = []

        self.acc = 0
        self.zero = True
        self.address_reg = 0
        self.data_reg = 0

        for i, val in enumerate(data_mem_init_state):
            self.data_mem[i] = val

    def set_flags(self, val):
        self.zero = val == 0

    def has_next_input_token(self):
        return len(self.input_buffer)

    def next_input_token(self):
        return ord(self.input_buffer.pop(0))

    def is_zero(self) -> bool:
        return self.zero

    def address_reg_set(self, value: int):
        assert self.min_val <= value <= self.max_val, "overflow occurred"
        self.address_reg = value

    def data_reg_put(self, value: int):
        assert self.min_val <= value <= self.max_val, "overflow occurred"
        self.data_reg = value

    def latch_mem(self):
        self.data_mem[self.address_reg] = self.acc

    def latch_acc(self, from_mem=True):
        if from_mem:
            self.acc = self.data_mem[self.address_reg]
        else:
            self.acc = self.data_reg

    def latch_data_reg(self):
        self.data_reg = self.data_mem[self.address_reg]

    def acc_wr(self, sel: Opcode):
        if sel in {Opcode.ADD}:
            self.acc = self.__alu()
        if sel == Opcode.DIV:
            self.acc = self.acc / self.data_reg
        if sel == Opcode.MOD:
            self.acc = self.acc % self.data_reg

    def __alu(self):
        result = self.acc + self.data_reg
        if result > self.max_val:
            result = self.min_val + (result - self.max_val) - 1
        if result < self.min_val:
            result = self.max_val - (self.min_val - result) + 1
        return result

    def output(self):
        symbol = chr(self.acc)
        print(f"{{new output symbol '{symbol}' will be added to {repr(''.join(self.output_buffer))}}}")
        self.output_buffer.append(symbol)


class ControlUnit:

    def __init__(self, code, data_path):
        self.code = code
        self.instr_ptr = 0
        self.data_path = data_path
        self._tick = 0

    def tick(self):
        self._tick += 1
        print(self)

    def current_tick(self):
        return self._tick

    def get_operand(self, instr):
        if instr[1] is None:
            return None
        op_type = instr[1][0]
        op_arg = instr[1][1]
        if op_type == OperandType.CONSTANT:
            self.data_path.data_reg_put(op_arg)
            return op_arg
        if op_type == OperandType.DIRECT_ADDRESS:
            self.data_path.address_reg_set(op_arg)
            self.data_path.latch_data_reg()
            self.tick()
            return self.data_path.data_reg
        if op_type == OperandType.INDIRECT_ADDRESS:
            self.data_path.address_reg_set(op_arg)
            self.data_path.latch_data_reg()
            self.tick()
            self.data_path.address_reg_set(self.data_path.data_reg)
            self.data_path.latch_data_reg()
            self.tick()
            return self.data_path.data_reg

    def latch_instr_ptr(self, sel_next):
        if sel_next:
            self.instr_ptr += 1
        else:
            instr = self.code[self.instr_ptr]
            arg = self.get_operand(instr)
            self.instr_ptr = arg

    def decode_and_execute_instr(self):
        instr = self.code[self.instr_ptr]
        print(f"{{starting executing: {instr}}}")
        opcode = instr[0]

        if opcode == Opcode.LD:
            self.get_operand(instr)
            self.data_path.latch_acc(instr[1][0] != OperandType.CONSTANT.value)
            self.latch_instr_ptr(sel_next=True)
            self.tick()
        elif opcode == Opcode.ST:
            self.data_path.address_reg_set(self.get_operand(instr))
            self.data_path.latch_mem()
            self.latch_instr_ptr(sel_next=True)
            self.tick()
        elif opcode == Opcode.OUT:
            self.data_path.output()
            self.tick()
            self.latch_instr_ptr(sel_next=True)
            self.tick()
        elif opcode == Opcode.IN:
            if self.data_path.has_next_input_token() == 0:
                raise EOFError
            self.data_path.acc = self.data_path.next_input_token()
            self.tick()
            self.latch_instr_ptr(sel_next=True)
            self.tick()
        elif opcode == Opcode.ADD or opcode == Opcode.MOD or opcode == Opcode.DIV:
            self.get_operand(instr)
            self.data_path.acc_wr(opcode)
            self.tick()
            self.latch_instr_ptr(sel_next=True)
            self.tick()
        elif opcode == Opcode.CMP:
            second_val = self.get_operand(instr)
            self.data_path.set_flags(self.data_path.acc - second_val)
            self.latch_instr_ptr(sel_next=True)
            self.tick()
        elif opcode == Opcode.JMP:
            self.latch_instr_ptr(False)
            self.tick()
        elif opcode == Opcode.JE:
            self.latch_instr_ptr(not self.data_path.is_zero())
            self.tick()
        elif opcode == Opcode.HLT:
            raise StopIteration()
        else:
            assert False, "opcode not found!"

    def __repr__(self):
        state = f"{{TICK: {self._tick}, PC: {self.instr_ptr}, ADDR: {self.data_path.address_reg}, " \
                f"ACC: {self.data_path.acc}, DR: {self.data_path.data_reg}}}"
        return state


def simulation(program, input_tokens, data_memory_size, simulation_limit):
    data_path = DataPath(data_memory_size, program['data'], input_tokens)
    control_unit = ControlUnit(program['code'], data_path)
    instr_counter = 0
    try:
        while True:
            assert simulation_limit > instr_counter, "too long execution, increase simulation_limit!"
            control_unit.decode_and_execute_instr()
            instr_counter += 1
    except StopIteration:
        pass
    except EOFError:
        print('Input buffer is empty!')

    print('simulation finished')
    print('memory state', data_path.data_mem)
    return f"output: '{''.join(data_path.output_buffer)}', instructions: '{instr_counter}', " \
           f"ticks: '{control_unit.current_tick()}'"
