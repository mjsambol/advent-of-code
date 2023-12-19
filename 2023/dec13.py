puzzles = []
with open("dec13in.txt") as input_txt:
    puzzle = []
    for line in input_txt:
        if len(line.strip()) == 0:
            puzzles.append(puzzle)
            puzzle = []
            continue
        puzzle.append(line.strip())
    puzzles.append(puzzle)

rotate = lambda grid: [[row[c] for row in grid] for c in range(len(grid[0]))]

num_diff = lambda row1, row2: sum([1 if row1[i] != row2[i] else 0 for i in range(len(row1))])

def get_line_of_reflection(puzzle,part):
    for before_row in range(1,len(puzzle)):
        found = True
        fixed_smudge = False
        for delta in range(0, min(len(puzzle) // 2, before_row, len(puzzle) - before_row)):
            if puzzle[before_row - 1 - delta] != puzzle[before_row + delta]:
                if part == 2 and not fixed_smudge and num_diff(puzzle[before_row - 1 - delta], puzzle[before_row + delta]) == 1:
                    fixed_smudge = True
                else:
                    found = False
                    break
        if found and (part==1 or fixed_smudge):
            return ['h', before_row]
    return ['v', get_line_of_reflection(rotate(puzzle), part)[1]]

for part in [1,2]:
    tot = 0
    for puzzle in puzzles:
        vert_or_horiz, before_index = get_line_of_reflection(puzzle, part)
        tot += before_index if vert_or_horiz == 'v' else 100 * before_index
    print(tot)