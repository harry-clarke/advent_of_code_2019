INPUT = '134564-585159'


def has_double(p):
    a = p[0]
    for b in p[1:]:
        if a == b:
            return True
        a = b
    return False


def never_decreases(p):
    a = int(p[0])
    for b in iter(map(int, p[1:])):
        if b < a:
            return False
        a = b
    return True


def has_double_2(p):
    groups = []
    a = p[0]
    count = 1
    for b in p[1:]:
        if a == b:
            count += 1
        else:
            groups.append(count)
            count = 1
            a = b
    groups.append(count)
    return any([g == 2 for g in groups])


def valid_1(pint):
    pstr = str(pint)
    return len(pstr) == 6 and has_double(pstr) and never_decreases(pstr)


def valid_2(pint):
    pstr = str(pint)
    return len(pstr) == 6 and has_double_2(pstr) and never_decreases(pstr)


def answer_1():
    lb, ub = map(int, INPUT.split('-'))
    passwords = list(filter(valid_1, range(lb, ub + 1)))
    print('Answer 1: %s' % len(passwords))


def answer_2():
    lb, ub = map(int, INPUT.split('-'))
    passwords = list(filter(valid_2, range(lb, ub + 1)))
    print('Answer 2: %s' % len(passwords))


def test_2():
    pass_str = {True: 'Passed', False: 'Failed'}
    print('Answer 2 T1: %s' % pass_str[valid_2(112233)])
    print('Answer 2 T2: %s' % pass_str[not has_double_2('123444')])
    print('Answer 2 T3: %s' % pass_str[not valid_2(123444)])
    print('Answer 2 T4: %s' % pass_str[valid_2(111122)])

if __name__ == '__main__':
    answer_1()
    test_2()
    answer_2()
