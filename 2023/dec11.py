with open("dec11in.txt") as data:
    puzzle = [[c for c in line.strip()] for line in data]

rows_to_expand = [r for r in range(len(puzzle)) if not '#' in puzzle[r]]
cols_to_expand = [c for c in range(len(puzzle[0])) if not '#' in [puzzle[r][c] for r in range(len(puzzle))]]
orig_galaxies = [(r,c) for r in range(len(puzzle)) for c in range(len(puzzle[0])) if puzzle[r][c]=='#']
print(orig_galaxies)
for part in [1,1000000-1]:
    galaxies = [(g[0] + sum(r < g[0] for r in rows_to_expand) * part, g[1] + sum(c < g[1] for c in cols_to_expand) * part) for g in orig_galaxies]
    print(sum([abs(g1[0] - g2[0]) + abs(g1[1] - g2[1]) for g1 in galaxies for g2 in galaxies[galaxies.index(g1)+1:]]))