from math import prod

with open("dec09in.txt") as in_file:
    all_input = in_file.readlines()

puzzle = [[int(c) for c in line.strip()] for line in all_input]
for row in puzzle:  # add a frame of 10s to make the logic of calculating neighbors simpler
    row.insert(0,10)
    row.append(10)
row_len = len(puzzle[0])
puzzle.insert(0,[10] * row_len)
puzzle.append([10] * row_len)

def make_basin(p,r,c,included_coords=None,included_vals=None):

    if included_coords is None:
        included_coords = []
    if included_vals is None:
        included_vals = []

    if (r,c) in included_coords or p[r][c] >= 9:
        return included_vals

    included_vals.append(p[r][c])
    included_coords.append((r,c))
    if r > 1:
        make_basin(p, r-1, c, included_coords, included_vals)
    if r < len(p)-1:
        make_basin(p, r+1, c, included_coords, included_vals)
    if c > 1:
        make_basin(p, r, c-1, included_coords, included_vals)
    if c < len(p[0])-1:
        make_basin(p, r, c+1, included_coords, included_vals)
    return included_vals

low_points = []
basins = []

for r in range(1, len(puzzle)-1):
    for c in range(1, row_len-1):
        neighbors = [puzzle[r-1][c], puzzle[r][c-1], puzzle[r][c+1], puzzle[r+1][c]]
        if puzzle[r][c] < min(neighbors):
            low_points.append(puzzle[r][c])
            basins.append(make_basin(puzzle,r,c))

print(sum(low_points) + len(low_points))
print(prod(sorted([len(basin) for basin in basins], reverse=True)[0:3]))