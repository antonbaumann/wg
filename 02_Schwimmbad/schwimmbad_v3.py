#! /usr/bin/env python3

import math
import prices
import copy


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
        all = d['e'] + d['j']
        # mit einer Tageskarte können 6 Personen ins Schwimmbad
        d['r'] = all - math.floor(all / 6) * 6
        d['nr_t'] = all - d['r']

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
        # print(d)
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

    while d['r'] > 0:
        # print(left)
        if tmp_j > 0:
            left['j'] += 1
            tmp_j -= 1
        else:
            left['e'] += 1
        d['r'] -= 1

    while left['e'] + left['j'] > 0:
        # print(left)
        table = prices.prices(left['e'], left['j'], we, 0)
        row_to_use = table[0]

        tmp_e, tmp_j = row_to_use['e'], row_to_use['j']

        if row_to_use['c'] == 1100:
            variant['t'].append((tmp_e, tmp_j))
        if row_to_use['c'] == 800:
            variant['f'].append((tmp_e, tmp_j))
        if 280 == row_to_use['c'] or row_to_use['c'] == 350:
            variant['e'] += 1
        if 200 == row_to_use['c'] or row_to_use['c'] == 250:
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


    ############# GUTSCHEINE ##################
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

        while variant['e'] > 0 and g > 0:
            g -= 1
            variant['e'] -= 1
            variant['e_g'] += 1
            c -= p['e']

        while variant['j'] > 0 and g > 0:
            g -= 1
            variant['j'] -= 1
            variant['j_g'] += 1
            c -= p['j']

        return c, variant

    # Komplexer Fall:
    # Es gibt mehr Gutscheine als Einzelkarten
    if g > variant['e'] + variant['j']:
        print("Variant 3:")
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
            variant["e_g"] += erw
            variant["j_g"] += jug
            c -= 800
            g -= 4

        # solange wie möglich Tageskarten auflösen
        # Tageskarten als zweites, da profitabler als Familienkarten
        if "t" in variant:
            variant["t"] = sorted(variant["t"])
            while g > 6 and len(variant["t"]) > 0:
                erw, jug = variant["t"].pop()
                variant["e_g"] += erw
                variant["j_g"] += jug
                c -= 1100
                g -= 6

        # jetzt ist 1 <= g <= 6
        kosten_gutschein_gruppe = c * 90 / 100

        f_variant = copy.deepcopy(variant)
        f_g = g
        f_c = c
        if len(f_variant["f"]) > 0:
            erw, jug = f_variant["f"].pop()
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
                erw, jug = t_variant["t"].pop()

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

        if kosten_gutschein_gruppe <= f_c and kosten_gutschein_gruppe <= t_c:
            return kosten_gutschein_gruppe, variant
        if f_c <= t_c and f_c <= kosten_gutschein_gruppe:
            return f_c, f_variant
        else:
            return t_c, t_variant

    return c, variant


if __name__ == '__main__':
    we = True
    fe = False
    g = 18
    k = 10
    j = 11
    e = 7

    lst = main(we, fe, g, k, j, e)
    print(lst)
