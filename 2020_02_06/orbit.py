class TransferOrbit(list):
    def __str__(self):
        return '->'.join(map(lambda obj: obj.name, self))

class SpaceObject:
    def __init__(self, name, direct_orbits=None, is_orbited_by=None):
        self.name = name

        if direct_orbits is None:
            direct_orbits = set()

        if is_orbited_by is None:
            is_orbited_by = set()

        self.direct_orbits = direct_orbits
        self.is_orbited_by = is_orbited_by

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

    def __rshift__(self, space_object):
        return self.add_orbitee(space_object)

    def __hash__(self):
        return hash(self.name)

    def find_path(self, obj, skip_obj=None):
        skip_objs = set()
        if isinstance(skip_obj, SpaceObject):
            skip_objs = set([skip_obj])

        obj_set = (self.direct_orbits | self.is_orbited_by) - skip_objs
        if obj in obj_set:
            return TransferOrbit([self, obj])

        for other_obj in obj_set:
            p = other_obj.find_path(obj, skip_obj=self)
            if p:
                return TransferOrbit([self] + p)

        return None

class Universe:
    objects = {}

    @property
    def orbit_count(self):
        total_count = 0

        for space_object in self.objects.values():
            total_count += space_object.total_orbit_count

        return total_count

    def __getitem__(self, key):
        if key not in self.objects:
            self.objects[key] = SpaceObject(key)

        return self.objects[key]

    def __add__(self, orbit):
        orbitee, orbiter = orbit.strip().split(')')
        self[orbiter] >> self[orbitee]

        return self


if __name__ == '__main__':
    import sys

    universe = Universe()
    filename = sys.argv[1]

    with open(filename) as orbit_file:
        for orbit in orbit_file:
            universe += orbit

    print(universe.orbit_count)

    if len(sys.argv) > 2:
        a, b = sys.argv[2:]
        path = universe[a].find_path(universe[b])

        print(path)

        print(len(path))

