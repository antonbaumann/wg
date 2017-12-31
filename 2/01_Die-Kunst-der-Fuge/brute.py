#! /usr/bin/env python3

import itertools

def generate_all_possible_rows(n):
    lst = list(itertools.permutations([x for x in range(1, n+1)]))
    _lst = []

    for p in lst:
        tmp = []
        s = 0
        for e in p:
            s += e
            tmp.append(s)
        _lst.append(tmp)
    lst = _lst

    return lst



def main(n):
    possible_rows = generate_all_possible_rows(n)
    print(len(possible_rows))
    for el in possible_rows:
        print(el)


if __name__ == '__main__':
    n = 10
    main(n)