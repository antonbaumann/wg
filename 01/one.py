import numpy as np
import sys
from queue import *

def readFile(s):
    f = open(s, 'r')
    p = f.readlines()
    personen = []
    for i in range(0, len(p), 4):
        name = p[i].replace("\n", "")
        pro =  p[i+1].replace("\n", "").replace("+", "").split(" ")
        con =  p[i+2].replace("\n", "").replace("-", "").split(" ")

        while '' in pro:    # ineffizient -> O(n^2) Aber: Listen sehr kurz: max 2 durchläufe -> O(n)
            pro.remove('')
        while '' in con:
            con.remove('')

        person = [name, pro, con]
        personen.append(person)
    return sorted(personen)

def createMatrix(l, names):
    matrix = np.array([ [0] * len(l) for _ in range(len(l))])

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

def operateOnMatrix(matrix):
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

def allVisited(l):
    for i in l:
        if not i:
            return False
    return True

def getFirstNotVisited(l):
    for i in range(len(l)):
        if not l[i]:
            return i


def BFS(matrix):
    adjListe = []
    adjListeCon = []
    roomList = []
    for y in range(len(matrix)):
        tmp = []
        con = []
        for x in range(len(matrix)):
            if matrix[y][x] == 1:
                tmp.append(x)
            if matrix[y][x] == -1:
                con.append(x)
        adjListe.append(tmp)
        adjListeCon.append(con)

    visited = []
    for i in range(len(matrix)):
        visited.append(False)

    while not allVisited(visited):
        room = []
        q = Queue(maxsize=len(matrix))
        firstNotVisited = getFirstNotVisited(visited)
        q.put(firstNotVisited)
        visited[firstNotVisited] = True
        room.append(firstNotVisited)

        while not q.empty():
            node = q.get()

            for child in adjListe[node]:
                if not visited[child]:
                    print(room)
                    print(str(child) + " " + str(adjListeCon[child]))
                    print()
                    if len(set(room).intersection(adjListeCon[child])) > 0:
                        print("Zimmerverteilung nicht möglich!")
                        sys.exit()

                    q.put(child)
                    visited[child] = True
                    room.append(child)

        roomList.append(sorted(set(room)))

    return roomList

def main():
    personen = readFile("zimmerbelegung/zimmerbelegung10")
    schuelerListe = []
    for p in personen:
        schuelerListe.append(p[0])

    adjazenzmatrix = createMatrix(personen, schuelerListe)
    operateOnMatrix(adjazenzmatrix)
    roomList = BFS(adjazenzmatrix)

    print(adjazenzmatrix)

    roomListNamen = []
    for l in roomList:
        tmp = []
        for i in l:
            tmp.append(schuelerListe[i])
        roomListNamen.append(tmp)

    print("Zimmeraufteilung möglich!")
    for l in roomListNamen:
        print(l)

main()