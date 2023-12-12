import re
from math import prod

with open("dec06in.txt") as my_input:
    lines = my_input.readlines()

times = [int(x) for x in re.split(" +", lines[0][6:].strip())]
print(times)

distance = [int(x) for x in re.split(" +", lines[1][10:].strip())]
print(distance)

def does_charge_win(avail_time, charge_time, distance):
    return ((avail_time - charge_time) * charge_time) > distance

def ways_to_win(avail_time, distance):
    print(f"checking ways_to_win {avail_time}, {distance}")
    return sum([1 if does_charge_win(avail_time, charge_time, distance) else 0 for charge_time in range(1, avail_time-1)])

print(prod(ways_to_win(avail_time, distance) for avail_time, distance in zip(times,distance)))
# for race in range(len(times)):

part2_time = int(''.join(re.split(" +", lines[0][6:].strip())))
part2_distance = int(''.join(re.split(" +", lines[1][10:].strip())))
print(ways_to_win(part2_time, part2_distance))
# alt approach for large numbers: search to the smallest num that wins, and to the largest. All the numbers between them will win, so just add up the range