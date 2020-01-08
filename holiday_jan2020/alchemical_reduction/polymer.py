
def print_polymer(polymer_list, location, max_width=16):
    """
    Just a silly visualization for a single polymer reaction
    """

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


def single_reaction(polymer):
    """
    Find the first pair of matching units with opposite polarity,
    delete them from the polymer, and return the reacted polymer

    Inputs
    ------
    polymer: list of str
        The polymer represented as a list of characters

    Returns
    -------
    polymer: list of str
        Polymer without the reacted units
    had_a_reaction: bool
        Whether or not the polymer underwent a reaction
    """

    if len(polymer) == 0:
        return polymer

    for i in range(len(polymer) - 1):
        p1 = polymer[i]
        p2 = polymer[i+1]

        if p1.lower() == p2.lower() and p1 != p2:
            #print_polymer(polymer, i)

            # remove units that reacted
            polymer.pop(i)
            polymer.pop(i)

            return polymer, True

    return polymer, False

def full_reaction(polymer):
    """
    Fully react a polymer

    Input
    -----
    polymer: list of str
        Polymer represented as a list of characters

    Output
    ------
    reacted_polymer: list of str
        The polymer after being fully reacted

    """
    did_react = True

    while did_react:
        polymer, did_react = single_reaction(polymer)

    return polymer

if __name__ == '__main__':
    import sys

    # read polymer from stdin
    polymer_txt = sys.stdin.read().rstrip().lstrip()

    # convert to list
    polymer = [c for c in polymer_txt]

    reacted_polymer = full_reaction(polymer)
    print(len(reacted_polymer), "is the length of the reacted polymer")

    units = set(polymer_txt.lower())
    for unit_to_remove in units:
        bad_units = {unit_to_remove, unit_to_remove.upper()}

        polymer = [c for c in polymer_txt if c not in bad_units]
        reacted_polymer = full_reaction(polymer)
        print(f"Without unit '{bad_units}', reacted polymer length is {len(reacted_polymer)}")


