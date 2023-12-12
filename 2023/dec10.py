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

with open("dec10in.txt") as data:
    puzzle = [[c for c in line.strip()] for line in data.readlines()]

max_len = 0
prev_head = prev_tail = [cell(r,c) for r in range(len(puzzle)) for c in range(len(puzzle[0])) if puzzle[r][c] == 'S'][0]
head, tail = get_connected_pipes(prev_head["row"], prev_head["col"], puzzle)
while head["row"] != tail["row"] or head["col"] != tail["col"]:
    max_len += 1
    temp = (head, tail)
    head = increment(prev_head, head, puzzle)
    tail = increment(prev_tail, tail, puzzle)
    prev_head, prev_tail = temp
print(max_len+1)