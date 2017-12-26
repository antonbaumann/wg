#! /usr/bin/env python3
# encoding: utf-8

# by Anton Baumann

import sys


def open_file(name):
    with open(name, 'r', encoding='UTF-8') as file:
        return sorted({line.strip() for line in file.readlines()})


def is_possible(s, kuerzel):
    if len(s) > 5: return False
    umlaute = set('ÄÖÜ')
    s = s.upper().strip()
    for i in range(1, min(len(s), 4)):
        # Teilt String in 2 Teile
        pre, post = s[:i], s[i:]
        # Zweiter Teil darf laut Aufgabestellung nicht >2 sein
        if len(post) > 2: continue
        if not any((c in umlaute) for c in post) and pre in kuerzel:
            return True
    return False


def find_words(wordlist, kuerzel):
    w_list, k_list = open_file(wordlist), open_file(kuerzel)
    return sorted(set([word for word in w_list if not is_possible(word, k_list)]))


if __name__ == '__main__':
    if len(sys.argv) > 1:
        nr_letters = str(sys.argv[1])
    else:
        print("Usage:", "4b.py [n]")
        sys.exit()

    wordlist = "wordlist.txt"
    kuerzel = "../txt/kuerzelliste.txt"
    words = find_words(wordlist, kuerzel)
    [print(w.upper()) for w in words if len(w) == int(nr_letters)]
