from collections import defaultdict

def bit_arr_to_int(bits):
    result = 0
    for bit in bits:
        result = (result << 1) | bit
    return result

def most_common_bit(list_of_bitfields, index):
    tot = sum(bf[index] for bf in list_of_bitfields)
    return tot >= len(list_of_bitfields) / 2


sum_by_column = defaultdict(int)
all_input = []

with open("dec03in.txt") as in_file:
    for line in in_file:
        line_as_int_arr = [int(c) for c in line.strip()]
        all_input.append(line_as_int_arr)
        for pos, val in enumerate(line_as_int_arr):
            sum_by_column[pos] += val

gamma = [1 if sum_by_column[i] > (len(all_input) / 2) else 0 for i in range(len(sum_by_column))]
epsilon = [0 if sum_by_column[i] > (len(all_input) / 2) else 1 for i in range(len(sum_by_column))]

gamma_as_int = bit_arr_to_int(gamma)
epsilon_as_int = bit_arr_to_int(epsilon)

print(f"gamma: {gamma}, epsilon: {epsilon}")
print(f"as ints: {gamma_as_int}, {epsilon_as_int}, {gamma_as_int * epsilon_as_int}")

# part 2

def filter_input(input, seek_ones=True):
    filtered_input = input.copy()
    for i in range(len(gamma)):
        if len(filtered_input) == 1:
            return filtered_input[0]
        most_common_at_i = most_common_bit(filtered_input, i) if seek_ones else 1 - most_common_bit(filtered_input, i)
        filtered_input = list(filter(lambda x: x[i] == most_common_at_i, filtered_input))
#        print(f"filtered input is now: {filtered_input}")
    return filtered_input[0]


oxygen = filter_input(all_input)
co2 = filter_input(all_input, False)

print(f"oxygen is {oxygen}, co2 is {co2}")
print(f"multiplied: {bit_arr_to_int(oxygen) * bit_arr_to_int(co2)}")