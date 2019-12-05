

TEST_INPUT_2 = [
    ('R75,D30,R83,U83,L12,D49,R71,U7,L72','U62,R66,U55,R34,D71,R55,D58,R83', 610),
    ('R98,U47,R26,D63,R33,U87,L62,D20,R33,U53,R51','U98,R91,D20,R16,D67,R40,U7,R15,U6,R7', 410)
]

DIRECTION_MAPPING = {
    'U': (lambda x, y, d: (x, y + d)),
    'D': (lambda x, y, d: (x, y - d)),
    'L': (lambda x, y, d: (x + d, y)),
    'R': (lambda x, y, d: (x - d, y)),
}


def parse_wire_segment(s: str):
    direction = DIRECTION_MAPPING[s[0]]
    distance = int(s[1:])
    return direction, distance


def parse_wire(s: str):
    return list(map(parse_wire_segment, s.split(',')))


def unravel(w):
    coords = {(0, 0)}
    posx, posy = 0, 0
    for (direction, distance) in w:
        new_coords = set([direction(posx, posy, d) for d in range(1, distance + 1)])
        coords = coords.union(new_coords)
        posx, posy = direction(posx, posy, distance)
    return coords


def unravel_2(w):
    coords = {(0, 0): 0}
    posx, posy = 0, 0
    total_distance = 0
    for (direction, distance) in w:
        new_coords = [(direction(posx, posy, d), total_distance + d) for d in range(1, distance + 1)]
        total_distance += distance
        posx, posy = new_coords[-1][0]
        updates = filter(lambda coord: coord[0] not in coords.keys() or coords.get(coord[0]) > coord[1], new_coords)
        coords.update(updates)
    return coords


def manhattan(coords): return abs(coords[0]) + abs(coords[1])


def answer_1(w1, w2):
    uw1 = unravel(w1)
    uw2 = unravel(w2)
    cross_points = list(uw1.intersection(uw2))
    cross_points.sort(key=manhattan)
    print('Answer 1: %s' % manhattan(cross_points[1]))


def answer_2(w1, w2):
    uw1 = unravel_2(w1)
    uw2 = unravel_2(w2)
    cross_points = set(uw1.keys()).intersection(set(uw2.keys()))
    cross_points = [(point, uw1.get(point) + uw2.get(point)) for point in cross_points]
    cross_points.sort(key=lambda d: d[1])
    return cross_points[1]

def main():
    with open('input.txt') as f:
        s = f.readlines()
        w1 = parse_wire(s[0])
        w2 = parse_wire(s[1])
        answer_1(w1, w2)
        print('Answer 2 T1: %s: %s' % answer_2(parse_wire(TEST_INPUT_2[0][0]), parse_wire(TEST_INPUT_2[0][1])))
        print('Answer 2 T2: %s: %s' % answer_2(parse_wire(TEST_INPUT_2[1][0]), parse_wire(TEST_INPUT_2[1][1])))
        print('Answer 2: %s: %s' % answer_2(w1, w2))


if __name__ == '__main__':
    main()