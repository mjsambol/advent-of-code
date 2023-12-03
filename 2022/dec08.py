
tot_num_externally_vis = 0

def update_vis_from_outside(r,c,digits,vis):
    global tot_num_externally_vis
    if (r == 0 or r == len(digits)-1 or c == 0 or c == len(digits[0])-1 or
        (digits[r][c] > max(digits[r][0:c])) or
        (digits[r][c] > max(digits[r][c+1:])) or
        (digits[r][c] > max([digits[a_row][c] for a_row in range(r)])) or
        (digits[r][c] > max([digits[a_row][c] for a_row in range(r+1,len(digits))]))
        ):
        vis[r][c] = True
        tot_num_externally_vis += 1
        return

def outward_visibity(digits, r, c):
    left_vis,right_vis,top_vis,bot_vis = 0,0,0,0
    for leftwards in range(c-1,-1,-1):
        left_vis += 1
        if digits[r][leftwards] >= digits[r][c]:
            break
    for rightwards in range(c+1, len(digits[0])):
        right_vis += 1
        if digits[r][rightwards] >= digits[r][c]:
            break
    for upwards in range(r-1,-1,-1):
        top_vis += 1
        if digits[upwards][c] >= digits[r][c]:
            break
    for downwards in range(r+1, len(digits)):
        bot_vis += 1
        if digits[downwards][c] >= digits[r][c]:
            break

    return left_vis * right_vis * top_vis * bot_vis

with open("dec08in.txt") as my_input:

    digit_map = [[int(c) for c in line.strip()] for line in my_input.readlines()]
    inbound_visibility_map = [[False for col in row] for row in digit_map]
    [[update_vis_from_outside(r,c,digit_map,inbound_visibility_map) 
        for c in range(len(digit_map[r]))] 
        for r in range(len(digit_map))]
    print(f"Total externally visible: {tot_num_externally_vis}")

    max_outward_visibility = 0
    for row in range(len(digit_map)):
        for col in range(len(digit_map[row])):
            max_outward_visibility = max(max_outward_visibility, outward_visibity(digit_map, row, col))

    print(f"Max outward visibility: {max_outward_visibility}")

