from day09 import Computer, StoreInstruction, PrintInstruction, InstructionFactory
from enum import Enum
import os
import time


class MazeInstructionFactory(InstructionFactory):
    def __init__(self, computer):
        super().__init__(computer)

    def get_instruction(self, opcode):
        operation = opcode % 100

        if operation == 3:
            return MazeStoreInstruction(InstructionFactory.split_opcodes(opcode), self._computer)
        elif operation == 4:
            return MazePrintInstruction(InstructionFactory.split_opcodes(opcode), self._computer)
        else:
            return super().get_instruction(opcode)


class MazeStoreInstruction(StoreInstruction):
    """Provide a movement command, from among
    1: go North
    2: go South
    3: go West
    4: go East"""

    def __init__(self, param_modes, computer):
        super(StoreInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):

        destination = memory.get(at_pos + 1)

        next_dir = self._computer.get_next_direction_to_explore()
        memory.set(destination, next_dir.value)


class MazePrintInstruction(PrintInstruction):
    """
    Program's response to our movement request:
    0: there is a wall there
    1: move successful
    2: move successful and destination achieved
    """

    def __init__(self, param_modes, computer):
        super(PrintInstruction, self).__init__(param_modes, computer)

    def run(self, memory, at_pos):
        val = super().get_param_value(memory, at_pos, 1)
        # if val == 2:
        #     print("We found destination!")

        self._computer.set_status_of_next_explore_cell(MazeCellType(val))


class MazeCellType(Enum):
    WALL = 0
    PATH = 1
    DESTINATION = 2
    DROID = 3
    UNKNOWN = 4

    def __str__(self):
        if self.value == 0:
            return '#'
        if self.value == 1:
            return '.'
        if self.value == 2:
            return '$'
        if self.value == 3:
            return 'D'
        return ' '


def from_to(loc1, loc2):
    if loc1.x < loc2.x:
        return Direction.EAST
    if loc1.x > loc2.x:
        return Direction.WEST
    if loc1.y < loc2.y:
        return Direction.SOUTH
    if loc1.y > loc2.y:
        return Direction.NORTH


class Direction(Enum):
    NORTH = 1
    SOUTH = 2
    WEST = 3
    EAST = 4

    def increment_cell(self, in_cell):
        if self.value == 1:  # going up means lower Y values
            return Cell(in_cell.x, in_cell.y - 1)
        if self.value == 2:
            return Cell(in_cell.x, in_cell.y + 1)
        if self.value == 3:
            return Cell(in_cell.x - 1, in_cell.y)
        return Cell(in_cell.x + 1, in_cell.y)


class Cell:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __str__(self):
        return f"{self.x},{self.y}"

    def __repr__(self):
        return f"Cell({self.x}, {self.y})"

    def equals(self, col, row):
        return self.x == col and self.y == row


