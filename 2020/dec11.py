from collections import Counter

def read_input():
    board = []
    with open("dec11in.txt") as in_file:
        for line in in_file:
            row = list(line.strip())
            board.append(row)
    return board

def next_gen_2(board, row, col):
    curr = board[row][col]
    neighbors = 0

    # up & left:
    r = row - 1
    c = col - 1
    while r >= 0 and c >= 0 and board[r][c] == '.':
        r = r - 1
        c = c - 1
    if r >= 0  and c >= 0 and board[r][c] == '#':
        neighbors += 1

    # up 
    r = row - 1
    c = col
    while r >= 0 and board[r][c] == '.':
        r = r - 1
    if r >= 0 and board[r][c] == '#':
        neighbors += 1

    # up & right:
    r = row - 1
    c = col + 1
    while r >= 0 and c <= len(board[0]) - 1 and board[r][c] == '.':
        r = r - 1
        c = c + 1
    if r >= 0  and c <= len(board[0]) - 1 and board[r][c] == '#':
        neighbors += 1


    # left:
    r = row
    c = col - 1
    while c >= 0 and board[r][c] == '.':
        c = c - 1
    if c >= 0 and board[r][c] == '#':
        neighbors += 1

    # right:
    r = row
    c = col + 1
    while r >= 0 and c <= len(board[0])-1 and board[r][c] == '.':
        c = c + 1
    if r >= 0  and c <= len(board[0])-1 and board[r][c] == '#':
        neighbors += 1


    # down & left:
    r = row + 1
    c = col - 1
    while r <= len(board)-1 and c >= 0 and board[r][c] == '.':
        r = r + 1
        c = c - 1
    if r <= len(board)-1 and c >= 0 and board[r][c] == '#':
        neighbors += 1

    # down
    r = row + 1
    c = col
    while r <= len(board)-1 and board[r][c] == '.':
        r = r + 1
    if r <= len(board)-1 and board[r][c] == '#':
        neighbors += 1

    # down & right:
    r = row + 1
    c = col + 1
    while r <= len(board)-1 and c <= len(board[0])-1 and board[r][c] == '.':
        r = r + 1
        c = c + 1
    if r <= len(board)-1  and c <= len(board[0])-1 and board[r][c] == '#':
        neighbors += 1

    if curr == 'L' and neighbors == 0:
        return '#'
    if curr == '#' and neighbors >= 5:
        return 'L'
    return curr


def next_gen_1(board, row, col):
    curr = board[row][col]
    neighbors = 0
    if row == 0:
        neighbors += (board[1][col] == '#')
        if len(board[0]) - 1 > col > 0 :
            neighbors += (board[0][col-1] == '#')
            neighbors += (board[0][col+1] == '#')
            neighbors += (board[1][col-1] == '#')
            neighbors += (board[1][col+1] == '#')
        elif col == 0:
            neighbors += (board[0][1] == '#')
            neighbors += (board[1][col+1] == '#')
        else:
            neighbors += (board[0][col-1] == '#')
            neighbors += (board[1][col-1] == '#')
    elif row == (len(board) - 1):
        neighbors += (board[row-1][col] == '#')
        if len(board[0]) - 1 > col > 0 :
            neighbors += (board[row][col-1] == '#')
            neighbors += (board[row][col+1] == '#')
            neighbors += (board[row-1][col-1] == '#')
            neighbors += (board[row-1][col+1] == '#')
        elif col == 0:
            neighbors += (board[row][1] == '#')
            neighbors += (board[row-1][col+1] == '#')
        else:
            neighbors += (board[row][col-1] == '#')
            neighbors += (board[row-1][col-1] == '#')
    else:
        neighbors += (board[row-1][col] == '#')
        neighbors += (board[row+1][col] == '#')
        if col == 0:
            neighbors += (board[row][col+1] == '#')
            neighbors += (board[row-1][col+1] == '#')
            neighbors += (board[row+1][col+1] == '#')
        elif col == (len(board[0]) - 1):
            neighbors += (board[row][col-1] == '#')
            neighbors += (board[row-1][col-1] == '#')
            neighbors += (board[row+1][col-1] == '#')
        else:
            # print(f"{row},{col}")
            # print(board[row])
            # print(board[row][col])
            neighbors += (board[row][col+1] == '#')
            neighbors += (board[row-1][col+1] == '#')
            neighbors += (board[row+1][col+1] == '#')
            neighbors += (board[row][col-1] == '#')
            neighbors += (board[row-1][col-1] == '#')
            neighbors += (board[row+1][col-1] == '#')

    if curr == 'L' and neighbors == 0:
        return '#'
    if curr == '#' and neighbors >= 4:
        return 'L'
    return curr

def run_round(board, next_gen):
    new_board = []
    num_changes = 0
    for row_num, row in enumerate(board):
        new_row = []
        new_board.append(new_row)
        for cell_num, cell in enumerate(row):
            new_cell = next_gen(board, row_num, cell_num)
            new_row.append(new_cell)
            if new_cell != cell:
                num_changes += 1

    return (new_board, num_changes)


for algo in [next_gen_1, next_gen_2]:
    board = read_input()

    while True:
        board, changes = run_round(board, algo)
        print(f"{changes} changes")
        if changes == 0:
            break

    c = Counter()
    for row in board:
        c.update(row)
    print(f"total occupied seats: {c['#']}\n\n")