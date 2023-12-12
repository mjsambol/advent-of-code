def process_line(nums):
    if all(nums[i] == nums[0] for i in range(len(nums))):
        return (nums[-1], nums[-1])
    if all(nums[i] - nums[i-1] == nums[i-1] - nums[i-2] for i in range(2, len(nums))):
        return (nums[0] - (nums[1] - nums[0]), nums[-1] + nums[-1] - nums[-2])
    first_deriv = [nums[i] - nums[i-1] for i in range(1, len(nums))]
    delta = process_line(first_deriv)
    return (nums[0] - delta[0], nums[-1] + delta[-1])

tot_next_vals = tot_prev_vals = 0
with open("dec09in.txt") as my_input:
    for line in my_input:
        prefix, suffix = process_line([int(x) for x in line.strip().split(' ')])
        tot_next_vals += suffix
        tot_prev_vals += prefix
        
print(tot_next_vals, tot_prev_vals)