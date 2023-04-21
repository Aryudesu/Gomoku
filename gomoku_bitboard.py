import os
import random


class Gomoku:
    SIZE = 19

    def __init__(self):
        self.init_board()
        self.l_mask = 0
        self.full_board = (1 << (self.SIZE * self.SIZE)) - 1
        self.r_mask = 0
        for i in range(self.SIZE + 1):
            self.r_mask |= 1 << (i * self.SIZE)
        self.r_mask >>= (self.SIZE)
        self.r_mask = (~self.r_mask) & self.full_board
        self.l_mask = ((self.r_mask << (self.SIZE - 1)) & self.full_board)

    def is_full_board(self):
        return not (self.full_board ^ (self.BLACK | self.WHITE))

    def init_board(self):
        """ボード初期化"""
        self.BLACK = 0
        self.WHITE = 0
        self.can_put = set()
        pos = 1
        for _ in range(self.SIZE * self.SIZE):
            self.can_put.add(pos)
            pos <<= 1

    def change_turn(self, turn):
        """ターン交代"""
        return not turn

    def XY2Bit(self, y, x):
        """座標からBitに"""
        return (1 << (self.SIZE - x)) << (self.SIZE * (self.SIZE - y))

    def can_put(self, pos):
        return not ((self.BLACK | self.WHITE) & pos)

    def deback_board(self, b):
        """デバッグ用描画"""
        os.system("cls")
        tmp = self.XY2Bit(1, 1)
        for _ in range(self.SIZE):
            for _ in range(self.SIZE):
                print("[-]" if tmp & b else "[ ]", end="")
                tmp >>= 1
            print()

    def print_board(self, pos=0):
        """描画"""
        os.system("cls")
        tmp = self.XY2Bit(1, 1)
        for _ in range(self.SIZE):
            for _ in range(self.SIZE):
                d = "[ ]"
                if tmp & pos:
                    if tmp & self.BLACK:
                        d = "=o="
                    elif tmp & self.WHITE:
                        d = "=x="
                else:
                    if tmp & self.BLACK:
                        d = "[o]"
                    elif tmp & self.WHITE:
                        d = "[x]"
                print(d, end="")
                tmp >>= 1
            print()

    def put_stone(self, pos, turn):
        """石を置く"""
        if turn:
            self.BLACK |= pos
        else:
            self.WHITE |= pos

    def horizon(self, pos, board):
        """ー"""
        result = -1
        p = pos
        b = board & self.r_mask
        while p:
            p = (p << 1) & b
            result += 1
        p = pos
        b = board & self.l_mask
        while p:
            p = (p >> 1) & b
            result += 1
        return 1 << ((result - 1) if result <= 6 else 5)

    def vertical(self, pos, board):
        """｜"""
        result = -1
        p = pos
        while p:
            p = (p << self.SIZE) & board
            result += 1
        p = pos
        while p:
            p = (p >> self.SIZE) & board
            result += 1
        return 1 << ((result - 1) if result <= 6 else 5)

    def right_down(self, pos, board):
        """＼"""
        result = -1
        p = pos
        b = board & self.r_mask
        s1 = self.SIZE + 1
        while p:
            p = (p << s1) & b
            result += 1
        p = pos
        b = board & self.l_mask
        while p:
            p = (p >> s1) & b
            result += 1
        return 1 << ((result - 1) if result <= 6 else 5)

    def right_up(self, pos, board):
        """／"""
        result = -1
        p = pos
        b = board & self.l_mask
        s1 = self.SIZE - 1
        while p:
            p = (p << s1) & b
            result += 1
        p = pos
        b = board & self.r_mask
        while p:
            p = (p >> s1) & b
            result += 1
        return 1 << ((result - 1) if result <= 6 else 5)

    def judge(self, pos, turn):
        """勝敗判定"""
        f = self.BLACK if turn else self.WHITE
        result = self.vertical(pos, f)
        ar = [self.horizon, self.right_down, self.right_up]
        for a in ar:
            tmp = a(pos, f)
            if (result & (1 << 2)) and (tmp & (1 << 2)) and turn:
                return -1
            if (result & (1 << 3)) and (tmp & (1 << 3)) and turn:
                return -1
            result |= tmp
        if result & (1 << 5):
            return -1
        if (result & (1 << 4)):
            return 1 if turn else -1
        return 0

    def cause(self, pos, turn):
        """勝敗要因"""
        f = self.BLACK if turn else self.WHITE
        result = self.vertical(pos, f)
        ar = [self.horizon, self.right_down, self.right_up]
        for a in ar:
            tmp = a(pos, f)
            if (result & (1 << 2)) and (tmp & (1 << 2)) and turn:
                return "三三"
            if (result & (1 << 3)) and (tmp & (1 << 3)) and turn:
                return "四四"
            result |= tmp
        if result & (1 << 5):
            return "長連"
        if (result & (1 << 4)):
            return "五"
        return "引分"

    def cpu_turn(self):
        """ランダムにマスを選ぶ"""
        tmp = random.sample(self.can_put, 1)[0]
        self.can_put.remove(tmp)
        return tmp

    def main(self, prt=False):
        """メインループ"""
        turn = True
        while True:
            if prt:
                self.print_board()
            pos = self.cpu_turn()
            self.put_stone(pos, turn)
            ju = self.judge(pos, turn)
            if ju:
                break
            if self.is_full_board():
                ju = 0
                break
            turn = self.change_turn(turn)
        if prt:
            self.print_board(pos)
            if ju == 0:
                print("Draw")
            elif ju == 1:
                print("Black Win")
            else:
                print("White Win")
            print(self.cause(pos, turn))
        return ju

    def try_loop(self, n):
        result = dict()
        for _ in range(n):
            r = self.main()
            result[r] = result.get(r, 0) + 1
            self.init_board()
        print(result)


gm = Gomoku()
# gm.try_loop(10000)
gm.main(True)
