import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap


class Spielfeld:
    feld = np.matrix([[0] * 8] * 8)
    bauern = []
    turm = []

    def remove_poss_moves_turret(self):
        for x in range(8):
            for y in range(8):
                if self.feld[y, x] == 4:
                    self.feld[y, x] = 0

    def add_if_zero(self, n, y, x):
        if y in range(8) and x in range(8) and self.feld[y, x] == 0:
            self.feld[y, x] = n

    def visualize(self):
        cmap = ListedColormap(['w', 'k', 'b', 'r', 'y'])
        row_labels = range(1, 9)
        col_labels = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H']
        plt.matshow(self.feld, cmap=cmap)
        plt.xticks(range(8), col_labels)
        plt.yticks(range(8), row_labels)
        plt.show()

    def add_chessman(self, fig, x, y):
        if self.feld[y, x] != 0:
            print()
            print(x, y)
            print("Feld besetzt!")
            return False
        if fig == 1:
            self.bauern.append((x, y))
            for b in self.bauern:
                self.possible_moves(b, 1)
        elif fig == 2:
            self.turm.append((x, y))
        else:
            print("Error:\n1 -> B\n2 -> T")
            return False

        self.feld[y, x] = fig

    def pawn_next_move(self):
        best = [tuple(), tuple(), 100]
        for b in self.bauern:
            for m in self.possible_moves(b, 1):
                self.feld[b[1], b[0]] = 0
                self.feld[m[1], m[0]] = 1
                tmp = self.possible_moves(self.turm[0], 8)
                if len(tmp) <= best[2]:
                    best = [b, m, len(tmp)]
                self.feld[b[1], b[0]] = 1
                self.feld[m[1], m[0]] = 0




    def turret_next_move(self):
        if len(self.turm) != 1:
            print("Es muss sich genau ein Turm auf dem Spielfeld befinden!")
            return False

        print(self.feld)
        self.visualize()
        return

        best = [tuple(), -1]

        moves = self.possible_moves(self.turm[0], 8)
        for f in moves:
            f = (f[1], f[0])
            tmp = self.possible_moves(f, 1)
            # print(len(tmp))
            # print(best)
            if len(tmp) > best[1]:
                best[0] = f
                best[1] = len(tmp)

        self.turm.append(best[0])
        r = self.turm.pop(0)

        self.feld[r[1], r[0]] = 0
        self.feld[best[0][1], best[0][0]] = 2

        self.possible_moves(self.turm[0], 8)
        self.visualize()


    def possible_moves(self, pos):
        fields = set()
        p_from = pos

        self.remove_poss_moves_turret()

        # Down
        for i in range(p_from[1], 8):
            if self.feld[i, p_from[0]] == 1:
                break
            if self.feld[i, p_from[0]] == 0:
                fields.add((i, p_from[0]))
        # Up
        for i in range(p_from[1], -1, -1):
            if self.feld[i, p_from[0]] == 1:
                break
            if self.feld[i, p_from[0]] == 0:
                fields.add((i, p_from[0]))
        # Left
        for i in range(p_from[0], -1, -1):
            if self.feld[p_from[1], i] == 1:
                break
            if self.feld[p_from[1], i] == 0:
                fields.add((p_from[1], i))
        # Right
        for i in range(p_from[0], 8):
            if self.feld[p_from[1], i] == 1:
                break
            if self.feld[p_from[1], i] == 0:
                fields.add((p_from[1], i))

        print(fields)
        if n == 8:
            for f in fields:
                if self.feld[f] != 2:
                    self.feld[f] = 4
        else:
            for f in fields:
                if self.feld[f] != 1:
                    self.feld[f] = 3

        # self.visualize()
        print(self.feld)
        print()
        print()
        print()
        return fields


if __name__ == '__main__':
    F = Spielfeld()
    F.add_chessman(1, 0, 0)
    F.add_chessman(1, 0, 1)
    F.add_chessman(1, 0, 2)
    F.add_chessman(1, 2, 3)
    F.add_chessman(1, 4, 4)
    F.add_chessman(1, 6, 5)
    F.add_chessman(1, 2, 6)
    F.add_chessman(1, 3, 7)
    F.add_chessman(2, 6, 2)

    F.turret_next_move()
