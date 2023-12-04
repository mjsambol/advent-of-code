import re
cards = []
p1_total = 0
with open("dec04in.txt") as my_input:
    for line in my_input:
        winning_str, have_str = line[line.index(': ') + 2:].split("|")
        winning = set(int(x) for x in re.split("\s+", winning_str.strip()))
        have = set(int(x) for x in re.split("\s+", have_str.strip()))
        cards.append({"card_num":len(cards)+1, "winning":winning, "have":have, "won":len(winning.intersection(have))})
        p1_total += pow(2, len(winning.intersection(have)) - 1) if len(winning.intersection(have)) > 0 else 0

for card in cards:
    for i in range(card["won"]):
        cards.append(cards[card["card_num"] + i])

print(p1_total)
print(len(cards))