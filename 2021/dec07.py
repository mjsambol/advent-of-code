with open("dec07in.txt") as in_file:
    input = list(map(int, in_file.readline().split(',')))

all_options = list(range(min(input), max(input)+1))

def get_min_cost_option(cost_to_move_to=lambda x: x):

    costs_per_input = {an_input: [cost_to_move_to(abs(an_input - option)) for option in all_options] for an_input in input}

    tot_costs_per_option = [sum([costs_per_input[an_input][i] for an_input in input]) for i in all_options]

    return min(tot_costs_per_option)


print(get_min_cost_option())

tot_cost_to_move = {option: sum([i for i in range(option+1)]) for option in all_options}

print(get_min_cost_option(lambda x: tot_cost_to_move[x]))