import numpy as np
import sys
from queue import *


def read_file(s):
    f = open(s, 'r')
    p = f.readlines()
    personen = []
    for i in range(0, len(p), 4):
        name = p[i].replace("\n", "")
        pro = p[i + 1].replace("\n", "").replace("+", "").split(" ")
        con = p[i + 2].replace("\n", "").replace("-", "").split(" ")

        while '' in pro:  # ineffizient -> O(n^2) Aber: Listen sehr kurz: max 2 durchläufe -> O(n)
            pro.remove('')
        while '' in con:
            con.remove('')

        person = [name, pro, con]
        personen.append(person)
    return sorted(personen)


def create_matrix(l, names):
    matrix = np.array([[0] * len(l) for _ in range(len(l))])

    for i in range(len(l)):
        pro = l[i][1]
        con = l[i][2]

        for p in pro:
            ind = names.index(p)
            matrix[i][ind] = 1
        for p in con:
            ind = names.index(p)
            matrix[i][ind] = -1

    return matrix


def operate_on_matrix(matrix):
    size = len(matrix)
    for y in range(size):
        for x in range(size):
            if matrix[y][x] == 1 and matrix[x][y] == -1:
                print("Zimmerverteilung nicht möglich!")
                sys.exit(0)
            if matrix[y][x] == 1:
                matrix[x][y] = 1
            if matrix[y][x] == -1:
                matrix[x][y] = -1


def all_visited(l):
    for i in l:
        if not i:
            return False
    return True


def get_first_non_visited(l):
    for i in range(len(l)):
        if not l[i]:
            return i


def bfs(matrix):
    adj_liste = []
    adj_liste_con = []
    room_list = []
    for y in range(len(matrix)):
        pro = []
        con = []
        for x in range(len(matrix)):
            if matrix[y][x] == 1:
                pro.append(x)
            if matrix[y][x] == -1:
                con.append(x)
        adj_liste.append(pro)
        adj_liste_con.append(con)

    visited = []
    for i in range(len(matrix)):
        visited.append(False)

    while not all_visited(visited):
        room = []
        q = Queue(maxsize=len(matrix))
        first_non_visited = get_first_non_visited(visited)
        q.put(first_non_visited)
        visited[first_non_visited] = True
        room.append(first_non_visited)

        while not q.empty():
            node = q.get()

            for child in adj_liste[node]:
                if not visited[child]:
                    # print(room)
                    # print(str(child) + " " + str(adj_liste_con[child]))
                    # print()
                    if len(set(room).intersection(adj_liste_con[child])) > 0:
                        # braucht keinen check ob schülerinnen im zimmer mit neuer schuelerin zusammen sein wollen,
                        # weil matrix gespiegelt
                        print("Zimmerverteilung nicht möglich!")
                        sys.exit()

                    q.put(child)
                    visited[child] = True
                    room.append(child)

        room_list.append(sorted(set(room)))

    return room_list


def find_room(person, zimmeraufteilung):
    for zimmer in zimmeraufteilung:
        if person[0] in zimmer:
            return zimmer


def test(zimmeraufteilung, personen):   # überprüft ob alle wünsche erfüllt wurden
    for p in personen:
        zimmer = find_room(p, zimmeraufteilung)
        for pro in p[1]:
            if pro not in zimmer:
                print(p)
                print(pro + " not in")
                print(zimmer)
                return False
        for con in p[2]:
            if con in zimmer:
                print(p)
                print(con + " in")
                print(zimmer)
                return False
    print("Alles gut!")
    return True


if __name__ == '__main__':
    personen = read_file("txt/zimmerbelegung6.txt")

    print(personen)

    schuelerListe = []
    for p in personen:
        schuelerListe.append(p[0])

    matrix = create_matrix(personen, schuelerListe)
    operate_on_matrix(matrix)
    room_list = bfs(matrix)

    print()
    print(matrix)
    print()

    room_list_namen = []
    for l in room_list:
        tmp = []
        for i in l:
            tmp.append(schuelerListe[i])
        room_list_namen.append(tmp)

    print("Zimmeraufteilung möglich!")
    for l in room_list_namen:
        print(l)

    print()
    test(room_list_namen, personen)
