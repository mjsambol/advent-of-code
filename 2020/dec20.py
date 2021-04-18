from collections import Counter

class Transformation: 

    def __init__(self):
        self.ops = []

    def rotate(self):
        self.ops.append("R")
        return self

    def flip_horizontally(self):
        self.ops.append("H")
        return self

    def flip_vertically(self):
        self.ops.append("V")
        return self

    def make_compatible_with(self, other):
        if len(self.ops) == 0:
            self.ops.extend(other.ops)
            return True

        if len(other.ops) == 0:
            return True

        if len(self.ops) != len(other.ops):
            return False

        for i in range(len(self.ops)):
            if self.ops[i] != other.ops[i]:
                return False

        return True

    def needed(self):
        return len(self.ops) > 0

    def run(self, data):
        dim = len(data)

        for op in self.ops:
            new_data = [[None for c in row] for row in data]
            for r in range(dim):
                for c in range(dim):
                    if op == 'V':
                        new_data[r][c] = data[dim-1-r][c]
                    elif op == 'H':
                        new_data[r][c] = data[r][dim-1-c]
                    elif op == 'R':
                        new_data[r][c] = data[dim-1-c][r]

            data = new_data
        
        return data

class Tile:
    TOP_FWD,TOP_BWD,RT_FWD,RT_BWD,BOT_FWD,BOT_BWD,LT_FWD,LT_BWD = 0,1,2,3,4,5,6,7
    TILE_DIRS = (TOP_FWD, TOP_BWD, RT_FWD, RT_BWD, BOT_FWD, BOT_BWD, LT_FWD, LT_BWD)
    TILE_DIR_PAIRS = ((TOP_FWD,TOP_BWD), (RT_FWD,RT_BWD), (BOT_FWD,BOT_BWD), (LT_FWD,LT_BWD))

    def __init__(self, name, data):
        self.name = name
        self.data = data

        # a dict of key = min(fwd_fingerprint, bwd_fingerprint), and value=other Tile with this edge
        self.edge_matches = dict()

        # a list of edges known in advance to be on the border of the enclosing picture, unordered
        self.on_picture_edge = []  

        self.oriented = False

        self.make_edge_pairs()


    def make_edge_pairs(self):
        top_as_bits = ''.join(self.data[0]).replace('#','1').replace('.','0')
        bottom_as_bits = ''.join(self.data[-1]).replace('#','1').replace('.','0')
        left_as_bits = ''.join([r[0] for r in self.data]).replace('#','1').replace('.','0')
        right_as_bits = ''.join([r[-1] for r in self.data]).replace('#','1').replace('.','0')

        self.fingerprints = dict()
        self.fingerprints[Tile.TOP_FWD] = int(top_as_bits, 2)
        self.fingerprints[Tile.TOP_BWD] = int(top_as_bits[::-1], 2)
        self.fingerprints[Tile.BOT_FWD] = int(bottom_as_bits, 2)
        self.fingerprints[Tile.BOT_BWD] = int(bottom_as_bits[::-1], 2)
        self.fingerprints[Tile.LT_FWD] = int(left_as_bits, 2)
        self.fingerprints[Tile.LT_BWD] = int(left_as_bits[::-1], 2)
        self.fingerprints[Tile.RT_FWD] = int(right_as_bits, 2)
        self.fingerprints[Tile.RT_BWD] = int(right_as_bits[::-1], 2)

        self.edge_pairs = dict()
        self.edge_pairs[self.fingerprints[Tile.TOP_FWD]] = self.fingerprints[Tile.TOP_BWD]
        self.edge_pairs[self.fingerprints[Tile.TOP_BWD]] = self.fingerprints[Tile.TOP_FWD]
        self.edge_pairs[self.fingerprints[Tile.BOT_FWD]] = self.fingerprints[Tile.BOT_BWD]
        self.edge_pairs[self.fingerprints[Tile.BOT_BWD]] = self.fingerprints[Tile.BOT_FWD]
        self.edge_pairs[self.fingerprints[Tile.LT_FWD]] = self.fingerprints[Tile.LT_BWD]
        self.edge_pairs[self.fingerprints[Tile.LT_BWD]] = self.fingerprints[Tile.LT_FWD]
        self.edge_pairs[self.fingerprints[Tile.RT_FWD]] = self.fingerprints[Tile.RT_BWD]
        self.edge_pairs[self.fingerprints[Tile.RT_BWD]] = self.fingerprints[Tile.RT_FWD]


    def do_orientation(self, transform):

        self.data = transform.run(self.data)

        self.make_edge_pairs()

        self.oriented = True


    # passed a set of constraints indicating its neighbors in clockwise order from top 
    # as either fingerprint-pairs, the special object Picture.OUTSIDE, or None to indicate no constraint yet, 
    # if this tile can orient itself to match those neighbors it will, and then return True. 
    # Otherwise, return False.
    def orient(self, constraints):
        
        if self.oriented:
            return False

        top_transforms = {
            Tile.TOP_FWD: Transformation(),
            Tile.TOP_BWD: Transformation().flip_horizontally(),
            Tile.RT_FWD:  Transformation().rotate().rotate().rotate(),
            Tile.RT_BWD:  Transformation().flip_horizontally().rotate(),
            Tile.BOT_FWD: Transformation().flip_vertically(),
            Tile.BOT_BWD: Transformation().rotate().rotate(),
            Tile.LT_FWD:  Transformation().flip_vertically().rotate(),
            Tile.LT_BWD:  Transformation().rotate()
        }

        rt_transforms = {
            Tile.TOP_FWD: Transformation().rotate(),
            Tile.TOP_BWD: Transformation().flip_horizontally().rotate(),
            Tile.RT_FWD:  Transformation(),
            Tile.RT_BWD:  Transformation().flip_vertically(),
            Tile.BOT_FWD: Transformation().flip_vertically().rotate(),
            Tile.BOT_BWD: Transformation().rotate().rotate().rotate(),
            Tile.LT_FWD:  Transformation().flip_horizontally(),
            Tile.LT_BWD:  Transformation().rotate().rotate()
        }

        bot_transforms = {
            Tile.TOP_FWD: Transformation().flip_vertically(),
            Tile.TOP_BWD: Transformation().flip_horizontally(),
            Tile.RT_FWD:  Transformation().flip_vertically().rotate(),
            Tile.RT_BWD:  Transformation().rotate(),
            Tile.BOT_FWD: Transformation(),
            Tile.BOT_BWD: Transformation().rotate().rotate().rotate(),
            Tile.LT_FWD:  Transformation().rotate().rotate(),
            Tile.LT_BWD:  Transformation().flip_horizontally().rotate()
        }

        lt_transforms = {
            Tile.TOP_FWD: Transformation().flip_vertically().rotate(),
            Tile.TOP_BWD: Transformation().rotate().rotate().rotate(),
            Tile.RT_FWD:  Transformation().flip_horizontally(),
            Tile.RT_BWD:  Transformation().rotate().rotate(),
            Tile.BOT_FWD: Transformation().rotate(),
            Tile.BOT_BWD: Transformation().flip_horizontally().rotate(),
            Tile.LT_FWD:  Transformation(),
            Tile.LT_BWD:  Transformation().flip_vertically()
        }

        transformers = (top_transforms, rt_transforms, bot_transforms, lt_transforms)

        transform = Transformation()
        
        for direc in range(4):

            if constraints[direc] is not None:
                if constraints[direc] == Picture.OUTSIDE:
                    if len(self.on_picture_edge) == 0:
                        return False
                else:
                    if constraints[direc][0] not in self.fingerprints.values():
                        return False
                    
                    for d in Tile.TILE_DIRS:
                        if constraints[direc][0] == self.fingerprints[d]:
                            section_transform = transformers[direc][d]
                            if not transform.make_compatible_with(section_transform):
                                print("Constraints violated, returning false")
                                return False
                            break

        if transform.needed():
            self.do_orientation(transform)
            
        return True        

    def unmatched_edge(self):
        for f,b in Tile.TILE_DIR_PAIRS:
            edge = (self.fingerprints[f],self.fingerprints[b])
            if min(edge) not in self.edge_matches and max(edge) not in self.edge_matches and (min(edge),max(edge)) not in self.edge_matches:
                return edge

    def set_as_picture_edge(self, edge):
        if edge not in self.on_picture_edge and self.edge_pairs[edge] not in self.on_picture_edge:
            self.on_picture_edge.append(edge)
            self.edge_matches[edge] = None  # so that this edge won't be returned by 'unmatched_edge()'

    def is_corner(self):
        return len(self.on_picture_edge) == 2

    def matches(self, other_tile):
        if other_tile in self.edge_matches.values():
            return True
        
        for side in Tile.TILE_DIR_PAIRS:
            if self.fingerprints[side[0]] in other_tile.fingerprints.values():
                ordered_edge = (min(self.fingerprints[side[0]], self.fingerprints[side[1]]), max(self.fingerprints[side[0]], self.fingerprints[side[1]]))
                self.edge_matches[ordered_edge] = other_tile
                other_tile.edge_matches[ordered_edge] = self
                return True
        
        return False

    # return the pair of fingerprints which represent the edge of the tile 
    # which is opposite the one passed as edge_pair param
    def opposite(self, edge_pair):
        for index, direc in enumerate(Tile.TILE_DIR_PAIRS):
            if self.fingerprints[direc[0]] in edge_pair or self.fingerprints[direc[1]] in edge_pair:
                opposite_dir = Tile.TILE_DIR_PAIRS[(index + 2) % 4]
                return (self.fingerprints[opposite_dir[0]], self.fingerprints[opposite_dir[1]])


