from typing import Union, Set, List, Optional

class Connection:
    def __init__(self, left: Union[int, str], right: Union[int, str]):
        self.left = int(left)
        self.right = int(right)

    def flip(self):
        self.left, self.right = self.right, self.left

    @property
    def can_start_bridge(self) -> bool:
        return self.left == 0 or self.right == 0

    @property
    def ports(self) -> Set[int]:
        return set([self.left, self.right])

    def __repr__(self) -> str:
        left, right = sorted([self.left, self.right])
        return f'{left}/{right}'

    __hash__ = __repr__


class Bridge:
    def __init__(self):
        self.connections = []

    def copy(self) -> 'Bridge':
        b = Bridge()
        b.connections = [c for c in self.connections]
        return b

    @property
    def endpoint(self) -> int:
        if len(self.connections) == 0:
            return 0

        return self.connections[-1]

    @property
    def strength(self) -> int:
        if len(self.connections) == 0:
            return 0
        return sum(self.connections)

    def can_connect(self, connection: Connection) -> bool:
        if len(self.connections) == 0:
            return connection.can_start_bridge

        return self.endpoint in connection.ports

    def connect(self, connection: Connection) -> 'Bridge':
        if not self.can_connect(connection):
            raise ValueError(f'cannot connect {connection} to endpoint {self.endpoint}')

        if not self.endpoint == connection.left:
            connection.flip()

        self.connections.extend([connection.left, connection.right])

        return self


def read_file(filename: str) -> List[Connection]:
    connections = []
    with open(filename, 'r') as infile:
        for line in infile:
            left, right = line.split('/')
            connections.append(Connection(left, right))
    return connections

def all_unique_bridges(connections: List[Connection], bridge: Optional[Bridge] = None) -> List[Bridge]:
    if bridge is None:
        bridge = Bridge()

    bridges = [bridge]
    for connection in connections:
        if bridge.can_connect(connection):
            remaining_connections = [c for c in connections if c != connection]
            new_bridge = bridge.copy().connect(connection)
            bridges += all_unique_bridges(remaining_connections, bridge=new_bridge)

    return bridges


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]

    connections = read_file(filename)
    bridges = all_unique_bridges(connections)

    print(len(bridges), "possible bridges; max strength of ", max([b.strength for b in bridges]))

    max_len = max([len(b.connections) for b in bridges])
    max_len_bridges = [b for b in bridges if len(b.connections) == max_len]
    print("max bridge length = ", int(max_len / 2),
          "max strength of bridges with this length", max([b.strength for b in max_len_bridges]))

