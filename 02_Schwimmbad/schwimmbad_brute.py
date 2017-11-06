#! /usr/bin/env python3

import copy
import prices
import sys
from prices import show_table

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


def adjust(t):
    return sorted(t, key=lambda k: k['ind'], reverse=False)


def main(we, fe, g, k, j, e):
    if k > 0 and e == 0:
        print("Kinder unter 4J dürfen nicht ohne begleitung eines Erwachsenen ins Schwimmbad gehen!")
        return False

    # prices() gibt eine Tabelle mit allen möglichen Karten für eine Kombination (e, j)
    # zurück
    table = prices.prices(e, j, we)
    table = adjust(table)
    # Hilfsstack: speichert wie viele Elemente die Tabelle an einer bestimmten Ebene hat
    #             und welche Reihe gerade verwendet wird
    h = []
    stack = []
    # Liste mit allen Kombinationsmöglichkeiten
    poss = []
    min_costs = 999999999999

    stack.append([e, j, table, 0])
    h.append([len(table), 0])

    costs = 0
    tmp = []
    while not finished(h):
        # oberstes Element vom Stack wird bestimmt
        top = stack[len(stack) - 1]
        # t ist die Tabelle mit Preisen
        t = top[2]

        if V:
            print(h)
            print(top[0], top[1], top[3])
            show_table(t)

        row = t[h[len(h) - 1][1]]
        tmp.append(row)

        costs += row['c']
        new = [
            top[0] - row['e'],
            top[1] - row['j'],
            prices.prices(top[0] - row['e'], top[1] - row['j'], we),
            top[3] + 1
        ]

        t = adjust(t)

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

    # Gutscheine anwenden:
    if not fe:
        new_poss = []
        g_copy = g

        for comb in poss:
            # Bis nur noch ein Gutschein übrig bleibt werden alle Gutscheine eingelöst
            while g > 1:
                # suchen ob noch ein Erwachsener mit Einzelkarte übrig ist
                i = find(comb[1], 'e', 'ind', 1, 1)
                # wenn ein Erwachsener mit Einzelkarte übrig ist
                if i == -1:
                    # suchen ob noch ein Jugendlicher mit Einzelkarte übrig ist
                    i = find(comb[1], 'j', 'ind', 1, 1)
                # wenn E oder J übrig -> Gutschein anwenden
                if i != -1:
                    c = comb[1][i]['c']
                    comb[1][i]['c'] = 0
                    comb[1][i]['c_s'] = 0
                    comb[1][i]['ind'] = 0
                    comb[0] -= c
                    g -= 1
                # sonst Schleife beenden
                else:
                    break

            # letzter Gutschein -> ein mal als Gutschein für die gesamte Gruppe verwenden
            #                   -> ein mal für Einzelperson verwenden
            if g > 0:
                comb_gruppengutschein = copy.deepcopy(comb)
                comb_gruppengutschein[0] *= -9/10
                i = find(comb[1], 'e', 'ind', 1, 1)
                if i == -1:
                    i = find(comb[1], 'j', 'ind', 1, 1)
                if i != -1:
                    c = comb[1][i]['c']
                    comb[1][i]['c'] = 0
                    comb[1][i]['c_s'] = 0
                    comb[1][i]['ind'] = 0
                    comb[0] -= c
                    g -= 1
                new_poss.append(comb_gruppengutschein)
            g = g_copy
        poss += new_poss

    poss = remove_duplicates(poss)
    poss = sorted(poss, key=lambda k: abs(k[0]))

    # bestes Ergebnis zurückgeben
    return poss[:1]


def find(lst, key1, key2, val1, val2):
    for i, d in enumerate(lst):
        if d[key1] == val1 and d[key2] == val2:
            return i
    return -1


if __name__ == '__main__':
    if len(sys.argv) == 7:
        we = sys.argv[1].lower() == 't'
        fe = sys.argv[2].lower() == 't'
        e = int(sys.argv[3])
        j = int(sys.argv[4])
        k = int(sys.argv[5])
        g = int(sys.argv[6])
    else:
        we = input("Wochenende (T|f):\n> ").lower() != 'f'
        fe = input("Ferien (T|f):\n> ").lower() != 'f'
        e = int(input("Erwachsene:\n> "))
        j = int(input("Jugentliche:\n> "))
        k = int(input("Kinder:\n> "))
        g = int(input("Gutscheine:\n> "))

    print()
    print("Bester Preis wird berechnet für:")
    print("Wochenende:\t", we)
    print("Ferien:\t\t", fe)
    print("Erwachsene:\t", e)
    print("Jugendl.:\t", j)
    print("Kinder:\t\t", k)
    print("Gutscheine:\t", g)
    print()

    lst = main(we, fe, g, k, j, e)

    for p in lst:
        s = "mit Gruppengutschein" if p[0] < 0 else ""
        print(abs(p[0]), s)
        prices.show_table(p[1])