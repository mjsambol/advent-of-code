import re

class Board:
    def __init__(self, num, lines) -> None:
        self.id = num
        self.rows = []
        self.status = []
        for line in lines:
            self.rows.append([int(c) for c in re.split('\s+', line.strip())])
            self.status.append([0,0,0,0,0])

    def __str__(self) -> str:
        result = f"Board #{self.id}\n"
        for row in self.rows:
            result = result + str(row) + '\n'
        return result

    def call(self, num):
        for row_num, row in enumerate(self.rows):
            for col_num, col in enumerate(row):
                if num == col:
                    self.status[row_num][col_num] = 1

    def is_won(self):
        for row in self.status:
            if sum(row) == 5:
                return True
        for col_num in range(5):
            if sum([row[col_num] for row in self.status]) == 5:
                return True
        return False

    def uncalled_sum(self):
        return sum([self.rows[r][c] if not self.status[r][c] else 0 for r in range(5) for c in range(5)])


def call_and_get_next_winners(called_num):
    result = []
    for board in all_boards:
        board.call(called_num)
        if board.is_won():
            result.append(board)
    return result


with open("dec04in.txt") as in_file:
    all_input = in_file.readlines()
    called_numbers = [int(c) for c in all_input[0].strip().split(',')]
    all_boards = []

    for board_num in range(int((len(all_input) -1) / 6)):
        all_boards.append( Board(board_num, all_input[(2 + board_num * 6):(2 + board_num * 6)+5]) )

part = 1
for called_num in called_numbers:
#    print(f"Calling {called_num}")
    winning_boards = call_and_get_next_winners(called_num)
    if len(winning_boards) > 0:
#        print("Found a winner")
        if part == 1:
            print(winning_boards[0])
            print(winning_boards[0].uncalled_sum() * called_num)
            part = 2

        all_boards = [board for board in all_boards if board not in winning_boards]
        if len(all_boards) == 0:
            break

print("final winner: \n" + str(winning_boards[-1]))
print(winning_boards[-1].uncalled_sum() * (called_num if called_num else called_numbers[-1]))