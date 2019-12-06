import itertools

TEST_INPUT_1 = ['COM)B', 'B)C', 'C)D', 'D)E', 'E)F', 'B)G', 'G)H', 'D)I', 'E)J', 'J)K', 'K)L']
TEST_INPUT_2 = ['COM)B'
    , 'B)C'
    , 'C)D'
    , 'D)E'
    , 'E)F'
    , 'B)G'
    , 'G)H'
    , 'D)I'
    , 'E)J'
    , 'J)K'
    , 'K)L'
    , 'K)YOU'
    , 'I)SAN']


class OrbitMap:
    def __init__(self, orbit_map):
        # A map of objects to their center
        self.orbit_map: dict[str, str] = orbit_map
        # A map of orbits to their orbit count
        self.orbit_counts: dict[str, int] = {'COM': 0}

    def count_all_orbits(self):
        count = 0
        for obj in self.orbit_map.keys():
            count += self.count_orbits(obj)
        return count

    # Counts the number of orbits for a specific object
    def count_orbits(self, obj):
        if obj in self.orbit_counts:
            return self.orbit_counts[obj]

        center = self.orbit_map[obj]
        if center not in self.orbit_counts:
            self.count_orbits(center)

        self.orbit_counts[obj] = self.orbit_counts[center] + 1
        return self.orbit_counts[obj]

    # Lists the objects between the parameter and COM
    def path_object(self, obj):
        path = []
        center = self.orbit_map[obj]
        while center != 'COM':
            path.append(center)
            center = self.orbit_map[center]
        return path

    # Lists the objects between the first parameter and the second
    def path_objects(self, obj1, obj2):
        p1 = self.path_object(obj1)
        p2 = self.path_object(obj2)
        while p1[-1] == p2[-1] and p1[-2] == p2[-2]:
            p1.pop()
            p2.pop()
        join = p1 + list(reversed(p2[:-1]))
        return join


def parse_line(line): return tuple(reversed(line.split(')')))


def map_orbits(orbits): return dict(orbits)


def parse(lines): return OrbitMap(map_orbits(map(parse_line, lines)))


def test_1():
    m = parse(TEST_INPUT_1)
    c = m.count_all_orbits()
    print('Answer 1 T1: %s' % c)


def answer_1():
    with open('input.txt') as f:
        s = map(str.strip, f.readlines())
        m = parse(s)
        c = m.count_all_orbits()
        print('Answer 1: %s' % c)


def test_2():
    m = parse(TEST_INPUT_2)
    print(m.path_objects('YOU', 'SAN'))


def answer_2():
    with open('input.txt') as f:
        s = map(str.strip, f.readlines())
        m = parse(s)
        p = m.path_objects('YOU', 'SAN')
        c = len(p) - 1
        print(c)


if __name__ == '__main__':
    test_1()
    answer_1()
    test_2()
    answer_2()
