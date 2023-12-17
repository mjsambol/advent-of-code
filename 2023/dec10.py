pipe_run_rules = {
        'F': lambda from_r, from_c, pipe_r, pipe_c, puzzle: cell(from_r -1,from_c +1) if from_c == pipe_c else cell(from_r +1,from_c -1),
        'J': lambda from_r, from_c, pipe_r, pipe_c, puzzle: cell(from_r +1,from_c -1) if from_c == pipe_c else cell(from_r -1,from_c +1),
        'L': lambda from_r, from_c, pipe_r, pipe_c, puzzle: cell(from_r +1,from_c +1) if from_c == pipe_c else cell(from_r -1,from_c -1),
        '7': lambda from_r, from_c, pipe_r, pipe_c, puzzle: cell(from_r -1,from_c -1) if from_c == pipe_c else cell(from_r +1,from_c +1),
        '|': lambda from_r, from_c, pipe_r, pipe_c, puzzle: cell(from_r -2,from_c) if from_r -1 == pipe_r else cell(from_r +2,from_c),
        '-': lambda from_r, from_c, pipe_r, pipe_c, puzzle: cell(from_r,from_c +2) if from_c +1== pipe_c else cell(from_r,from_c -2)}

pipe_check_rules = {
        'F': lambda from_r, from_c, pipe_r, pipe_c: (from_c == pipe_c and from_r - 1 == pipe_r) or (from_r == pipe_r and from_c -1 == pipe_c),
        'J': lambda from_r, from_c, pipe_r, pipe_c: (from_c == pipe_c and from_r + 1 == pipe_r) or (from_r == pipe_r and from_c +1 == pipe_c),
        'L': lambda from_r, from_c, pipe_r, pipe_c: (from_c == pipe_c and from_r + 1 == pipe_r) or (from_r == pipe_r and from_c -1 == pipe_c),
        '7': lambda from_r, from_c, pipe_r, pipe_c: (from_c == pipe_c and from_r - 1 == pipe_r) or (from_r == pipe_r and from_c +1 == pipe_c),
        '|': lambda from_r, from_c, pipe_r, pipe_c: (from_c == pipe_c and from_r - 1 == pipe_r) or (from_c == pipe_c and from_r +1 == pipe_r),
        '-': lambda from_r, from_c, pipe_r, pipe_c: (from_r == pipe_r and from_c - 1 == pipe_c) or (from_r == pipe_r and from_c +1 == pipe_c),
        '.': lambda from_r, from_c, pipe_r, pipe_c: False}

def cell(r,c):
    return {"row":r, "col":c, "name":puzzle[r][c]}

def get_connected_pipes(r_in, c_in, puzzle):
    return [cell(r,c) for (r,c) in [(r_in-1, c_in), (r_in, c_in-1), (r_in, c_in+1), (r_in+1, c_in)]
                   if len(puzzle)>r>=0 and len(puzzle[0])>c>=0 and pipe_check_rules[puzzle[r][c]](r_in, c_in, r, c)]

def increment(prev, pipe, puzzle):
    return pipe_run_rules[pipe["name"]](prev["row"], prev["col"], pipe["row"], pipe["col"], puzzle)

def replace_s_with_joint(puzzle, s_loc):
    row, col = s_loc["row"], s_loc["col"]
    puzzle[row][col] = (
        '-' if (0 < col < len(puzzle[row]) -1 and puzzle[row][col-1] in ['-', 'F', 'L'] and puzzle[row][col+1] in ['-', 'J', '7']) else
        '|' if (0 < row < len(puzzle) -1      and puzzle[row-1][col] in ['|', 'F', '7'] and puzzle[row+1][col] in ['|', 'J', 'L']) else 
        'F' if (row < len(puzzle) -1 and col < len(puzzle[row]) -1 and puzzle[row][col+1] in ['-', 'J', '7'] and puzzle[row+1][col] in ['|', 'J', 'L']) else 
        'J' if (0 < row              and col > 0                   and puzzle[row-1][col] in ['|', 'F', '7'] and puzzle[row][col-1] in ['-', 'F', 'L']) else 
        '7' if (0 < row              and col < len(puzzle[row]) -1 and puzzle[row][col-1] in ['-', 'F', 'L'] and puzzle[row+1][col] in ['|', 'J', 'L']) else 
        'L')

with open("dec10in.txt") as data:
    puzzle = [[c for c in line.strip()] for line in data.readlines()]
    puzzle_copy = [[' ' for c in row] for row in puzzle]

max_len = 1
prev_head = prev_tail = s_loc = [cell(r,c) for r in range(len(puzzle)) for c in range(len(puzzle[0])) if puzzle[r][c] == 'S'][0]
head, tail = get_connected_pipes(prev_head["row"], prev_head["col"], puzzle)
while head["row"] != tail["row"] or head["col"] != tail["col"]:
    max_len += 1
    temp = (head, tail)
    head = increment(prev_head, head, puzzle)
    tail = increment(prev_tail, tail, puzzle)
    puzzle_copy[prev_head["row"]][prev_head["col"]] = puzzle[prev_head["row"]][prev_head["col"]]
    puzzle_copy[prev_tail["row"]][prev_tail["col"]] = puzzle[prev_tail["row"]][prev_tail["col"]]
    prev_head, prev_tail = temp
print(f"Part 1: {max_len}")

puzzle_copy[prev_head["row"]][prev_head["col"]] = puzzle[prev_head["row"]][prev_head["col"]]
puzzle_copy[prev_tail["row"]][prev_tail["col"]] = puzzle[prev_tail["row"]][prev_tail["col"]]
puzzle_copy[tail["row"]][tail["col"]] = puzzle[tail["row"]][tail["col"]]

replace_s_with_joint(puzzle_copy, s_loc)

tot_inside = 0
for row in puzzle_copy:
    status = 'O'   # may be O (outside), I (inside), F (traversing pipe from F) or L (traversing pipe from L)
    for char in row:
        if char == ' ' and status == 'I':
            tot_inside += 1
        elif char == '|':
            status = 'I' if status == 'O' else 'O'
        elif char in ['F', 'L']:
            status = status + char
        elif char == '7':
            if status[1] == 'F':
                status = status[0]
            else:
                status = 'I' if status[0] == 'O' else 'O'
        elif char == 'J':
            if status[1] == 'F':
                status = 'I' if status[0] == 'O' else 'O'
            else:
                status = status[0]

print(f"Part 2: total inside: {tot_inside}")