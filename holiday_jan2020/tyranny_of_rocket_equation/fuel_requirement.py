
def fuel_requirement(mass):
    return int(mass / 3.) - 2

def fuel_requirement_with_fuel(mass):
    total_fuel = 0.

    fuel = fuel_requirement(mass)
    total_fuel += fuel

    while fuel_requirement(fuel) > 0:
        fuel = fuel_requirement(fuel)
        total_fuel += fuel

    return total_fuel

if __name__ == '__main__':
    import sys
    import argparse

    parser = argparse.ArgumentParser(description='Compute fuel requirements')
    parser.add_argument('--all-fuel', action='store_true',
                        help='Compute total requirements (including fuel for your fuel)')

    args = parser.parse_args()
    total_fuel = 0.

    if args.all_fuel:
        for mass in sys.stdin:
            total_fuel += fuel_requirement_with_fuel(float(mass))
    else:
        for mass in sys.stdin:
            total_fuel += fuel_requirement(float(mass))

    print(f"Total fuel requirement: {total_fuel}")
