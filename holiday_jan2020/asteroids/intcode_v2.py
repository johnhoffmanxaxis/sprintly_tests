# parameter modes
POSITION = 0
IMMEDIATE = 1

# instruction opcodes
TERMINATE = 99
ADD = 1
MULTIPLY = 2

# added in problem 5.1
INPUT = 3
OUTPUT = 4

# added in problem 5.2
JUMP_IF_TRUE = 5
JUMP_IF_FALSE = 6
LESS_THAN = 7
EQUALS = 8

# parameter counts for each instruction opcode
PARAM_COUNT = {
        MULTIPLY: 3,
        ADD: 3,
        TERMINATE: 0,
        INPUT: 1,
        OUTPUT: 1,
        JUMP_IF_TRUE: 2,
        JUMP_IF_FALSE: 2,
        LESS_THAN: 3,
        EQUALS: 3
}


def execute(opcodes, pointer, verbose=False):
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
    code = str(opcodes[pointer])
    instruction = int(code[-2:])
    param_modes = list(map(int, reversed(code[:-2])))

    n_params = PARAM_COUNT[instruction]

    # fill in zeros for any missing parameter modes (because they have leading zeros)
    if len(param_modes) < n_params:
        param_modes.extend([0] * (n_params - len(param_modes)))


    vals = ','.join(map(str, opcodes[pointer:pointer+n_params+1]))

    if instruction == TERMINATE:
        if verbose:
            print("TERMINATE!")
        return opcodes, True, pointer + n_params + 1

    if instruction == INPUT:
        if verbose:
            print("INPUT")
        result_address = opcodes[pointer+1]
        opcodes[result_address] = int(input("input > "))
        return opcodes, False, pointer + n_params + 1

    if instruction == OUTPUT:
        out_addr = pointer + 1
        if param_modes[0] == 0:
            out_addr = opcodes[out_addr]
        if verbose:
            print(f"INSTRUCTION = OUTPUT @ pos {pointer};  {vals}")
            print(f"    | VALUE AT ADDR {out_addr}; param_modes = {param_modes}; ")
        print("output>", opcodes[out_addr])
        return opcodes, False, pointer + n_params + 1

    if instruction == JUMP_IF_TRUE:
        value_address = pointer + 1]


    address_a = pointer + 1
    address_b = pointer + 2
    if param_modes[0] == POSITION:
        address_a = opcodes[address_a]
    if param_modes[1] == POSITION:
        address_b = opcodes[address_b]

    inst = {ADD: 'ADD', MULTIPLY: 'MULTIPLY'}[instruction]
    a = opcodes[address_a]
    b = opcodes[address_b]
    result_address = opcodes[pointer + 3]

    if verbose:
        print(f"INSTRUCTION = {inst} @ pos {pointer};  {vals}")
        print(f"    | addr({address_a},{address_b}) = values({a},{b}); store at {result_address}")
        print(f"    | param_modes = {param_modes}")

    opcodes[result_address] = {ADD: a + b,
                               MULTIPLY: a * b}[instruction]

    return opcodes, False, pointer + n_params + 1


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

    filename = sys.argv[1]

    with open(filename, 'r') as infile:
        text = infile.read()
        text = text.rstrip().lstrip()
        original_opcodes = list(map(int, text.split(',')))

    opcodes = copy.deepcopy(original_opcodes)

    result = run(opcodes)
