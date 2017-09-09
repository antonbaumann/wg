def open_file(name):
    file = open(name, 'r')
    w_list = set()
    for line in file.readlines():
        w_list.add(line.strip())
    w_list = sorted(w_list)
    file.close()
    return w_list

def find_words(wordlist, kuerzel):
    ret = []
    w_list = open_file(wordlist)
    k_list = open_file(kuerzel)
    for word in w_list:
        tmp = ""
        for i in range(0, min(3, len(word)-1)):
            tmp += word[i]
            if len(word) == 4 and i == 0:
                continue
            if tmp in k_list:
                ret.append(word)
    return sorted(set(ret))



if __name__ == '__main__':
    wordlist = "wordlist_max_4.txt"
    kuerzel = "../txt/kuerzelliste.txt"
    words = find_words(wordlist, kuerzel)
    for w in words:
        if len(w) == 4:
            print(w)
