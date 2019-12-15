import re
from math import gcd


class Moon:

    def __init__(self, x, y, z):
        self.pos = [int(x), int(y), int(z)]
        self.vel = [0, 0, 0]

    def apply_gravity(self, a_moon):
        for index in range(3):
            a = self.pos[index]
            b = a_moon.pos[index]

            if a == b:
                continue

            if a < b:
                self.vel[index] += 1
                a_moon.vel[index] -= 1
            else:
                self.vel[index] -= 1
                a_moon.vel[index] += 1

    def apply_velocity(self):
        for index in range(3):
            self.pos[index] = int(self.pos[index]) + int(self.vel[index])

    def get_pot_energy(self):
        return abs(self.pos[0]) + abs(self.pos[1]) + abs(self.pos[2])

    def get_kin_energy(self):
        return abs(self.vel[0]) + abs(self.vel[1]) + abs(self.vel[2])

    def get_tot_energy(self):
        return self.get_kin_energy() * self.get_pot_energy()

    def __repr__(self):
        return f"pos=<x={self.pos[0]}, y={self.pos[1]}, z={self.pos[2]}>, vel=<x={self.vel[0]}, y={self.vel[1]}, z={self.vel[2]}>"


def time_step(moons):
    num_moons = len(moons)

    for moon_index, a_moon in enumerate(moons):
        for other_moon_index in range(moon_index + 1, num_moons):
            # print(f"Updating moons {moon_index} and {other_moon_index}")
            other_moon = moons[other_moon_index]
            a_moon.apply_gravity(other_moon)

    for a_moon in moons:
        a_moon.apply_velocity()


def print_all(moons):
    tot_energy = 0
    for a_moon in moons:
        print(a_moon)
        tot_energy += a_moon.get_tot_energy()
    print(f"Total energy: {tot_energy}")


def read_input():
    moon_input_pat = re.compile(r"<x=(.+), y=(.+), z=(.+)>")
    moons = []

    infile = open("day12-in.txt")
    for line in infile:
        result = moon_input_pat.search(line)
        moon = Moon(result.group(1), result.group(2), result.group(3))
        moons.append(moon)
    return moons


def part1():
    moons = read_input()

    for i in range(1000):
        time_step(moons)
    print_all(moons)


def lowest_common_multiple(x, y):
    return x * y // gcd(x, y)


def part2():
    moons = read_input()
    x_sync, y_sync, z_sync = 0, 0, 0

    for i in range(1000000):
        time_step(moons)
        if x_sync == 0 and 0 == moons[0].vel[0] == moons[1].vel[0] == moons[2].vel[0] == moons[3].vel[0]:
            print(f"All four moons have x velocity 0 at iteration {i+1}")
            x_sync = i + 1
        if y_sync == 0 and 0 == moons[0].vel[1] == moons[1].vel[1] == moons[2].vel[1] == moons[3].vel[1]:
            print(f"All four moons have Y velocity 0 at iteration {i+1}")
            y_sync = i + 1
        if z_sync == 0 and 0 == moons[0].vel[2] == moons[1].vel[2] == moons[2].vel[2] == moons[3].vel[2]:
            print(f"All four moons have Z velocity 0 at iteration {i+1}")
            z_sync = i + 1

        if x_sync > 0 and y_sync > 0 and z_sync > 0:
            all_sync = lowest_common_multiple(lowest_common_multiple(x_sync, y_sync), z_sync)
            print(f"Lowest common multiple of syncrhonized periods is {all_sync}")
            print(f"Solution is 2 * that: {2 * all_sync}")
            break


part2()
