with open("dec14in.txt") as puzzle_file:
    puzzle_rows = [l.strip() for l in puzzle_file.readlines()]

rotate = lambda grid: [[row[c] for row in grid] for c in range(len(grid[0]))]

def shift(col, rev=False):
    new_col = []
    for chunk in ''.join(col).split('#'):
        new_col.extend(sorted(chunk, reverse=rev))
        new_col.extend('#')
    new_col.pop()
    return new_col

adjusted_puzzle_columns = [shift(col, rev=True) for col in rotate(puzzle_rows)]
balanced_puzzle = rotate(adjusted_puzzle_columns)

total = sum([balanced_puzzle[row].count('O') * (len(balanced_puzzle) - row) for row in range(len(balanced_puzzle))])
print(total)

def spin(puzzle):
    # north
    adjusted_puzzle_columns = [shift(col, rev=True) for col in rotate(puzzle)]
    puzzle = rotate(adjusted_puzzle_columns)
    # west
    puzzle = [shift(row, rev=True) for row in puzzle]
    # south
    adjusted_puzzle_columns = [shift(col) for col in rotate(puzzle)]
    puzzle = rotate(adjusted_puzzle_columns)
    # east
    return [shift(row) for row in puzzle]

results = []
weights = []
while True:
    puzzle_rows = spin(puzzle_rows)
    result = ''.join([''.join(row) for row in puzzle_rows])
    if result in results:
        offset = results.index(result)
        frequency = len(results) - offset
        print(f"Repeated after {len(results)} spins. We had it also at {offset}, so the pattern repeats every {frequency}.")
        break
    results.append(result)
    weights.append(sum([puzzle_rows[row].count('O') * (len(puzzle_rows) - row) for row in range(len(puzzle_rows))]))

remainder = (1000000000 - offset) % frequency
print(weights[offset + remainder - 1])