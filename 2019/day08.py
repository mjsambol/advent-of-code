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

    def get_pixel(self, in_row, in_col):
        # print(f"Layer.get_pixel({in_row},{in_col})={self._values[in_row * self._width + in_col]}")
        # print(f"from data: {self._values}")
        return self._values[in_row * self._width + in_col]


def get_pixel(row, col):
    for in_layer in list_of_layers:
        p = in_layer.get_pixel(row, col)
        if p != '2':
            return in_layer.get_pixel(row, col)

    return -1


def print_layers():
    for row in range(6):
        r = ''
        for col in range(25):
            pixel = get_pixel(row, col)
            if pixel == '1':
                r = r + ' '
            else:
                r = r + '*'
        print(r)
    print()


list_of_layers = []
in_file = open("day08-in.txt")


while True:
    # each layer is 25 wide by 6 tall = 150 'pixels'
    line = in_file.read(150)
    if line is None or line.strip() == '':
        break
    line = line.strip()
    # print(f"line is {line}")
    pixels = list(line)
    # print(f"size of list is {len(pixels)}")
    layer = Layer(25, 6, pixels)
    list_of_layers.append(layer)

sorted_layers = sorted(list_of_layers, key=lambda l: l.get_freq('0'))

layer_w_min_zeros = sorted_layers[0]

print(f"Layer w/min zeros has: {layer_w_min_zeros._digit_freqs}")
print(f"num_ones * num_twos is {layer_w_min_zeros.get_freq('1') * layer_w_min_zeros.get_freq('2')}")
print("\n")

print_layers()
