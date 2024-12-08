import re

mul_pat = r"(do\(\)|don't\(\)|mul\((\d{1,3}),(\d{1,3})\))"
p1_tot, p2_tot = 0,0
active = True

with open("dec03.in") as infile:
    for line in infile:
        for mult_op in re.findall(mul_pat, line):
            if mult_op[0].startswith("mul"):
                if active:
                    p2_tot += int(mult_op[1]) * int(mult_op[2])
                else:
                    p1_tot += int(mult_op[1]) * int(mult_op[2])
            elif mult_op[0].startswith("don't") and active:
                active = False
            elif mult_op[0].startswith("do()") and not active:
                active = True
print(p1_tot + p2_tot, p2_tot)