class Maze(Computer):

    def __init__(self, p_program):
        super().__init__(p_program)
        self.i_factory = MazeInstructionFactory(self)
        self._maze = {}
        self._droid_position = Cell(21, 21)
        self._maze[str(self._droid_position)] = MazeCellType.DROID
        self._next_explore_direction = Direction.NORTH
        self._exploration_route = [self._droid_position]
        self._destination = None
        self._keep_running = True

    def get_as_array(self):
        col_range, row_range = self.get_size()
        result = [['?' for _ in range(col_range)] for _ in range(row_range)]
        for row in range(row_range):
            for col in range(col_range):
                key = f'{col},{row}'
                if key not in self._maze:
                    continue
                result[row][col] = str(self._maze[key])

        result[self._destination.y][self._destination.x] = '0'
        return result

    # def get_droid_position(self):
    #     return self._droid_position
    #
    def move_droid(self, direction):
        # print(f"move_droid: to {direction}")
        prev_pos = self._droid_position
        self._droid_position = direction.increment_cell(self._droid_position)
        self._exploration_route.append(self._droid_position)
        if prev_pos == self._destination:
            self._maze[str(prev_pos)] = MazeCellType.DESTINATION
        else:
            self._maze[str(prev_pos)] = MazeCellType.PATH

        self._maze[str(self._droid_position)] = MazeCellType.DROID

    def set_status_of_next_explore_cell(self, status):
        next_cell = self._next_explore_direction.increment_cell(self._droid_position)
        self._maze[str(next_cell)] = status

        if status == MazeCellType.DESTINATION:
            print("YOU HAVE REACHED YOUR DESTINATION!")
            self._destination = next_cell
            self.move_droid(self._next_explore_direction)
        elif status == MazeCellType.PATH:
            self.move_droid(self._next_explore_direction)

        time.sleep(0.1)
        os.system('clear')
        print(f"After updating status maze is now:")
        print(self)
        print(f"Route length is : {len(self._exploration_route)}, final entry is {self._exploration_route[-1]}")

    # noinspection SpellCheckingInspection
    def get_next_direction_to_explore(self):
        directions = (Direction.NORTH, Direction.SOUTH, Direction.WEST, Direction.EAST)

        for direc in directions:
            check_cell = direc.increment_cell(self._droid_position)
            if str(check_cell) not in self._maze:
                self._next_explore_direction = direc
                # print(f"get_next_direction_to_explore: returning {direc}")
                return direc

        # we've run into a dead end, so now need to back-track and explore
        # the options we didn't consider yet.

        if len(self._exploration_route) < 2:
            print("Back to the beginning, all done.")
            self._keep_running = False
            return Direction.SOUTH  # Arbitrary

        self._exploration_route.pop()  # backtracking, so remove current location from history
        prev_loc = self._exploration_route.pop()
        backup = from_to(self._droid_position, prev_loc)
        self._next_explore_direction = backup
        return backup

    def get_curr_instruction(self):
        if self._keep_running:
            return super().get_curr_instruction()
        else:
            return 99  # indicates the program should stop running.

    def get_dimensions(self):
        # the puzzle starts at an 'origin', and we don't know in advance how far in any direction
        # we'll be moving, so we don't know the coordinates of the origin
        max_col = int(max(self._maze.keys(), key=lambda s: int(s.split(',')[0])).split(',')[0])
        max_row = int(max(self._maze.keys(), key=lambda s: int(s.split(',')[1])).split(',')[1])
        min_col = int(min(self._maze.keys(), key=lambda s: int(s.split(',')[0])).split(',')[0])
        min_row = int(min(self._maze.keys(), key=lambda s: int(s.split(',')[1])).split(',')[1])
        col_range = max_col - min_col + 1
        row_range = max_row - min_row + 1
        return max_col, max_row, min_col, min_row, col_range, row_range

    def get_size(self):
        max_col, max__row, min_col, min_row, col_range, row_range = self.get_dimensions()
        return col_range, row_range

    def __str__(self):
        result = ""
        max_col, max__row, min_col, min_row, col_range, row_range = self.get_dimensions()
        # print(f"Printing the maze, col_range={col_range}, row_range={row_range}")
        # print(f"         min_row={min_row}, max_row={max_row}, min_col={min_col}, max_col={max_col}")

        for row in range(row_range):
            row_str = ""
            for col in range(col_range):
                key = str(Cell(col + min_col, row + min_row))
                if key not in self._maze:
                    row_str = row_str + ' '
                elif self._destination and self._destination.equals(col + min_col, row + min_row):
                    row_str = row_str + '$'
                elif col + min_col == 0 and row + min_row == 0:
                    row_str = row_str + 's'
                else:
                    row_str += str(self._maze[key])
            result += row_str + '\n'

        return result


