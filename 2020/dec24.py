def translate(route):
    x, y, i = 0, 0, 0
    while i < len(route):
        if route[i] == 'e':
            x += 1
            i += 1
        elif route[i] == 'w':
            x -= 1
            i += 1
        elif route[i] == 'n' and route[i+1] == 'e':
            y += 1
            i += 2
        elif route[i] == 's' and route[i+1] == 'w':
            y -= 1
            i += 2
        elif route[i] == 'n' and route[i+1] == 'w':
            x -= 1
            y += 1
            i += 2
        elif route[i] == 's' and route[i+1] == 'e':
            x += 1
            y -= 1
            i += 2
    return (x, y)

def neighbor_coords(x, y):
    return ((x,y+1),(x+1,y),(x+1,y-1),(x,y-1),(x-1,y),(x-1,y+1))

class Tile:
    def __init__(self, route=None, coords=None):
        self.route = route
        if route is not None:
            self.coords = translate(route)
        else:
            self.coords = coords
        self.living = True

    def flip(self):
        self.living = not self.living

    def alive(self):
        return self.living

class TileSet:
    def __init__(self):
        self.tiles = dict()
        self.num_alive = 0

    def flip(self, tile):
        # print(f"flipping tile at {tile.coords}")
        if tile.coords in self.tiles:
            self.tiles[tile.coords].flip()
        else:
            self.tiles[tile.coords] = tile
        self.num_alive += 1 if self.tiles[tile.coords].alive() else -1

    def num_living_neighbors(self, x, y):
        num_living = 0
        for nc in neighbor_coords(x, y):
            if nc in self.tiles:
                num_living += 1 if self.tiles[nc].alive() else 0
        return num_living

    def iterate(self):
        next_gen = TileSet()
        evaluated = set()
        for coords in self.tiles:
            if not self.tiles[coords].alive():
                # neighbors of dead tiles won't come alive due to the dead tile
                # we may get to them (and this tile itself) later, due to other living neighbors
                pass
            check_coords = list(neighbor_coords(*coords))
            check_coords.append(coords)
            for check_coord in check_coords:
                if check_coord in evaluated:
                    continue
                nln = self.num_living_neighbors(*check_coord)                
                if check_coord in self.tiles and self.tiles[check_coord].alive() and nln in [1,2]:
                    next_gen.flip(Tile(coords=check_coord))
                if (check_coord not in self.tiles or not self.tiles[check_coord].alive()) and nln == 2:
                    next_gen.flip(Tile(coords=check_coord))
                evaluated.add(check_coord)
        self.tiles = next_gen.tiles
        self.num_alive = next_gen.num_alive



with open("dec24in.txt") as in_file:
    tiles = TileSet()

    for line in in_file:
        line = line.strip()
        tiles.flip( Tile(line) )

print(f"Part 1: Tile set has {tiles.num_alive} living tiles out of total {len(tiles.tiles)}")

for generation in range(100):
    tiles.iterate()
    print(tiles.num_alive)

print(f"Part 2: Tile set has {tiles.num_alive} living tiles out of total {len(tiles.tiles)}")