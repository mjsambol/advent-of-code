from collections import defaultdict

with open("dec10in.txt") as in_file:
    all_input = in_file.readlines()

bracket_pairs = {'(':')', '[':']', '{':'}', '<':'>'}
bracket_costs = {')':3, ']':57, '}':1197, '>':25137}
openers = bracket_pairs.keys()
bad_chars = defaultdict(int)
incomplete_lines = []

for line in all_input:
    braces = []
    for i,c in enumerate(line.strip()):
        if c in openers:
            braces.append(c)
        else:
            if len(braces) == 0 or bracket_pairs[braces.pop()] != c:
                bad_chars[c] += 1
                break
    if i == len(line.strip()) - 1:
        incomplete_lines.append(braces)

print( sum(
    bracket_costs[bad_char] * bad_chars[bad_char] 
    for bad_char in bad_chars.keys()) )

incomplete_costs = {')':1, ']':2, '}':3, '>':4}
incomplete_line_scores = []
for line in incomplete_lines:
    print(f"processing incomplete: {line}")
    line_score = 0
    for c in reversed(line):
        line_score = line_score * 5 + incomplete_costs[bracket_pairs[c]]
    print(f"it costs {line_score}")
    incomplete_line_scores.append(line_score)

print(f"Middle score: {sorted(incomplete_line_scores)[len(incomplete_line_scores) // 2]}")