board = []

with open("dec11in.txt") as in_file:
    for line in in_file.readlines():
        board.append([int(c) for c in line.strip()])

def print_board():
    for row in board:
        print(''.join([str(i) for i in row]))
    print()

def increment_neighbors(r, c):
    all_neighbors = [(r-1,c-1), (r-1,c), (r-1,c+1), (r,c-1), (r,c+1), (r+1,c-1), (r+1,c), (r+1,c+1)]
    for n in all_neighbors:
        if len(board) > n[0] >= 0 and len(board[0]) > n[1] >= 0:
            board[n[0]][n[1]] += 1


def do_step():
    flashed = [[0 for i in range(len(board))] for j in range(len(board))]
    for row in board:
        for col in range(len(row)):
            row[col] += 1

    found_flasher = True
    while found_flasher:
        found_flasher = False
        for row in range(len(board)):
            for col in range(len(board[0])):
                if board[row][col] > 9 and flashed[row][col] == 0:
                    found_flasher = True
                    flashed[row][col] = 1
                    increment_neighbors(row, col)
    
    num_flashes = 0
    for row in range(len(board)):
        for col in range(len(board[0])):
            if flashed[row][col]:
                num_flashes += 1
                board[row][col] = 0

    return num_flashes

tot_flashes = 0
for i in range(1,401):
    curr_flashes = do_step()
    tot_flashes += curr_flashes
    if curr_flashes == 100:
        print(f"**** 100 flashes on round {i}! ******");
        exit()
    if i % 10 == 0:
        if i == 100:
            print(f'step 100:  ===============')
        print(f'Flashes so far: {tot_flashes}')
