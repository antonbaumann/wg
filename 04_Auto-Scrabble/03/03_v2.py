import time

# Debug print() an/aus
v = False


# Liest ein Textfile ein
# Gibt eine alphabetisch sortierte Liste von Strings zurück
def open_file(name):
    file = open(name, 'r')
    w_list = set()
    for line in file.readlines():
        line.replace('/n', '')
        w_list.add(line.strip())
    w_list = sorted(w_list)
    file.close()
    return w_list


# mit bin_search und ohne output:    0.00542 s
# mit naiver suche und ohne output:  0.81236 s
# O(log n)
def binary_search(lst, target):
    min = 0
    max = len(lst) - 1
    avg = (min + max) // 2
    while min < max:
        if lst[avg] == target:
            return True
        elif lst[avg] < target:
            return binary_search(lst[avg + 1:], target)
        else:
            return binary_search(lst[:avg], target)
    return False

# überprüft ob String s auf einem einzelnen Numernschild darstellbar ist
# O(log n)
def is_possible(s):
    umlaute = set('ÄÖÜ')
    s = s.upper().strip()
    for i in range(1, min(len(s), 4)):  # O(1)
        # Teilt String in 2 Teile
        pre = s[:i]
        post = s[i:]

        # Zweiter Teil darf laut Aufgabestellung nicht >2 sein
        if len(post) > 2:
            continue

        # Ueberprueft ob pre in kuerzelliste ist
        # Ueberprueft ob Umlaute in post
        # triviale suche -> if pre in KUERZEL and not any((c in umlaute) for c in post):
        if not any((c in umlaute) for c in post) and binary_search(KUERZEL, pre):
            return True
    return False


def check(word):
    START, STOP, STEP = 5, 2, -1
    stack = [[0, START]]
    i, n = 0, STOP
    while i < len(word):
        if v: print(stack)
        i, n = stack[len(stack) - 1]
        tmp = word[i:i + n]
        if is_possible(tmp):
            stack.append([i + n, START])
        else:
            if STEP < 0 and n > STOP or STEP > 0 and n < STOP:
                i, n = stack.pop()
                n += STEP
                stack.append([i, n])
            else:
                stack.pop()
                if len(stack) == 0:
                    print("Nicht darstellbar!")
                    return False
                i, n = stack.pop()
                n += STEP
                stack.append([i, n])

    stack.pop()  # letzter vorberechneter eintrag wird gelöscht

    print("Darstellbar!")

    comb = []
    for i, n in stack:
        comb.append(word[i: i + n])

    print(comb)
    return True


if __name__ == '__main__':
    global KUERZEL
    KUERZEL = open_file("../txt/kuerzelliste.txt")
    AUTOSCRABBLE = open_file("../txt/autoscrabble.txt")

    start = time.time()
    for word in AUTOSCRABBLE:
        print(word)
        check(word)
        print()
    end = time.time()

    print(end - start)
