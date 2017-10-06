def price_list(we, g):
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

    if g:
        prices['f'] = prices['f'] * 9 / 10
        if not we:
            prices['t'] = prices['t'] * 9 / 10

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


def remove_bad_items(t, param):
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
        # Fill wih adults
        for i in range(1, min(m, e)+1):
            tmp = {
                'e': i,
                'j': 0,
                'c': prices['t'],
                'c_s': prices['e'] * i,
                'ind': prices['t'] / (prices['e'] * i)
            }
            t.append(tmp)

        # Fill with adolescents
        for i in range(1, min(m, j)+1):
            tmp = {
                'e': 0,
                'j': i,
                'c': prices['t'],
                'c_s': prices['j'] * i,
                'ind': prices['t'] / (prices['j'] * i)
            }
            t.append(tmp)

        # mix
        c_e, c_j = e, 0
        if c_e >= 6: c_e = 5
        while c_e >= 0 and c_j <= j:
            tmp = {
                'e': c_e,
                'j': c_j,
                'c': prices['t'],
                'c_s': prices['j'] * c_j + prices['e'] * c_e,
                'ind': prices['t'] / (prices['j'] * c_j + prices['e'] * c_e)
            }
            c_e -= 1
            c_j += 1
            t.append(tmp)

        t = sort_and_remove_duplicates(t)
        t = remove_bad_items(t, 1)

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
    f = remove_bad_items(f, 1)

    groups.extend(f)

    # Einzelpreise

    # Adult
    tmp = {
        'e': 1,
        'j': 0,
        'c': prices['e'],
        'c_s': prices['e'],
        'ind': 1
    }
    groups.append(tmp)

    # Adulescent
    tmp = {
        'e': 0,
        'j': 1,
        'c': prices['j'],
        'c_s': prices['j'],
        'ind': 1
    }
    groups.append(tmp)

    return sort_and_remove_duplicates(groups)


def main():
    inp = ''
    we  = None
    h   = None
    e   = 0
    j   = 0
    g   = None

    we, h, e, j, g = False, True, 6, 6, 0

    print(we, h, e, j, g)
    prices = price_list(we, g)
    for p in prices:
        print(p, prices[p])
    groups = generate_groups(e, j, prices)

    for g in groups:
        print(g)


if __name__ == '__main__':
    main()
