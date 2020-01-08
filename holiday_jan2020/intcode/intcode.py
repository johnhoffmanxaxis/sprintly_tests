
# instruction opcodes
TERMINATE = 99
MULTIPLY = 2
ADD = 1

# parameter counts for each instruction opcode
PARAM_COUNT = {
        MULTIPLY: 3,
        ADD: 3,
        TERMINATE: 0
}

def execute(opcodes, pointer):
    """
    Execute operation located at pointer in memory

    Inputs
    ------
    opcodes: list of int
        The full memory of the program
    pointer: int
        The index to the instruction opcode we want to execute

    Returns
    -------
    opcodes: list of int
        The full memory of the program after the instruction execution
    terminated: bool
        Whether or not the program should terminate
    n_params: int
        The number of parameters consumed by this operation

    """
    instruction = opcodes[pointer]
    n_params = PARAM_COUNT[instruction]

    if instruction == TERMINATE:
        return opcodes, True, n_params

    a = opcodes[opcodes[pointer + 1]]
    b = opcodes[opcodes[pointer + 2]]
    result_address = opcodes[pointer + 3]

    opcodes[result_address] = {ADD: a + b,
                               MULTIPLY: a * b}[instruction]

    return opcodes, False, n_params


def run(program):
    """
    Run a full opcode program

    """
    pointer, terminate = 0, False

    while not terminate:
        program, terminate, n_params = execute(program, pointer)

        # move pointer by 1 (instruction) + n_params
        pointer += (n_params + 1)

    return program

if __name__ == '__main__':
    import sys
    import copy
    import argparse

    # One small step for man
    OUTPUT_VALUE = 19690720

    parser = argparse.ArgumentParser(description='intcode problem')
    parser.add_argument('--fix-fire', action='store_true')
    parser.add_argument('--find-inputs', action='store_true')

    args = parser.parse_args()

    original_opcodes = list(map(int, sys.stdin.read().rstrip().lstrip().split(',')))

    opcodes = copy.deepcopy(original_opcodes)
    if args.fix_fire:
        print("FIXING FIRE. REPLACING POSITION 1 WITH VALUE '12' AND POSITION 2 WITH VALUE '2'")
        opcodes[1] = 12
        opcodes[2] = 2

        result = run(opcodes)

        print("Resulting opcodes = ")
        print(result)

        print("OUTPUT: ", result[0])
        sys.exit()

    for i in range(100):
        for j in range(100):
            opcodes = copy.deepcopy(original_opcodes)
            opcodes[1] = i
            opcodes[2] = j
            result = run(opcodes)[0]
            if result == OUTPUT_VALUE:
                print(f"FOUND INPUTS THAT GIVE AN OUTPUT OF {OUTPUT_VALUE}")
                print(i, j)
                print("100 * noun + verb = ", 100 * i + j)


