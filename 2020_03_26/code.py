from typing import List, Tuple

class Register:
    value = 0

class Registry:
    _registers = {}
    def __getitem__(self, register_name) -> Register:
        if register_name not in self._registers:
            self._registers[register_name] = Register()

        return self._registers[register_name]

    @property
    def current_registers(self) -> List[str]:
        return sorted(self._registers.keys())

    @property
    def register_with_max_value(self) -> str:
        return max(self.current_registers,
                   key=lambda r_key: self[r_key].value)

    @property
    def max_value(self) -> int:
        return self[self.register_with_max_value].value

    def __str__(self):

        lines = []
        for r in self.current_registers:
            lines.append(" %-10s = %d"%(r, self[r].value))

        return '\n'.join(lines)

def parse_command(command) -> Tuple:
    words = command.rstrip().lstrip().split(' ')

    register_to_change = words[0]
    transform_type = words[1]
    amount = int(words[2])

    conditional_register = words[4]
    conditional_type = words[5]
    conditional_amount = int(words[6])

    transform = dict(
            inc=lambda reg: reg.value + amount,
            dec=lambda reg: reg.value - amount
    )[transform_type]

    conditional = {
            ">" : lambda reg: reg.value > conditional_amount,
            ">=" : lambda reg: reg.value >= conditional_amount,
            "<" : lambda reg: reg.value < conditional_amount,
            "<=" : lambda reg: reg.value <= conditional_amount,
            '==' : lambda reg: reg.value == conditional_amount,
            '!=' : lambda reg: reg.value != conditional_amount
    }[conditional_type]

    return (register_to_change,
            transform,
            conditional,
            conditional_register)


class Program:
    def __init__(self, registry=None):
        if registry is None:
            registry = Registry()

        self.registry = registry
        self.max_value_ever = None

    def execute(self, command):
        r, transform, conditional, cr = parse_command(command)

        # just to make sure this registry exists
        R = self.registry[r]

        if conditional(self.registry[cr]):
            new_value = transform(self.registry[r])

            if self.max_value_ever is None or new_value > self.max_value_ever:
                self.max_value_ever = new_value

            self.registry[r].value = new_value

        return self

if __name__ == '__main__':
    import sys

    program_file = sys.argv[1]

    p = Program()

    with open(program_file, 'r') as commands:
        for command in commands:
            p.execute(command)

    print("max value of registry after code execution: ", p.registry.max_value)
    print("max value ever held in the registry: ", p.max_value_ever)
