import re

class NumRange:
    def __init__(self, start, end):
        self.start = start
        self.end = end

    def is_valid(self, val):
        return val >= self.start and val <= self.end


class TicketField:
    RULE_PAT = re.compile(r'(.+): (\d+)-(\d+) or (\d+)-(\d+)')

    def __init__(self, rule_text):
        m = TicketField.RULE_PAT.match(rule_text)
        self.name = m.group(1)
        self.ranges = []

        self.ranges.append( NumRange(int(m.group(2)), int(m.group(3))) )
        self.ranges.append( NumRange(int(m.group(4)), int(m.group(5))) )
        
    def is_valid_val(self, value):
        for r in self.ranges:
            if r.is_valid(value):
                return True
        return False


class FieldMapper:
    def __init__(self):
        self.all_fields = []
        self.fields_by_col = dict()

    def add_field(self, f):
        self.all_fields.append(f)

    def matching_fields(self, value):
        result = []
        for f in self.all_fields:
            if f.is_valid_val(value):
                result.append(f)
        return set(result)

    def num_cols(self):
        return len(self.all_fields)

    def fields_by_column(self, col_num):
        if col_num not in self.fields_by_col:
            self.fields_by_col[col_num] = set(self.all_fields)
        return self.fields_by_col[col_num]

    def update_column_fields(self, col_num, possible_fields):
        self.fields_by_col[col_num] = self.fields_by_column(col_num) & set(possible_fields)

    def simplify(self):
        simplified_fields = []

        while True:
            num_changes = 0
            for col in self.fields_by_col.keys():
                possible_fields = self.fields_by_col[col]
                if len(possible_fields) == 1:
                    # this is the only field this column can map to,
                    # so remove it as a possibility from the other columns
                    only_possible_field = list(possible_fields)[0]
                    if only_possible_field not in simplified_fields:
                        for col2 in self.fields_by_col.keys():
                            if col2 != col and only_possible_field in self.fields_by_col[col2]:
                                self.fields_by_col[col2].remove(only_possible_field)
                                num_changes += 1
                        simplified_fields.append(only_possible_field)
            if num_changes == 0:
                break

sum_invalid = 0
field_mapper = FieldMapper()
my_ticket = []

def read_input():
    with open("/home/msambol/git/adventofcode/2020/dec16in.txt") as in_file:
        section_parser = rules_parser
        for line in in_file:
            line = line.strip()
            if len(line) == 0:
                continue
            if line.startswith('your ticket'):
                section_parser = my_ticket_parser
                continue
            if line.startswith('nearby tickets'):
                section_parser = other_ticket_parser
                continue

            section_parser(line)


def rules_parser(line):
    field_mapper.add_field(TicketField(line))

def my_ticket_parser(line):
    global my_ticket
    my_ticket = [int(i) for i in line.split(',')]
    print(f"My ticket: {my_ticket}")

def other_ticket_parser(line):
    global sum_invalid

    ticket_vals = line.split(',')
    all_valid = True
    possible_fields = []

    for t in ticket_vals:
        matching_fields = field_mapper.matching_fields(int(t))
        if len(matching_fields) == 0:
            print(f"Invalid: {t}")
            sum_invalid += int(t)
            all_valid = False
        else:
            possible_fields.append(matching_fields)

    if all_valid:
        for i,mf in enumerate(possible_fields):
            field_mapper.update_column_fields(i, mf)

read_input()
print(f"Part 1: {sum_invalid}")

field_mapper.simplify()
part2 = 1

for i in range(field_mapper.num_cols()):
    field_name = field_mapper.fields_by_column(i).pop().name
    print(f"column {i}: possible fields: {field_name}")
    if field_name.startswith('departure'):
        part2 *= my_ticket[i]

print(f"Part 2: {part2}")

