
class SpaceObject:
    def __init__(self, name, direct_orbits=None, is_orbited_by=None):
        self.name = name
        self.direct_orbits = direct_orbits if direct_orbits else set()
        self.is_orbited_by = is_orbited_by if is_orbited_by else set()

    @property
    def indirect_orbits(self):
        indir_orb = set()

        for space_obj in self.direct_orbits:
            indir_orb |= (space_obj.direct_orbits
                          | space_obj.indirect_orbits)

        return indir_orb

    @property
    def total_orbit_count(self):
        return len(self.direct_orbits | self.indirect_orbits)

    def add_orbitee(self, space_object):
        self.direct_orbits.add(space_object)
        space_object.is_orbited_by.add(self)
        return self

    def add_orbiter(self, space_object):
        self.is_orbited_by.add(space_object)
        space_object.direct_orbits.add(self)
        return self

    def __rshift__(self, space_object):
        return self.add_orbitee(space_object)

    def __lshift__(self, space_object):
        return self.add_orbiter(space_object)

    def __str__(self):
        return self.name

    def find_path(self, obj, skip=None):
        skip_objs = set([skip]) if skip else set()

        obj_set = (self.direct_orbits | self.is_orbited_by) - skip_objs
        if obj in obj_set:
            return TransferOrbit([self, obj])

        for other_obj in obj_set:
            if (p := other_obj.find_path(obj, skip=self)):
                return TransferOrbit([self] + p)

        return None

class TransferOrbit(list):
    def __str__(self):
        return '->'.join(map(str, self))

class Universe:
    objects = {}

    @property
    def orbit_count(self):
        """ Total orbits + indirect orbits """
        return sum([obj.total_orbit_count
                    for obj in self.objects.values()])

    def __getitem__(self, key):
        if key not in self.objects:
            self.objects[key] = SpaceObject(key)

        return self.objects[key]

    def __add__(self, something):
        """ add another orbit to the universe """
        orbitee, orbiter = orbit.strip().split(')')
        self[orbiter] >> self[orbitee]

        return self


if __name__ == '__main__':
    import sys

    filename = sys.argv[1]

    # ingest + digest input
    u = Universe()
    with open(filename) as orbit_file:
        for orbit in orbit_file:
            u += orbit

    print("Total orbit count:", u.orbit_count)

    if len(sys.argv) > 2:
        a, b = sys.argv[2:]

        print(f"Finding path between {a} and {b}")
        path = u[a].find_path(u[b])

        print(path)
        print(f"Path length: {len(path)}")

