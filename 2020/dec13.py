def read_input():
    with open("dec13in.txt") as in_file:
        lines = in_file.readlines()
        my_time = int(lines[0].strip())
        buses = [int(x) if x != 'x' else 0 for x in lines[1].strip().split(',')]
        return (my_time, buses)

me, buses = read_input()
print(f"I'm at {me} and buses are at:")
for i,e in enumerate(buses):
    print(f"{i}: {e}")

wait_time = 0
while True:
    for bus in buses:
        if bus == 0:
            continue
        if (me + wait_time) % bus == 0:
            print(f"Bus {bus} is best at {wait_time} after my arrival.")
            print(bus * wait_time)
            exit()
    wait_time += 1