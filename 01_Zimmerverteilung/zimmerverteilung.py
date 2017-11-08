#! /usr/bin/env python3

# by Anton Baumann

import sys
import numpy as np

def read_file(s):
    f = open(s, 'r')
    p = f.readlines()
    personen = []
    for i in range(0, len(p), 4):
        name = p[i].replace("\n", "")
        pro = p[i + 1].replace("\n", "").replace("+", "").split(" ")
        con = p[i + 2].replace("\n", "").replace("-", "").split(" ")

        # entfernt leere Einträge in Liste
        while '' in pro:
            pro.remove('')
        while '' in con:
            con.remove('')

        person = [name, pro, con]
        personen.append(person)
    f.close()
    return sorted(personen)


# erstellt eine Beziehungsmatrix
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

# spiegelt Beziehungsmatrix wenn möglich
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
    for b in l:
        if not b:
            return False
    return True


def get_first_non_visited(l):
    for i in range(len(l)):
        if not l[i]:
            return i

# Modifizierte iterative Implementierung der Breitensuche
# Hier werden durch zwei ungerichtete Graphen die Zusammenhangskomponenten herausgesucht
def bfs(matrix):
    # Adjazenzliste für Graph_1
    adj_liste_pro = []
    # Adjazenzliste für Graph_2
    adj_liste_con = []
    room_list = []

    # Adjazenzmatrix wird in zwei Adjazenzlisten konvertiert
    for y in range(len(matrix)):
        pro = []
        con = []
        for x in range(len(matrix)):
            if matrix[y][x] == 1:
                pro.append(x)
            if matrix[y][x] == -1:
                con.append(x)
        adj_liste_pro.append(pro)
        adj_liste_con.append(con)

    # hier wird gespeichert, ob ein Knoten schon besucht wurde
    visited = [False] * len(matrix)
    q = []

    while not all_visited(visited):
        # Raum = Zusammenhangskomponente
        room = []

        # Erster Knoten im Graph wird
        # der Warteschlange hinzugefügt,
        node = get_first_non_visited(visited)
        q.append(node)
        # als besucht markiert,
        visited[node] = True
        # dem Zimmer hinzugefügt
        room.append(node)

        # fügt alle vom `first_non_visited` Knoten erreichbaren Knoten der Raumliste hinzu
        while not len(q) == 0:
            node = q.pop(0)
            for child in adj_liste_pro[node]:
                if not visited[child]:
                    if len(set(room).intersection(adj_liste_con[child])) > 0:
                        # braucht keinen Check ob Schülerinnen im Zimmer mit neuer Schuelerin zusammen sein wollen,
                        # weil matrix gespiegelt
                        print("Zimmerverteilung nicht möglich! Person:", child)
                        # gibt Person aus, bei der das "Problem" ausgelöst wurde
                        sys.exit()
                    q.append(child)
                    visited[child] = True
                    room.append(child)
        room_list.append(sorted(set(room)))
    return room_list


def find_room(person, zimmeraufteilung):
    for zimmer in zimmeraufteilung:
        if person[0] in zimmer:
            return zimmer


# überprüft ob abgegebe Listen Sinn ergeben,
# zum Beispiel steht Marie in "zimmerbelegung5.txt" auf ihrer eigenen Kontra Liste
def check(personen):
    names_1 = set()
    names_2 = set()
    for pers in personen:
        names_1.add(pers[0])
        names_2.add(pers[0])
        names_1.update(pers[1])
        names_1.update(pers[2])
        if pers[0] in pers[2]:
            print()
            print("[INFO]", pers[0] + " steht auf ihrer eigenen Kontra-Liste!")
            print("[INFO]", pers[0] + " wird von " + str(pers[2]) + " entfernt.")
            pers[2].remove(pers[0])

    for n in names_1 - names_2:
        print("[INFO]", n, "wurde erwähnt, hat jedoch selbst keinen Zettel abgegeben.")
        personen.append([n, [], []])



def zimmeraufteilung(personen):
    check(personen)

    schuelerListe = []
    for p in personen:
        schuelerListe.append(p[0])

    matrix = create_matrix(personen, schuelerListe)

    operate_on_matrix(matrix)   # Spiegelt Matrix wenn möglich
    room_list = bfs(matrix)

    room_list_namen = []
    for l in room_list:
        tmp = []
        for i in l:
            tmp.append(schuelerListe[i])
        room_list_namen.append(tmp)

    print("Zimmeraufteilung möglich!")
    for l in room_list_namen:
        print(l)

    return room_list_namen, personen


if __name__ == '__main__':
    path = sys.argv[1]
    personen = read_file(path)
    zimmeraufteilung(personen)
