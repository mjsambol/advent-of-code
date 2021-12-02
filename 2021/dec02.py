position = {'x':0, 'y':0, 'aim': 0}

def forward(position, amount):
    position['x'] = position['x'] + amount
    position['y'] = position['y'] + amount * position['aim']

def up(position, amount):
    # position['y'] = position['y'] - amount
    position['aim'] = position['aim'] - amount        

def down(position, amount):
    # position['y'] = position['y'] + amount
    position['aim'] = position['aim'] + amount

movements = {'forward': forward, 'up': up, 'down': down}

with open("dec02in.txt") as in_file:
    for line in in_file:
        parts = line.split()
        movements[parts[0]](position, int(parts[1]))

print(position)
print(position['x'] * position['y'])
