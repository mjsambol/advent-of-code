def read_input():
    depths = []

    with open("dec01in.txt") as in_file:

        for line in in_file:
            depths.append(int(line.strip()))    

    return depths

depths = read_input()
three_sums = [sum(depths[i:i+3]) for i in range(len(depths)-2)]
p1_increases = [1 if depths[i] > depths[i-1] else 0 for i in range(1, len(depths))]
p2_increases = [1 if three_sums[i] > three_sums[i-1] else 0 for i in range(1, len(three_sums))]
print(f"{sum(p1_increases), sum(p2_increases)}") 