from computer import Computer, StoreInstruction, PrintInstruction, InstructionFactory
import matplotlib.pyplot as plt


class TurtleInstructionFactory(InstructionFactory):
    def __init__(self, computer):
        super().__init__(computer)

    def get_instruction(self, opcode):
        operation = opcode % 100

        if operation == 3:
            param_1_mode = (opcode // 100) % 10
            param_2_mode = (opcode // 1000) % 10
            param_3_mode = opcode // 10000
            # print(f"operation is {operation}, param1={param_1_mode}, param2={param_2_mode}")
            param_modes = (param_1_mode, param_2_mode, param_3_mode)
            return TurtleStoreInstruction(param_modes, self._computer)
        elif operation == 4:
            param_1_mode = (opcode // 100) % 10
            param_2_mode = (opcode // 1000) % 10
            param_3_mode = opcode // 10000
            # print(f"operation is {operation}, param1={param_1_mode}, param2={param_2_mode}")
            param_modes = (param_1_mode, param_2_mode, param_3_mode)
            return TurtlePrintInstruction(param_modes, self._computer)
        else:
            return super().get_instruction(opcode)


class TurtleStoreInstruction(StoreInstruction):
    def __init__(self, param_modes, computer):
        super(StoreInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):

        destination = memory.get(at_pos + 1)

        sitting_on = self._computer.get_curr_color()
        # print(f"The color at {self._computer._at} is {sitting_on}")
        memory.set(destination, sitting_on)


class TurtlePrintInstruction(PrintInstruction):
    def __init__(self, param_modes, computer):
        super(PrintInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val = super().get_param_value(memory, at_pos, 1)

        if self._computer.get_dual_instruction_part() == 0:
            print(f"Set color at {self._computer._at} to {val}")
            self._computer.set_curr_color(val)
        else:
            # print(f"set direction to {val}")
            self._computer.set_direction(val)

        self._computer.increment_dual_instruction()


class Turtle(Computer):
    _route = [[0, 0]]
    _painting = {}
    _at = [0, 0]     # x,y  NOT row,col
    _direction = 0   # 0 = up, 1 = right, 2 = down, 3 = left
    _dual_instruction_part = 0

    def __init__(self, program):
        super().__init__(program)
        self.ifactory = TurtleInstructionFactory(self)

    def get_dual_instruction_part(self):
        return self._dual_instruction_part

    def increment_dual_instruction(self):
        self._dual_instruction_part = (self._dual_instruction_part + 1) % 2

    def get_curr_color(self):
        if str(self._at) not in self._painting:
            return 0
        return self._painting[str(self._at)]

    def set_curr_color(self, color):
        self._painting[str(self._at)] = color

    def set_direction(self, delta):
        if delta == 0:
            self._direction -= 1
        else:
            self._direction += 1

        # now we also advance one in that direction
        dir = self._direction % 4
        if dir == 0:
            self._at[1] += 1
        elif dir == 1:
            self._at[0] += 1
        elif dir == 2:
            self._at[1] -= 1
        else:
            self._at[0] -= 1

        self._route.append(self._at[:])


def day11p1():
    program = [3,8,1005,8,291,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,28,1,1003,20,10,2,1103,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,59,1,1004,3,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,84,1006,0,3,1,1102,12,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,114,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,135,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,158,2,9,9,10,2,2,10,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,188,1006,0,56,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,212,1006,0,76,2,1005,8,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,241,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,264,1006,0,95,1,1001,12,10,101,1,9,9,1007,9,933,10,1005,10,15,99,109,613,104,0,104,1,21102,838484206484,1,1,21102,1,308,0,1106,0,412,21102,1,937267929116,1,21101,0,319,0,1105,1,412,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,206312598619,1,1,21102,366,1,0,1105,1,412,21101,179410332867,0,1,21102,377,1,0,1105,1,412,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,709580595968,1,21102,1,400,0,1106,0,412,21102,868389384552,1,1,21101,411,0,0,1106,0,412,99,109,2,21202,-1,1,1,21102,1,40,2,21102,1,443,3,21101,0,433,0,1106,0,476,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,438,439,454,4,0,1001,438,1,438,108,4,438,10,1006,10,470,1102,0,1,438,109,-2,2106,0,0,0,109,4,1202,-1,1,475,1207,-3,0,10,1006,10,493,21102,0,1,-3,21202,-3,1,1,21201,-2,0,2,21101,0,1,3,21102,1,512,0,1106,0,517,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,540,2207,-4,-2,10,1006,10,540,22101,0,-4,-4,1106,0,608,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,0,559,0,1106,0,517,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,578,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,600,21201,-1,0,1,21102,600,1,0,106,0,475,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
    c = Turtle(program)
    c.run()
    print(f"Run complete, {len(c._painting.keys())} locations were painted.")
    xs = []
    ys = []
    for coord in c._route:
        if str(coord) in c._painting.keys() and c._painting[str(coord)] == 1:
            xs.append(coord[0])
            ys.append(coord[1])

    plt.plot(xs, ys, 'ro')
    plt.show()

def day11p2():
    program = [3,8,1005,8,291,1106,0,11,0,0,0,104,1,104,0,3,8,1002,8,-1,10,101,1,10,10,4,10,108,0,8,10,4,10,1002,8,1,28,1,1003,20,10,2,1103,19,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,1001,8,0,59,1,1004,3,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,0,8,10,4,10,1001,8,0,84,1006,0,3,1,1102,12,10,3,8,1002,8,-1,10,101,1,10,10,4,10,1008,8,1,10,4,10,101,0,8,114,3,8,1002,8,-1,10,101,1,10,10,4,10,108,1,8,10,4,10,101,0,8,135,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,0,10,4,10,102,1,8,158,2,9,9,10,2,2,10,10,3,8,1002,8,-1,10,1001,10,1,10,4,10,1008,8,1,10,4,10,101,0,8,188,1006,0,56,3,8,1002,8,-1,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,212,1006,0,76,2,1005,8,10,3,8,102,-1,8,10,1001,10,1,10,4,10,108,1,8,10,4,10,1001,8,0,241,3,8,102,-1,8,10,101,1,10,10,4,10,1008,8,0,10,4,10,1002,8,1,264,1006,0,95,1,1001,12,10,101,1,9,9,1007,9,933,10,1005,10,15,99,109,613,104,0,104,1,21102,838484206484,1,1,21102,1,308,0,1106,0,412,21102,1,937267929116,1,21101,0,319,0,1105,1,412,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,3,10,104,0,104,1,3,10,104,0,104,0,3,10,104,0,104,1,21102,206312598619,1,1,21102,366,1,0,1105,1,412,21101,179410332867,0,1,21102,377,1,0,1105,1,412,3,10,104,0,104,0,3,10,104,0,104,0,21101,0,709580595968,1,21102,1,400,0,1106,0,412,21102,868389384552,1,1,21101,411,0,0,1106,0,412,99,109,2,21202,-1,1,1,21102,1,40,2,21102,1,443,3,21101,0,433,0,1106,0,476,109,-2,2105,1,0,0,1,0,0,1,109,2,3,10,204,-1,1001,438,439,454,4,0,1001,438,1,438,108,4,438,10,1006,10,470,1102,0,1,438,109,-2,2106,0,0,0,109,4,1202,-1,1,475,1207,-3,0,10,1006,10,493,21102,0,1,-3,21202,-3,1,1,21201,-2,0,2,21101,0,1,3,21102,1,512,0,1106,0,517,109,-4,2105,1,0,109,5,1207,-3,1,10,1006,10,540,2207,-4,-2,10,1006,10,540,22101,0,-4,-4,1106,0,608,21201,-4,0,1,21201,-3,-1,2,21202,-2,2,3,21101,0,559,0,1106,0,517,21201,1,0,-4,21102,1,1,-1,2207,-4,-2,10,1006,10,578,21101,0,0,-1,22202,-2,-1,-2,2107,0,-3,10,1006,10,600,21201,-1,0,1,21102,600,1,0,106,0,475,21202,-2,-1,-2,22201,-4,-2,-4,109,-5,2106,0,0]
    c = Turtle(program)
    c._painting['[0, 0]'] = 1
    c.run()
    print(f"Run complete, {len(c._painting.keys())} locations were painted.")
    xs = []
    ys = []
    for coord in c._route:
        if str(coord) in c._painting.keys() and c._painting[str(coord)] == 1:
            xs.append(coord[0])
            ys.append(coord[1])

    plt.plot(xs, ys, 'ro')
    plt.show()


day11p2()