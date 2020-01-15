import math
from collections import OrderedDict, defaultdict


class Molecule:
    element = ''
    quantity = 0

    def __init__(self, num_and_elem):
        components = num_and_elem.split(' ')
        self.quantity = int(components[0].strip())
        self.element = components[1].strip()

    def __repr__(self):
        return f"Molecule({self.quantity}, {self.element})"


def read_input():
    recipes_dict = {}

    with open("day14-in.txt") as in_file:
        for line in in_file:
            rule_parts = line.split(' => ')
            recipe_ingredients_str = rule_parts[0]
            recipe_output = Molecule(rule_parts[1])
            recipe_ingredients = []
            for chunk in recipe_ingredients_str.split(', '):
                recipe_ingredients.append(Molecule(chunk))
            # print(f"Recipe: {recipe_output} <= {recipe_ingredients}")
            recipes_dict[recipe_output.element] = {'produced': recipe_output.quantity, 'needed': recipe_ingredients}

    return recipes_dict


dict_of_rules = read_input()
unneeded_produced = defaultdict(lambda: 0)
ore_required = 0


def part1():
    global ore_required
    global unneeded_produced

    still_need = OrderedDict()  # mapping of element names to quantities

    # initialize the list of 'molecules' we need based on the formula for FUEL
    for molecule in dict_of_rules['FUEL']['needed']:
        still_need[molecule.element] = molecule.quantity

    while len(still_need) > 0:
        # print(f"We still need {len(still_need)} molecules: {still_need.items()}")

        required_elem, required_quantity = still_need.popitem(last=False)

        # print(f"Let's manufacture {required_quantity} {required_elem}...")

        spare_capacity = unneeded_produced[required_elem]
        if spare_capacity > 0:
            # print(f"We already have relevant leftovers: {spare_capacity}")

            if spare_capacity >= required_quantity:
                # print(f"Great, no need to produce any, just use the extra!")
                unneeded_produced[required_elem] -= required_quantity
                # print(f"Now we're left with {unneeded_produced[required_elem]}")
                continue
            else:
                required_quantity -= spare_capacity
                unneeded_produced[required_elem] = 0
                # print(f"Thanks to excess we only need to produce {required_quantity}")

        production_rule = dict_of_rules[required_elem]
        multiples_required = math.ceil(required_quantity / production_rule["produced"])
        overproduction = (multiples_required * production_rule["produced"]) - required_quantity
        # print(f"We have no choice but to produce {overproduction} unnecessary molecules")
        unneeded_produced[required_elem] += overproduction
        # print(f"We now have {unneeded_produced[required_elem]} stored excess of {required_elem}")

        # print(f"To produce {required_quantity} {required_elem} we will need {multiples_required} "
        #       f"X {production_rule['needed']}")

        for molecule in production_rule["needed"]:
            if molecule.element == "ORE":
                ore_required += multiples_required * molecule.quantity
                # print(f"Adding {multiples_required * molecule.quantity} ORE")
                continue

            # print(f"Adding to our list: {multiples_required * molecule.quantity} {molecule.element}")
            if molecule.element not in still_need:
                still_need[molecule.element] = 0
            still_need[molecule.element] = still_need[molecule.element] + multiples_required * molecule.quantity

    print(f"Total ORE required: {ore_required}")
    # print(f"Remaining excess: {unneeded_produced.items()}")


def part2():
    global ore_required
    global unneeded_produced

    fuel_produced = 0
    while ore_required < 1000000000000:
        part1()
        fuel_produced += 1
        if fuel_produced % 1000 == 0:
            print(f"Fuel Produced: {fuel_produced}  based on Ore: {ore_required}")

    print(f"Total Fuel Produced: {fuel_produced}  based on Ore: {ore_required}")


part2()
