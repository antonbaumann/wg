# CODE IST TOTAL BESCHISSEN!!!!!!!!!!!!

from itertools import permutations

def open_file(name):
    file = open(name, 'r')
    w_list = set()
    for line in file.readlines():
        line.replace('/n', '')
        w_list.add(line.strip())
    w_list = sorted(w_list)
    file.close()
    return w_list

class unique_element:
    def __init__(self,value,occurrences):
        self.value = value
        self.occurrences = occurrences

def perm_unique(elements):
    eset=set(elements)
    listunique = [unique_element(i,elements.count(i)) for i in eset]
    u=len(elements)
    return perm_unique_helper(listunique,[0]*u,u-1)

def perm_unique_helper(listunique,result_list,d):
    if d < 0:
        yield tuple(result_list)
    else:
        for i in listunique:
            if i.occurrences > 0:
                result_list[d]=i.value
                i.occurrences-=1
                for g in  perm_unique_helper(listunique,result_list,d-1):
                    yield g
                i.occurrences+=1


def is_possible(w, kuerzel):
    tmp = ""
    for i in range(0, min(3, len(w) - 1)):
        tmp += w[i]
        if len(w) == 4 and i == 0:
            continue
        if tmp in kuerzel:
            return True
    return False


def test_if_possible(word, kuerzel):
    word = word.strip()
    print(len(word))
    permutations = set()
    tmp = []
    for a in range(0, len(word)//2+1):
        for b in range(0, len(word)//3+1):
            for c in range(0, len(word)//4+1):
                if len(word) == a*2 + b*3 + c*4:
                    tmp.append([a, b, c])
    # print(tmp)
    muster = []
    for v in tmp:
        s = []
        for i in range(3):
            while v[i] > 0:
                s.append(i+2)
                v[i] -= 1
        muster.append(s)

    print(muster)

    c = 0
    for m in muster:
        c += 1
        print(str(c) + ' / ' + str(len(muster)))
        permutations.update(list(perm_unique(m)))

    c = 0
    for p in permutations:
        c += 1
        ind = 0
        b = True
        tmp = []
        for e in p:
            tmp = word[ind:ind+e]
            ind += e
        for w in tmp:
            if not is_possible(w, kuerzel):
                b = False
                break
        if b:
            print("Möglich!")
            print(tmp)
            return True
    print("Nicht möglich")
    print()
    print()





if __name__ == '__main__':
    kuerzel = open("../txt/kuerzelliste.txt")
    autoscrabble = open("../txt/autoscrabble.txt")

    for word in autoscrabble:
        test_if_possible(word, kuerzel)