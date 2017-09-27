
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

        print(pre, post)

        if len(post) >= 3:
            continue

        # Ueberprueft ob pre in kuerzelliste ist
        # Ueberprueft ob Umlaute in post
        if pre in KUERZEL and not any((c in umlaute) for c in post):
            return True

    return False

if __name__ == '__main__':
    global KUERZEL
    KUERZEL = open_file("../txt/kuerzelliste.txt")

    while True:
        print(is_possible(input("word: ")))
