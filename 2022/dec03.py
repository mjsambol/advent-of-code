letter_vals=[None]
letter_vals.extend([chr(97+i) for i in range(26)])
letter_vals.extend([chr(65+i) for i in range(26)])

tot_overlaps,tot_priorities = 0,0

with open("dec03in.txt") as my_input:
    lines = [l.strip() for l in my_input.readlines()]
    for line in lines:
        fh,sh=line[:len(line)//2],line[len(line)//2:]
        overlap = set(fh).intersection(sh).pop()
        tot_overlaps += letter_vals.index(overlap)
    my_input.seek(0)
    for tstart in range(0,len(lines), 3):
        overlap = set(lines[tstart]).intersection(lines[tstart+1]).intersection(lines[tstart+2]).pop()
        tot_priorities += letter_vals.index(overlap)

print(tot_overlaps)
print(tot_priorities)