#! /usr/bin/env python3

import sys
import math
import copy
import prices


# überprüft ob es sich lohn eine Familienkarte zu kaufen
def f_makes_sense(d):
    if d['r'] < 4:
        return False
    if d['e'] >= 1 and d['j'] >= 3:
        return True
    if d['e'] >= 2 and d['j'] >= 2:
        return True
    return False


def main(we, fe, g, k, j, e):
    if k > 0 and e == 0:
        print("Kinder können nur mit einem Erwachsenem ins Schwimmbad gehen!")
        return False

    # enthält alle für den Alg. wichtigen daten
    d = {
        'e': e,  # Anzahl Erwachsener
        'j': j,  # Anzahl Jugendlicher
        'nr_t': 0,  # Anzahl zu kaufender Tageskarten
        # 'nr_f':     0,  # Anzahl zu kaufender Familienkarte
        'r': e + j  # Anzahl an noch "verwendbaren" Personen
    }

    d_copy = d.copy()

    # Am Wochenende werden keine Tageskarten verkauft
    # -> Tageskarten werden aus dict(d) entfernt
    if we:
        d.pop('nr_t')

    # wenn !Wochenende
    # -> Tageskarten werden verkauft
    if not we:
        all_p = d['e'] + d['j']
        # mit einer Tageskarte können 6 Personen ins Schwimmbad
        d['r'] = all_p - math.floor(all_p / 6) * 6
        d['nr_t'] = all_p - d['r']

    # Dictionary das alle verschiedenen Eintrittsmöglichkeiten enthält
    # t, f -> [] von (e, j)
    # e, j -> int
    variant = {
        't': [],
        'f': [],
        'e': 0,
        'j': 0
    }

    # Am Wochenende werden keine Tageskarten verkauft
    # -> Tageskarten werden aus dict(variant) entfernt
    if we:
        variant.pop('t')

    # Familienkarten
    while f_makes_sense(d):
        if d['e'] >= 1 and d['j'] >= 3 and d['j'] > d['e'] + 3:
            variant['f'].append((1, 3))
            d['e'] -= 1
            d['j'] -= 3
            d['r'] -= 4
        elif d['e'] >= 2 and d['j'] >= 2:
            variant['f'].append((2, 2))
            d['e'] -= 2
            d['j'] -= 2
            d['r'] -= 4
        elif d['e'] >= 1 and d['j'] >= 3:
            variant['f'].append((1, 3))
            d['e'] -= 1
            d['j'] -= 3
            d['r'] -= 4

    # Einzelkarten
    left = {'e': 0, 'j': 0}
    tmp_j = d['j']

    # solange noch Karten gekauft werden müssen
    while d['r'] > 0:
        # print(left)
        if tmp_j > 0:
            left['j'] += 1
            tmp_j -= 1
        else:
            left['e'] += 1
        d['r'] -= 1

    while left['e'] + left['j'] > 0:
        table = prices.prices(left['e'], left['j'], we, 0)
        best_choice = table[0]

        tmp_e, tmp_j = best_choice['e'], best_choice['j']

        if best_choice['c'] == 1100:
            variant['t'].append((tmp_e, tmp_j))
        if best_choice['c'] == 800:
            variant['f'].append((tmp_e, tmp_j))
        if 280 == best_choice['c'] or best_choice['c'] == 350:
            variant['e'] += 1
        if 200 == best_choice['c'] or best_choice['c'] == 250:
            variant['j'] += 1

        left['e'] -= tmp_e
        left['j'] -= tmp_j

    # Mit Tageskarten auffüllen
    if not we:
        while d['nr_t'] > 0:
            tmp_e = min(6, d['e'])
            tmp_j = 6 - tmp_e

            variant['t'].append((tmp_e, tmp_j))
            d['e'] -= tmp_e
            d['j'] -= tmp_j
            d['nr_t'] -= tmp_e + tmp_j

    p = prices.price_list(we)
    c = len(variant['f']) * p['f'] + variant['e'] * p['e'] + variant['j'] * p['j']
    if not we:
        c += len(variant['t']) * p['t']

    print("KOSTEN OHNE GUTSCHEINE:")
    print(c, variant, "\n")

    # ############ GUTSCHEINE ##################
    if g == 0 or fe:
        return c, variant

    print("GUTSCHEINE:", g)

    # Extrem seltener Fall:
    # Es gibt gleich viele oder mehr Gutscheine als Personen
    if g >= d_copy['e'] + d_copy['j']:
        print("Jeder kann kostenlos ins Schwimmbad gehen!")
        return 0, {'t': [], 'f': [], 'e': d_copy['e'], 'j': d_copy['j']}

    # Einfacher Fall:
    # Es gibt gleich viele oder weniger Gutscheine als Einzelkarten
    if g <= variant['e'] + variant['j']:
        variant['e_g'] = 0
        variant['j_g'] = 0

        while variant['e'] > 0 and g > 1:
            g -= 1
            variant['e'] -= 1
            variant['e_g'] += 1
            c -= p['e']

        while variant['j'] > 0 and g > 1:
            g -= 1
            variant['j'] -= 1
            variant['j_g'] += 1
            c -= p['j']

        gutschein_gruppe = c * 0.9
        gutschein_eizel = c - p['e'] if variant['e'] > 0 else c - p['j']

        if gutschein_gruppe <= gutschein_eizel:
            variant["g_group"] = True
            c = gutschein_gruppe
        else:
            if variant['e'] > 0:
                variant['e'] -= 1
                variant['e_g'] += 1
            else:
                variant['j'] -= 1
                variant['j_g'] += 1
            c = gutschein_eizel

        return c, variant

    # Komplexer Fall:
    # Es gibt mehr Gutscheine als Einzelkarten
    if g > variant['e'] + variant['j']:
        variant['e_g'] = 0
        variant['j_g'] = 0
        while variant['e'] > 0 and g > 1:
            g -= 1
            variant['e'] -= 1
            variant['e_g'] += 1
            c -= p['e']
        while variant['j'] > 0 and g > 1:
            g -= 1
            variant['j'] -= 1
            variant['j_g'] += 1
            c -= p['j']

        # solange wie möglich Familienkarten auflösen
        variant["f"] = sorted(variant["f"])
        while g > 4 and len(variant["f"]) > 0:
            erw, jug = variant["f"].pop()
            variant["j"] += jug
            variant["e"] += erw
            c += p["e"]*variant["e"] + p["j"]*variant["j"]
            while variant['e'] > 0 and g > 1:
                g -= 1
                variant['e'] -= 1
                variant['e_g'] += 1
                c -= p['e']
            while variant['j'] > 0 and g > 1:
                g -= 1
                variant['j'] -= 1
                variant['j_g'] += 1
                c -= p['j']

        # solange wie möglich Tageskarten auflösen
        # Tageskarten als zweites, da profitabler als Familienkarten
        if "t" in variant:
            variant["t"] = sorted(variant["t"])
            while g > 6 and len(variant["t"]) > 0:
                erw, jug = variant["t"].pop()
                # print(erw, jug)
                variant["j"] += jug
                variant["e"] += erw
                c += p["e"] * variant["e"] + p["j"] * variant["j"]
                while variant['e'] > 0 and g > 1:
                    g -= 1
                    variant['e'] -= 1
                    variant['e_g'] += 1
                    c -= p['e']
                while variant['j'] > 0 and g > 1:
                    g -= 1
                    variant['j'] -= 1
                    variant['j_g'] += 1
                    c -= p['j']

        # jetzt ist 1 <= g <= 6
        kosten_gutschein_gruppe = c * 90 / 100
        # print(kosten_gutschein_gruppe)

        f_variant = copy.deepcopy(variant)
        f_g = g
        f_c = c
        if len(f_variant["f"]) > 0:
            erw, jug = f_variant["f"].pop(0)
            f_variant["e"] += erw
            f_variant["j"] += jug
            f_c -= 800
            f_c += p["e"]*erw + p["j"]*jug
            while f_variant['e'] > 0 and f_g > 0:
                f_g -= 1
                f_variant['e'] -= 1
                f_variant['e_g'] += 1
                f_c -= p['e']
            while f_variant['j'] > 0 and f_g > 0:
                f_g -= 1
                f_variant['j'] -= 1
                f_variant['j_g'] += 1
                f_c -= p['j']

        if "t" in variant:
            t_variant = copy.deepcopy(variant)
            t_g = g
            t_c = c
            if len(t_variant["t"]) > 0:
                erw, jug = t_variant["t"].pop(0)
                t_variant["e"] += erw
                t_variant["j"] += jug

                t_c -= 1100
                t_c += p["e"]*erw + p["j"]*jug
                while t_variant['e'] > 0 and t_g > 0:
                    t_g -= 1
                    t_variant['e'] -= 1
                    t_variant['e_g'] += 1
                    t_c -= p['e']
                while t_variant['j'] > 0 and t_g > 0:
                    t_g -= 1
                    t_variant['j'] -= 1
                    t_variant['j_g'] += 1
                    t_c -= p['j']

        else:
            t_c = 10000000000000000
            t_variant = None

        # print(kosten_gutschein_gruppe, f_c, t_c)
        if kosten_gutschein_gruppe <= f_c and kosten_gutschein_gruppe <= t_c:
            variant["g_group"] = True
            variant["g_left"] = g - 1
            c = kosten_gutschein_gruppe
            if len(variant['f']) > 0 and variant['g_left'] >= 1:
                tmp_g = variant['g_left']
                tmp_c = c
                tmp_variant = copy.deepcopy(variant)
                tmp_variant['f'] = sorted(tmp_variant['f'])
                tmp_e, tmp_j = tmp_variant['f'].pop(0)
                tmp_variant['e'] += tmp_e
                tmp_variant['j'] += tmp_j
                while tmp_variant['e'] > 0 and tmp_g > 0:
                    tmp_g -= 1
                    tmp_variant['e'] -= 1
                    tmp_variant['e_g'] += 1
                    tmp_variant['g_left'] -= 1
                    tmp_c -= p['e']
                while tmp_variant['j'] > 0 and tmp_g > 0:
                    tmp_g -= 1
                    tmp_variant['j'] -= 1
                    tmp_variant['j_g'] += 1
                    tmp_variant['g_left'] -= 1
                    tmp_c -= p['j']
                if tmp_c < c:
                    tmp_variant['g_left'] = tmp_g
                    return tmp_c, tmp_variant

            if 't' in variant and len(variant['t']) > 0 and variant['g_left'] >= 1:
                tmp_g = variant['g_left']
                tmp_c = c
                tmp_variant = copy.deepcopy(variant)
                tmp_variant['t'] = sorted(tmp_variant['t'])
                tmp_e, tmp_j = tmp_variant['t'].pop(0)
                tmp_variant['e'] += tmp_e
                tmp_variant['j'] += tmp_j
                while tmp_variant['e'] > 0 and tmp_g > 0:
                    tmp_g -= 1
                    tmp_variant['e'] -= 1
                    tmp_variant['e_g'] += 1
                    tmp_c -= p['e']
                while tmp_variant['j'] > 0 and tmp_g > 0:
                    tmp_g -= 1
                    tmp_variant['j'] -= 1
                    tmp_variant['j_g'] += 1
                    tmp_c -= p['j']
                if tmp_c < c:
                    tmp_variant['g_left'] = tmp_g
                    return tmp_c, tmp_variant
            return c, variant

        if f_c <= t_c and f_c <= kosten_gutschein_gruppe:
            return f_c, f_variant
        else:
            return t_c, t_variant

    return c, variant


if __name__ == '__main__':
    if len(sys.argv) == 7:
        we = sys.argv[1].lower() == 't'
        fe = sys.argv[2].lower() == 't'
        e = int(sys.argv[3])
        j = int(sys.argv[4])
        k = int(sys.argv[5])
        g = int(sys.argv[6])
    else:
        we = input("Wochenende (True|False):\n> ").lower() == 't'
        fe = input("Ferien (True|False):\n> ").lower() == 't'
        e = int(input("Erwachsene:\n> "))
        j = int(input("Jugentliche:\n> "))
        k = int(input("Kinder:\n> "))
        g = int(input("Gutscheine:\n> "))

    print(we, fe, e, j, k, g)
    lst = main(we, fe, g, k, j, e)

    print("Bester Preis\n", lst)
