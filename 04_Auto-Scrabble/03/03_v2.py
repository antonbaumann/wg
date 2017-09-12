
def open_file(name):
    file = open(name, 'r')
    w_list = set()
    for line in file.readlines():
        line.replace('/n', '')
        w_list.add(line.strip())
    w_list = sorted(w_list)
    file.close()
    return w_list


def is_possible(s):
    umlaute = set('ÄÖÜ')
    s = s.upper().strip()
    for i in range(1, min(len(s), 4)):
        pre = s[:i]
        post = s[i:]

        # print(pre, post)

        if len(post) >= 3:
            continue

        # Ueberprueft ob pre in kuerzelliste ist
        # Ueberprueft ob Umlaute in post
        if pre in KUERZEL and not any((c in umlaute) for c in post):
            return True

    return False


def check(word):
    stack = [[0, 3]]
    i, n = 0, 3
    while True:
        i, n = stack[len(stack)-1]
        if i >= len(word):
            break
        tmp = word[i:i+n]
        if is_possible(tmp):
            stack.append([i+n, 3])
        else:
            if n < 5:
                i, n = stack.pop()
                n += 1
                stack.append([i, n])
            else:
                #
                stack.pop()
                if len(stack) == 0:
                    print("Nicht darstellbar!")
                    return False
                i, n = stack.pop()
                n += 1
                stack.append([i, n])

    stack.pop()     # letzter vorberechneter eintrag wird gelöscht

    print("Darstellbar!")

    comb = []
    for i, n in stack:
        comb.append(word[i: i+n])

    print(comb)
    return True


if __name__ == '__main__':
    global KUERZEL
    KUERZEL = open_file("../txt/kuerzelliste.txt")
    AUTOSCRABBLE = open_file("../txt/autoscrabble.txt")

    for word in AUTOSCRABBLE:
        print(word)
        check(word)
        print()
