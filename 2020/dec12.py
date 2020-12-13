def read_input():
    dirs = []
    with open("dec12in.txt") as in_file:
        for line in in_file:
            line = line.strip()
            dirs.append((line[0], int(line[1:])))
    return dirs

def step(x,y,d,amt):
    if d == 'N':
        y += amt
    elif d == 'S':
        y -= amt
    elif d == 'E':
        x += amt
    elif d == 'W':
        x -= amt
    return (x, y)


compass = ['N', 'E', 'S', 'W']

x, y = 0, 0
facing = 1

for d,amt in read_input():
    if d in compass:
        x,y = step(x,y,d,amt)
    elif d == 'L':
        facing = (facing - (amt // 90)) % 4
    elif d == 'R':
        facing = (facing + (amt // 90)) % 4
    elif d == 'F':
        x,y = step(x,y,compass[facing],amt)
    # print(f"Now at: {x},{y}")

print(f"Part 1 Manhattan distance = {abs(x)}+{abs(y)} = {abs(x) + abs(y)}\n\n")

x, y = 0, 0
facing = 1
way_x, way_y = 10, 1

for d,amt in read_input():
    if d in compass:
        way_x,way_y = step(way_x,way_y,d,amt)
    elif d == 'L':
        for _ in range(amt // 90):
            way_x, way_y  = -1 * way_y, way_x   
    elif d == 'R':
        for _ in range(amt // 90):
            way_x, way_y  = way_y, -1 * way_x  
    elif d == 'F':
        x += amt * way_x
        y += amt * way_y
    print(f"[{d}{amt}] Now at: {x},{y}  and waypoint deltas {way_x},{way_y}")

print(f"Manhattan distance = {abs(x)}+{abs(y)} = {abs(x) + abs(y)}\n\n")
