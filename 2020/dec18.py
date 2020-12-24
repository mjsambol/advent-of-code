from operator import add,sub,mul,truediv

# a solution to https://adventofcode.com/2020/day/18

class Statement:
    def __init__(self):
        self.operator = None
        self.operand1 = None
        self.operand2 = None

    def add_operand(self, op):
        if self.operand1 is None:
            self.operand1 = op
        else:
            if self.operand2 is None:
                self.operand2 = op
            else:  # only relevant for part 2
                self.operand2.add_operand(op)

    def ready(self):
        return self.operand1 is not None and self.operand2 is not None and self.operator is not None

    def value(self):
        return self.operator(self.operand1.value(),self.operand2.value())

class Num:
    def __init__(self, val):
        self.val = float(val)

    def ready(self):
        return True

    def value(self):
        return self.val

class ParenGroup:
    def __init__(self, content):
        self.content = content[1:-1]  # strip off enclosing parentheses
        self.val = parse(self.content)

    def value(self):
        return self.val

known_operators = {
    '+':add,
    '-':sub,
    '*':mul,
    '/':truediv
}

def parse(line):
    chunks = line.strip().split(' ')
    token_index = 0
    statement = Statement()

    while token_index < len(chunks):
        chunk = chunks[token_index]
        if chunk.isnumeric():
            n = Num(chunk)
            statement.add_operand(n)
        elif chunk in known_operators:
            if statement.ready():
                s2 = Statement()
                s2.operator = known_operators[chunk]

                if part == 1 or chunk != '+':
                    s2.operand1 = statement
                    statement = s2
                else:
                    s2.operand1 = statement.operand2
                    statement.operand2 = s2
            else:
                statement.operator = known_operators[chunk]                    
        elif chunk.startswith('('):
            num_parens = 0
            parenthetical = []
            while token_index < len(chunks):
                num_parens += chunks[token_index].count('(')
                num_parens -= chunks[token_index].count(')')
                parenthetical.append(chunks[token_index])
                if num_parens == 0:
                    break
                token_index += 1
            pg = ParenGroup(' '.join(parenthetical))
            statement.add_operand(pg)
        else:
            print(f"Uh oh: unexpected: {chunk}")
            exit()

        token_index += 1
    
    return statement.value()


def process():
    total = 0
    with open("dec18in.txt") as in_file:

        for line in in_file:
            result = parse(line.strip())
            total += result
            print(result)

        print(total)

part = 1
#print(parse('1 + 2 * 3 + 4 * 5 + 6'))
process()
part = 2
# print(parse('1 + (2 * 3) + (4 * (5 + 6))'))
# print(parse('2 * 3 + (4 * 5)'))
# print(parse('5 + (8 * 3 + 9 + 3 * 4 * 3)'))
# print(parse('5 * 9 * (7 * 3 * 3 + 9 * 3 + (8 + 6 * 4))'))
# print(parse('((2 + 4 * 9) * (6 + 9 * 8 + 6) + 6) + 2 + 4 * 2'))
process()