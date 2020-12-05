
MAX_ROW = 127
MAX_COL = 7

def read_input():

    boarding_passes = dict()

    with open("dec05in.txt") as in_file:

        for line in in_file:
            line = line.strip()
            min_row, max_row, min_col, max_col = 0, MAX_ROW, 0, MAX_COL
            for c in line:
                if c == 'B':
                    min_row = (max_row - min_row) // 2 + min_row + 1 
                elif c == 'F':
                    max_row = (max_row - min_row) // 2 + min_row
                elif c == 'R':
                    min_col = (max_col - min_col) // 2 + min_col + 1 
                elif c == 'L':
                    max_col = (max_col - min_col) // 2 + min_col

            boarding_passes[line] = (min_row, min_col, min_row * 8 + min_col)

    return boarding_passes

boarding_passes = read_input()
sorted_passes = sorted(boarding_passes.values(), key=lambda x: x[2], reverse=True)
print(f"highest: {sorted_passes[0]}")
it = iter(sorted_passes)
for p in it:
    q = next(it)
    if p[2] - q[2] != 1:
        print(f"prev: {p}")
        print(f"next: {q}")
