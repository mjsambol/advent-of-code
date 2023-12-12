import re
from collections import defaultdict

class AlmanacMap:
    def __init__(self, line=None, origin=None, destination=None, computation=None) -> None:
        if line:
            m = re.match("^(\w+)-to-(\w+) map:", line.strip())
            self.origin = m.group(1)
            self.destination = m.group(2)
        else:
            self.origin = origin
            self.destination = destination

        self.mappings = []
        self.cached_computation = computation

    def add_mapping(self, line):
        new_mapping_info = [int(x) for x in line.split(' ')]
        self.mappings.append({"range_start":new_mapping_info[1], 
                              "range_end":new_mapping_info[1] + new_mapping_info[2] - 1, 
                              "transform": lambda x: x + new_mapping_info[0] - new_mapping_info[1]})

    def compute(self, origin_value):
        if self.cached_computation:
            return self.cached_computation(origin_value)

        for mapping in self.mappings:
            if mapping["range_start"] <= origin_value <= mapping["range_end"]:
                return mapping["transform"](origin_value)  
        return origin_value

class Almanac:
    def __init__(self) -> None:
        self.mappings = defaultdict(list)  # we'll keep them as origin-name to list of AlmanacMaps in case there's more than one, even as optimization later

    def add(self, almanac_map):
        self.mappings[almanac_map.origin].append(almanac_map)

    def get_transformation(self, destination, origin):
        for mapping_option in self.mappings[origin]:
            if mapping_option.destination == destination:
                return mapping_option.compute
        return None

    def get(self, destination, origin_name, origin_value, depth=0):
        prefix = ' ' * depth
#        print(f"{prefix}Almanac.get(from {origin_name}@{origin_value} to {destination})")
        # is there a direct route from this origin to that destination?
        tx = self.get_transformation(destination, origin_name)
        if tx:
 #           print(f"{prefix}There's a direct mapping, returning {tx(origin_value)}")
            return tx(origin_value)
        
 #       print(f"{prefix}No direct mapping, checking indirects...")
        for mapping_option in self.mappings[origin_name]:
            one_transform = mapping_option.compute(origin_value)
            remaining_transformations = self.get(destination, mapping_option.destination, one_transform, depth=depth+1)
            if remaining_transformations:
  #              print(f"{prefix}That indirect mapping worked, caching it and returning {remaining_transformations}")
                shortcut_computation = lambda x: self.get_transformation(destination, mapping_option.destination)(mapping_option.compute(x))
                shortcut_mapping = AlmanacMap(origin=origin_name, destination=destination, computation=shortcut_computation)
                self.mappings[origin_name].append(shortcut_mapping)

                return remaining_transformations
            else:
  #              print(f"{prefix}Not a viable indirect transformation")
                return None


seeds = []
almanac = Almanac()

with open("dec05in.txt") as my_input:
    for line in my_input:
        if line.startswith("seeds: "):
            seeds = [int(x) for x in line[6:].strip().split(' ')]
        elif len(line.strip()) == 0:
            continue
        else:
            if line[0].isdigit():
                current_map.add_mapping(line)
            else:
                current_map = AlmanacMap(line)
                almanac.add(current_map)

print("Part 1:")
print(min(almanac.get("location", "seed", s) for s in seeds))
print("---------------")

def my_generator(nums):
    while len(nums) > 0 and nums[0] > 0:
        result = nums[0]
        if nums[1] > 0:
            nums[0] += 1
            nums[1] -= 1
            yield result
        else:
            nums = nums[2:]

# print(min(almanac.get("location", "seed", s) for s in my_generator(seeds)))

# for part 2 we need a different approach, there are too many numbers. 
# 1. for each of the "stages", sort the mappings for that stage from lowest to highest *results* produced
# 2. starting at the last stage and working backwards to the first stage:
#    1. starting at the rule producing lowest output, get the range of inputs to that rule
#    2. in the previous stage, what are the input ranges that will produce as output, the selected inputs for the next stage?
#    3.  keep working backwards like that until we have the seed number ranges that will produce the lowest location values. Do we have any matching seed numbers?
         # if not, go back to step 2.1 and select the next lowest rule

# the attempt below didn't work out and I moved on to other days 