with open("dec09in.txt") as my_input:
    head_v_gap, head_h_gap = 0,0
    visited_coords =  {(0,0)}
    tail_x, tail_y = 0,0

    for line in my_input:
        direction, amount_str = line.strip().split()
        amount = int(amount_str)

        if direction in ['R','L']:
            magnitude = 1 if direction == 'R' else -1
            if head_h_gap == 0:
                if head_v_gap != 0 and amount > 1: # head above or below
                    tail_x += magnitude
                    tail_y += head_v_gap
                visited_coords.update([(x, tail_y) for x in range(tail_x, tail_x + magnitude * (amount - 1), magnitude)])
                tail_x += amount - 1
            else:
                if head_v_gap != 0: # head diagonally above or below
                    tail_x += magnitude
                    tail_y += head_v_gap
                visited_coords.update([(x, tail_y) for x in range(tail_x, tail_x + magnitude * (amount - 1), magnitude)])
                tail_x += amount
            head_h_gap = 1
            head_v_gap = 0
        else:  # travelling up or down
            magnitude = 1 if direction == 'U' else -1
            if head_v_gap == 0:
                if head_h_gap != 0 and amount > 1:  # head to R or L
                    tail_x += head_h_gap
                    tail_y += magnitude
                visited_coords.update([(tail_x, y) for y in range(tail_y, tail_y + magnitude * (amount - 1), magnitude)])
                tail_y += amount - 1
            else:
                if head_h_gap != 0:
                    tail_x += head_h_gap
                    tail_y += magnitude
                visited_coords.update([(tail_x, y) for y in range(tail_y, tail_y + magnitude * (amount - 1), magnitude)])
                tail_y += amount
            head_h_gap = 0
            head_v_gap = 1
        
        print(f"After move {direction} {amount}, tail is at {tail_x},{tail_y}")
        print(f"      and visited={visited_coords}")

