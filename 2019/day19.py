from day09 import Computer, Memory, PrintInstruction, StoreInstruction, InstructionFactory
import math


class TractorBeamInstructionFactory(InstructionFactory):
    def __init__(self, computer):
        super().__init__(computer)

    def get_instruction(self, opcode):
        operation = opcode % 100

        if operation == 3:
            return TractorBeamStoreInstruction(self.split_opcodes(opcode), self._computer)
        elif operation == 4:
            return TractorBeamPrintInstruction(self.split_opcodes(opcode), self._computer)
        else:
            return super().get_instruction(opcode)


class TractorBeamStoreInstruction(StoreInstruction):

    def __init__(self, param_modes, computer):
        super(TractorBeamStoreInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):

        destination = memory.get(at_pos + 1)
        if self._param_modes[0] == 2:  # relative mode
            destination = destination + self._computer.get_relative_base()

        next_coord = self._computer.get_next_unknown_coord()
        memory.set(destination, next_coord)


class TractorBeamPrintInstruction(PrintInstruction):

    def __init__(self, param_modes, computer):
        super(PrintInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val = super().get_param_value(memory, at_pos, 1)

        self._computer.set_next_reading(val)


class TractorBeamComputer2(Computer):
    def __init__(self, prog):
        super().__init__(prog[:])
        self._orig_program = prog
        self.i_factory = TractorBeamInstructionFactory(self)
        self._next_unknown_x = 0
        self._next_unknown_y = 0
        self._next_is_X = True
        self._reading = None

    def check_one_coord(self, x, y):
        self.memory = Memory(self._orig_program[:])
        self._next_unknown_x = x
        self._next_unknown_y = y
        self._next_is_X = True

    def get_next_unknown_coord(self):
        self._next_is_X = not self._next_is_X

        if self._next_is_X:
            return self._next_unknown_y
        else:
            return self._next_unknown_x

    def set_next_reading(self, val):
        self._reading = val

    def get_reading(self):
        return self._reading


class TractorBeamComputer(Computer):
    def __init__(self, prog):
        super().__init__(prog[:])
        self._orig_program = prog
        self.i_factory = TractorBeamInstructionFactory(self)
        self._beam_map = []
        self._next_unknown_x = 0
        self._next_unknown_y = 0
        self._tot_scanned = 0
        self._tot_beamed = 0
        self._next_is_X = True

    def reset(self):
        self.memory = Memory(self._orig_program[:])

    def get_next_unknown_coord(self):
        self._next_is_X = not self._next_is_X

        if self._next_is_X:
            return self._next_unknown_y
        else:
            return self._next_unknown_x

    def get_tot_scanned(self):
        return self._tot_scanned

    def set_next_reading(self, val):
        if len(self._beam_map) <= self._next_unknown_y:
            self._beam_map.append([])
        row = self._beam_map[-1]
        row.append(val)
        self._next_unknown_x = (self._next_unknown_x + 1) % 50
        if self._next_unknown_x == 0:
            self._next_unknown_y += 1
        self._tot_beamed += val
        self._tot_scanned += 1

    def get_screen(self):
        i = 0
        result = ''
        for row in self._beam_map:
            for col in row:
                result += str(col)
            result += f' {i}\n'
            i += 1

        return result

    def get_tot_beamed(self):
        return self._tot_beamed


program = [109, 424, 203, 1, 21102, 1, 11, 0, 1106, 0, 282, 21101, 0, 18, 0, 1106, 0, 259, 1202, 1, 1, 221, 203, 1,
           21101, 0, 31, 0, 1105, 1, 282, 21102, 38, 1, 0, 1105, 1, 259, 20102, 1, 23, 2, 21201, 1, 0, 3, 21102, 1, 1,
           1, 21101, 0, 57, 0, 1105, 1, 303, 2101, 0, 1, 222, 20102, 1, 221, 3, 21002, 221, 1, 2, 21101, 0, 259, 1,
           21101, 0, 80, 0, 1106, 0, 225, 21102, 1, 152, 2, 21101, 91, 0, 0, 1106, 0, 303, 1201, 1, 0, 223, 21001, 222,
           0, 4, 21101, 0, 259, 3, 21102, 225, 1, 2, 21101, 0, 225, 1, 21102, 1, 118, 0, 1105, 1, 225, 20101, 0, 222, 3,
           21102, 61, 1, 2, 21101, 133, 0, 0, 1106, 0, 303, 21202, 1, -1, 1, 22001, 223, 1, 1, 21102, 148, 1, 0, 1105,
           1, 259, 2101, 0, 1, 223, 21001, 221, 0, 4, 21001, 222, 0, 3, 21101, 0, 14, 2, 1001, 132, -2, 224, 1002, 224,
           2, 224, 1001, 224, 3, 224, 1002, 132, -1, 132, 1, 224, 132, 224, 21001, 224, 1, 1, 21101, 0, 195, 0, 105, 1,
           109, 20207, 1, 223, 2, 20101, 0, 23, 1, 21102, -1, 1, 3, 21102, 214, 1, 0, 1105, 1, 303, 22101, 1, 1, 1, 204,
           1, 99, 0, 0, 0, 0, 109, 5, 2101, 0, -4, 249, 21202, -3, 1, 1, 21202, -2, 1, 2, 21201, -1, 0, 3, 21102, 1,
           250, 0, 1106, 0, 225, 22101, 0, 1, -4, 109, -5, 2106, 0, 0, 109, 3, 22107, 0, -2, -1, 21202, -1, 2, -1,
           21201, -1, -1, -1, 22202, -1, -2, -2, 109, -3, 2105, 1, 0, 109, 3, 21207, -2, 0, -1, 1206, -1, 294, 104, 0,
           99, 22102, 1, -2, -2, 109, -3, 2105, 1, 0, 109, 5, 22207, -3, -4, -1, 1206, -1, 346, 22201, -4, -3, -4,
           21202, -3, -1, -1, 22201, -4, -1, 2, 21202, 2, -1, -1, 22201, -4, -1, 1, 21202, -2, 1, 3, 21101, 343, 0, 0,
           1106, 0, 303, 1105, 1, 415, 22207, -2, -3, -1, 1206, -1, 387, 22201, -3, -2, -3, 21202, -2, -1, -1, 22201,
           -3, -1, 3, 21202, 3, -1, -1, 22201, -3, -1, 2, 22101, 0, -4, 1, 21101, 0, 384, 0, 1106, 0, 303, 1105, 1, 415,
           21202, -4, -1, -4, 22201, -4, -3, -4, 22202, -3, -2, -2, 22202, -2, -4, -4, 22202, -3, -2, -3, 21202, -4, -1,
           -2, 22201, -3, -2, 1, 21201, 1, 0, -4, 109, -5, 2106, 0, 0]


def part1():
    c = TractorBeamComputer(program)
    while c.get_tot_scanned() < 50*50:
        c.reset()
        c.run()
        # print("Screen so far:")
        # print(c.get_screen())
    print()
    print("Run complete, screen is:")
    print(c.get_screen())
    print()
    print(f"Total affected points: {c.get_tot_beamed()}")


def check_one_coord(computer, row, col):
    computer.check_one_coord(col, row)
    computer.run()
    return computer.get_reading()


def get_first_hit_index(computer, row):
    col = row // 2  # good lower bound approximation of where the first hit may be found.
    while not check_one_coord(computer, row, col):
        col += 1  # larger jumps may miss the section of hits altogether

    return col


def get_hits_in_row(computer, row):
    start_col = get_first_hit_index(computer, row)
    col = start_col

    while check_one_coord(computer, row, col):
        col += 1

    return col - start_col, start_col


def part2():
    c = TractorBeamComputer2(program)
    num_hits = 0
    target = 100
    row_to_test = target

    while num_hits < target:
        num_hits, start_col = get_hits_in_row(c, row_to_test)
        print(f"Row {row_to_test} has {num_hits} hits starting at {start_col}")
        row_to_test += math.floor(1.9 * (target - num_hits))

    print(f"First row with enough hits: {row_to_test}")

    rows_examined = 0

    while True:
        top_row_hits, top_row_start_pos = get_hits_in_row(c, row_to_test)
        bot_row_hits, bot_row_start_pos = get_hits_in_row(c, row_to_test + target - 1)

        # print(f"test: {row_to_test}, trh={top_row_hits}, trsp={top_row_start_pos}")
        # print(f"                     brh={bot_row_hits}, brsp={bot_row_start_pos}")

        if top_row_start_pos + top_row_hits - bot_row_start_pos >= target:
            print(f"Match: top r={row_to_test}, hits={top_row_hits} start={top_row_start_pos}")
            print(f"       bot r={row_to_test + target - 1}, hits={bot_row_hits} start={bot_row_start_pos}")
            break

        if rows_examined % 50 == 0:
            print(f"testing... row #{row_to_test} (have examined {rows_examined})")

        rows_examined += 1
        row_to_test += 1

    print(f"Solution: {1000*bot_row_start_pos + row_to_test}")


part2()
