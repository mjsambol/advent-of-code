from collections import defaultdict

def mk_range(n1, n2):
    return range(n1, n2+1) if n1 < n2 else range(n2, n1+1)

with open("dec05in.txt") as in_file:
    all_input = in_file.readlines()

vents = defaultdict(int)

for line in all_input:
    l,r = line.split(" -> ")
    lx,ly = map(int, l.split(','))
    rx,ry = map(int, r.split(','))

    if lx == rx:
        for y in mk_range(ly, ry):
            vents[f'{lx},{y}'] += 1
    elif ly == ry:
        for x in mk_range(lx, rx):
            vents[f'{x},{ly}'] += 1
    else:
        if (lx < rx):
            xs = range(lx, rx + 1)
        else:
            xs = range(lx, rx - 1, -1)

        if (ly < ry):
            ys = range(ly, ry + 1)
        else:
            ys = range(ly, ry - 1, -1)

        coords = zip(xs, ys)
        for x,y in coords:
            vents[f'{x},{y}'] += 1

print(sum([1 if vents[key] > 1 else 0 for key in vents] ))