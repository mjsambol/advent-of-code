print(sum([((all(n>0 for n in deltas) or all(n<0 for n in deltas)) and max(deltas) <= 3 and min(deltas) >= -3) for deltas in [[int(line_of_nums[i]) - int(line_of_nums[i+1]) for i in range(len(line_of_nums) - 1)] for line_of_nums in [line.strip().split(' ') for line in open("day02.in").readlines()]]]), sum(any([((all(n > 0 for n in deltas) or all(n < 0 for n in deltas)) and max(deltas) <= 3 and min(deltas) >= -3) for deltas in line]) for line in ([[int(line_of_nums[i]) - int(line_of_nums[i+1]) for i in range(len(line_of_nums) - 1)] for line_of_nums in subset_options] for subset_options in [[line_of_numchars[:elem_to_skip] + line_of_numchars[elem_to_skip + 1:] for elem_to_skip in range(len(line_of_numchars))] for line_of_numchars in [line.strip().split(' ') for line in open("day02.in").readlines()]])))