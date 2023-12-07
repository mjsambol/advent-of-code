def get_hand_type(hand, part):
    number_of_each_card = {'J':0}
    
    for card in hand:
#        print(f"Checking what we know about {card}")
        if card not in number_of_each_card:
#            print("We haven't seen it yet")
            number_of_each_card[card] = 1
        else:
#            print("We have already seen it")
            number_of_each_card[card] = number_of_each_card[card] + 1

#    print(number_of_each_card)

    how_many_pairs = 0
    how_many_triplets = 0
    how_many_jokers = 0 if part==1 else number_of_each_card['J']

    for card in number_of_each_card:
        if part == 2 and card == 'J':
            continue
        if number_of_each_card[card] + how_many_jokers == 5:
            return "Five of a kind"
        elif number_of_each_card[card] + how_many_jokers == 4:
            return "Four of a kind"
        elif number_of_each_card[card] == 3:
            how_many_triplets = how_many_triplets + 1
        elif number_of_each_card[card] == 2:
            how_many_pairs = how_many_pairs + 1

    if part == 2:
        # special case that got ignored above:
        if how_many_jokers == 5:
            return "Five of a kind"
        
        if how_many_jokers == 2:
            if how_many_pairs == 1:
                return "Full house"
            return "Three of a kind"
        elif how_many_jokers == 1:
            if how_many_pairs == 2:
                return "Full house"
            elif how_many_pairs == 1:
                return "Three of a kind"
            else:
                return "One pair"

    if how_many_triplets == 1:
        if how_many_pairs == 1:
            return "Full house"
        else:
            return "Three of a kind"

    if how_many_pairs == 2:
        return "Two pair"
    elif how_many_pairs == 1:
        return "One pair"

    return "High card"           
            
def get_card_tziyun_common(card, ordering):
    tziyun =1
    for letter in card["hand"]:
        tziyun = tziyun * 100 + ordering.index(letter)
    card['tziyun'] = tziyun
    return tziyun

def get_card_tziyun(card):
    card_ordering = ['A', 'K', 'Q', 'J', 'T', '9', '8', '7', '6', '5', '4', '3', '2']
    return get_card_tziyun_common(card, card_ordering)

def get_card_tziyun_part2(card):
    card_ordering = ['A', 'K', 'Q', 'T', '9', '8', '7', '6', '5', '4', '3', '2', 'J']
    return get_card_tziyun_common(card, card_ordering)


def sort_the_hands(hands, part):
    sorted_list = []
    same_kind_list = []

    kinds_of_hands = ["Five of a kind", "Four of a kind", "Full house", "Three of a kind", "Two pair", "One pair", "High card"]

    for kind in kinds_of_hands:
        for pair in hands:
            if pair["type"] == kind:
                same_kind_list.append(pair)

        key = get_card_tziyun if part == 1 else get_card_tziyun_part2
        same_kind_list = sorted(same_kind_list, key=key)

        sorted_list.extend(same_kind_list)
        same_kind_list = []

    # for pair in hands:
    #     if pair["type"] == "Four of a kind":
    #         sorted_list.append(pair["hand"])
    
    # for pair in hands:
    #     if pair["type"] == "Full house":
    #         sorted_list.append(pair["hand"])

    # for pair in hands:
    #     if pair["type"] == "Three of a kind":
    #         sorted_list.append(pair["hand"])

    # for pair in hands:
    #     if pair["type"] == "Two pair":
    #         sorted_list.append(pair["hand"])

    # for pair in hands:
    #     if pair["type"] == "One pair":
    #         sorted_list.append(pair["hand"])

    # for pair in hands:
    #     if pair["type"] == "High card":
    #         sorted_list.append(pair["hand"])

    return sorted_list


with open("dec07in.txt") as my_input:
    all_lines = my_input.readlines()

for part in (1,2):    
    all_the_hands = []

    for line in all_lines:
        hand, bid = line.strip().split(' ')
 #       print(f"Got this hand: {hand}")
        hand_type = get_hand_type(hand, part)
#        print(f"the hand's type is {hand_type}")
        all_the_hands.append( {"hand":hand, "bid": int(bid), "type":hand_type} )

#    print(all_the_hands)

    print(f"Part {part}:")

    sorted_hands = sort_the_hands(all_the_hands, part)
    print("\nI reorded them for you. Now they look like this:")
#    print(sorted_hands)

    top_rank = len(sorted_hands)
    total = 0
    current_rank = top_rank

    for hand in sorted_hands:
        print(f'{hand} adds {current_rank * hand["bid"]} to the total')
        total = total + current_rank * hand["bid"]
        current_rank = current_rank - 1

    print(total)