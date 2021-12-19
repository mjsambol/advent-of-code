from collections import defaultdict

class Paper:
    def __init__(self, dots) -> None:
        self.rows = defaultdict(lambda: [])
        for coord in dots:
            c,r = coord
            self.rows[r].append(c)
        self.height = max(self.rows.keys()) +1
        self.width = max([max(r) for r in self.rows.values()]) +1
        
    def fold(self, axis, where):
        if axis == 'y':
            for delta_y in range(1, self.height - where):
                row = set(self.rows[where + delta_y])
                add_to_row = set(self.rows[where - delta_y])
                self.rows[where - delta_y] = list(row | add_to_row)
            for y in range(where, self.height):
#                self.rows[y] = []
                if y in self.rows:
                    self.rows.pop(y)
            self.height = where
        else:
            for row in self.rows:
                new_row = [c for c in range(where) if c in self.rows[row] or (2 * where - c) in self.rows[row]]
                self.rows[row] = new_row
            self.width = where

    def getTotalDots(self):
        return sum([len(row) for row in self.rows.values()])

    def __str__(self) -> str:
        result = ''
        for row in sorted(self.rows.keys()):
            result = result + ''.join(['#' if c in self.rows[row] else '.' for c in range(self.width)]) + '\n'
        return result


page = None

with open("dec13in.txt") as in_file:
    dots = []
    for line in in_file.readlines():
        if line.find(',') > 0:
            r,c = map(int, line.split(','))
            dots.append((r,c))
        elif len(line.strip()) == 0:
            continue
        else:
            if page is None:
                page = Paper(dots)
            fold_instruction = line[11:].split('=')
            page.fold(fold_instruction[0], int(fold_instruction[1]))
            print(page.getTotalDots())

print(page)