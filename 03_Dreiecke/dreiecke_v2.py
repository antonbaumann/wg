#!/usr/bin/python
# -*- coding: UTF-8 -*-

# by Anton Baumann

# imports
import matplotlib.pyplot as plt

# Findet zweithöchstes bzw. niedrigstes Element in Liste:
# True-> höchstes; False -> niedrigstes
def find_second(l, b):
    tmp = []
    for e in l:
        tmp.append(e)
        tmp.sort(reverse=not b)
        while len(tmp) > 2:
            tmp.pop(0)
    return tmp[0]

def calculate_intersection(a, b):
    x = (a[0][0], a[1][0], b[0][0], b[1][0])
    y = (a[0][1], a[1][1], b[0][1], b[1][1])

    denominator = (y[3] - y[2]) * (x[1] - x[0]) - (y[1] - y[0]) * (x[3] - x[2])
    if denominator == 0:
        return None

    upper_x_a = max(a[0][0], a[1][0])
    lower_x_a = min(a[0][0], a[1][0])
    upper_y_a = max(a[0][1], a[1][1])
    lower_y_a = min(a[0][1], a[1][1])

    upper_x_b = max(b[0][0], b[1][0])
    lower_x_b = min(b[0][0], b[1][0])
    upper_y_b = max(b[0][1], b[1][1])
    lower_y_b = min(b[0][1], b[1][1])

    s_x = ((x[3] - x[2]) * (x[1] * y[0] - x[0] * y[1]) - (x[1] - x[0]) * (x[3] * y[2] - x[2] * y[3])) / denominator
    s_y = ((y[0] - y[1]) * (x[3] * y[2] - x[2] * y[3]) - (y[2] - y[3]) * (x[1] * y[0] - x[0] * y[1])) / denominator

    if s_x == -0.0:
        s_x = 0.0
    if s_y == -0.0:
        s_y = 0.0
    S = (s_x, s_y)

    if lower_x_a <= s_x <= upper_x_a and lower_x_b <= s_x <= upper_x_b:
        if lower_y_a <= s_y <= upper_y_a and lower_y_b <= s_y <= upper_y_b:
            # plt.plot(S[0], S[1], marker='x', color='r')
            return S

    return None


def read_File(filename):
    f = open(filename, 'r')
    p = f.readlines()
    n = int(p.pop(0).replace('\n', ''))

    punkt_geraden, gerade_punkte = {}, {}
    punkte = set()

    for i in range(n):
        tmp = p[i].replace('\n', '')
        tmp = tmp.split()
        tmp = [float(x) for x in tmp]

        points = [(tmp[0], tmp[1]), (tmp[2], tmp[3])]

        punkte.add(points[0])
        punkte.add(points[1])

        # erreichbare_punkte.setdefault(points[0], set()).add(points[1])
        # erreichbare_punkte.setdefault(points[1], set()).add(points[0])

        for poi in points:
            if poi not in punkt_geraden:
                punkt_geraden.setdefault(poi, set()).add(i)
            else:
                punkt_geraden.get(poi).add(i)

        gerade_punkte[i] = points

    return punkt_geraden, gerade_punkte, punkte


# returns punkt_geraden, gerade_punkte, punkte
def evaluate(punkt_geraden, gerade_punkte, punkte):
    for g1 in gerade_punkte:
        for g2 in gerade_punkte:
            if g1 is g2:
                continue
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
    for punkt,geraden in punkt_geraden.items():
        dreieck = [None, None, None]
        # print(str(punkt) + " -> " + str(geraden))
        for g1 in geraden:
            erreichbar = set(gerade_punkte[g1])
            erreichbar.remove(punkt)

            dreieck[0] = punkt

            for p2 in erreichbar:
                dreieck[1] = p2
                g2 = punkt_geraden[p2] - set([g1])
                if g2 == set():
                    continue
                g2 = g2.pop()
                tmp = set(gerade_punkte[g2]) - set([p2])
                e2 = tmp

                for p3 in e2:
                    dreieck[2] = p3
                    e3 = set()
                    for g3 in punkt_geraden[p3]:
                        e3.update(gerade_punkte[g3])
                    if punkt in e3:
                        dreiecke.add(tuple(sorted(dreieck)))
    return dreiecke


if __name__ == '__main__':
    punkt_geraden, gerade_punkte, punkte = read_File("txt/dreiecke1.txt")

    evaluate(punkt_geraden, gerade_punkte, punkte)

    dreiecke = modified_dfs(punkt_geraden, gerade_punkte)
    i = 1
    for d in dreiecke:
        print(str(i) + " -> " + str(d))
        i += 1
        for p in punkte:
            plt.plot(p[0], p[1], marker='o', color='grey')
        for k, v in gerade_punkte.items():
            plt.plot([v[0][0], v[1][0]], [v[0][1], v[1][1]], color='black')
        plt.plot([d[0][0], d[1][0], d[2][0], d[0][0] ], [ d[0][1], d[1][1], d[2][1], d[0][1] ], color='y')
        plt.show()

    print()
    print(len(dreiecke))
