from functools import cmp_to_key


def print_map(in_map):
    for row in in_map:
        print(row)


def read_map(filename):
    # read the input into aster_map
    infile = open(filename)

    y = 0
    asteroid_map = []
    total_visibility_map = []

    for line in infile:
        asteroid_map.append([])
        total_visibility_map.append([])
        for char in line.strip():
            asteroid_map[y].append(char)
            total_visibility_map[y].append(0)
        y += 1

    return asteroid_map, total_visibility_map


def get_manhattan_distance(r1, c1, r2, c2):
    return abs(r1 - r2) + abs(c1 - c2)


def d10p2():

    asteroid_map, total_visibility_map = read_map("d10-in.txt")
    origin = (11, 19)

    # create a map of clockwise-angle to list of asteroids,
    asteroids_by_angle = {}

    for rnum, row in enumerate(asteroid_map):
        for cnum, col in enumerate(row):
            if col == '.':
                continue

            if rnum == origin[0] and cnum == origin[1]:
                continue

            slope = get_slope(origin[0], origin[1], rnum, cnum)
            # print(f"at {rnum},{cnum} got slope {slope}")
            if slope in asteroids_by_angle:
                coangled_asteroids = asteroids_by_angle[slope]
            else:
                coangled_asteroids = []
                asteroids_by_angle[slope] = coangled_asteroids

            coangled_asteroids.append((rnum, cnum, get_manhattan_distance(origin[0], origin[1], rnum, cnum)))


    # fetch the lists of coangled asteroids by angle, sorted by clock geometry
    # then sort the list by manhattan distance
    all_angles = asteroids_by_angle.keys()
    print(f"asteroids_by_angle has {len(all_angles)} keys")

    comparison_key = cmp_to_key(compare_slopes_by_clock_geo)
    all_angles_sorted = list(all_angles)
    all_angles_sorted.sort(key=comparison_key)
    print(f"all_angles_sorted is {len(all_angles_sorted)} long")

    for angle in all_angles_sorted:
        asteroids_at_angle = asteroids_by_angle[angle]
        asteroids_at_angle.sort(key=lambda x: x[2])


    # walk through the lists of all angles and take one item off each list - make sure taking from the head!
    # and keep a count of # items taken. Keep cycling through until # items = 200 and print the 200th
    tot_asteroids_processed = 0

    while tot_asteroids_processed < 201:
        for angle in all_angles_sorted:
            print(f"{tot_asteroids_processed + 1}: Processing an asteroid at angle {angle}")
            asteroids_at_angle = asteroids_by_angle[angle]
            print(f"There are **{len(asteroids_at_angle)}** asteroids at that angle")
            asteroid = asteroids_at_angle.pop(0)
            print(f"asterod details: {asteroid}")
            tot_asteroids_processed += 1


def d10p1():
    asteroid_map, total_visibility_map = read_map("d10-in.txt")

    print("Debug: asterpod map is:")
    print_map(asteroid_map)

    for row_num, row in enumerate(asteroid_map):
        for col_num, col in enumerate(row):
            total_visibility_map[row_num][col_num] = 0

            if col == '.':  # nothing there
                continue

            # we have an 'origin' asteroid at row_num, col_num
            # print(f"\n\nChecking origin star at ({row_num},{col_num})")
            # now count how many stars are visible from it = those with unique slopes
            set_of_slopes = set([])

            for other_row_num, other_row in enumerate(asteroid_map):
                for other_col_num, other_col in enumerate(other_row):
                    if other_col_num == col_num and other_row_num == row_num:
                        continue
                    if other_col == '.':  # nothing there
                        continue

                    # we have a 'destination' asteroid

                    slope = get_slope(row_num, col_num, other_row_num, other_col_num)

                    if slope in set_of_slopes:
                        pass
                        # print(f"star at ({other_row_num},{other_col_num}) with slope {slope} is NOT visible")
                    else:
                        set_of_slopes.add(slope)
                        # print(f"star at ({other_row_num},{other_col_num}) with slope {slope} IS visible")
                        total_visibility_map[row_num][col_num] += 1
                        # print(f"its visibility is now {visibility_map[row_num][col_num]}")
                        # print(f"slopes is now {set_of_slopes}")

    print_map(total_visibility_map)

    max_visibility = 0
    max_row = 0
    max_col = 0

    for rnum, row in enumerate(total_visibility_map):
        for cnum, col in enumerate(row):
            if total_visibility_map[rnum][cnum] > max_visibility:
                max_visibility = total_visibility_map[rnum][cnum]
                max_row = rnum
                max_col = cnum

    print(f"Maximum value {max_visibility} at x,y=({max_col},{max_row})")


def get_slope(row_num, col_num, other_row_num, other_col_num):
    dx = other_col_num - col_num
    dy = row_num - other_row_num
    # print(f"dx={dx}, dy={dy}")
    if dx == 0:
        slope = 'V'
    else:
        slope = dy / dx

    if other_col_num < col_num:
        slope = str(slope) + 'L'
    else:
        slope = str(slope) + 'R'

    if other_row_num < row_num:
        slope = slope + 'U'
    else:
        slope = slope + 'D'

    return slope


def compare_slopes_by_clock_geo(s1, s2):
    quadrant1 = s1[-2:]
    quadrant2 = s2[-2:]

    if quadrant1 == quadrant2:
        if s1[0] != 'V' and s2[0] != 'V':
            if quadrant1 == 'RU':
                return float(s2[:-2]) - float(s1[:-2])
            elif quadrant1 == 'RD':
                return abs(float(s1[:-2])) - abs(float(s2[:-2]))
            elif quadrant1 == 'LD':
                return float(s2[:-2]) - float(s1[:-2])
            else:
                return float(s2[:-2]) - float(s1[:-2])

        # one of them has vertical slope and therefore considered quadrant 1 or 2
        if quadrant1 == 'RU':
            if s1[0] == 'V':
                return -1
            else:
                return 1
        else:
            if s2[0] == 'V':
                return -1
            else:
                return 1

    elif quadrant1 == 'RU':
        return -1  # all aother quadrants are bigger
    elif quadrant2 == 'LU':
        return -1  # everything is smaller than quadrant 4
    elif quadrant2 == 'RU':
        return 1
    elif quadrant1 == 'LU':
        return 1
    elif quadrant1 == 'RD':
        return -1
    else:
        return 1

d10p2()