class Picture:

    OUTSIDE = object()

    def __init__(self, tiles):
        self.tiles = tiles
        self.corner_tiles = []
        self.edge_tiles = []

        all_fingerprints = dict()
        for tile in self.tiles.values():
            for edge_dir in tile.fingerprints:
                fingerprint = tile.fingerprints[edge_dir]
                if fingerprint in all_fingerprints:
                    all_fingerprints[fingerprint].append(tile.name)
                else:
                    all_fingerprints[fingerprint] = [tile.name]

        # at this point every 'fingerprint' (which represents a tile edge + direction) in the all_fingerprints dict
        # maps to either one or two tiles. If one, then that tile edge is on the outside border of the overall picture
        # if two, then those two tiles meet at this edge

        # some tiles have not just one edge on the outside border, but two. Those are the four corners.

        # border_counter = Counter()
        for key in all_fingerprints:
            if len(all_fingerprints[key]) == 1:
                # tell that tile which of its edges sit on the edge of the Picture
                tile_name = all_fingerprints[key][0]
                tile = self.tiles[tile_name]
                tile.set_as_picture_edge(key)
                if tile not in self.edge_tiles:
                    self.edge_tiles.append(tile)

        for tile in self.edge_tiles:
            # if tile has two edges on edge of the Picture, it's a corner
            if tile.is_corner() and tile not in self.corner_tiles:
                self.corner_tiles.append(tile)
