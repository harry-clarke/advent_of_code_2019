import math


def calc_fuel(mass): return math.floor(mass / 3) - 2


def calc_fuel_corrected(mass):
    fuel = calc_fuel(mass)
    if fuel <= 0:
        return 0

    return fuel + calc_fuel_corrected(fuel)


with open('input.txt') as f:
    s = f.readlines()
    total = 0
    total_corrected = 0
    for x in s:
        total += calc_fuel(int(x))
        total_corrected += calc_fuel_corrected(int(x))

    print('Answer 1: %s' % total)
    print('Answer 2: %s' % total_corrected)
