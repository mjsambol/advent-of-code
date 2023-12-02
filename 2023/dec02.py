import math

tot_poss, tot_pows = 0,0
colors = ['red', 'green', 'blue']

def get_rgb(part_arr):
    result = {color:0 for color in colors}
    for part in part_arr.split(','):
        n, c = part.strip().split(' ')
        result[c.strip()] += int(n)
    return result

with open("dec02in.txt") as my_input:
    for line in my_input:
        game, pulls = line.strip().split(':')
        game_id = int(game.split(' ')[1])
        parr = pulls.split(';')
        
        max_rgb = {color:0 for color in colors}
        fits = True
        for part in parr:
            rgb = get_rgb(part)
            max_rgb = {color: max(max_rgb[color], rgb[color]) for color in colors}
            fits = fits and rgb['red'] <= 12 and rgb['green'] <= 13 and rgb['blue'] <= 14
        tot_pows += math.prod([max_rgb[color] for color in colors])
        tot_poss += game_id if fits else 0

    print(f"Total possible: {tot_poss}. Total powers: {tot_pows}")