# by Anton Baumann

# imports
import math


alphabet = "ABCDEFGHIJKLMNOPQRSTUVWXYZ"
digits = "0123456789"


def index_to_name(n, b):
    le = n // len(alphabet)
    ret = alphabet[0]*le + alphabet[n%len(alphabet)]
    if b:
        return ret
    else:
        return ret.lower()

# Findet zweithöchstes/niedrigstes Element in Liste:
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

    upper_lim_x = find_second(x, True)
    lower_lim_x = find_second(x, False)

    upper_lim_y = find_second(y, True)
    lower_lim_y = find_second(y, False)

    s_x = ((x[3] - x[2]) * (x[1] * y[0] - x[0] * y[1]) - (x[1] - x[0]) * (x[3] * y[2] - x[2] * y[3])) / denominator
    s_y = ((y[0] - y[1]) * (x[3] * y[2] - x[2] * y[3]) - (y[2] - y[3]) * (x[1] * y[0] - x[0] * y[1])) / denominator

    if s_x == -0.0:
        s_x = 0.0
    if s_y == -0.0:
        s_y = 0.0
    S = (s_x, s_y)

    if (lower_lim_x <= s_x <= upper_lim_x) and (lower_lim_y <= s_y <= upper_lim_y):
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
    erreichbar = dict()
    for punkt,geraden in punkt_geraden.items():
        # print(str(punkt) + " -> " + str(geraden))
        erreichbar[punkt] = set()
        for g in geraden:
            erreichbar[punkt].update(gerade_punkte[g])
        erreichbar[punkt].remove(punkt)
    

    print(erreichbar)

if __name__ == '__main__':
    punkt_geraden, gerade_punkte, punkte = read_File("txt/dreiecke1.txt")
    evaluate(punkt_geraden, gerade_punkte, punkte)
    dreiecke = modified_dfs(punkt_geraden, gerade_punkte)
