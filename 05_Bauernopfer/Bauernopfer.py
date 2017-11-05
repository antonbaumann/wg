import numpy as np

class Spielfeld:
    feld = np.matrix
    def __init__(self):
        self.feld = np.matrix([[0] * 8] * 8)

    def move(self, fr, to):
        if not self.feld[fr] == 0:
            self.feld[to] = self.feld[fr]
            self.feld[fr] = 0
        else:
            print("Keine Figur auf diesem Feld!")

    def __str__(self):
        return "\n" + str(self.feld)

    def add(self, p, f):
        if self.feld[p] == 0:
            self.feld[p] = f


def main(S):
    S.add((4,0), 1)
    S.add((4,1), 1)
    S.add((4,2), 1)
    S.add((4,3), 1)
    S.add((4,4), 1)
    S.add((4,5), 1)
    S.add((4,6), 1)
    S.add((4,7), 1)
    S.add((0,4), 2)
    print(S)
    S.move(fr=(0, 0), to=(4,2))
    print(S)

if __name__ == '__main__':
    S = Spielfeld()
    main(S)
