import re

robots = []
board_dim = (101,103)
#board_dim = (11,7)  # x,y

def make_board(part):
    board = []
    for r in range(board_dim[1]):
        row = []
        for c in range(board_dim[0]):
            robots_present = sum([1 if robot[0][1] == r and robot[0][0] == c else 0 for robot in robots])
            row.append((robots_present if robots_present > 0 else '.') if part==1 else ('1' if robots_present else ' '))
        board.append(row)
    return board


def print_board(b):
    for row in b:
        print(''.join([str(c) if c != 0 else ' ' for c in row]))


with open("dec14.in") as infile:
    for line in infile:
        p, v = line.strip().split(' ')
        robots.append(([int(i) for i in p.split('=')[1].split(',')], [int(i) for i in v.split('=')[1].split(',')]))

    for rob in robots:
        rob[0][0] = (rob[0][0] + 100 * rob[1][0]) % board_dim[0]
        rob[0][1] = (rob[0][1] + 100 * rob[1][1]) % board_dim[1]

    board = make_board(1)
    mid_row = board_dim[1] // 2
    mid_col = board_dim[0] // 2
    quadrant_1 = sum([sum([0 if c == '.' else int(c) for row in board[0:mid_row] for c in row[0:mid_col]])])
    quadrant_2 = sum([sum([0 if c == '.' else int(c) for row in board[0:mid_row] for c in row[mid_col+1:]])])
    quadrant_3 = sum([sum([0 if c == '.' else int(c) for row in board[mid_row+1:] for c in row[0:mid_col]])])
    quadrant_4 = sum([sum([0 if c == '.' else int(c) for row in board[mid_row+1:] for c in row[mid_col+1:]])])
    print(quadrant_1 * quadrant_2 * quadrant_3 * quadrant_4)

    for i in range(10000):
        for rob in robots:
            rob[0][0] = (rob[0][0] + rob[1][0]) % board_dim[0]
            rob[0][1] = (rob[0][1] + rob[1][1]) % board_dim[1]

        if i % 100 == 0:
            print(f" #### {i} ####\n")

        b = make_board(2)
        if sum([1 if re.search(r'\d{4}', ''.join(row)) else 0 for row in b]) > 5:
            print(f" #### {i} ####\n")
            print_board(b)
            print("\n\n\n")
