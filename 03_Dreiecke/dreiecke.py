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

    S = (s_x, s_y)

    if (lower_lim_x <= s_x <= upper_lim_x) and (lower_lim_y <= s_y <= upper_lim_y):
        return S

    return None


def read_File(filename):
    f = open(filename, 'r')
    p = f.readlines()
    n = int(p.pop(0).replace('\n', ''))

    erreichbare_punkte, punkt_geraden, gerade_punkte, geraden = {}, {}, {}, {}

    for i in range(n):
        tmp = p[i].replace('\n', '')
        tmp = tmp.split()
        points = [(tmp[0], tmp[1]), (tmp[2], tmp[3])]
        geraden.setdefault(i, set())
        geraden[i].add(points[0])
        geraden[i].add(points[1])
        erreichbare_punkte.setdefault(points[0], set()).add(points[1])
        erreichbare_punkte.setdefault(points[1], set()).add(points[0])

        for poi in points:
            if poi not in punkt_geraden:
                punkt_geraden.setdefault(poi, set()).add(i)
            else:
                punkt_geraden.get(poi).add(i)

        gerade_punkte[i] = set(points)

    return erreichbare_punkte, punkt_geraden, gerade_punkte, geraden

if __name__ == '__main__':
    erreichbare_punkte, punkt_geraden, gerade_punkte, geraden = read_File("txt/dreiecke1.txt")

    print(erreichbare_punkte)
    print(punkt_geraden)
    print(gerade_punkte)
    print(geraden)
