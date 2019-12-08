import functools
import itertools

IMAGE_WIDTH = 25
IMAGE_HEIGHT = 6


def parse_image(s, width, height):
    raw_ints = list(map(int, s))
    row_count = int(len(raw_ints) / width)
    rows = [raw_ints[i * width:(i + 1) * width] for i in range(row_count)]
    layer_count = int(len(rows) / height)
    image = [rows[i * height: (i + 1) * height] for i in range(layer_count)]
    return image


def read_image():
    with open('input.txt') as f:
        return parse_image(f.readline()[:-1], IMAGE_WIDTH, IMAGE_HEIGHT)


def checksum(image, cell_value):
    return [sum([len(list(filter(lambda cell: cell == cell_value, row))) for row in layer]) for layer in image]


def answer_1():
    image = read_image()
    layer_zero_count = checksum(image, 0)
    layer_index = sorted(enumerate(layer_zero_count), key=lambda x: x[1])[0][0]
    answer = checksum(image, 1)[layer_index] * checksum(image, 2)[layer_index]
    print('Answer 1: %s' % answer)


def merge_pixels(p):
    if p[0] == 2:
        return p[1]
    return p[0]


def merge_layers(layers):
    def __merge_layers__(layer_1, layer_2):
        layer_n = zip(layer_1, layer_2)
        layer_n = map(lambda layers: zip(*layers), layer_n)
        return map(lambda row: map(merge_pixels, row), layer_n)

    image = functools.reduce(__merge_layers__, layers)
    return list(map(list, image))


def view_image(image):
    translation = {0: '~', 1: '#', 2: ' '}
    for row in image:
        s = ''.join([translation[cell] for cell in row])
        print(s)


def answer_2():
    layered_image = read_image()
    image = merge_layers(layered_image)
    view_image(image)


def test_2():
    layered_image = parse_image('0222112222120000', 2, 2)
    image = merge_layers(layered_image)
    view_image(image)


if __name__ == '__main__':
    answer_1()
    test_2()
    answer_2()
