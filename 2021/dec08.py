with open("dec08in.txt") as in_file:
    all_input = in_file.readlines()

part_1_result = 0
part_2_result = 0

for line in all_input:
    left, right = line.strip().split(' | ')
    r_parts = right.split(' ')
    for word in r_parts:
        if len(word) in (2,3,4,7):
            part_1_result += 1

    left = sorted([''.join(sorted(word)) for word in left.split(' ')], key=len)
    one = left.pop(0)
    seven = left.pop(0)
    four = left.pop(0)
    top_bar = (set(seven) - set(one)).pop()
    fives = [word for word in left if len(word)==5]   # 2, 3, 5
    sixes = [word for word in left if len(word)==6]   # 0, 9, 6
    eight = [word for word in left if len(word)==7].pop()
    almost_nine = four + top_bar
    for word in sixes:
        delta = (set(word) - set(almost_nine)) 
        if len(delta) == 1:
            nine = word
            sixes.remove(nine)
            break
    bottom_left_bar = (set(eight) - set(nine)).pop()
    two = [word for word in fives if bottom_left_bar in word].pop()
    fives.remove(two)
    three = [word for word in fives if one[0] in word and one[1] in word].pop()
    fives.remove(three)
    five = fives.pop()
    six = [word for word in sixes if len(set(word) - set(five))==1].pop()
    sixes.remove(six)
    zero = sixes.pop()
    wiring = [zero, one, two, three, four, five, six, seven, eight, nine]

    right_val = 0
    for word in r_parts:
        right_val = 10 * right_val + wiring.index(''.join(sorted(word)))
    part_2_result += right_val

print(part_1_result)
print(part_2_result)


