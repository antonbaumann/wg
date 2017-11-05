#! /usr/bin/env python3

import prices
import sys
from prices import show_table
import time

global V
V = False


def finished(lst):
    for a, b in lst:
        if a != b:
            return False
    return True


def remove_duplicates(lst):
    c = []
    tmp = [0, 0]
    for e in lst:
        comp = [e[0], e[1]]
        b = True
        for i in range(len(tmp)):
            if tmp[i] != comp[i]:
                b = False
        if not b:
            c.append(e)
        tmp = comp
    return c


def adjust(t, e, j, we):
    # t = sorted(t, key=lambda k: k['c'], reverse=True)
    # best = 0
    # end = len(t)
    # for r in t:
    #     if r['c'] > best:
    #         best = r['c']
    # if best >= 800:
    #     for i in range(len(t)):
    #         if t[i]['c'] < best:
    #             end = i
    #             break
    # t = t[:end]

    # print('START-----{')
    if e > 6 and not we:
        t = [d for d in t if d['e'] == 6]
    elif e + j > 6:
        if not we:
            t = [d for d in t if d['e'] + d['j'] == 6]
        else:
            t = [d for d in t if d['e'] + d['j'] == 4]
    t = sorted(t, key=lambda k: k['ind'], reverse=False)
    print(t)
    # print("}------END")
    return t


def main(we, k, j, e, g):
    if k > 0 and e == 0:
        print("Kinder unter 4J dürfen nicht ohne begleitung eines Erwachsenen ins Schwimmbad gehen!")
        return False

    table = prices.prices(e, j, we)
    table = adjust(table, e, j, we)
    h = []
    stack = []
    poss = []
    min_costs = 999999999999

    stack.append([e, j, table])
    h.append([len(table), 0])

    costs = 0
    tmp = []
    while not finished(h):
        top = stack[len(stack) - 1]
        t = top[2]

        if V:
            print(h)
            print(top[0], top[1])
            show_table(t)

        row = t[h[len(h) - 1][1]]
        tmp.append(row)

        costs += row['c']
        new = [
            top[0] - row['e'],
            top[1] - row['j'],
            prices.prices(top[0] - row['e'], top[1] - row['j'], we),
            # top[3] + 1
        ]

        new[2] = adjust(new[2], new[0], new[1], we)
        h[len(h) - 1][1] += 1

        if new[0] == new[1] == 0:
            if V:
                print(costs)
                print(tmp)
                print()
                print("##################################################################")

            poss.append([costs, sorted(tmp, key=lambda k: k['c'], reverse=True)])
            if costs < min_costs:
                min_costs = costs

            p = tmp.pop()
            costs -= p['c']
            while len(h) != 0 and h[len(h) - 1][0] == h[len(h) - 1][1]:
                stack.pop()
                h.pop()
                if len(tmp) > 0:
                    p = tmp.pop()
                    costs -= p['c']

        if len(new[2]) != 0:
            stack.append(new)
            h.append([len(new[2]), 0])

    poss = sorted(poss, key=lambda k: k[0])
    poss = remove_duplicates(poss)
    # poss = poss[:min(len(poss), 5)]
    return poss


if __name__ == '__main__':
    we = False
    fe = False
    g = 0
    k = 1
    j = 16
    e = 15
    start = time.time()
    lst = main(we, k, j, e, g)


    for p in lst[:5]:
        print(p[0])
        prices.show_table(p[1])

    end = time.time()

    print(end - start)
    print(len(lst))
