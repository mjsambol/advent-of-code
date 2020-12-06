from collections import Counter

def read_input_chunks():

    with open("dec06in.txt") as in_file:

        chunk = []

        for line in in_file:
            line = line.strip()
            if len(line) == 0:
                if len(chunk) > 0:
                    yield chunk
                    chunk = []
            else:
                chunk.append(line)

        if len(chunk) > 0:
            yield chunk


tot_answers = 0
tot_unanimous = 0

for chunk in read_input_chunks():
    c = Counter()
    for line in chunk:
        c.update(line)
    # print(f"{c}: {len(c.keys())}")
    
    tot_answers += len(c.keys())
    tot_unanimous += sum( [1 for key in c if c[key] == len(chunk)] )

print(f"TOTAL: {tot_answers}")
print(f"TOTAL UNANIMOUS: {tot_unanimous}")

