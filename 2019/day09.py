from queue import SimpleQueue, LifoQueue


class Memory:
    _program_space = []
    _program_len = 0
    _data_space = {}

    def __init__(self, program):
        self._program_space = program[:]
        self._program_len = len(program)

    def get(self, index):
        if 0 <= index < self._program_len:
            return self._program_space[index]
        else:
            if index in self._data_space:
                return self._data_space[index]
            else:
                return 0  # no value stored for that index yet

    def set(self, index, val):
        if 0 <= index < self._program_len:
            self._program_space[index] = val
        elif index < 0:
            print(f"\n\n\nERROR: attempt to store value {val} in memory at index {index}\n\n\n")
            # exit(-1)
        else:
            self._data_space[index] = val


class Instruction:
    def __init__(self, param_modes, computer):
        self._param_modes = param_modes
        self._computer = computer

    def run(self, memory, at_pos):
        pass

    def get_param_value(self, memory, at, param_num):
        if self._param_modes[param_num - 1] == 0:    # position mode
            loc = memory.get(at + param_num)
            val = memory.get(loc)
        elif self._param_modes[param_num - 1] == 1:  # absolute mode
            val = memory.get(at + param_num)
        elif self._param_modes[param_num - 1] == 2:  # relative mode
            amt = memory.get(at + param_num)
            val = memory.get(amt + self._computer.get_relative_base())
        else:
            val = -1

        return val

    def get_destination_addr(self, memory, at, param_num):
        if self._param_modes[param_num - 1] == 0:
            loc = memory.get(at + param_num)
            val = memory.get(loc)
        elif self._param_modes[param_num - 1] == 1:  # absolute mode
            val = memory.get(at + param_num)
        elif self._param_modes[param_num - 1] == 2:  # relative mode
            val = memory.get(at + param_num) + self._computer.get_relative_base()
        else:
            val = -1

        return val

    def get_num_op_codes(self):
        return 0


