from queue import SimpleQueue, LifoQueue


class Instruction:
    def __init__(self, param_modes):
        self._param_modes = param_modes

    def run(self, memory, at_pos):
        pass

    def getParamValue(self, memory, at, param_num):
        if self._param_modes[param_num - 1] == 0:
            loc = memory[at + param_num]
            val = memory[loc]
        else:
            val = memory[at + param_num]

        return val

    def getNumOpCodes(self):
        return 0


class AddInstruction(Instruction):
    def __init__(self, param_modes):
        super(AddInstruction, self).__init__(param_modes)

    def run(self, memory, at_pos):
        val1 = super().getParamValue(memory, at_pos, 1)
        val2 = super().getParamValue(memory, at_pos, 2)

        result = val1 + val2

        destination = memory[at_pos + 3]
        memory[destination] = result

    def getNumOpCodes(self):
        return 4


class MultiplyInstruction(Instruction):

    def __init__(self, param_modes):
        super(MultiplyInstruction, self).__init__(param_modes)

    def run(self, memory, at_pos):
        val1 = super().getParamValue(memory, at_pos, 1)
        val2 = super().getParamValue(memory, at_pos, 2)

        result = val1 * val2

        destination = memory[at_pos + 3]
        memory[destination] = result

    def getNumOpCodes(self):
        return 4


class StoreInstruction(Instruction):
    def __init__(self, param_modes, computer):
        super(StoreInstruction, self).__init__(param_modes)
        self._computer = computer

    def run(self, memory, at_pos):
        destination = memory[at_pos + 1]
        #        print("Input requested:")
        # user_in = int(input())
        user_in = self._computer.get_input()
        # print(f"Received input {user_in}")
        memory[destination] = user_in

    def getNumOpCodes(self):
        return 2


class PrintInstruction(Instruction):
    def __init__(self, param_modes, computer):
        super(PrintInstruction, self).__init__(param_modes)
        self._computer = computer

    def run(self, memory, at_pos):
        val = super().getParamValue(memory, at_pos, 1)

        # print(f"Storing output: {val}")

        self._computer.store_output(val)

    def getNumOpCodes(self):
        return 2


class JumpIfTrue(Instruction):
    def __init__(self, param_modes, computer):
        super(JumpIfTrue, self).__init__(param_modes)
        self._computer = computer

    def run(self, memory, at_pos):
        val1 = super().getParamValue(memory, at_pos, 1)
        val2 = super().getParamValue(memory, at_pos, 2)

        if val1 == 0:
            return

        #        print(f"Jumping to instruction {val2}")
        self._computer.set_instruction_pos(val2)

    def getNumOpCodes(self):
        return 3


class JumpIfFalse(Instruction):
    def __init__(self, param_modes, computer):
        super(JumpIfFalse, self).__init__(param_modes)
        self._computer = computer

    def run(self, memory, at_pos):
        val1 = super().getParamValue(memory, at_pos, 1)
        val2 = super().getParamValue(memory, at_pos, 2)

        if val1 != 0:
            return

        #        print(f"Jumping to instruction {val2}")
        self._computer.set_instruction_pos(val2)

    def getNumOpCodes(self):
        return 3


class LessThan(Instruction):
    def __init__(self, param_modes):
        super(LessThan, self).__init__(param_modes)

    def run(self, memory, at_pos):
        val1 = super().getParamValue(memory, at_pos, 1)
        val2 = super().getParamValue(memory, at_pos, 2)

        destination = memory[at_pos + 3]
        memory[destination] = int(val1 < val2)

    def getNumOpCodes(self):
        return 4


class Equals(Instruction):
    def __init__(self, param_modes):
        super(Equals, self).__init__(param_modes)

    def run(self, memory, at_pos):
        val1 = super().getParamValue(memory, at_pos, 1)
        val2 = super().getParamValue(memory, at_pos, 2)

        destination = memory[at_pos + 3]
        memory[destination] = int(val1 == val2)

    def getNumOpCodes(self):
        return 4


