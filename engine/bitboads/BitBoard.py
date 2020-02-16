import numpy as np
from itertools import count
import re

from engine.bitboads.Searcher import Searcher

A1, H1, A8, H8 = 91, 98, 21, 28
initial = np.array(list("         \n"
                    "         \n" 
                    " rnbqkbnr\n"  
                    " pppppppp\n" 
                    " ........\n"  
                    " ........\n"  
                    " ........\n"
                    " ........\n" 
                    " PPPPPPPP\n" 
                    " RNBQKBNR\n" 
                    "         \n" 
                    "         \n"), dtype=str)

N, E, S, W = -10, 1, 10, -1

pieces = {
    'P': (N, N + N, N + W, N + E),
    'N': (N + N + E, E + N + E, E + S + E, S + S + E, S + S + W, W + S + W, W + N + W, N + N + W),
    'B': (N + E, S + E, S + W, N + W),
    'R': (N, E, S, W),
    'Q': (N, E, S, W, N + E, S + E, S + W, N + W),
    'K': (N, E, S, W, N + E, S + E, S + W, N + W)
}

piece = {'P': 100, 'N': 320, 'B': 330, 'R': 500, 'Q': 900, 'K': 20000}
pst = {
    'P': (0,  0,  0,  0,  0,  0,  0,  0,
        50, 50, 50, 50, 50, 50, 50, 50,
        10, 10, 20, 30, 30, 20, 10, 10,
         5,  5, 10, 25, 25, 10,  5,  5,
         0,  0,  0, 20, 20,  0,  0,  0,
         5, -5,-10,  0,  0,-10, -5,  5,
         5, 10, 10,-20,-20, 10, 10,  5,
         0,  0,  0,  0,  0,  0,  0,  0),
    'N':(-50,-40,-30,-30,-30,-30,-40,-50,
        -40,-20,  0,  0,  0,  0,-20,-40,
        -30,  0, 10, 15, 15, 10,  0,-30,
        -30,  5, 15, 20, 20, 15,  5,-30,
        -30,  0, 15, 20, 20, 15,  0,-30,
        -30,  5, 10, 15, 15, 10,  5,-30,
        -40,-20,  0,  5,  5,  0,-20,-40,
        -50,-40,-30,-30,-30,-30,-40,-50),
    'B':(-20,-10,-10,-10,-10,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5, 10, 10,  5,  0,-10,
        -10,  5,  5, 10, 10,  5,  5,-10,
        -10,  0, 10, 10, 10, 10,  0,-10,
        -10, 10, 10, 10, 10, 10, 10,-10,
        -10,  5,  0,  0,  0,  0,  5,-10,
        -20,-10,-10,-10,-10,-10,-10,-20),
    'R':(0,  0,  0,  0,  0,  0,  0,  0,
         5, 10, 10, 10, 10, 10, 10,  5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
        -5,  0,  0,  0,  0,  0,  0, -5,
         -5,  0,  0,  0,  0,  0,  0, -5,
          0,  0,  0,  5,  5,  0,  0,  0),
    'Q': (-20,-10,-10, -5, -5,-10,-10,-20,
        -10,  0,  0,  0,  0,  0,  0,-10,
        -10,  0,  5,  5,  5,  5,  0,-10,
         -5,  0,  5,  5,  5,  5,  0, -5,
          0,  0,  5,  5,  5,  5,  0, -5,
        -10,  5,  5,  5,  5,  5,  0,-10,
        -10,  0,  5,  0,  0,  0,  0,-10,
        -20,-10,-10, -5, -5,-10,-10,-20),
    'K':(-30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -30,-40,-40,-50,-50,-40,-40,-30,
        -20,-30,-30,-40,-40,-30,-30,-20,
        -10,-20,-20,-20,-20,-20,-20,-10,
         20, 20,  0,  0,  0,  0, 20, 20,
         20, 30, 10,  0,  0, 10, 30, 20)
}

