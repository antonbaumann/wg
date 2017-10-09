import math
import prices


def f_makes_sense(e, j):
    if e >= 1 and j >= 3:
        return True
    if e >= 2 and j >= 2:
        return True
    return


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

    # Am Wochenende werden keine Tageskarten verkauft
    # -> Tageskarten werden aus dict(d) entfernt
    if we:
        d.pop('nr_t')

    # wenn !Wochenende -> Tageskarten werden verkauft
    if not we:
        all = d['e'] + d['j']
        # mit einer Tageskarte können 6 Personen ins Schwimmbad
        #
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

    # Familienkarten werden auf
    while f_makes_sense(d['e'], d['j']):
        print(d)
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

    left = {'e': 0, 'j': 0}
    tmp_j = d['j']
    while d['r'] > 0:
        if tmp_j > 0:
            left['j'] += 1
            tmp_j -= 1
        else:
            left['e'] += 1
        d['r'] -= 1

    while left['e'] + left['j'] > 0:
        print(left)
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
        while d['e'] > 0 and d['j'] > 0:
            tmp_e = min(6, d['e'])
            tmp_j = 6 - tmp_e

            variant['t'].append((tmp_e, tmp_j))
            d['e'] -= tmp_e
            d['j'] -= tmp_j

    p = prices.price_list(we)
    c = len(variant['f']) * p['f'] + variant['e'] * p['e'] + variant['j'] * p['j']
    if not we:
        c += len(variant['t']) * p['t']

    print(c, variant)
    return variant


if __name__ == '__main__':
    we = True
    fe = False
    g = 1
    k = 1
    j = 10
    e = 9

    lst = main(we, fe, g, k, j, e)
