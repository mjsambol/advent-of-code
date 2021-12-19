from collections import defaultdict

connections = defaultdict(list)

with open("dec12in.txt") as in_file:
    for line in in_file.readlines():
        frm,to = line.strip().split('-')
        connections[frm].append(to)
        if frm != 'start' and to != 'end':
            connections[to].append(frm)


def recurse(from_node, this_route, all_routes, can_revisit):
    this_route.append(from_node)

    if from_node == 'end':
        all_routes.append(''.join(this_route))
        return #  anything?

    next_steps = connections[from_node]
    for option in next_steps:
        if option.islower() and option in this_route:  
            if option != can_revisit:
                continue

            num_times_present = len([x for x in this_route if x == option])
            if num_times_present == 2:
                continue  # can't revisit lowercase nodes already visited
            
        recurse(option, this_route.copy(), all_routes, can_revisit)


all_routes = []
recurse('start', list(), all_routes, None)
# print(f"{len(all_routes)} total routes. They are:")
# for r in all_routes:
#     print(r)
print(f"Part 1 Total: {len(all_routes)}")

part_2_routes = set(all_routes)
part_2_repeatable = {k for k in connections.keys() if k.islower() and k not in ['start','end']}

for r in part_2_repeatable:
    all_routes = []
    recurse('start', list(), all_routes, r)
    part_2_routes.update(all_routes)

print(f"Part 2 Total: {len(part_2_routes)}")