import copy
import re

import time

letters = "ABCDEFGH"
digits = "87654321"

# Bsp: 'A1' -> 7, 0
def str_to_coord(s):
    r = re.compile('[A-H][1-8]')
    if r.match(s):
        return digits.find(s[0]), letters.find(s[1])

# Bsp: (7, 0) -> 'A1'
def coord_to_str(pos):
    return coords_to_str(pos[0], pos[1])

# Bsp: 7, 0 -> 'A1'
def coords_to_str(y, x):
    if 0 <= y <= 7 and 0 <= x <= 7:
        return letters[x] + digits[y]

# Bsp: [(7, 0), (7, 1)] -> ['A1', 'B1']
def coord_list_to_str(lst):
    return [coord_to_str(x) for x in lst]

# Gibt zurück ob p von einem Bauern erreicht werden kann
def is_threatened(p, board):
    surr = {(p[0] - 1, p[1]), (p[0] + 1, p[1]), (p[0], p[1] - 1), (p[0], p[1] + 1)}
    surr = {pos for pos in surr if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7}

    for box in surr:
        if board[box[0]][box[1]].is_pawn():
            return True
    return False

# Oberklasse: Schachfigur
class Chessman:
    def __init__(self, y, x):
        self.pos = (y, x)

    def is_pawn(self):
        return False

    def is_rook(self):
        return False


# Leeres Feld
class EmptyField(Chessman):
    CHAR = '.'

    def __str__(self):
        return self.CHAR


# Bauer
class Pawn(Chessman):
    CHAR = '♙'

    def is_pawn(self):
        return True

    def __str__(self):
        return self.CHAR

    def possible_moves(self, pawns):
        p = self.pos
        moves = {(p[0]-1, p[1]), (p[0]+1, p[1]), (p[0], p[1]-1), (p[0], p[1]+1)}
        moves = {pos for pos in moves if 0 <= pos[0] <= 7 and 0 <= pos[1] <= 7}
        moves -= set(pawns)
        return sorted(moves)


# Turm
class Rook(Chessman):
    CHAR = '♜'

    def is_rook(self):
        return True

    def __str__(self):
        return self.CHAR

    def possible_moves(self, board):
        p = self.pos
        moves = []
        # Top
        for y in range(p[0], -1, -1):
            if board[y][p[1]].is_pawn():
                break
            if not is_threatened((y, p[1]), board):
                moves.append((y, p[1]))
        # Bottom
        for y in range(p[0], 8, 1):
            if board[y][p[1]].is_pawn():
                break
            if not is_threatened((y, p[1]), board):
                moves.append((y, p[1]))
        # Left
        for x in range(p[1], -1, -1):
            if board[p[0]][x].is_pawn():
                break
            if not is_threatened((p[0], x), board):
                moves.append((p[0], x))
        # Right
        for x in range(p[1], 8, 1):
            if board[p[0]][x].is_pawn():
                break
            if not is_threatened((p[0], x), board):
                moves.append((p[0], x))

        return sorted(set(moves))


# Spielbrett
class Board:
    def __init__(self):
        self.boxes = [[EmptyField(y, x) for x in range(8)] for y in range(8)]
        self.pawns = []
        self.rooks = []

    def add_pawn(self, y, x):
        p = Pawn(y, x)
        self.pawns.append(p)
        self.boxes[y][x] = p

    def add_rook(self, y, x):
        r = Rook(y, x)
        self.rooks.append(r)
        self.boxes[y][x] = r

    def move(self, chessman, to):
        if chessman.is_pawn() or chessman.is_rook():
            self.boxes[to[0]][to[1]] = self.boxes[chessman.pos[0]][chessman.pos[1]]
            if not to == chessman.pos:
                self.boxes[chessman.pos[0]][chessman.pos[1]] = EmptyField(chessman.pos[0], chessman.pos[1])
            chessman.pos = to

    def __str__(self):
        string = ""
        n = 8
        for r in self.boxes:
            string += str(n) + " "
            n -= 1
            for c in r:
                string += str(c) + " "
            string += "\n"
        string += "  A B C D E F G H"
        return string

    def print_pawns(self):
        s = ""
        for p in self.pawns:
            s += str(coord_to_str(p.pos))
        print(s)


class Game:
    B = Board()
    rook_next = True

    def __init__(self):
        self.B.add_pawn(4, 0)
        self.B.add_pawn(4, 1)
        self.B.add_pawn(4, 2)
        self.B.add_pawn(4, 3)
        self.B.add_pawn(4, 4)
        self.B.add_pawn(4, 5)
        self.B.add_pawn(4, 6)
        self.B.add_rook(0, 7)

    # Ruft possible_moves in Pawn auf.
    # Übergibt eine Liste der Positionen aller Bauern
    def possible_moves_pawn(self, pawn, pawns_pos=B.pawns):
        return pawn.possible_moves(pawns_pos)

    # Ruft possible_moves in Rook auf.
    # Übergibt Spielfeld
    def possible_moves_rook(self, rook, boxes=B.boxes):
        return rook.possible_moves(boxes)

    # Berechnet Besten Zug für die Bauern
    def pawn_next_move(self):
        print("WHITE is moving")
        pawns = self.B.pawns
        best_move = [None, None, 999, None]
        for i, pawn in enumerate(pawns):
            moves = self.possible_moves_pawn(pawn)
            for target_square in moves:
                B_copy = copy.deepcopy(self.B)
                start_square = pawn.pos
                B_copy.move(B_copy.pawns[i], target_square)
                nr_moves_rook = len(self.possible_moves_rook(B_copy.rooks[0], boxes=B_copy.boxes))
                if nr_moves_rook < best_move[2]:
                    best_move = [B_copy.pawns[i], target_square, nr_moves_rook, i]
        print("Best move:", coord_to_str(self.B.pawns[best_move[3]].pos), '-', coord_to_str(best_move[1]), ':',best_move[2])
        self.B.move(self.B.pawns[best_move[3]], best_move[1])

    # Berechnet besten Zug für den Turm
    def rook_next_move(self):
        print("BLACK is moving")
        moves = self.possible_moves_rook(self.B.rooks[0])
        best_move = [None, -1]

        for target_square in moves:
            B_copy = copy.deepcopy(self.B)
            B_copy.move(B_copy.rooks[0], target_square)
            nr_moves_rook = len(self.possible_moves_rook(B_copy.rooks[0], boxes=B_copy.boxes))
            if nr_moves_rook > best_move[1]:
                best_move = [target_square, nr_moves_rook]
        print("Best move:", coord_to_str(self.B.rooks[0].pos), '-', coord_to_str(best_move[0]), ':', best_move[1])
        self.B.move(self.B.rooks[0], best_move[0])

    def is_running(self):
        for row in self.B.boxes:
            for box in row:
                if box.is_rook():
                    return True
        return False


def main():
    G = Game()
    print(G.B)
    c = 1
    while G.is_running():
        time.sleep(0.5)
        print('\n')
        print(str(c)+'.')
        G.pawn_next_move()
        print(G.B)
        c += 1
        time.sleep(0.5)
        print('\n')
        print(str(c)+'.')
        G.rook_next_move()
        print(G.B)
        c += 1
    print("WHITE won!")


if __name__ == '__main__':
    main()