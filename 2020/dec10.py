# a solution to https://adventofcode.com/2020/day/10
 
from collections import Counter

def read_input():
    nums = []
    with open("dec10in.txt") as in_file:
        for line in in_file:
            nums.append(int(line.strip()))
    return nums

nums = read_input()
nums.sort()
print(nums)

# create a list of the differences between elements in the sorted list
diffs = [1] # from outlet to 1st adapter
it = iter(nums)
for e in nums[1:]:
    n = next(it)
    diffs.append(e-n)
diffs.append(3) # from last adapter to device
c = Counter(diffs)

print(f"Diffs: {diffs}")
print(c)
print(f"Part 1: {c[1] * c[3]}")

# for each sequence of 1,1,1... there is a number of alternatives
# (determined by hand) e.g. 1,1,1 ; 1,2 ; 2,1 ; 3
alternatives = {2:2, 3:4, 4:7, 5:13}
num_ones = 0
num_alts = 1
for elem in diffs:
    if elem == 1:
        num_ones += 1
    else:
        if num_ones > 1:
            num_alts *= alternatives[num_ones]
        num_ones = 0
if num_ones > 1:
    num_alts *= alternatives[num_ones]

print(f"Part 2: Total alternatives: {num_alts}")