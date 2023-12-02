import re

tot = 0

def findfirst(str_arr, my_str, from_end=False):
    locs = zip([(my_str.rfind(a_substr) if from_end else my_str.find(a_substr)) for a_substr in str_arr], str_arr)
    ll = list(locs)
  #  print(ll)
    return (max if from_end else min)(ll, key=lambda x: x[0] if x[0] >= 0 or from_end else 10000)


with open("dec01in.txt") as my_input:
    lines = my_input.readlines()

for line in lines:
    match = re.search("(\d)", line)
    d1 = int(match.group(1))
    match = re.search("(\d)", line[match.start(1):][::-1])
    d2 = int(match.group(1))
    tot += 10 * d1 + d2
print(tot)

tot = 0
nums = ['1','2','3','4','5','6','7','8','9','one','two','three','four','five','six','seven','eight','nine']
for line in lines:
    pos, match = findfirst(nums, line)
    nums_pos = nums.index(match)
    d1 = nums_pos + 1 if nums_pos < 9 else nums_pos - 8 
#    print(f"d1 is {d1} based on pos {pos}, match {match}, and num_pos {nums_pos}")
    pos, match = findfirst(nums, line, from_end=True)
    nums_pos = nums.index(match)
    d2 = nums_pos + 1 if nums_pos < 9 else nums_pos - 8 
 #   print(f"d2 is {d2} based on pos {pos}, match {match}, and num_pos {nums_pos}")
    tot += 10 * d1 + d2
print(tot)
