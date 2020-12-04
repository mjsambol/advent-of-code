from collections import Counter

class Rule:
    def __init__(self, text):
        parts = text.split(' ')
        char_range = parts[0].split('-')
        self.min = int(char_range[0])
        self.max = int(char_range[1])
        self.letter = parts[1]

    def evaluate(self, text):
        c = Counter(text)
        return c[self.letter] >= self.min and c[self.letter] <= self.max

    def evaluate2(self, text):
        return ((text[self.min] == self.letter and text[self.max] != self.letter) or
                (text[self.min] != self.letter and text[self.max] == self.letter))

def read_input():
    passwords = []

    with open("dec02in.txt") as in_file:
        for line in in_file:
            parts = line.split(':')
            rule = Rule(parts[0].strip())
            passwords.append((rule, parts[1]))

    return passwords

passwords = read_input()
num_valid_p1 = 0
num_valid_p2 = 0
for password in passwords:
    if password[0].evaluate(password[1]):
        num_valid_p1 += 1
    if password[0].evaluate2(password[1]):
        num_valid_p2 += 1

print ("Num valid_1 passwords: " + str(num_valid_p1))
print ("Num valid_2 passwords: " + str(num_valid_p2))