program = [3, 1033, 1008, 1033, 1, 1032, 1005, 1032, 31, 1008, 1033, 2, 1032, 1005, 1032, 58, 1008, 1033, 3, 1032, 1005,
           1032, 81, 1008, 1033, 4, 1032, 1005, 1032, 104, 99, 102, 1, 1034, 1039, 101, 0, 1036, 1041, 1001, 1035, -1,
           1040, 1008, 1038, 0, 1043, 102, -1, 1043, 1032, 1, 1037, 1032, 1042, 1105, 1, 124, 1001, 1034, 0, 1039, 102,
           1, 1036, 1041, 1001, 1035, 1, 1040, 1008, 1038, 0, 1043, 1, 1037, 1038, 1042, 1106, 0, 124, 1001, 1034, -1,
           1039, 1008, 1036, 0, 1041, 102, 1, 1035, 1040, 1002, 1038, 1, 1043, 101, 0, 1037, 1042, 1106, 0, 124, 1001,
           1034, 1, 1039, 1008, 1036, 0, 1041, 1002, 1035, 1, 1040, 102, 1, 1038, 1043, 101, 0, 1037, 1042, 1006, 1039,
           217, 1006, 1040, 217, 1008, 1039, 40, 1032, 1005, 1032, 217, 1008, 1040, 40, 1032, 1005, 1032, 217, 1008,
           1039, 37, 1032, 1006, 1032, 165, 1008, 1040, 39, 1032, 1006, 1032, 165, 1102, 2, 1, 1044, 1106, 0, 224, 2,
           1041, 1043, 1032, 1006, 1032, 179, 1101, 0, 1, 1044, 1105, 1, 224, 1, 1041, 1043, 1032, 1006, 1032, 217, 1,
           1042, 1043, 1032, 1001, 1032, -1, 1032, 1002, 1032, 39, 1032, 1, 1032, 1039, 1032, 101, -1, 1032, 1032, 101,
           252, 1032, 211, 1007, 0, 74, 1044, 1106, 0, 224, 1102, 0, 1, 1044, 1106, 0, 224, 1006, 1044, 247, 1002, 1039,
           1, 1034, 102, 1, 1040, 1035, 1002, 1041, 1, 1036, 102, 1, 1043, 1038, 1001, 1042, 0, 1037, 4, 1044, 1106, 0,
           0, 4, 35, 96, 8, 87, 44, 67, 40, 80, 25, 91, 53, 86, 23, 96, 7, 76, 76, 10, 30, 90, 46, 47, 40, 93, 75, 3,
           17, 1, 19, 89, 7, 92, 47, 95, 3, 92, 39, 72, 69, 6, 18, 86, 94, 19, 82, 98, 9, 7, 91, 42, 86, 29, 83, 65, 43,
           91, 71, 92, 16, 96, 82, 5, 81, 6, 92, 93, 76, 71, 17, 91, 91, 73, 64, 33, 27, 89, 4, 99, 81, 80, 6, 57, 87,
           9, 42, 99, 97, 13, 42, 81, 82, 72, 68, 35, 93, 2, 99, 6, 6, 94, 2, 39, 39, 86, 43, 97, 77, 86, 21, 56, 75,
           61, 91, 82, 56, 94, 32, 47, 90, 33, 72, 93, 13, 87, 12, 42, 68, 99, 71, 34, 97, 79, 87, 99, 79, 25, 42, 95,
           97, 51, 93, 80, 33, 71, 68, 89, 50, 49, 78, 77, 24, 93, 70, 13, 11, 56, 29, 18, 77, 77, 94, 60, 80, 75, 84,
           42, 87, 90, 58, 84, 27, 78, 3, 80, 70, 85, 79, 4, 36, 94, 65, 79, 93, 94, 13, 97, 75, 49, 92, 15, 84, 5, 85,
           35, 67, 96, 87, 64, 32, 83, 97, 20, 89, 64, 18, 93, 32, 46, 91, 57, 53, 75, 56, 7, 56, 92, 99, 36, 22, 93,
           19, 25, 29, 48, 86, 94, 68, 18, 95, 79, 87, 97, 55, 75, 44, 65, 82, 99, 31, 94, 42, 53, 81, 72, 85, 70, 93,
           47, 40, 77, 60, 85, 87, 11, 60, 98, 25, 90, 88, 93, 93, 85, 64, 43, 88, 96, 36, 83, 14, 98, 40, 48, 11, 18,
           80, 97, 49, 23, 2, 91, 85, 50, 88, 94, 41, 75, 99, 84, 15, 45, 9, 81, 83, 96, 51, 56, 58, 76, 72, 50, 94, 59,
           76, 87, 10, 25, 88, 73, 99, 20, 95, 46, 93, 88, 2, 50, 89, 86, 26, 18, 85, 72, 85, 75, 66, 83, 25, 97, 96,
           25, 94, 14, 34, 94, 89, 57, 88, 78, 17, 92, 59, 40, 29, 84, 87, 55, 61, 81, 9, 82, 93, 17, 33, 81, 81, 58,
           43, 91, 68, 86, 80, 61, 83, 23, 46, 78, 60, 14, 94, 79, 28, 91, 57, 79, 83, 48, 92, 5, 49, 97, 81, 56, 53,
           84, 42, 58, 93, 20, 71, 29, 29, 89, 88, 34, 31, 87, 92, 78, 62, 78, 72, 93, 3, 54, 97, 82, 38, 32, 89, 86,
           88, 38, 19, 84, 51, 99, 60, 90, 95, 14, 78, 11, 82, 89, 12, 87, 98, 70, 79, 33, 76, 44, 97, 79, 33, 19, 34,
           83, 58, 4, 89, 21, 88, 78, 46, 78, 76, 66, 61, 92, 91, 38, 86, 27, 61, 86, 46, 52, 97, 44, 80, 89, 53, 55,
           47, 83, 34, 44, 97, 37, 41, 92, 28, 70, 95, 82, 91, 76, 8, 99, 2, 80, 1, 66, 96, 71, 94, 1, 44, 89, 29, 13,
           99, 35, 80, 89, 31, 91, 19, 77, 46, 85, 77, 93, 61, 31, 62, 14, 92, 82, 73, 94, 86, 20, 31, 94, 72, 73, 44,
           61, 91, 79, 40, 88, 69, 85, 6, 83, 96, 49, 12, 77, 39, 83, 91, 24, 70, 13, 81, 57, 39, 88, 38, 23, 80, 43,
           92, 67, 46, 87, 25, 80, 93, 82, 68, 98, 93, 63, 85, 29, 18, 78, 94, 27, 89, 85, 20, 63, 89, 93, 96, 99, 50,
           71, 97, 15, 28, 53, 78, 85, 78, 82, 64, 67, 14, 94, 47, 96, 65, 58, 81, 20, 91, 36, 82, 55, 11, 85, 87, 59,
           84, 6, 67, 87, 69, 88, 81, 68, 38, 84, 52, 33, 79, 97, 69, 89, 89, 34, 96, 18, 78, 67, 87, 36, 93, 57, 77,
           77, 21, 47, 99, 27, 26, 79, 7, 88, 37, 90, 33, 25, 96, 66, 83, 24, 30, 82, 84, 16, 82, 85, 15, 55, 92, 20,
           80, 92, 38, 20, 34, 87, 67, 11, 84, 28, 42, 93, 26, 54, 89, 85, 78, 82, 60, 14, 9, 76, 85, 10, 80, 80, 50,
           85, 29, 86, 20, 61, 81, 80, 51, 32, 88, 91, 92, 34, 56, 79, 58, 76, 41, 47, 89, 24, 40, 90, 85, 88, 30, 48,
           91, 42, 2, 91, 95, 98, 60, 79, 40, 86, 61, 79, 81, 23, 91, 91, 12, 21, 78, 54, 75, 61, 11, 79, 89, 73, 84,
           13, 95, 81, 6, 52, 92, 37, 76, 65, 82, 84, 87, 40, 94, 70, 78, 71, 83, 46, 94, 2, 79, 57, 80, 35, 99, 21, 83,
           81, 93, 64, 81, 78, 99, 57, 87, 49, 87, 41, 92, 83, 82, 58, 92, 0, 0, 21, 21, 1, 10, 1, 0, 0, 0, 0, 0, 0]


def day15p1():
    c = Maze(program)
    c.run()
    print(f"Run complete, screen is:")
    print(c)
    return c


def print_maze_array(maze):
    for row in maze:
        row_to_print = ''
        for col in row:
            row_to_print += col
        print(row_to_print)


def day15p2(maze):
    fully_oxygenated = False
    num_rows = len(maze)
    num_cols = len(maze[0])
    num_steps = 0

    while not fully_oxygenated:
        fully_oxygenated = True
        gen_marker = f'{num_steps % 10}'
        next_gen_marker = f'{(num_steps + 1) % 10}'
        for row in range(num_rows):
            for col in range(num_cols):
                if maze[row][col] == '.':
                    if maze[row][col-1] == gen_marker or maze[row][col+1] == gen_marker or maze[row-1][col] == gen_marker or maze[row+1][col] == gen_marker:
                        maze[row][col] = next_gen_marker
                    else:
                        fully_oxygenated = False
        num_steps += 1
        time.sleep(0.2)
        os.system('clear')
        print_maze_array(maze)
        print(num_steps)

    print(f"Total steps: {num_steps}")


c = day15p1()
day15p2(c.get_as_array())
