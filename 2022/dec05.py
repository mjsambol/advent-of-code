import re

move_pat = "move (\d+) from (\d+) to (\d+)"

def run_through(mechanism):
    with open("dec05in.txt") as my_input:
        stacks = []
        for line in my_input:
            if line.startswith(" 1"):
                stacks = [list(reversed(s)) for s in stacks]
            elif len(line.strip()) == 0:
                continue
            else:
                m = re.match(move_pat, line)
                if m:
                    temp = []
                    for num_moves in range(int(m.group(1))):
                        item = stacks[int(m.group(2))-1].pop()
                        if mechanism == 1:
                            stacks[int(m.group(3))-1].append(item)
                        else:
                            temp.append(item)
                    if mechanism == 2:
                        stacks[int(m.group(3))-1].extend(list(reversed(temp)))
                    continue

                for chunk_num in range(len(line) // 4):
                    chunk = line[chunk_num*4:chunk_num*4 + 4].strip()
                    if len(chunk) == 0:
                        continue
                    if chunk[0] == '[':
                        while len(stacks) <= chunk_num:
                            stacks.append(list())
                        stacks[chunk_num].append(chunk[1])
    return stacks

for mechanism in (1,2):
    stacks = run_through(mechanism)
    print("here are the stacks:")
    for stack in stacks:
        print(stack)
    result = ''.join([s.pop() for s in stacks])
    print(result)