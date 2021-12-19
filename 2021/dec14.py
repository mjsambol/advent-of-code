from collections import Counter

rules = dict()

with open("dec14in.txt") as in_file:
    template = in_file.readline().strip()
    in_file.readline()

    for line in in_file.readlines():
        k,v = line.strip().split(' -> ')
        rules[k] = v

def next_step(base):
    result = [base[0:1]]
    for i in range(len(base) - 1):
        result.append(rules[base[i:i+2]])
        result.append(base[i+1])
    return ''.join(result)

for i in range(14):
    template = next_step(template)
    print(template)
    # c = Counter(template)
    # s = sorted(c.items(), key=lambda i: i[1])
    # print([i[1] for i in s])
    # least = s[0]
    # most = s[-1]
    # print(f'{i}: length: {len(template)}; least: {least}, most: {most}, result: {most[1] - least[1]}')