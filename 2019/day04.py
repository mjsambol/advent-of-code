MIN=307237
MAX=769058

# Solution: part 1: 889  part 2 = 589
import re

attempt = MIN - 1
part_1_matches = 0
part_2_matches = 0

# ([0-9])(?!\1)([0-9])\2(?!\2)  -- seen online
# (\d)((?!\1)\d)(\2)((?!\2)\d)  -- figured out with Ido's help

pat_first_two  = re.compile(r"^(\d)\1((?!\1)\d)")
pat_middle_two = re.compile(r"(\d)((?!\1)\d)(\2)((?!\2)\d)")
pat_last_two   = re.compile(r"(\d)((?!\1)\d)(\2)$")
while attempt <= MAX:

    attempt += 1
    pwd = str(attempt)
#    print("checking: " + pwd)
    # test1:
    # if len(pwd) != 6: continue

    # test2:
    # pwd >= MIN and pwd <= MAX

    # test3:  (not necessary for part 2 but minimal cost)
    if not (pwd[0] == pwd[1] or pwd[1] == pwd[2] or pwd[2] == pwd[3] or pwd[3] == pwd[4] or pwd[4] == pwd[5]):
        continue

    # test 4:
    if not (pwd[0] <= pwd[1] <= pwd[2] <= pwd[3] <= pwd[4] <= pwd[5]):
        continue

    part_1_matches +=1

    if pat_first_two.search(pwd) or pat_middle_two.search(pwd) or pat_last_two.search(pwd):
        part_2_matches += 1
        print(f"{pwd} matches (pat)")
        continue

    # if pwd[0] == pwd[1] and pwd[1] != pwd[2]:
    #     num_matches += 1
    #     print(f"{pwd} matches (01)")
    #     continue
    #
    # if pwd[1] == pwd[2] and pwd[0] != pwd[1] and pwd[2] != pwd[3]:
    #     num_matches += 1
    #     print(f"{pwd} matches (12)")
    #     continue
    #
    # if pwd[2] == pwd[3] and pwd[1] != pwd[2] and pwd[3] != pwd[4]:
    #     num_matches += 1
    #     print(f"{pwd} matches (23)")
    #     continue
    #
    # if pwd[3] == pwd[4] and pwd[2] != pwd[3] and pwd[4] != pwd[5]:
    #     num_matches += 1
    #     print(f"{pwd} matches (34)")
    #     continue
    #
    # if pwd[4] == pwd[5] and pwd[3] != pwd[4]:
    #     num_matches += 1
    #     print(f"{pwd} matches (45)")
    #     continue

print (f"Part 1: {part_1_matches}   Part 2: {part_2_matches}")
