from typing import Union
from functools import wraps


def convert_value(func):
    @wraps(func)
    def new_func(self, value, *args):
        if value in self.registers.keys():
            value = self.registers[value]
        return func(self, value, *args)
    return new_func


class Computer:
    def __init__(self, a=0, b=0, c=0, d=0):
        self.registers = dict(a=a, b=b, c=c, d=d)

    @convert_value
    def cpy(self, value: Union[str, int], register: str) -> int:
        self.registers[register] = value
        return 1

    def inc(self, register: str) -> int:
        self.registers[register] += 1
        return 1

    def dec(self, register: str) -> int:
        self.registers[register] -= 1
        return 1

    @convert_value
    def jnz(self, value: Union[int, str], jump_dist: int) -> int:
        if value != 0:
            return jump_dist
        return 1

    def execute_command(self, command: str) -> int:
        command, *args = command.split()
        args = [a if a in self.registers.keys() else int(a) for a in args]
        return getattr(self, command)(*args)

    def run_program(self, program: str) -> None:
        commands = program.split('\n')
        commands = [c for c in commands if len(c.split()) > 1]

        index = 0
        while 0 <= index < len(commands):
            index += self.execute_command(commands[index])

if __name__ == '__main__':
    import sys

    program_name = sys.argv[1]

    print("running ", program_name)

    c = Computer()
    with open(program_name, 'r') as program:
        c.run_program(program.read())

    print(c.registers)
