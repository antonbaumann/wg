import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap
import random


def r(t):
    if len(t) != 2:
        print("Länge muss 2 sein!")
        return None
    return t[1], t[0]


class Spielfeld:
    feld = np.matrix([[0] * 8] * 8)
    bauern = []
    turm = []

    # Visualisiert spielfeld
    def show(self):
        cmap = ListedColormap(['white', 'black', 'grey', 'red', 'yellow'])
        row_labels = range(1, 9)
        col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        self.prepare()
        plt.matshow(self.feld, cmap=cmap)
        plt.xticks(range(8), col_labels)
        plt.yticks(range(8), row_labels)
        plt.show()

    def print(self):
        print(self.feld)

    # Fügt Schachfigur auf Feld und in Liste hinzu
    def add(self, x, y, fig):
        # Feld besetzt -> Keine Figur hinzufügen
        if self.feld[y, x] != 0:
            return False

        # Bauer wird in liste angehängt
        if fig == 1:
            self.bauern.append((x, y))

        # Bauer wird in liste angehängt
        elif fig == 2:
            self.turm.append((x, y))
        # Bauer :=1 Turm := 2 Rest -> Fehlermeldung
        else:
            print("Error:\n1 -> B\n2 -> T")
            return False
        self.feld[y, x] = fig

    def prepare(self):
        # löscht alle als Bedroht markierten Felder
        for x in range(8):
            for y in range(8):
                if self.feld[y, x] in (3, 4):
                    self.feld[y, x] = 0

        for b in self.bauern:
            for m in self.possible_moves(b, 1):
                if self.feld[r(m)] == 0:
                    self.feld[r(m)] = 3

        tmp = set()
        for t in self.turm:
            for m in self.possible_moves(t, 2):
                tmp.add(m)
        if self.turm[0] in tmp:
            tmp.remove(self.turm[0])
        for e in tmp:
            self.feld[r(e)] = 4

    def next_move(self, a):
        # if Bauer
        if a == 1:
            best = [(100, tuple(), tuple())]
            for i in range(len(self.bauern)):
                b = self.bauern[i]
                for m in self.possible_moves(b, 1):
                    self.feld[r(m)] = 1
                    self.feld[r(b)] = 0
                    self.bauern[i] = m

                    self.prepare()
                    s = len(self.possible_moves(self.turm[0], 2))

                    # print(b, m, s)
                    # print(self.possible_moves(self.turm[0], 2))
                    # print(self.feld)
                    # self.show()

                    if s == best[0][0]:
                        best.append((s, b, m))
                    if s < best[0][0]:
                        best = [(s, b, m)]

                    self.feld[r(m)] = 0
                    self.feld[r(b)] = 1
                    self.bauern[i] = b

            c = random.choice(best)
            print("####################")
            print("Bauer:")
            print(best)
            print(c)
            print("####################")

            self.feld[r(c[1])] = 0
            self.feld[r(c[2])] = 1
            self.bauern.remove(c[1])
            self.bauern.append(c[2])

        if a == 2:
            best = [(0, tuple(), tuple())]
            for t in self.turm:
                for m in self.possible_moves(t, 2):

                    self.prepare()
                    s = len(self.possible_moves(t, 2))
                    if s == best[0][0]:
                        best.append((s, t, m))
                    if s > best[0][0]:
                        best = [(s, t, m)]

            c = random.choice(best)
            print("####################")
            print("Turm:")
            print(best)
            print(c)
            print("####################")

            self.feld[r(c[1])] = 0
            self.feld[r(c[2])] = 2
            self.turm.remove(c[1])
            self.turm.append(c[2])



    def possible_moves(self, XY, a):
        # if Bauer
        if a == 1:
            moves = set()

            pos = (XY[0] + 1, XY[1])
            moves.add(pos)
            pos = (XY[0] - 1, XY[1])
            moves.add(pos)
            pos = (XY[0], XY[1] + 1)
            moves.add(pos)
            pos = (XY[0], XY[1] - 1)
            moves.add(pos)

            # Felder außerhalb [0, 7] werden entfernt
            moves = [m for m in moves if all(0 <= x <= 7 for x in m)]
            # Wenn Feld schon von anderem Bauern besetzt ist wird auch dieses entfernt
            moves = [m for m in moves if self.feld[r(m)] != 1]
            return moves

        # if Turm
        if a == 2:
            moves = set()
            direction = ((-1, -1), (8, 1))

            # Feld selbst "Zug der Länge 0"
            moves.add(XY)
            # Vertically
            for e, s in direction:
                for i in range(XY[1], e, s):
                    if self.feld[i, XY[0]] == 1:
                        break
                    if self.feld[i, XY[0]] in (0, 4):
                        moves.add((XY[0], i))
            # Horizontally
            for e, s in direction:
                for i in range(XY[0], e, s):
                    if self.feld[XY[1], i] == 1:
                        break
                    if self.feld[XY[1], i] in (0, 4):
                        moves.add((i, XY[1]))

            return sorted(moves)


def main():
    F = Spielfeld()

    F.add(0, 4, 1)
    F.add(1, 4, 1)
    F.add(2, 4, 1)
    F.add(3, 4, 1)
    F.add(4, 4, 1)
    F.add(5, 4, 1)
    F.add(6, 4, 1)
    F.add(7, 4, 1)

    # F.add(0, 0, 1)
    # F.add(1, 1, 1)
    # F.add(2, 2, 1)
    # F.add(3, 3, 1)
    # F.add(4, 4, 1)
    # F.add(5, 5, 1)
    # F.add(6, 6, 1)
    # F.add(7, 7, 1)
    #
    F.add(6, 1, 2)

    p = 1
    while True:
        F.next_move(p)
        F.show()
        if len(F.possible_moves(F.turm[0], 2)) == 1:
            break
        if p == 1:
            p = 2
        else:
            p = 1


if __name__ == '__main__':
    main()
