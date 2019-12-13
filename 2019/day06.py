from anytree import Node, RenderTree, Walker
# anytree documentation is at https://anytree.readthedocs.io/en/latest/intro.html

# input = '''COM)B
# B)C
# C)D
# D)E
# E)F
# B)G
# G)H
# D)I
# E)J
# J)K
# K)L'''

orbits = {}
tot_depth = 0

input = open("d6-in.txt")

for orbit in input:
    orbit = orbit.strip()
    print(f"orbit is {orbit}")
    origin_name, orbiter_name = orbit.split(')')
    if origin_name not in orbits:
        origin = Node(origin_name)
        orbits[origin_name] = origin
    origin = orbits[origin_name]

    if orbiter_name not in orbits:
        orbiter = Node(orbiter_name, origin)
        orbits[orbiter_name] = orbiter
    else:
        orbiter = orbits[orbiter_name]
        orbiter.parent = origin

for pre, fill, node in RenderTree(orbits["COM"]):
#    print(f"{pre} {node.name} {node.depth}")
    tot_depth += node.depth

print (f"Total depth: {tot_depth}")

you = orbits['YOU']
san = orbits['SAN']

# print(f"You: {you.path}   Santa: {san.path}")

w = Walker()
path = w.walk(you, san)

# print(path)
# print("Going up:")
# print (path[0])
# print("\n\n\n")
# print("Going down:")
# print(path[2])
# print("\n\n")
print(f"Distance is {len(path[0]) + len(path[2]) - 2}")
# -2 because each route includes the end-point which we don't want to include in # jumps needed
# technically it should be -3 + 1  b/c route from YOU to common parent includes a "step" of curr
# parent, which isn't really a step in changing "orbits", and does not include the top common anscestor
# so instead of -3 +1 we just do -2
