from collections import namedtuple

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

def decode_value(opcodes, pointer, param_mode):
    if param_mode == POSITION:
        return opcodes[opcodes[pointer]]

    if param_mode == IMMEDIATE:
        return opcodes[pointer]

    raise ValueError(f"Do not recognize parameter mode: {param_mode}")

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
        result_addr = decode_value(opcodes, pointer + 1, 1)
        if verbose:
            print(f"INPUT -- to be stored @ {result_addr} (len(opcodes) = {len(opcodes)})")
        opcodes[result_addr] = int(input("input > "))
        return opcodes, False, pointer + n_params + 1

    if instruction == OUTPUT:
        #out_addr = decode_value(opcodes, pointer + 1, param_modes[0])

        out_addr = pointer + 1
        if param_modes[0] == 0:
            out_addr = opcodes[out_addr]
        if verbose:
            print(f"INSTRUCTION = OUTPUT @ pos {pointer};  {vals}")
            print(f"    | VALUE AT ADDR {out_addr}; param_modes = {param_modes}; ")
        print("output>", opcodes[out_addr])
        return opcodes, False, pointer + n_params + 1

    if instruction in {JUMP_IF_TRUE, JUMP_IF_FALSE}:
        value = decode_value(opcodes, pointer + 1, param_modes[0])
        jump_addr = decode_value(opcodes, pointer + 2, param_modes[1])

        jump = {JUMP_IF_TRUE: value != 0,
                JUMP_IF_FALSE: value == 0}[instruction]

        if verbose:
            inst = {JUMP_IF_TRUE: 'JUMP_IF_TRUE',
                    JUMP_IF_FALSE: 'JUMP_IF_FALSE'}[instruction]
            print(f"INSTRUCTION = {inst} @ pos {pointer};  {vals}")
            print(f"    | jump-to addr = {jump_addr}; param_modes = {param_modes};")
            print(f"    | value = {value}")
            print(f"    | WILL {'' if jump else 'NOT'} JUMP!")

        if jump:
            return opcodes, False, jump_addr

        return opcodes, False, pointer + n_params + 1

    if instruction in {LESS_THAN, EQUALS}:
        a = decode_value(opcodes, pointer + 1, param_modes[0])
        b = decode_value(opcodes, pointer + 2, param_modes[1])

        result_addr = opcodes[pointer + 3]
        #decode_value(opcodes, pointer + 3, param_modes[2])

        affirmative = {LESS_THAN: a < b,
                       EQUALS: a == b}[instruction]

        if verbose:
            inst = {LESS_THAN: 'LESS_THAN',
                    EQUALS: 'EQUALS'}[instruction]
            print(f"INSTRUCTION = {inst} @ pos {pointer};  {vals}")
            print(f"    | param_modes = {param_modes}")
            print(f"    | a = {a}, b = {b}")
            print(f"    | a {inst} b = {affirmative}")
            print(f"    | storing result @ {result_addr}")

        opcodes[result_addr] = 1 if affirmative else 0

        return opcodes, False, pointer + n_params + 1

    inst = {ADD: 'ADD', MULTIPLY: 'MULTIPLY'}[instruction]
    a = decode_value(opcodes, pointer + 1, param_modes[0])
    b = decode_value(opcodes, pointer + 2, param_modes[1])
    result_addr = opcodes[pointer + 3]

    value = {ADD: a + b,
             MULTIPLY: a * b}[instruction]

    if verbose:
        print(f"INSTRUCTION = {inst} @ pos {pointer};  {vals}")
        print(f"    | values({a},{b}) --> {value}; store at {result_addr}")
        print(f"    | param_modes = {param_modes}")

    opcodes[result_addr] = value


    return opcodes, False, pointer + n_params + 1


def run(program):
    """
    Run a full opcode program

    """
    pointer, terminate = 0, False

    while not terminate:
        program, terminate, pointer = execute(program, pointer, verbose=True)

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
