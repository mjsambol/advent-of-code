# Rock:     A  X
# Paper:    B  Y
# Scissors: C  Z
# 

def points_for_weapon(my_choice):
    if my_choice == 'A' or my_choice == 'X':
        return 1
    if my_choice == 'B' or my_choice == 'Y':
        return 2
    if my_choice == 'C' or my_choice == 'Z':
        return 3

def points_per_outcome(game_result):
    if game_result == 'LOSE':
        return 0
    if game_result == 'TIE':
        return 3
    if game_result == 'WIN':
        return 6

def get_game_outcome(her_move, my_move):
    if her_move == 'A' and my_move == 'X':
        return 'TIE'
    elif her_move == 'A' and my_move == 'Y':
        return 'WIN'
    elif her_move == 'A' and my_move == 'Z':
        return 'LOSE'
    elif her_move == 'B' and my_move == 'X':
        return 'LOSE'
    elif her_move == 'B' and my_move == 'Y':
        return 'TIE'
    elif her_move == 'B' and my_move == 'Z':
        return 'WIN'
    elif her_move == 'C' and my_move == 'X':
        return 'WIN'
    elif her_move == 'C' and my_move == 'Y':
        return 'LOSE'
    elif her_move == 'C' and my_move == 'Z':
        return 'TIE'


def part_1(her_move, my_move, my_total):

    my_total = my_total + points_for_weapon(my_move)  # chose rock
    outcome = get_game_outcome(her_move, my_move)
    my_total += points_per_outcome(outcome)   # we tied
        
    return my_total


def part_2(her_move, result, my_total):

    if her_move=='A' and result=='X':
        my_total = my_total + 3
        my_total += 0
    
    if her_move=='A' and result=='Y':
        my_total = my_total + 1
        my_total += 3
    
    if her_move=='A' and result=='Z':
        my_total = my_total + 2
        my_total += 6
    
    if her_move=='B' and result=='X':
        my_total = my_total + 1  # chose rock
    
    if her_move=='B' and result=='Y':
        my_total = my_total + 2
        my_total += 3   # we tied
    
    if her_move=='B' and result=='Z':
        my_total = my_total + 3
        my_total += 6
    
    if her_move=='C' and result=='X':
        my_total = my_total + 2
        my_total += 0
    
    if her_move=='C' and result=='Y':
        my_total = my_total + 3
        my_total += 3
    
    if her_move=='C' and result=='Z':
        my_total = my_total + 1
        my_total += 6
    
    return my_total




part_1_total = 0 
part_2_total = 0 

with open("dec02in.txt") as my_input:
    for line in my_input:
        line = line.strip()

        her_move, my_move = line.split(' ') 
        print("game: ", her_move, " ", my_move)
        part_1_total = part_1(her_move, my_move, part_1_total)
        part_2_total = part_2(her_move, my_move, part_2_total)

        print("total 1 is now ", part_1_total)
        print("total 2 is now ", part_2_total)


print("my winnings against that loser: ", part_1_total, " and ", part_2_total)
