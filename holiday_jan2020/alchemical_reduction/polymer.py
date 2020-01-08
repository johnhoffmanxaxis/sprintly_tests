
def print_polymer(polymer_list, location, max_width=16):
    polymer = ''.join(polymer_list)

    begin = max([0, int(location - max_width / 2)])
    end = min([len(polymer), int(location + max_width / 2)])

    offset = 0

    line = ''
    if begin > 0:
        line = line + f'...'
        offset += len(line)


    line = line + polymer[begin:location]
    line += '('
    line += polymer[location:location+2]
    line += ')'
    line += polymer[location+2:end]

    if end < len(polymer):
        line += '...'

    print(line)


def react(polymer):
    if len(polymer) == 0:
        return polymer

    for i in range(len(polymer) - 1):
        p1 = polymer[i]
        p2 = polymer[i+1]

        if p1.lower() == p2.lower() and p1 != p2:
            #print_polymer(polymer, i)
            polymer.pop(i)
            polymer.pop(i)

            return polymer, True

    return polymer, False

if __name__ == '__main__':
    import sys

    polymer_txt = sys.stdin.read().rstrip().lstrip()

    polymer = [c for c in polymer_txt]

    did_react = True

    reaction_no = 1
    while did_react:
        polymer, did_react = react(polymer)
        reaction_no += 1

    print(len(polymer), "is the length of the reacted polymer")

    units = set(polymer_txt.lower())

    for unit_to_remove in units:
        bad_units = {unit_to_remove, unit_to_remove.upper()}

        polymer = [c for c in polymer_txt if c not in bad_units]
        did_react = True
        while did_react:
            polymer, did_react = react(polymer)

        print(f"Without unit '{bad_units}', reacted polymer length is {len(polymer)}")