#                self.edge_tiles.remove(tile)

        print(f"Num edges: {len(self.edge_tiles)}")

        self.dim = (len(self.edge_tiles) // 4) + 1
        self.pic = [[None for i in range(self.dim)] for i in range(self.dim)] 


    def make_frame(self):
        self.pic[0][0] = self.corner_tiles[0]
        self.edge_tiles.remove(self.pic[0][0])

        # top edge
        being_matched = self.pic[0][0]
        edge_to_match = being_matched.unmatched_edge()
        constraints = [Picture.OUTSIDE, None, None, edge_to_match]
        
        for i in range(1,self.dim):
            for e in self.edge_tiles:
                if e.orient(constraints):
                    being_matched.matches(e)
                    self.pic[0][i] = e
                    self.edge_tiles.remove(e)
                    constraints[3] = e.opposite(constraints[3])
                    being_matched = e
                    break

        # left edge
        being_matched = self.pic[0][0]
        edge_to_match = being_matched.unmatched_edge()  # there's only one left!
        constraints = [edge_to_match, None, None, Picture.OUTSIDE]
        
        for i in range(1,self.dim):
            for e in self.edge_tiles:
                if e.orient(constraints):
                    being_matched.matches(e)
                    self.pic[i][0] = e
                    self.edge_tiles.remove(e)
                    constraints[0] = e.opposite(constraints[0])
                    being_matched = e
                    break

    def fill_frame(self):
        for row in range(1,self.dim):
            tile_to_left = self.pic[row][0]
            left_edge_to_match = tile_to_left.unmatched_edge()  # there's only one left!

            for col in range(1,self.dim):
                tile_above = self.pic[row-1][col]
                top_edge_to_match = tile_above.unmatched_edge()  # there's only one left!
                constraints = [top_edge_to_match, None, None, left_edge_to_match]
                for t in self.tiles.values():
                    if t.orient(constraints):
                        t.matches(tile_above)
                        t.matches(tile_to_left)
                        self.pic[row][col] = t
                        left_edge_to_match = t.opposite(left_edge_to_match)
                        tile_to_left = t
                        break
                if self.pic[row][col] is None:
                    print(f"Uh oh, no match found for {row},{col}")            

        print("All done making the picture!")

    def trim_tile_borders(self):
        num_tiles_per_row = self.dim
        tile_width = len(self.pic[0][0].data)
        new_row_len = num_tiles_per_row * (tile_width - 2)

        self.trimmed_pic = [[None for i in range(new_row_len)] for j in range(new_row_len)]

        new_pic_row, new_pic_col = 0, 0
        ctr = Counter()

        for orig_pic_row in range(self.dim * tile_width):
            if orig_pic_row % tile_width == 0:
                continue  # ignore the top of the tile's frame
            if (orig_pic_row + 1) % tile_width == 0:
                continue  # ignore the bottom of the tile's frame
            for orig_pic_col in range(self.dim * tile_width):
                if orig_pic_col % tile_width == 0:
                    continue # ignore the left border of the tile's frame
                if (orig_pic_col + 1) % tile_width == 0:
                    continue # ignore the right border of the tile's frame

                tile_in_row = orig_pic_row // tile_width
                tile_in_col = orig_pic_col // tile_width
                tile = self.pic[tile_in_row][tile_in_col]
                tiles_row = orig_pic_row % tile_width
                tiles_col = orig_pic_col % tile_width
                self.trimmed_pic[new_pic_row][new_pic_col] = tile.data[tiles_row][tiles_col]
                new_pic_col += 1
                if new_pic_col == new_row_len:
                    ctr.update(self.trimmed_pic[new_pic_row])
                    new_pic_col = 0
                    new_pic_row += 1

        self.num_tot_waves = ctr['#']
        print(f"Total # waves: {self.num_tot_waves}")

    def is_snake_at(self, sea, row, col):
        for spot in [0,5,6,11,12,17,18,19]:
            if sea[row][col + spot] != '#':
                return False
        for leg in [1,4,7,10,13,16]:
            if sea[row+1][col + leg] != '#':
                return False
        return sea[row-1][col + 18] == '#'        

    def seek_snakes(self):
        # for each transformation of: reg, r1, r2, r3, H, V, Vr1, Hr1:
        transformations = [
            Transformation(), Transformation().rotate(), Transformation().rotate().rotate(),
            Transformation().rotate().rotate().rotate(), Transformation().flip_horizontally(),
            Transformation().flip_vertically(), Transformation().flip_horizontally().rotate(),
            Transformation().flip_vertically().rotate()
        ]
        for transform in transformations:
            print(f"Seeking snakes with transformation {transform.ops}")
            sea = transform.run(self.trimmed_pic)

            num_snakes = 0
            for row in range(1,len(sea)-1):
                for col in range(len(sea)-19):
                    if self.is_snake_at(sea, row, col):
                        print(f"Found a snake at {row},{col}")
                        num_snakes += 1

            print(f"Total snakes in this orientation: {num_snakes}")
            if num_snakes > 0:
                print(f"Total non-snake waves: {self.num_tot_waves - num_snakes * 15}")

with open("/home/moshe/git/adventofcode/2020/dec20in.txt") as in_file:
    curr_tile = 0
    data_buffer = []
    all_tiles = dict()
    
    for line in in_file:
        line = line.strip()
        if len(line) == 0:
            if len(data_buffer) > 0:
                t = Tile(curr_tile, data_buffer)
                all_tiles[t.name] = t
                data_buffer = []
            continue
        if line.startswith('Tile'):
            curr_tile = line[5:-1]
            continue
        data_buffer.append(line)

    t = Tile(curr_tile, data_buffer)
    all_tiles[t.name] = t


pic = Picture(all_tiles)

corners_total = 1
for c in pic.corner_tiles:
    corners_total = corners_total * int(c.name)

print(f"Part 1: {corners_total}")

pic.make_frame()
pic.fill_frame()
pic.trim_tile_borders()
print("done trimming")
pic.seek_snakes()