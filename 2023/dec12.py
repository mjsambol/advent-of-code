import re
import time

def make_pattern(numbers):
    pat = '^[\.\?]*'
    num_groups = numbers.split(',')
    for num_group in num_groups:
        pat = pat + f'[#\?]\u007b{int(num_group)}\u007d[\.\?]+?'
    return pat[:-8] + '[\.\?]*$'


# a mapping of a mappings:
# for each string of ? and # characters, holds a map of int x -> to an int representing the number of ways to represent that many # signs in the string
# e.g. for key "#??" returns {1:1, 2:1, 3:1} 

cache = {}  

def num_possibilities(symbols, numbers, pat):
    if not re.match(pat, symbols):
        return 0
    if '?' not in symbols:
        return 1
    first_qmark_pos = symbols.index('?')
    return (num_possibilities(symbols[0:first_qmark_pos] + '#' + symbols[first_qmark_pos+1:], numbers, pat) 
            + num_possibilities(symbols[0:first_qmark_pos] + '.' + symbols[first_qmark_pos+1:], numbers, pat))

with open("dec12in.txt") as in_txt:
    tot_p1_arrangements = tot_p2_arrangements = row = 0
    for line in in_txt:
        symbols, numbers = line.strip().split(' ')
        pat = make_pattern(numbers)
        tot_p1_arrangements += num_possibilities(symbols, numbers, pat)
        p2s = symbols + '?' + symbols + '?' + symbols + '?' + symbols + '?' + symbols
        p2n = numbers + ',' + numbers + ',' + numbers + ',' + numbers + ',' + numbers
        p2p = make_pattern(p2n)
        tot_p2_arrangements += num_possibilities(p2s, p2n, p2p)
        row = row + 1
        print(f"{row}: {tot_p1_arrangements}, {tot_p2_arrangements}")
        time.sleep(3)

    print(tot_p1_arrangements)
    print(tot_p2_arrangements)