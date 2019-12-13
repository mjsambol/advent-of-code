# read input file

# each layer is 25 wide by 6 tall = 150 'pixels'

# for each layer, enter its digits into a Counter and check the number of zeros counted
# create a list with list[i] = # zeros in layer i
from collections import Counter

class Layer:

    def __init__(self, width, height, values):
        if len(values) != width * height:
            raise ValueError(f"Layer passed {len(values)} values; expecting {width} * {height}")
        self._width = width
        self._height = height
        self._values = values[:]
        self._digit_freqs = Counter(self._values)

    def get_vals(self):
        return self._values

    def get_freq(self, digit):
        return self._digit_freqs[digit]

    def get_pixel(self, row, col):
#        print(f"Layer.get_pixel({row},{col})={self._values[row * self._width + col]}")
#        print(f"from data: {self._values}")
        return self._values[row * self._width + col]

def getPixel(row, col, list_of_layers):
#    print(f"getPixel {row},{col}:")
    for lnum, layer in enumerate(list_of_layers):
        p = layer.get_pixel(row, col)
        if p != '2':
#            print(f"getPixel(r,c,l): returning {p} from row # {lnum}")
            return layer.get_pixel(row, col)

    return -1

list_of_layers = []
input = open("d8-in.txt")

while True:
    line = input.read(150)
    if line is None or line == '':
        break
    line = line.strip()
    if line is None or line == '':
        break
#    print(f"line is {line}")
    pixels = list(line)
#    print(f"size of list is {len(pixels)}")
    layer = Layer(25, 6, pixels)
    list_of_layers.append(layer)

sorted_layers = sorted(list_of_layers, key=lambda l: l.get_freq('0'))

layer_w_min_zeros = sorted_layers[0]

print(f"Layer w/min zeros has: {layer_w_min_zeros._digit_freqs}")

print(f"num_ones * num_twos is {layer_w_min_zeros._digit_freqs['1'] * layer_w_min_zeros._digit_freqs['2']}")

print("\n")
for row in range(6):
    r = ''
    for col in range(25):
        pixel = getPixel(row, col, list_of_layers)
        if pixel == '1':
            r = r + ' '
        else:
            r = r + '*'
    print(r)
print()
