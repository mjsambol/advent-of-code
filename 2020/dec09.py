from bisect import bisect_left

def read_input():
    result = []
    with open("dec09in.txt") as in_file:
        for line in in_file:
            result.append(int(line.strip()))
    return result

def binary_search(a, x): 
    i = bisect_left(a, x) 
    if i != len(a) and a[i] == x: 
        return i 
    else: 
        return -1

def make_two_sum(sorted_nums, target):
    for index1, n1 in enumerate(sorted_nums):
        if n1 >= target / 2:
            return (-1, -1)
        index2 = binary_search(sorted_nums, target - n1)
        if index2 != -1:
            return (n1, sorted_nums[index2])
    return (-1, -1)

def do_part1(prog_queue, buffer_size):
    preamble = prog_queue[0:buffer_size]

    for num in prog_queue[buffer_size:]:
        prog_sorted = sorted(preamble)
        pair = make_two_sum(prog_sorted, num)
        if pair[0] == pair[1] == -1:
            return num
        preamble.pop(0)
        preamble.append(num)

def make_contiguous_sum(nums, target):
    for index, num in enumerate(nums):
        attempt = [num]
        while sum(attempt) < target:
            index += 1
            attempt.append(nums[index])
        if sum(attempt) == target:
            return attempt
    return [] # just in case


prog_queue = read_input()

part1 = do_part1(prog_queue, 25)
print(f"{part1} cannot be created as a sum of elements in the previous 25 commands")

part2_range = make_contiguous_sum(prog_queue, part1)
print(f"from {part2_range[0]} to {part2_range[-1]} sums to {part1}")
print(part2_range)
print(f"{min(part2_range)} + {max(part2_range)} = {min(part2_range) + max(part2_range)}")