class AddInstruction(Instruction):
    def __init__(self, param_modes, computer):
        super(AddInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val1 = super().get_param_value(memory, at_pos, 1)
        val2 = super().get_param_value(memory, at_pos, 2)

        result = val1 + val2

        destination = memory.get(at_pos + 3)
        if self._param_modes[2] == 2:  # relative mode
            destination = destination + self._computer.get_relative_base()

        memory.set(destination, result)
        # print(f"Add: {val1} + {val2} = {result}, stored at {destination}")

    def get_num_op_codes(self):
        return 4


class MultiplyInstruction(Instruction):

    def __init__(self, param_modes, computer):
        super(MultiplyInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val1 = super().get_param_value(memory, at_pos, 1)
        val2 = super().get_param_value(memory, at_pos, 2)

        result = val1 * val2

        destination = memory.get(at_pos + 3)
        if self._param_modes[2] == 2:  # relative mode
            destination = destination + self._computer.get_relative_base()

        memory.set(destination, result)
        # print(f"Multiply: {val1} * {val2} = {result}, stored at {destination}")

    def get_num_op_codes(self):
        return 4


class StoreInstruction(Instruction):
    def __init__(self, param_modes, computer):
        super(StoreInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):

        # print(f"StoreInstruction: param types are {self._param_modes[0]}, {self._param_modes[1]}")
        # print(f"data is {self._computer.memory._program_space[0:30]}")
        # print(f"extended data is")
        print(self._computer.memory._data_space)
        # print(f"relative base: {self._computer.get_relative_base()}")

        destination = super().get_destination_addr(memory, at_pos, 1)

        # if self._param_modes[0] == 0:    # position mode
        #     loc = memory.get(at_pos + 1)
        #     destination = memory.get(loc)
        # elif self._param_modes[0] == 1:  # absolute mode
        #     destination = memory.get(at_pos + 1)
        # elif self._param_modes[0] == 2:  # relative mode
        #     loc = memory.get(at_pos + 1)
        #     destination = loc + self._computer.get_relative_base()

        # print(f"StoreInstruction: at_pos:{at_pos}, destination:{destination}")
        # print("Input requested:")
#        user_in = int(input())
        user_in = self._computer.get_input()
        # print(f"Received {user_in}")
        memory.set(destination, user_in)

    def get_num_op_codes(self):
        return 2


class PrintInstruction(Instruction):
    def __init__(self, param_modes, computer):
        super(PrintInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val = super().get_param_value(memory, at_pos, 1)

        print(f"Storing output: {val}")

        self._computer.store_output(val)

    def get_num_op_codes(self):
        return 2


class JumpIfTrue(Instruction):
    def __init__(self, param_modes, computer):
        super(JumpIfTrue, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val1 = super().get_param_value(memory, at_pos, 1)
        val2 = super().get_param_value(memory, at_pos, 2)

        if val1 == 0:
            return

#        print(f"Jumping to instruction {val2}")
        self._computer.set_instruction_pos(val2)

    def get_num_op_codes(self):
        return 3


class JumpIfFalse(Instruction):
    def __init__(self, param_modes, computer):
        super(JumpIfFalse, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val1 = super().get_param_value(memory, at_pos, 1)
        val2 = super().get_param_value(memory, at_pos, 2)
        if val1 != 0:
            return

#        print(f"Jumping to instruction {val2}")
        self._computer.set_instruction_pos(val2)

    def get_num_op_codes(self):
        return 3


class RelativeBaseAdjust(Instruction):
    def __init__(self, param_modes, computer):
        super(RelativeBaseAdjust, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        curr_base = self._computer.get_relative_base()
        # print(f"RBA: getting delta based on at_pos={at_pos}")

        if self._param_modes[0] == 1:
            delta = memory.get(at_pos + 1)
        elif self._param_modes[0] == 2:
            delta = memory.get(curr_base + memory.get(at_pos + 1))
        elif self._param_modes[0] == 0:
            delta = memory.get(memory.get(at_pos + 1))
        # print(f"RBA: curr_base is {curr_base}, delta is {delta}")
        self._computer.set_relative_base(curr_base + delta)
        # print(f"RBA: curr_base is now {self._computer.get_relative_base()}")

    def get_num_op_codes(self):
        return 2


class LessThan(Instruction):
    def __init__(self, param_modes, computer):
        super(LessThan, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):

        val1 = super().get_param_value(memory, at_pos, 1)
        val2 = super().get_param_value(memory, at_pos, 2)

        destination = memory.get(at_pos + 3)
        if self._param_modes[2] == 2:  # relative mode
            destination = destination + self._computer.get_relative_base()

        memory.set(destination, int(val1 < val2))
        # print(f"LessThan: {val1} < {val2}? = {int(val1 < val2)}, stored at {destination}")

    def get_num_op_codes(self):
        return 4


class Equals(Instruction):
    def __init__(self, param_modes, computer):
        super(Equals, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):

        val1 = super().get_param_value(memory, at_pos, 1)
        val2 = super().get_param_value(memory, at_pos, 2)

        destination = memory.get(at_pos + 3)
        if self._param_modes[2] == 2:  # relative mode
            destination = destination + self._computer.get_relative_base()

        memory.set(destination, int(val1 == val2))
        # print(f"Equals: {val1} == {val2}? = {int(val1 == val2)}, stored at {destination}")

    def get_num_op_codes(self):
        return 4


class InstructionFactory:

    def __init__(self, computer):
        self._computer = computer

    def get_instruction(self, opcode):
        # print(f"\nfactory: request for opcode {opcode}")
        operation = opcode % 100
        param_1_mode = (opcode // 100) % 10
        param_2_mode = (opcode // 1000) % 10
        param_3_mode = opcode // 10000
        # print(f"operation is {operation}, param1={param_1_mode}, param2={param_2_mode}")
        param_modes = (param_1_mode, param_2_mode, param_3_mode)
        if operation == 1:
            return AddInstruction(param_modes, self._computer)
        elif operation == 2:
            return MultiplyInstruction(param_modes, self._computer)
        elif operation == 3:
            return StoreInstruction(param_modes, self._computer)
        elif operation == 4:
            return PrintInstruction(param_modes, self._computer)
        elif operation == 5:
            return JumpIfTrue(param_modes, self._computer)
        elif operation == 6:
            return JumpIfFalse(param_modes, self._computer)
        elif operation == 7:
            return LessThan(param_modes, self._computer)
        elif operation == 8:
            return Equals(param_modes, self._computer)
        elif operation == 9:
            return RelativeBaseAdjust(param_modes, self._computer)


class Computer:
    input_simulation = SimpleQueue()
    output_simulation = LifoQueue()
    instruction_position = 0
    relative_base = 0
    memory = None

    def __init__(self, program):
        self.memory = Memory(program)
        self.ifactory = InstructionFactory(self)

    def store_input(self, input_data):
        self.input_simulation.put(input_data)

    def get_input(self):
        return self.input_simulation.get()

    def store_output(self, output_data):
        self.output_simulation.put(output_data)

    def get_output(self):
        return self.output_simulation.get()

    def has_output(self):
        return not self.output_simulation.empty()

    def get_instruction_pos(self):
        return self.instruction_position

    def set_instruction_pos(self, new_pos):
        self.instruction_position = new_pos

    def get_relative_base(self):
        return self.relative_base

    def set_relative_base(self, new_val):
        self.relative_base = new_val

    def get_curr_instruction(self):
        return self.memory.get(self.instruction_position)

    def dumpMem(self):
        # mem = self.memory._program_space
        # for i in range(10):
        #     startpos = i*10
        #     endpos = i*10 + 10
        #     row = mem[startpos:endpos]
        #     print(f"   {row}")
        mem = self.memory._data_space
        print(mem.items())


    def run(self):
        #    processing_op_num = 0
        self.instruction_position = 0

        while self.get_curr_instruction() != 99:
            instruction = self.ifactory.get_instruction(self.get_curr_instruction())
            # print(f"processing instruction #{self.instruction_position} = {self.memory.get(self.instruction_position)}: {instruction}")
            # print(f"    mem is {self.memory._program_space[0:11]}")

            instr_pos_pre = self.instruction_position

            instruction.run(self.memory, self.instruction_position)
            # print("post run, program is:")
#            self.dumpMem()

            if self.instruction_position == instr_pos_pre:
                # increment instruction pointer only if it wasn't changed by a jump operation
                self.instruction_position += instruction.get_num_op_codes()
        #        print(f"incremented instruction pointer to {instruction_position}")


def day9testp1():
    test1 = [109,1,204,-1,1001,100,1,100,1008,100,16,101,1006,101,0,99]
    c = Computer(test1)
    c.run()
    print("Run complete, output is ")
    while c.has_output():
        print(c.get_output())

    print("==========================")
    test2 = [1102,34915192,34915192,7,4,7,99,0]
    c = Computer(test2)
    c.run()
    print("Run complete, output is ")
    while c.has_output():
        print(c.get_output())

    print("==========================")
    test3 = [104,1125899906842624,99]
    c = Computer(test3)
    c.run()
    print("Run complete, output is ")
    while c.has_output():
        print(c.get_output())


def day9p1():
    boost = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,26,1014,1102,1,30,1013,1101,22,0,1000,1101,0,35,1015,1101,0,34,1011,1102,0,1,1020,1102,1,481,1022,1101,0,36,1003,1102,1,28,1005,1101,857,0,1024,1101,20,0,1008,1101,0,385,1026,1102,37,1,1006,1101,33,0,1017,1101,0,38,1002,1102,23,1,1007,1102,32,1,1010,1101,29,0,1016,1102,1,25,1009,1102,1,27,1012,1101,24,0,1018,1101,474,0,1023,1102,1,39,1004,1101,0,31,1001,1102,378,1,1027,1101,0,848,1025,1102,21,1,1019,1102,760,1,1029,1102,1,1,1021,1101,769,0,1028,109,-6,2107,21,6,63,1005,63,199,4,187,1106,0,203,1001,64,1,64,1002,64,2,64,109,16,2101,0,-6,63,1008,63,39,63,1005,63,225,4,209,1106,0,229,1001,64,1,64,1002,64,2,64,109,5,2108,20,-7,63,1005,63,247,4,235,1105,1,251,1001,64,1,64,1002,64,2,64,109,-1,2108,36,-8,63,1005,63,267,1106,0,273,4,257,1001,64,1,64,1002,64,2,64,109,-13,1201,-1,0,63,1008,63,22,63,1005,63,299,4,279,1001,64,1,64,1106,0,299,1002,64,2,64,109,15,2102,1,-8,63,1008,63,20,63,1005,63,321,4,305,1106,0,325,1001,64,1,64,1002,64,2,64,109,-13,21108,40,40,8,1005,1011,347,4,331,1001,64,1,64,1105,1,347,1002,64,2,64,109,-2,1207,8,24,63,1005,63,363,1105,1,369,4,353,1001,64,1,64,1002,64,2,64,109,35,2106,0,-9,1001,64,1,64,1106,0,387,4,375,1002,64,2,64,109,-26,21102,41,1,3,1008,1013,41,63,1005,63,409,4,393,1106,0,413,1001,64,1,64,1002,64,2,64,109,2,1202,-6,1,63,1008,63,36,63,1005,63,433,1106,0,439,4,419,1001,64,1,64,1002,64,2,64,109,-3,21102,42,1,10,1008,1019,40,63,1005,63,463,1001,64,1,64,1106,0,465,4,445,1002,64,2,64,109,15,2105,1,-1,1001,64,1,64,1106,0,483,4,471,1002,64,2,64,109,-27,1207,3,23,63,1005,63,505,4,489,1001,64,1,64,1105,1,505,1002,64,2,64,109,13,2102,1,-9,63,1008,63,28,63,1005,63,525,1105,1,531,4,511,1001,64,1,64,1002,64,2,64,109,1,2101,0,-8,63,1008,63,35,63,1005,63,551,1105,1,557,4,537,1001,64,1,64,1002,64,2,64,109,6,21107,43,44,-4,1005,1013,575,4,563,1106,0,579,1001,64,1,64,1002,64,2,64,109,-9,1201,-4,0,63,1008,63,40,63,1005,63,599,1105,1,605,4,585,1001,64,1,64,1002,64,2,64,109,12,1206,1,621,1001,64,1,64,1106,0,623,4,611,1002,64,2,64,109,-22,1202,9,1,63,1008,63,23,63,1005,63,649,4,629,1001,64,1,64,1105,1,649,1002,64,2,64,109,17,1206,5,667,4,655,1001,64,1,64,1106,0,667,1002,64,2,64,109,-3,1205,9,685,4,673,1001,64,1,64,1106,0,685,1002,64,2,64,109,3,1208,-9,37,63,1005,63,707,4,691,1001,64,1,64,1105,1,707,1002,64,2,64,109,7,1205,-2,723,1001,64,1,64,1106,0,725,4,713,1002,64,2,64,109,-15,21101,44,0,8,1008,1015,45,63,1005,63,745,1105,1,751,4,731,1001,64,1,64,1002,64,2,64,109,28,2106,0,-7,4,757,1001,64,1,64,1106,0,769,1002,64,2,64,109,-12,21101,45,0,-5,1008,1018,45,63,1005,63,791,4,775,1105,1,795,1001,64,1,64,1002,64,2,64,109,-9,2107,26,-5,63,1005,63,815,1001,64,1,64,1106,0,817,4,801,1002,64,2,64,109,-1,21107,46,45,-3,1005,1010,833,1105,1,839,4,823,1001,64,1,64,1002,64,2,64,109,3,2105,1,8,4,845,1001,64,1,64,1106,0,857,1002,64,2,64,109,-9,1208,-4,37,63,1005,63,877,1001,64,1,64,1105,1,879,4,863,1002,64,2,64,109,8,21108,47,46,2,1005,1017,895,1106,0,901,4,885,1001,64,1,64,4,64,99,21102,1,27,1,21102,1,915,0,1106,0,922,21201,1,14429,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1105,1,922,21202,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1105,1,968,21201,-2,0,-2,109,-3,2105,1,0]
    c = Computer(boost)
    c.store_input(1)
    c.run()
    print("Run complete, output is ")
    while c.has_output():
        print(c.get_output())


def day9p2():
    boost = [1102,34463338,34463338,63,1007,63,34463338,63,1005,63,53,1102,3,1,1000,109,988,209,12,9,1000,209,6,209,3,203,0,1008,1000,1,63,1005,63,65,1008,1000,2,63,1005,63,904,1008,1000,0,63,1005,63,58,4,25,104,0,99,4,0,104,0,99,4,17,104,0,99,0,0,1101,0,26,1014,1102,1,30,1013,1101,22,0,1000,1101,0,35,1015,1101,0,34,1011,1102,0,1,1020,1102,1,481,1022,1101,0,36,1003,1102,1,28,1005,1101,857,0,1024,1101,20,0,1008,1101,0,385,1026,1102,37,1,1006,1101,33,0,1017,1101,0,38,1002,1102,23,1,1007,1102,32,1,1010,1101,29,0,1016,1102,1,25,1009,1102,1,27,1012,1101,24,0,1018,1101,474,0,1023,1102,1,39,1004,1101,0,31,1001,1102,378,1,1027,1101,0,848,1025,1102,21,1,1019,1102,760,1,1029,1102,1,1,1021,1101,769,0,1028,109,-6,2107,21,6,63,1005,63,199,4,187,1106,0,203,1001,64,1,64,1002,64,2,64,109,16,2101,0,-6,63,1008,63,39,63,1005,63,225,4,209,1106,0,229,1001,64,1,64,1002,64,2,64,109,5,2108,20,-7,63,1005,63,247,4,235,1105,1,251,1001,64,1,64,1002,64,2,64,109,-1,2108,36,-8,63,1005,63,267,1106,0,273,4,257,1001,64,1,64,1002,64,2,64,109,-13,1201,-1,0,63,1008,63,22,63,1005,63,299,4,279,1001,64,1,64,1106,0,299,1002,64,2,64,109,15,2102,1,-8,63,1008,63,20,63,1005,63,321,4,305,1106,0,325,1001,64,1,64,1002,64,2,64,109,-13,21108,40,40,8,1005,1011,347,4,331,1001,64,1,64,1105,1,347,1002,64,2,64,109,-2,1207,8,24,63,1005,63,363,1105,1,369,4,353,1001,64,1,64,1002,64,2,64,109,35,2106,0,-9,1001,64,1,64,1106,0,387,4,375,1002,64,2,64,109,-26,21102,41,1,3,1008,1013,41,63,1005,63,409,4,393,1106,0,413,1001,64,1,64,1002,64,2,64,109,2,1202,-6,1,63,1008,63,36,63,1005,63,433,1106,0,439,4,419,1001,64,1,64,1002,64,2,64,109,-3,21102,42,1,10,1008,1019,40,63,1005,63,463,1001,64,1,64,1106,0,465,4,445,1002,64,2,64,109,15,2105,1,-1,1001,64,1,64,1106,0,483,4,471,1002,64,2,64,109,-27,1207,3,23,63,1005,63,505,4,489,1001,64,1,64,1105,1,505,1002,64,2,64,109,13,2102,1,-9,63,1008,63,28,63,1005,63,525,1105,1,531,4,511,1001,64,1,64,1002,64,2,64,109,1,2101,0,-8,63,1008,63,35,63,1005,63,551,1105,1,557,4,537,1001,64,1,64,1002,64,2,64,109,6,21107,43,44,-4,1005,1013,575,4,563,1106,0,579,1001,64,1,64,1002,64,2,64,109,-9,1201,-4,0,63,1008,63,40,63,1005,63,599,1105,1,605,4,585,1001,64,1,64,1002,64,2,64,109,12,1206,1,621,1001,64,1,64,1106,0,623,4,611,1002,64,2,64,109,-22,1202,9,1,63,1008,63,23,63,1005,63,649,4,629,1001,64,1,64,1105,1,649,1002,64,2,64,109,17,1206,5,667,4,655,1001,64,1,64,1106,0,667,1002,64,2,64,109,-3,1205,9,685,4,673,1001,64,1,64,1106,0,685,1002,64,2,64,109,3,1208,-9,37,63,1005,63,707,4,691,1001,64,1,64,1105,1,707,1002,64,2,64,109,7,1205,-2,723,1001,64,1,64,1106,0,725,4,713,1002,64,2,64,109,-15,21101,44,0,8,1008,1015,45,63,1005,63,745,1105,1,751,4,731,1001,64,1,64,1002,64,2,64,109,28,2106,0,-7,4,757,1001,64,1,64,1106,0,769,1002,64,2,64,109,-12,21101,45,0,-5,1008,1018,45,63,1005,63,791,4,775,1105,1,795,1001,64,1,64,1002,64,2,64,109,-9,2107,26,-5,63,1005,63,815,1001,64,1,64,1106,0,817,4,801,1002,64,2,64,109,-1,21107,46,45,-3,1005,1010,833,1105,1,839,4,823,1001,64,1,64,1002,64,2,64,109,3,2105,1,8,4,845,1001,64,1,64,1106,0,857,1002,64,2,64,109,-9,1208,-4,37,63,1005,63,877,1001,64,1,64,1105,1,879,4,863,1002,64,2,64,109,8,21108,47,46,2,1005,1017,895,1106,0,901,4,885,1001,64,1,64,4,64,99,21102,1,27,1,21102,1,915,0,1106,0,922,21201,1,14429,1,204,1,99,109,3,1207,-2,3,63,1005,63,964,21201,-2,-1,1,21102,1,942,0,1105,1,922,21202,1,1,-1,21201,-2,-3,1,21101,957,0,0,1106,0,922,22201,1,-1,-2,1105,1,968,21201,-2,0,-2,109,-3,2105,1,0]
    c = Computer(boost)
    c.store_input(2)
    c.run()
    print("Run complete, output is ")
    while c.has_output():
        print(c.get_output())



#day9p2()