class InstructionFactory:

    def __init__(self, computer):
        self._computer = computer

    def getInstruction(self, opcode):
        #        print(f"factory: request for opcode {opcode}")
        operation = opcode % 100
        param_1_mode = (opcode // 100) % 10
        param_2_mode = opcode // 1000
        param_modes = (param_1_mode, param_2_mode)
        if operation == 1:
            return AddInstruction(param_modes)
        elif operation == 2:
            return MultiplyInstruction(param_modes)
        elif operation == 3:
            return StoreInstruction(param_modes, self._computer)
        elif operation == 4:
            return PrintInstruction(param_modes, self._computer)
        elif operation == 5:
            return JumpIfTrue(param_modes, self._computer)
        elif operation == 6:
            return JumpIfFalse(param_modes, self._computer)
        elif operation == 7:
            return LessThan(param_modes)
        elif operation == 8:
            return Equals(param_modes)


class Computer:

    def __init__(self, program):
        self._program = program
        self.input_simulation = SimpleQueue()
        self.output_simulation = LifoQueue()
        self.instruction_position = 0
        self._is_it_running = False

    def store_input(self, input_data):
        self.input_simulation.put(input_data)

    def get_input(self):
        return self.input_simulation.get()

    def has_input(self):
        return not self.input_simulation.empty()

    def store_output(self, output_data):
        self.output_simulation.put(output_data)

    def get_output(self):
        return self.output_simulation.get()

    def get_instruction_pos(self):
        return self.instruction_position

    def set_instruction_pos(self, new_pos):
        self.instruction_position = new_pos

    def is_running(self):
        return self._is_it_running

    def run(self):
        #    processing_op_num = 0
        self.instruction_position = 0
        ifactory = InstructionFactory(self)

        self._is_it_running = True

        while self._program[self.instruction_position] != 99:
            instruction = ifactory.getInstruction(self._program[self.instruction_position])
            #        print(f"processing instruction #{self.instruction_position} = {self._program[self.instruction_position]}: {instruction}")

            instr_pos_pre = self.instruction_position

            instruction.run(self._program, self.instruction_position)
            #        print(f"post run, program is: {program}")

            if self.instruction_position == instr_pos_pre:
                # increment instruction pointer only if it wasn't changed by a jump operation
                self.instruction_position += instruction.getNumOpCodes()
    #        print(f"incremented instruction pointer to {instruction_position}")

        self._is_it_running = False


# starting_program = [1,0,0,0,99]
# starting_program = [2,3,0,3,99]
# starting_program = [2,4,4,5,99,0]
starting_program = [1, 1, 1, 4, 99, 5, 6, 0, 99]


# starting_program = [3,0,4,0,99]


def day2p2():
    starting_program = [1, 0, 0, 3, 1, 1, 2, 3, 1, 3, 4, 3, 1, 5, 0, 3, 2, 10, 1, 19, 1, 5, 19, 23, 1, 23, 5, 27, 2, 27,
                        10, 31, 1, 5, 31, 35, 2, 35, 6, 39, 1, 6, 39, 43, 2, 13, 43, 47, 2, 9, 47, 51, 1, 6, 51, 55, 1,
                        55, 9, 59, 2, 6, 59, 63, 1, 5, 63, 67, 2, 67, 13, 71, 1, 9, 71, 75, 1, 75, 9, 79, 2, 79, 10, 83,
                        1, 6, 83, 87, 1, 5, 87, 91, 1, 6, 91, 95, 1, 95, 13, 99, 1, 10, 99, 103, 2, 6, 103, 107, 1, 107,
                        5, 111, 1, 111, 13, 115, 1, 115, 13, 119, 1, 13, 119, 123, 2, 123, 13, 127, 1, 127, 6, 131, 1,
                        131, 9, 135, 1, 5, 135, 139, 2, 139, 6, 143, 2, 6, 143, 147, 1, 5, 147, 151, 1, 151, 2, 155, 1,
                        9, 155, 0, 99, 2, 14, 0, 0]
    for noun in range(100):
        for verb in range(100):
            attempt = starting_program[:]
            attempt[1] = noun
            attempt[2] = verb
            c = Computer(attempt)
            c.run()
            print(f"Result of run with {noun}, {verb} is {attempt[0]}")
            if attempt[0] == 19690720:
                print(f"That's it! Result = {100 * noun + verb}")
                exit()


def day2p1():
    c = Computer(starting_program)
    c.run()
    print(starting_program)


input_equals_8_prog = [3, 9, 8, 9, 10, 9, 4, 9, 99, -1, 8]
input_lt_8_prog = [3, 9, 7, 9, 10, 9, 4, 9, 99, -1, 8]
input_eq_8_v2 = [3, 3, 1108, -1, 8, 3, 4, 3, 99]
input_lt_8_v2 = [3, 3, 1107, -1, 8, 3, 4, 3, 99]
is_input_zero = [3, 12, 6, 12, 15, 1, 13, 14, 13, 4, 13, 99, -1, 0, 1, 9]
is_input_zero_v2 = [3, 3, 1105, -1, 9, 1101, 0, 0, 12, 4, 12, 99, 1]
compare_to_8 = [3, 21, 1008, 21, 8, 20, 1005, 20, 22, 107, 8, 21, 20, 1006, 20, 31,
                1106, 0, 36, 98, 0, 0, 1002, 21, 125, 20, 4, 20, 1105, 1, 46, 104,
                999, 1105, 1, 46, 1101, 1000, 1, 20, 4, 20, 1105, 1, 46, 98, 99]

d5_program = [3, 225, 1, 225, 6, 6, 1100, 1, 238, 225, 104, 0, 1101, 82, 10, 225, 101, 94, 44, 224, 101, -165, 224, 224,
              4, 224, 1002, 223, 8, 223, 101, 3, 224, 224, 1, 224, 223, 223, 1102, 35, 77, 225, 1102, 28, 71, 225, 1102,
              16, 36, 225, 102, 51, 196, 224, 101, -3468, 224, 224, 4, 224, 102, 8, 223, 223, 1001, 224, 7, 224, 1, 223,
              224, 223, 1001, 48, 21, 224, 101, -57, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 6, 224, 224, 1, 223, 224,
              223, 2, 188, 40, 224, 1001, 224, -5390, 224, 4, 224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 224, 223,
              223, 1101, 9, 32, 224, 101, -41, 224, 224, 4, 224, 1002, 223, 8, 223, 1001, 224, 2, 224, 1, 223, 224, 223,
              1102, 66, 70, 225, 1002, 191, 28, 224, 101, -868, 224, 224, 4, 224, 102, 8, 223, 223, 101, 5, 224, 224, 1,
              224, 223, 223, 1, 14, 140, 224, 101, -80, 224, 224, 4, 224, 1002, 223, 8, 223, 101, 2, 224, 224, 1, 224,
              223, 223, 1102, 79, 70, 225, 1101, 31, 65, 225, 1101, 11, 68, 225, 1102, 20, 32, 224, 101, -640, 224, 224,
              4, 224, 1002, 223, 8, 223, 1001, 224, 5, 224, 1, 224, 223, 223, 4, 223, 99, 0, 0, 0, 677, 0, 0, 0, 0, 0,
              0, 0, 0, 0, 0, 0, 1105, 0, 99999, 1105, 227, 247, 1105, 1, 99999, 1005, 227, 99999, 1005, 0, 256, 1105, 1,
              99999, 1106, 227, 99999, 1106, 0, 265, 1105, 1, 99999, 1006, 0, 99999, 1006, 227, 274, 1105, 1, 99999,
              1105, 1, 280, 1105, 1, 99999, 1, 225, 225, 225, 1101, 294, 0, 0, 105, 1, 0, 1105, 1, 99999, 1106, 0, 300,
              1105, 1, 99999, 1, 225, 225, 225, 1101, 314, 0, 0, 106, 0, 0, 1105, 1, 99999, 8, 226, 226, 224, 1002, 223,
              2, 223, 1006, 224, 329, 101, 1, 223, 223, 1008, 677, 677, 224, 102, 2, 223, 223, 1006, 224, 344, 101, 1,
              223, 223, 1107, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 359, 101, 1, 223, 223, 1008, 226, 226, 224,
              1002, 223, 2, 223, 1006, 224, 374, 1001, 223, 1, 223, 1108, 677, 226, 224, 1002, 223, 2, 223, 1006, 224,
              389, 1001, 223, 1, 223, 7, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 404, 101, 1, 223, 223, 7, 226,
              226, 224, 1002, 223, 2, 223, 1005, 224, 419, 101, 1, 223, 223, 8, 226, 677, 224, 1002, 223, 2, 223, 1006,
              224, 434, 1001, 223, 1, 223, 7, 226, 677, 224, 1002, 223, 2, 223, 1006, 224, 449, 1001, 223, 1, 223, 107,
              226, 677, 224, 1002, 223, 2, 223, 1005, 224, 464, 1001, 223, 1, 223, 1007, 677, 677, 224, 102, 2, 223,
              223, 1005, 224, 479, 101, 1, 223, 223, 1007, 226, 226, 224, 102, 2, 223, 223, 1005, 224, 494, 1001, 223,
              1, 223, 1108, 226, 677, 224, 102, 2, 223, 223, 1005, 224, 509, 101, 1, 223, 223, 1008, 677, 226, 224, 102,
              2, 223, 223, 1005, 224, 524, 1001, 223, 1, 223, 1007, 677, 226, 224, 102, 2, 223, 223, 1005, 224, 539,
              101, 1, 223, 223, 1108, 226, 226, 224, 1002, 223, 2, 223, 1005, 224, 554, 101, 1, 223, 223, 108, 226, 226,
              224, 102, 2, 223, 223, 1005, 224, 569, 101, 1, 223, 223, 108, 677, 677, 224, 102, 2, 223, 223, 1005, 224,
              584, 101, 1, 223, 223, 1107, 226, 226, 224, 1002, 223, 2, 223, 1006, 224, 599, 101, 1, 223, 223, 8, 677,
              226, 224, 1002, 223, 2, 223, 1006, 224, 614, 1001, 223, 1, 223, 108, 677, 226, 224, 102, 2, 223, 223,
              1006, 224, 629, 1001, 223, 1, 223, 1107, 677, 226, 224, 1002, 223, 2, 223, 1006, 224, 644, 1001, 223, 1,
              223, 107, 677, 677, 224, 102, 2, 223, 223, 1005, 224, 659, 101, 1, 223, 223, 107, 226, 226, 224, 102, 2,
              223, 223, 1006, 224, 674, 1001, 223, 1, 223, 4, 223, 99, 226]


def day5p1():
    c = Computer(d5_program[:])
    c.store_input(1)
    c.run()
    print(c.get_output())


def day5p2():
    c = Computer(d5_program[:])
    c.store_input(5)
    c.run()
    print(c.get_output())
