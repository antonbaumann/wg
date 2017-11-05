#! /usr/bin/env python3
# -*- coding: UTF-8 -*-

# by Anton Baumann

import sys


def calculate_intersection(a, b):
    x = (a[0][0], a[1][0], b[0][0], b[1][0])
    y = (a[0][1], a[1][1], b[0][1], b[1][1])

    denominator = (y[3] - y[2]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[3] - x[2])
    if denominator == 0:
        return None

    # höchster und niedrigster y und x Wert von a
    upper_x_a = max(a[0][0], a[1][0])
    lower_x_a = min(a[0][0], a[1][0])
    upper_y_a = max(a[0][1], a[1][1])
    lower_y_a = min(a[0][1], a[1][1])

    # höchster und niedrigster y und x Wert von a
    upper_x_b = max(b[0][0], b[1][0])
    lower_x_b = min(b[0][0], b[1][0])
    upper_y_b = max(b[0][1], b[1][1])
    lower_y_b = min(b[0][1], b[1][1])

    s_x = ((x[3] - x[2]) * (x[1] * y[0] - x[0] * y[1]) - (x[1] - x[0]) * (x[3] * y[2] - x[2] * y[3])) / denominator
    s_y = ((y[0] - y[1]) * (x[3] * y[2] - x[2] * y[3]) - (y[2] - y[3]) * (x[1] * y[0] - x[0] * y[1])) / denominator

    if s_x == -0.0: s_x = 0.0
    if s_y == -0.0: s_y = 0.0
    S = (s_x, s_y)

    if lower_x_a <= s_x <= upper_x_a and lower_x_b <= s_x <= upper_x_b:
        if lower_y_a <= s_y <= upper_y_a and lower_y_b <= s_y <= upper_y_b:
            return S
    return None


def read_file(filename):
    with open(filename, 'r') as f:
        lst = f.readlines()
    length = int(lst.pop(0).replace('\n', ''))
    punkt_geraden, gerade_punkte, punkte = {}, {}, set()

    for i in range(length):
        tmp = lst[i].replace('\n', '').split()
        tmp = [float(x) for x in tmp]
        line = [(tmp[0], tmp[1]), (tmp[2], tmp[3])]
        punkte.update(line)
        for p in line:
            if p not in punkt_geraden:
                punkt_geraden.setdefault(p, set()).add(i)
            else:
                punkt_geraden.get(p).add(i)
        gerade_punkte[i] = line
    return punkt_geraden, gerade_punkte, punkte


# returns punkt_geraden, gerade_punkte, punkte
def process(punkt_geraden, gerade_punkte, punkte):
    for g1 in range(len(gerade_punkte)):
        for g2 in range(g1 + 1, len(gerade_punkte)):
            schnittpunkt = calculate_intersection(gerade_punkte[g1], gerade_punkte[g2])
            if schnittpunkt is None:
                continue
            if schnittpunkt in punkte:
                if schnittpunkt not in gerade_punkte[g1]:
                    gerade_punkte[g1].append(schnittpunkt)
                elif schnittpunkt not in gerade_punkte[g2]:
                    gerade_punkte[g2].append(schnittpunkt)
                punkt_geraden[schnittpunkt].add(g1)
                punkt_geraden[schnittpunkt].add(g2)
            else:
                gerade_punkte[g1].append(schnittpunkt)
                gerade_punkte[g2].append(schnittpunkt)
                punkt_geraden.setdefault(schnittpunkt, set()).add(g1)
                punkt_geraden.setdefault(schnittpunkt, set()).add(g2)
            punkte.add(schnittpunkt)


def modified_dfs(punkt_geraden, gerade_punkte):
    dreiecke = set()
    # iteriere über jeden Punkt im Graphen
    for p1, geraden in punkt_geraden.items():
        dreieck = [None, None, None]
        for g1 in geraden:
            e1 = set(gerade_punkte[g1])
            e1.remove(p1)
            dreieck[0] = p1
            for p2 in e1:
                dreieck[1] = p2
                g2 = punkt_geraden[p2] - {g1}
                if len(g2) == 0:
                    continue
                g2 = g2.pop()
                tmp = set(gerade_punkte[g2]) - {p2}
                e2 = tmp

                for p3 in e2:
                    dreieck[2] = p3
                    e3 = set()
                    for g3 in punkt_geraden[p3]:
                        e3.update(gerade_punkte[g3])
                    if p1 in e3:
                        dreiecke.add(tuple(sorted(dreieck)))
    return dreiecke


def main(b, path):
    punkt_geraden, gerade_punkte, punkte = read_file(path)
    process(punkt_geraden, gerade_punkte, punkte)
    dreiecke = modified_dfs(punkt_geraden, gerade_punkte)

    if b:
        import matplotlib.pyplot as plt
        for p in punkte:
            plt.plot(p[0], p[1], marker='o', color='grey')
        for k, v in gerade_punkte.items():
            plt.plot([v[0][0], v[1][0]], [v[0][1], v[1][1]], color='black')
        plt.show()

        for i, d in enumerate(dreiecke):
            print(str(i+1) + " -> " + str(d))
            for p in punkte:
                plt.plot(p[0], p[1], marker='o', color='grey')
            for k, v in gerade_punkte.items():
                plt.plot([v[0][0], v[1][0]], [v[0][1], v[1][1]], color='black')
            plt.plot([d[0][0], d[1][0], d[2][0], d[0][0]], [d[0][1], d[1][1], d[2][1], d[0][1]],
                     color='y', linewidth=5)
            plt.show()
    else:
        for i, d in enumerate(dreiecke):
            print(str(i+1) + " -> " + str(d))

    print("Anzahl Dreiecke: ", len(dreiecke))


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print("dreiecke.py")
        print("Usage:\n", "dreiecke.py FILE [--visualize|-v]")
        sys.exit(0)

    file_path = sys.argv[1]
    visualize = False
    if len(sys.argv) >= 3:
        if sys.argv[2] in ['--visualize', '-v']:
            visualize = True
    main(visualize, file_path)
