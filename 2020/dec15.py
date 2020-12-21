data = [int(j) for j in "1,0,18,10,19,6".split(',')]

def list_rindex(li, x, from_index=-1):
    if from_index == -1:
        from_index += len(li)
    for i in range(from_index, -1, -1):
        if li[i] == x:
            return i
    raise ValueError("{} is not in list".format(x))


tot_len = len(data)
list_last_index = dict()
for i in range(tot_len-1):
    list_last_index[data[i]] = i

prev_val = data[-1]
part_1 = None
part_2 = None

for i in range(6,30000000):
#        prev_index = list_rindex(data, prev_val, len(data) -2)
    if prev_val not in list_last_index:
        new_val = 0
    else:
        new_val = tot_len - 1 - list_last_index[prev_val]
#    print(new_val)
    list_last_index[prev_val] = tot_len - 1
    prev_val = new_val
    tot_len += 1
    if i == 2019:
        part_1 = new_val
    elif i == 30000000-1:
        part_2 = new_val

print(part_1)
print(part_2)