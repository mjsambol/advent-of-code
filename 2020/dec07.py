import regex

class Luggage:
    
    all_luggage_by_color = dict()

    def __init__(self, color):
        self.color = color
        self.can_hold = dict()
        self.held_by = []
        Luggage.all_luggage_by_color[color] = self

    def can_eventually_hold(self, child):
        if child in self.can_hold:
            return True
        for holdable_color in self.can_hold:
            holdable = Luggage.all_luggage_by_color[holdable_color]
            if holdable.can_eventually_hold(child):
                return True
        return False

    def total_contents(self):
        tot = 0
        for holdable_name in self.can_hold:
            holdable = Luggage.all_luggage_by_color[holdable_name]
            num_to_hold = self.can_hold[holdable_name]
            tot += num_to_hold * (1 + holdable.total_contents())
        return tot



rule_pat = r"(.+) bags contain (?:(\S+) (.+?) bags?,? ?)+." 

def read_input():

    with open("dec07in.txt") as in_file:

        for line in in_file:
            line = line.strip()
            if len(line) == 0:
                continue
            m = regex.match(rule_pat, line)
            luggage = Luggage(m.group(1))
            held_quantities = m.captures(2)
            held_names      = m.captures(3)
            for index, quantity in enumerate(held_quantities):
                if quantity == 'no':
                    continue
                luggage.can_hold[held_names[index]] = int(quantity)
            
            for other_luggage in Luggage.all_luggage_by_color.values():
                if other_luggage == luggage:
                    continue
                if luggage.color in other_luggage.can_hold:
                    luggage.held_by.append(other_luggage)


read_input()
shiny_gold_holders = 0
for l in Luggage.all_luggage_by_color.values():
    if l.can_eventually_hold('shiny gold'):
        shiny_gold_holders += 1
print(f"shiny gold holders: {shiny_gold_holders}")

shiny_gold = Luggage.all_luggage_by_color['shiny gold']
print(f"shiny gold contents: {shiny_gold.total_contents()}")