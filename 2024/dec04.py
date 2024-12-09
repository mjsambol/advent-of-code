import re
with open("dec04.in") as infile:
    puzzle_txt = [line.strip() for line in infile]

height, width = len(puzzle_txt), len(puzzle_txt[0])
num_matches = 0
for line in puzzle_txt:
    num_matches += len(re.findall("XMAS", line))
    num_matches += len(re.findall("XMAS", line[::-1]))

for col in range(width):
    num_matches += len(re.findall("XMAS", ''.join([puzzle_txt[row][col] for row in range(height)])))
    num_matches += len(re.findall("XMAS", ''.join([puzzle_txt[row][col] for row in range(height-1,-1,-1)])))

r,c,wrap_from_r,wrap_from_c = 0,0,0,0
diagonal = ''
while not (r==height-1 and c==width-1):
    diagonal += puzzle_txt[r][c]
    if c == 0 or r == height - 1:
        num_matches += len(re.findall("XMAS", diagonal))
        num_matches += len(re.findall("XMAS", diagonal[::-1]))
        diagonal = ""
        if wrap_from_c < width - 1:
            r,c = wrap_from_r, wrap_from_c + 1
            wrap_from_r, wrap_from_c = r,c
        else:
            r,c = wrap_from_r + 1, wrap_from_c 
            wrap_from_r = r
    else:
        r,c = r+1, c-1

r,c,wrap_from_r,wrap_from_c = 0,width-1,0,width-1
diagonal = ''
while not (r==height-1 and c==0):
    diagonal += puzzle_txt[r][c]
    if c == width-1 or r == height - 1:
        num_matches += len(re.findall("XMAS", diagonal))
        num_matches += len(re.findall("XMAS", diagonal[::-1]))
        diagonal = ""
        if wrap_from_c > 0:
            r,c = wrap_from_r, wrap_from_c - 1
            wrap_from_r, wrap_from_c = r,c
        else:
            r,c = wrap_from_r + 1, wrap_from_c 
            wrap_from_r = r
    else:
        r,c = r+1, c+1

print(num_matches)

def get(r,c):
    if r < 0 or r >= height or c < 0 or c >= width:
        return ''
    return puzzle_txt[r][c]

num_p2_matches = 0
for r in range(height):
    for c in range(width):
        num_p2_matches += puzzle_txt[r][c] == 'A' and (
            ((get(r-1,c-1)=='M' and get(r+1,c+1) == 'S') or
            (get(r-1,c-1)=='S' and get(r+1,c+1) == 'M')) and
            ((get(r-1,c+1)=='M' and get(r+1,c-1) == 'S') or
            (get(r-1,c+1)=='S' and get(r+1,c-1) == 'M')))
print(num_p2_matches)