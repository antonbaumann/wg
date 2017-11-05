def price_list(we):
    prices = {
            'e':  350,
            'j':  250,
            'f':  800,
            't': 1100
            }
    if not we:
        prices['e'] = prices['e'] * 4 / 5
        prices['j'] = prices['j'] * 4 / 5
    else:
        prices.pop('t')

    return prices


def sort_and_remove_duplicates(t):
    t = sorted(t, key=lambda k: k['ind'])

    c = []
    tmp = [0, 0, 0, 0]
    for e in t:
        comp = [e['e'], e['j'], e['c'], e['c_s']]
        b = True
        for i in range(len(tmp)):
            if tmp[i] != comp[i]:
               b = False
        if not b:
            c.append(e)
        tmp = comp
    return c


def remove_bad_items(t):
    end = 0
    for i in range(len(t)):
        if t[i]['ind'] > 1:
            end = i
            break
    return t[:end]



def generate_groups(e, j, prices):
    groups = []
    # Tageskarten
    t = []
    m = 6

    if 't' in prices:
        for i in range(min(e, 6) + 1):
            for k in range(min(j, 6) + 1):
                if not i == k == 0 and i + k <= 6:
                    tmp = {
                        'e': i,
                        'j': k,
                        'c': prices['t'],
                        'c_s': prices['j'] * k + prices['e'] * i,
                        'ind': prices['t'] / (prices['j'] * k + prices['e'] * i)
                    }
                    t.append(tmp)

        t = sort_and_remove_duplicates(t)
        # print("Tageskarte:")
        # show_table(t)
        # print()
        t = remove_bad_items(t)

        groups.extend(t)

    # Familenkarte
    # 1. 1E; 3J
    # 2. 2E; 2J
    f = []

    if e >= 1 and j >= 3:
        tmp = {
            'e': 1,
            'j': 3,
            'c': prices['f'],
            'c_s': prices['j'] * 3 + prices['e'] * 1,
            'ind': prices['f'] / (prices['j'] * 3 + prices['e'] * 1)
        }
        f.append(tmp)

    max_e = min(2, e)
    max_j = min(2, j)

    for i in range(max_e+1):
        for k in range(max_j+1):
            if not i == k == 0:
                tmp = {
                    'e': i,
                    'j': k,
                    'c': prices['f'],
                    'c_s': prices['j'] * k + prices['e'] * i,
                    'ind': prices['f'] / (prices['j'] * k + prices['e'] * i)
                }
                f.append(tmp)
    f = sort_and_remove_duplicates(f)
    # print("Familienkarte:")
    # show_table(f)
    # print()
    f = remove_bad_items(f)

    groups.extend(f)

    # Einzelpreise

    # Adult
    if e > 0:
        tmp = {
            'e': 1,
            'j': 0,
            'c': prices['e'],
            'c_s': prices['e'],
            'ind': 1
        }
        groups.append(tmp)

    # Adulescent
    if j > 0:
        tmp = {
            'e': 0,
            'j': 1,
            'c': prices['j'],
            'c_s': prices['j'],
            'ind': 1
        }
        groups.append(tmp)

    return sort_and_remove_duplicates(groups)


def show_table(groups):
    import texttable as tt
    tab = tt.Texttable()
    headings = ['Erw.', 'Jug.', 'Kosten', 'Kosten einzeln', 'index']
    tab.header(headings)

    for g in groups:
        tab.add_row((g['e'], g['j'], g['c'], g['c_s'], g['ind']))

    s = tab.draw()
    print(s)
    print()


def prices(e, j, we):
    prices = price_list(we)
    groups = generate_groups(e, j, prices)
    return groups

def main():
    inp = ''
    we  = None
    h   = None
    e   = 0
    j   = 0
    g   = None

    we, h, e, j = False, True, 5, 7

    # print(we, h, e, j, g)
    print(e, j, we, 0)
    prices = price_list(we)
    for p in prices:
        print(p, prices[p])
    groups = generate_groups(e, j, prices)

    show_table(groups)


if __name__ == '__main__':
    main()
