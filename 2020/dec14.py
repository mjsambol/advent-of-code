import re
from collections import Counter

def masked(mask, val):
    result = []
    for i in range(len(mask)):
        if mask[i] == 'X':
            result.append(val[i])
        else:
            result.append(mask[i])
    return ''.join(result)
   
def get_p2_variations(mask, val):
    results = []
    variants = []
    result = []
    variants.append(result)
    for i in range(len(mask)):
        if mask[i] == 'X':
            # grow results
            new_variants = []
            for v in variants:
                z = list(v)
                v.append('0')
                z.append('1')
                new_variants.append(z)
            variants.extend(new_variants)
        elif mask[i] == '0':
            for v in variants:
                v.append(val[i])
        else:
            for v in variants:
                v.append('1')
    
    for variant in variants:
        results.append(''.join(variant))
    return results
    


line_pat = r'mem\[(\d+)\] = (\d+)'
with open("/home/msambol/git/adventofcode/2020/dec14in.txt") as in_file:
    p1_commands = dict()
    p2_commands = dict()

    for line in in_file:
        line = line.strip()
        # print(line)
        if line.startswith('mask = '):
            mask = line[7:]
            continue
        match = re.match(line_pat, line)

        # part 1
        as_bits = format(int(match.group(2)), '036b')
        # print(as_bits)
        # print(masked(mask, as_bits))
        p1_commands[match.group(1)] = masked(mask, as_bits)

        # part 2
        as_bits = format(int(match.group(1)), '036b')
        # print(as_bits)
        variations = get_p2_variations(mask, as_bits)
        for variation in variations:
            # print(variation)
            p2_commands[variation] = match.group(2)


p1_total = 0
for key in p1_commands:
    p1_total += int(p1_commands[key], 2)

print(f"Part 1: {p1_total}")

p2_total = 0
for key in p2_commands:
    p2_total += int(p2_commands[key])

print(f"Part 2: {p2_total}")