for k, table in pst.items():
    padrow = lambda row: (0,) + tuple(x+piece[k] for x in row) + (0,)
    pst[k] = sum((padrow(table[i*8:i*8+8]) for i in range(8)), ())
    pst[k] = (0,)*20 + pst[k] + (0,)*20


class Position:

    def __init__(self, board, score, currentplayer, wc, bc, ep, kp):
        super().__init__()
        self.board = board
        self.score = score
        self.player = currentplayer
        self.wc = wc
        self.bc = bc
        self.ep = ep
        self.kp = kp

    def gen_moves(self):
        test = []
        for i, tile in enumerate(self.board):
            if not checkAlliance(tile, self.player):
                continue
            for d in pieces[tile.upper()]:
                for j in count(i+d, d):
                    q = self.board[j]
                    if self.player == 'b':
                        tile = tile.upper()
                    if q.isspace() or checkAlliance(q, self.player):
                        break
                    if tile == 'P' and d in (N, N+N) and q != '.': break
                    if tile == 'P' and d == N+N and (i < A1+N or self.board[i+N] != '.'): break
                    if tile == 'P' and d in (N+W, N+E) and q == '.' \
                            and j not in (self.ep, self.kp, self.kp-1, self.kp+1): break
                    test.append((i, j))
                    yield i, j
                    if tile.upper() in 'PNK' or not checkAlliance(q, self.player): break

    def rotate(self):
        return Position(np.flip(self.board), -self.score, self.player, self.bc, self.wc, 119-self.ep if self.ep else 0,
            119-self.kp if self.kp else 0)

    def move(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]
        
        board = self.board

        if self.player == 'b':
            p = p.upper()

        wc, bc, ep, kp = self.wc, self.bc, 0, 0,

        score = self.score + self.value(move)
        board[j] = board[i]
        board[i] = '.'

        if i == A1: wc = (False, wc[1])
        if i == H1: wc = (wc[0], False)
        if j == A8: bc = (bc[0], False)
        if j == H8: bc = (False, bc[1])

        if p == 'P':
            if A8 <= j <= H8:
                board[j] = 'Q'
            if j - i == 2 * N:
                ep = i + N
            if j == self.ep:
                board[j + S] = '.'

        pos = Position(board, score, 'b' if self.player == 'w' else 'w', wc, bc, ep, kp)
        return pos.rotate()

    def value(self, move):
        i, j = move
        p, q = self.board[i], self.board[j]

        if self.player == 'b':
            p = p.upper()

        score = pst[p][j] - pst[p][i]

        if q.islower():
            score += pst[q.upper()][119-j]

        return score

def checkAlliance(tile: str, player: str) -> bool:
    if tile.isupper() and player == "w":
        return True
    elif tile.islower() and player == "b":
        return True
    return False

def print_pos(pos):
    print()
    uni_pieces = {'R':'♜', 'N':'♞', 'B':'♝', 'Q':'♛', 'K':'♚', 'P':'♟',
                  'r':'♖', 'n':'♘', 'b':'♗', 'q':'♕', 'k':'♔', 'p':'♙', '.':'·'}
    for i, row in enumerate(np.split(pos.board, 12)):
        print(' ', 12-i, ' '.join(uni_pieces.get(p, p) for p in row))
    print('    a b c d e f g h \n\n')


def parse(c):
    fil, rank = ord(c[0]) - ord('a'), int(c[1]) - 1
    return A1 + fil - 10*rank


if __name__ == "__main__":
    p = Position(initial, 0, 'w', (True, True), (True, True), 0, 0)

    print_pos(p)
    match = re.match('([a-h][1-8])' * 2, input('Your move: '))
    if match:
        move = parse(match.group(1)), parse(match.group(2))
    new = p.move(move)
    new.rotate()
    print_pos(new)
    searcher = Searcher()
    n = new.move(searcher.execute(new, 4, True))
    print_pos(n)
