import random
import os


class Gomoku:
    WALL = -1
    BLACK = 1
    WHITE = 2
    EMPTY = 0
    FIELD_SIZE = 19

    def i_w(self, value):
        s2 = self.FIELD_SIZE + 2
        return value == s2 - 1 or value == 0

    def make_board(self):
        e = self.EMPTY
        w = self.WALL
        s = self.FIELD_SIZE
        s2 = self.FIELD_SIZE + 2
        board = [[w for _ in range(s2)]]
        for _ in range(s):
            board.append([w if self.i_w(i) else e for i in range(s2)])
        board.append([w for _ in range(s2)])
        return board

    def init_board(self):
        self.board = self.make_board()

    def __init__(self):
        self.init_board()

    def print_board(self):
        os.system("cls")
        b = self.BLACK
        w = self.WHITE
        for y in range(1, self.FIELD_SIZE + 2):
            for x in range(1, self.FIELD_SIZE + 2):
                p = self.board[y][x]
                d = "[x]" if p == b else "[o]" if p == w else "[ ]"
                print(d, end="")
            print()

    def print_end_board(self, ey, ex):
        os.system("cls")
        b = self.BLACK
        w = self.WHITE
        for y in range(1, self.FIELD_SIZE + 2):
            for x in range(1, self.FIELD_SIZE + 2):
                p = self.board[y][x]
                if y == ey and x == ex:
                    d = "{x}" if p == b else "{o}" if p == w else "{ }"
                else:
                    d = "[x]" if p == b else "[o]" if p == w else "[ ]"
                print(d, end="")
            print()

    def put(self, y, x, turn):
        self.board[y][x] = turn

    def can_put(self, y, x):
        return self.board[y][x] == self.EMPTY

    def change_turn(self, turn):
        return 2 - turn + 1

    def judge(self, y, x, turn, toukei):
        mem = set()
        for dx in range(-1, 1):
            for dy in range(-1, 1):
                if not dx and not dy:
                    continue
                s1 = 1
                while self.board[y + dy * s1][x + dx * s1] == turn:
                    s1 += 1
                s2 = 0
                while self.board[y - dy * s2][x - dx * s2] == turn:
                    s2 += 1
                s = s1 + s2 - 1
                if turn == self.BLACK:
                    if (s == 3 or s == 4) and s in mem:
                        key = "三三" if s == 3 else "四四"
                        toukei[key] = 1 + toukei.get(key, 0)
                        return self.WHITE
                    if s > 5:
                        key = "長連（黒）"
                        toukei[key] = 1 + toukei.get(key, 0)
                        return self.WHITE
                if s >= 5:
                    if s == 5:
                        key = "五"
                    elif s > 5:
                        key = "長連（白）"
                    toukei[key] = 1 + toukei.get(key, 0)
                    return turn
                mem.add(s)
        return self.EMPTY

    def cpu_turn(self):
        data = []
        for y in range(1, self.FIELD_SIZE):
            for x in range(1, self.FIELD_SIZE):
                if self.can_put(y, x):
                    data.append((y, x))
        return random.choice(data)

    def is_end(self):
        for y in range(1, self.FIELD_SIZE):
            for x in range(1, self.FIELD_SIZE):
                if self.can_put(y, x):
                    return False
        return True

    def main(self):
        toukei = dict()
        win_num = [0] * 3
        for i in range(3000):
            self.init_board()
            turn = self.BLACK
            ju = None
            while True:
                y, x = self.cpu_turn()
                self.put(y, x, turn)
                if self.is_end():
                    ju = self.EMPTY
                    key = "引分"
                    toukei[key] = 1 + toukei.get(key, 0)
                    break
                ju = self.judge(y, x, turn, toukei)
                if ju != self.EMPTY:
                    break
                turn = self.change_turn(turn)
            if ju == 0:
                win_num[0] += 1
            elif ju == self.BLACK:
                win_num[1] += 1
            else:
                win_num[2] += 1
        print(toukei)
        print(win_num)


gm = Gomoku()
gm.main()
