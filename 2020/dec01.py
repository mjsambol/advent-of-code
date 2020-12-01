from bisect import bisect_left

def binary_search(a, x): 
    i = bisect_left(a, x) 
    if i != len(a) and a[i] == x: 
        return i 
    else: 
        return -1

def read_input_to_sorted_array():
    expenses = []

    with open("dec01in.txt") as in_file:
        for line in in_file:
            expenses.append(int(line.strip()))

    expenses.sort()
    return expenses

def part1():
    expenses = read_input_to_sorted_array()
    for item in expenses:
        if binary_search(expenses, 2020-item) >= 0:
            print(f"{item} * {2020-item} = {item * (2020-item)}")
            exit()

    print("No match found")

def read_input_to_index():
    expenses = [0] * 2020

    with open("dec01in.txt") as in_file:
        for line in in_file:
            try:
                expenses[int(line.strip())] = 1
            except:
                pass

    return expenses


def part2():
    expenses = read_input_to_index()
    for index1 in range(2020):
        if expenses[index1] == 0:
            continue

        for index2 in range(index1+1, 2020):
            if expenses[index2] == 0  or (index1 + index2 >= 2020):
                continue
            
            if expenses[2020 - index1 - index2]:
                print(f"{index1} * {index2} * {2020-index1-index2} = {index1 * index2 * (2020-index1-index2)}")
                exit()

    print("No match found")

part2()